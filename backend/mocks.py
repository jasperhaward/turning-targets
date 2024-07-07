class MockGpiod:
  LINE_REQ_DIR_OUT = ""

  def Chip(self, name: str):
    return MockGpiodChip(name)


class MockGpiodChip:
  def __init__(self, name: str):
    self.name = name

  def get_line(self, pin: int):
    return MockGpiodLine(pin)


class MockGpiodLine:
  def __init__(self, pin: int):
    self.pin = pin

  def request(self, consumer: str, type: str):
    self.consumer = consumer
    self.type = type

  def set_value(self, value: int):
    print(f"Setting pin {self.pin} to {value}")
