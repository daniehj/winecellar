from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Record(BaseModel):
    id: Optional[int]
    date: datetime
    loc: str
    temperature: float

    class Config:
        orm_mode = True
