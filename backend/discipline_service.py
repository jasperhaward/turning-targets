from typing import Callable
from threading import Thread
from time import time
import asyncio


from .models import Discipline
from .targets import TargetService, TargetState

# refactor to use proper event types/objects

class DisciplineService:
  def __init__(self, target: TargetService, dispatch_event: Callable[[str], None]):
    self.target = target
    self.dispatch_event = dispatch_event
    self.is_stopped = False
    
  def start(self, discipline: Discipline):
    self.discipline = discipline
    thread = Thread(
      target = asyncio.run, 
      args = (
        self.execute(
          self.target,
          self.dispatch_event,
          lambda: self.is_stopped, 
          self.discipline
        ),
      )
    )
    thread.start()

  def stop(self):
    self.is_stopped = True
    self.discipline = None

  async def execute(
    self,
    target: TargetService,  
    dispatch_event: Callable[[str], None], 
    is_stopped: Callable[[], bool],
    discipline: Discipline,
  ):
    interval_index = 0
    interval_start_ms = time()

    await dispatch_event("Discipline started")
    target.show()
    await dispatch_event("Target shown")

    while True:
      if is_stopped():
        target.hide()
        await dispatch_event("Discipline stopped")
        break

      if time() >= interval_start_ms + discipline.intervals[interval_index]:
        if interval_index is len(discipline.intervals) - 1:
          target.hide()
          await dispatch_event("Discipline finished")
          break

        interval_index += 1
        interval_start_ms = time()

        if target.value is TargetState.SHOW:
          target.hide()
          await dispatch_event("Target hidden")
        else:
          target.show()
          await dispatch_event("Target shown")




