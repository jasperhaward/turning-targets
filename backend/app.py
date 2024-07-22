from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from .config import DISCIPLINES_DATABASE
from .models import Discipline, DisciplineParameters
from .disciplines import DisciplinesStore
from .discipline_service import DisciplineService
from .targets import TargetService

app = FastAPI()
active_websockets: list[WebSocket] = []

async def dispatch_event(event: str):
  for websocket in active_websockets:
    print(event)
    await websocket.send_text(event)

target = TargetService(4)
disciplines = DisciplinesStore(DISCIPLINES_DATABASE)
discipline_service = DisciplineService(target, dispatch_event)

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

  discipline_service.start(discipline)

  return discipline


@app.get("/disciplines/stop")
def stop_discipline():
  if discipline_service.discipline is None:
    raise HTTPException(status_code=400, detail="No active discipline")

  discipline_service.stop()

@app.websocket("/disciplines/events")
async def discipline_events(websocket: WebSocket):
  await websocket.accept()
  active_websockets.append(websocket)

  try:
    while True:
      await websocket.receive()
  except WebSocketDisconnect:
      active_websockets.remove(websocket)