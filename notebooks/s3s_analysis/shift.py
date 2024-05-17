import dataclasses
import datetime
from typing import Optional

from .stage import Stage

@dataclasses.dataclass(frozen=True)
class Shift:
  start: datetime.datetime
  stage: Stage

  def to_label(self) -> str:
    japaneze_name = {
      Stage.sujiko: "スジコジャンクション",
      Stage.aramaki: "アラマキ砦",
      Stage.donbrako: "難破船ドンブラコ",
      Stage.dam: "シェケナダム",
      Stage.tokishirazu: "トキシラズ",
      Stage.donpiko: "どんぴこ闘技場",
      Stage.meuniere: "ムニエール",
    }[self.stage]
    return f"{self.start.strftime('%m/%d')}{japaneze_name}"

  def is_in(self, stage: Stage, timestamp: datetime.datetime) -> bool:
    if self.stage == stage:
      return(
        self.start < timestamp and timestamp < self.start + datetime.timedelta(hours=40)
      )
    else:
      return False


def find_shift(stage: Stage, timestamp: datetime.datetime, shifts: list[Shift]) -> Optional[Shift]:
  try:
    return next(filter(lambda shift: shift.is_in(stage, timestamp), shifts))
  except StopIteration:
    return None
