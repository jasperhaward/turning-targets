from pydantic import BaseModel


class DisciplineParameters(BaseModel):
  code: str
  name: str
  description: str
  intervals: list[int]


class Discipline(DisciplineParameters):
  id: int
