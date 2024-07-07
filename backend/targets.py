from .mocks import MockGpiod

try:
  import gpiod  # type: ignore
except ImportError:
  gpiod = MockGpiod()


class TargetService:
  def __init__(self, pin: int):
    chip = gpiod.Chip('gpiochip4')

    self.output_line = chip.get_line(pin)
    self.output_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

  def show(self):
    self.output_line.set_value(1)

  def hide(self):
    self.output_line.set_value(0)
