from .mocks import MockGpiod

try:
  import gpiod  # type: ignore
except ImportError:
  import warnings

  warnings.warn("Mocking GPIOD module, no gpiod install found")
  gpiod = MockGpiod()

class TargetState:
  SHOW = "SHOW"
  HIDE = "HIDE"


class TargetService:
  def __init__(self, pin: int):
    chip = gpiod.Chip('gpiochip4')

    self.output_line = chip.get_line(pin)
    self.output_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    self.value = TargetState.HIDE

  def show(self):
    self.output_line.set_value(1)
    self.value = TargetState.SHOW

  def hide(self):
    self.output_line.set_value(0)
    self.value = TargetState.HIDE
