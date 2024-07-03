from fastapi import FastAPI, HTTPException
from .config import DISCIPLINES_DATABASE
from .models import Discipline, DisciplineParameters
from .disciplines import DisciplinesStore

app = FastAPI()


disciplines = DisciplinesStore(DISCIPLINES_DATABASE)


@app.get("/disciplines")
def get_disciplines() -> list[Discipline]:
  return disciplines.get_disciplines()


@app.post("/disciplines")
def create_discipline(params: DisciplineParameters) -> Discipline:
  return disciplines.create_discipline(params)


@app.get("/disciplines/{id}/start")
def start_discipline(id: int) -> Discipline:
  discipline = disciplines.get_discipline_by_id(id)

  if discipline is None:
    raise HTTPException(status_code=404, detail="Discipline not found")

  return discipline


@app.get("/disciplines/{id}/stop")
def stop_discipline(id: int) -> Discipline:
  discipline = disciplines.get_discipline_by_id(id)

  if discipline is None:
    raise HTTPException(status_code=404, detail="Discipline not found")

  return discipline
