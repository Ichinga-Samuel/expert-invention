from tortoise.models import Model
from tortoise import fields


class AggregatorORM(Model):
    name = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255, pk=True)
    email = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255)
    mobile = fields.BigIntField()
    target = fields.FloatField()
    token = fields.TextField(default="", null=True)
    agents: fields.ReverseRelation['AgentORM']

    class Meta:
        table = "aggregators"
        unique_together = (('username', 'mobile'),)


class AgentORM(Model):
    id = fields.UUIDField(pk=True)
    agent_id = fields.IntField()
    name = fields.CharField(max_length=255)
    mobile = fields.BigIntField()
    aggregator: fields.ForeignKeyRelation = fields.ForeignKeyField('models.AggregatorORM', related_name='agents', on_delete="CASCADE")

    class Meta:
        table = "agents"
