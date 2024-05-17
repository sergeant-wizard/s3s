import json
import pathlib
from datetime import datetime
from typing import Optional

import requests

from .shift import Shift
from .stage import Stage


default_path = pathlib.Path(__file__).parents[1] / "shifts.jsonl"


def dict_to_shift(adict: dict) -> Shift:
  stage_map = {
    "すじこジャンクション跡": Stage.sujiko,
    "シェケナダム": Stage.dam,
    "アラマキ砦": Stage.aramaki,
    "難破船ドン・ブラコ": Stage.donbrako,
    "トキシラズいぶし工房": Stage.tokishirazu,
    "どんぴこ闘技場": Stage.donpiko,
    "ムニ・エール海洋発電所": Stage.meuniere,
  }
  return Shift(
    stage=stage_map[adict["stage"]["name"]],
    start=datetime.fromisoformat(adict["start_time"]),
  )


def load_shift_history(path: Optional[pathlib.Path]) -> list[Shift]:
  shift_history_path = path or default_path
  return list(
    map(
      lambda jsonl: dict_to_shift(json.loads(jsonl)),
      shift_history_path.read_text().splitlines()
    )
  )


def save_latest_shift(path: Optional[pathlib.Path]) -> None:
  r = requests.get("https://spla3.yuu26.com/api/coop-grouping/schedule")
  response = r.json()

  existing_shifts = load_shift_history(path)
  shift_history_path = path or default_path

  with shift_history_path.open("a") as f:
    for shift in response["results"]:
      if dict_to_shift(shift) not in existing_shifts:
        f.write(json.dumps(shift))
        f.write("\n")
