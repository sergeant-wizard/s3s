import dataclasses
import datetime
from typing import Optional

from .stage import Stage


def is_bigrun(stage: Stage) -> bool:
  return stage in {
    Stage.barnacle_dime,
    Stage.eeltail_alley,
    Stage.inkblot_art_academy,
    Stage.undertow_spillway,
    Stage.wahoo_world,
    Stage.umami_ruins,
  }


@dataclasses.dataclass(frozen=True)
class Shift:
  start: datetime.datetime
  stage: Optional[Stage]

  def to_label(self) -> str:
    japaneze_name = {
      Stage.sujiko: "スジコジャンクション",
      Stage.aramaki: "アラマキ砦",
      Stage.donbrako: "難破船ドンブラコ",
      Stage.dam: "シェケナダム",
      Stage.tokishirazu: "トキシラズ",
      Stage.donpiko: "どんぴこ闘技場",
      Stage.meuniere: "ムニエール",
      None: "ビッグラン",
    }[self.stage]
    return f"{self.start.strftime('%m/%d')}{japaneze_name}"

  def is_in(self, stage: Stage, timestamp: datetime.datetime) -> bool:
    if timestamp < self.start or self.start + datetime.timedelta(hours=40) < timestamp:
      return False

    if self.stage is None:
      return is_bigrun(stage)
    else:
      return self.stage == stage


def find_shift(stage: Stage, timestamp: datetime.datetime, shifts: list[Shift]) -> Optional[Shift]:
  try:
    return next(filter(lambda shift: shift.is_in(stage, timestamp), shifts))
  except StopIteration:
    return None
