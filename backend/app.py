from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()


class DisciplineParameters(BaseModel):
  code: str
  name: str
  description: str
  intervals: list[int]


class Discipline(DisciplineParameters):
  id: int


disciplines = [
    Discipline(
        id=1,
        code="P1",
        name="Phoenix Fast",
        description="",
        intervals=[3, 5, 8]
    ),
    Discipline(
        id=2,
        code="P2",
        name="Phoenix Slow",
        description="",
        intervals=[4, 8, 12]
    )
]


@app.get("/disciplines")
def get_disciplines() -> list[Discipline]:
  return disciplines


@app.post("/disciplines")
def create_discipline(params: DisciplineParameters) -> Discipline:
  last_discipline_id = disciplines[-1].id

  discipline = Discipline(
      id=last_discipline_id + 1,
      code=params.code,
      name=params.name,
      description=params.description,
      intervals=params.intervals,
  )

  disciplines.append(discipline)

  return discipline


@app.get("/disciplines/{id}/start")
def start_discipline(id: int):
  discipline = get_discipline_by_id(id)

  return discipline


@app.get("/disciplines/{id}/stop")
def stop_discipline(id: int):
  discipline = get_discipline_by_id(id)

  return discipline


def get_discipline_by_id(id: int):
  for discipline in disciplines:
    if discipline.id == id:
      return discipline

  raise HTTPException(status_code=404, detail="Discipline not found")
