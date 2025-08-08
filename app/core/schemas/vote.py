import datetime

from pydantic import BaseModel


class VoteSchema(BaseModel):
    menu_id: int


class VoteCreateSchema(VoteSchema):
    pass


class VoteReadSchema(VoteSchema):
    id: int
    employee_id: int
    vote_date: datetime.date

