import datetime
from functools import cache

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from utils.client import ClientTransaction, Auth, Agent

from .tables_orm import AggregatorORM, AgentORM
from .transaction import Transactions


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Aggregator(BaseModel):
    username: str
    password: str
    mobile: int
    target: float
    name: str = ""
    token: str = ""
    email: EmailStr | None = None

    class Config:
        orm_mode = True
        allow_arbitrary_types = True

    def __hash__(self):
        return hash(self.mobile)

    @property
    async def orm(self) -> type(AggregatorORM):
        orm = await AggregatorORM.get(username=self.username)
        return orm

    @property
    @cache
    def session(self):
        sess = ClientTransaction(auth=Auth(username=self.username, password=self.password, token=self.token))
        return sess

    async def update(self, **kwargs):
        orm = await self.orm
        await orm.update_from_dict(kwargs)
        await orm.save(update_fields=tuple(kwargs.keys()))

    async def authenticate(self):

        await self.session.authenticate()
        await self.update(token=self.session.auth.token)
        return self.session.is_auth

    @property
    async def agents(self):
        agg = await self.orm
        await agg.fetch_related('agents')
        return [Agent.from_orm(agent) for agent in agg.agents]

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def update_agents(self):
        sess = self.session
        agents = {Agent(**agent.dict()) for agent in await sess.get_agents()}
        agents = agents - {*await self.agents}
        aggregator = await self.orm
        await AgentORM.bulk_create(objects=[AgentORM(**agent.dict(), aggregator=aggregator) for agent in agents])
        return len(agents)

    async def get_transactions(self, start_date: datetime.date | None = None, end_date: datetime.date | None = None):
        today = datetime.date.today()
        start_date = start_date or today
        end_date = end_date or today
        title = f"Transactions Report for {self.name}.{start_date.strftime('%A, %B %d %Y')}"
        session = self.session
        agents = await self.agents
        transactions = await session.get_transactions_by_agents(start_date=start_date, end_date=end_date, agents=agents)
        trans = Transactions(title=title, transactions=transactions, agents=agents)
        pdf = await trans.get_pdf()
        await session.close()
        return pdf

