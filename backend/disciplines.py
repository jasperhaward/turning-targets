
import sqlite3
from .models import Discipline, DisciplineParameters


class DisciplinesStore:
  def __init__(self, database: str):
    self.connection = sqlite3.connect(database, check_same_thread=False)
    self.connection.row_factory = self.__discipline_factory
    self.__create_table()

  def __discipline_factory(self, cursor: sqlite3.Cursor, raw_row: tuple):
    row = sqlite3.Row(cursor, raw_row)

    return Discipline(
      id=row["id"],
      code=row["code"],
      name=row["name"],
      description=row["description"],
      intervals=self.__parse_intervals(row["intervals"])
    )

  def __create_table(self):
    sql = """
      CREATE TABLE IF NOT EXISTS disciplines (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          code TEXT,
          name TEXT,
          description TEXT,
          intervals TEXT
      )
    """
    self.connection.execute(sql)
    self.connection.commit()

  def get_disciplines(self) -> list[Discipline]:
    sql = "SELECT * FROM disciplines"

    cursor = self.connection.cursor()
    disciplines = cursor.execute(sql).fetchall()
    cursor.close()

    return disciplines

  def get_discipline_by_id(self, id: int) -> Discipline | None:
    sql = "SELECT * FROM disciplines WHERE id = ?"

    cursor = self.connection.cursor()
    discipline = cursor.execute(sql, (id,)).fetchone()
    cursor.close()

    return discipline

  def create_discipline(self, params: DisciplineParameters) -> Discipline:
    sql = """
      INSERT INTO disciplines (code, name, description, intervals)
      VALUES (?, ?, ?, ?)
    """

    cursor = self.connection.cursor()
    cursor.execute(sql, (
      params.code,
      params.name,
      params.description,
      self.__stringify_intervals(params.intervals)
    ))
    self.connection.commit()
    cursor.close()

    return Discipline(
      id=cursor.lastrowid,
      code=params.code,
      name=params.name,
      description=params.description,
      intervals=params.intervals
    )

  def __parse_intervals(self, intervals: str) -> list[int]:
    return [int(interval) for interval in intervals.split(",")]

  def __stringify_intervals(self, intervals: list[int]) -> str:
    return ','.join(str(x) for x in intervals)
