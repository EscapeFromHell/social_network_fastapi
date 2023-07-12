from pydantic import BaseModel, PositiveInt


class ReactionBase(BaseModel):
    reaction_type: str


class ReactionCreate(ReactionBase):
    pass


class ReactionUpdate(ReactionBase):
    pass


class ReactionInDB(ReactionBase):
    id: PositiveInt
    user_id: PositiveInt
    post_id: PositiveInt

    class Config:
        orm_mode = True


class Reaction(ReactionInDB):
    pass
