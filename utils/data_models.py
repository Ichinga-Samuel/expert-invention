from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, time

from pydantic import BaseModel


class Agent(BaseModel):
    agent_id: int
    name: str
    mobile: int

    class Config:
        orm_mode = True

    def __hash__(self):
        return self.agent_id


@dataclass
class Transaction:
    business_name: str
    time: datetime
    trans_type: str
    agent_id: int
    amount: int = 0

    @classmethod
    def create(cls, trans: dict) -> 'Transaction':
        name = trans['agent']['businessName'].title()
        time = datetime.strptime(trans['createdOn'], "%Y-%m-%dT%H:%M:%S.%f%z")
        return cls(business_name=name, time=time, trans_type=trans['transactionType'], amount=trans['amount'], agent_id=trans['agent']['id'])


@dataclass
class Auth:
    password: str
    username: str
    token: str = ""
    status: bool = False


class Filter:
    def __init__(self, start: time = time(hour=0, minute=0, second=0), end: time = time(hour=23, minute=59, second=59)):
        self.start = start
        self.end = end

    def __call__(self, *, trans: Transaction) -> bool:
        return self.start <= trans.time.time() <= self.end


MorningFilter = Filter(start=time(hour=0, minute=0, second=0), end=time(hour=11, minute=59, second=59))

AfternoonFilter = Filter(start=time(hour=12, minute=0, second=0), end=time(hour=15, minute=59, second=59))

EveningFilter = Filter(start=time(hour=16, minute=0, second=0), end=time(hour=23, minute=59, second=59))
