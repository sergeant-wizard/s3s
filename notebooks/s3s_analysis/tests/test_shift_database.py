import json
import pathlib
import tempfile

from ..shift_database import load_shift_history


def test_load_shift_history() -> None:
  entry1 = {
    "start_time": "2024-04-23T17:00:00+09:00",
    "stage": {
      "name": "すじこジャンクション跡"
    }
  }
  entry2 = {
    "start_time": "2024-04-23T17:00:00+09:00",
    "stage": {
      "name": "シェケナダム",
    }
  }
  entries = [entry1, entry2]

  with tempfile.NamedTemporaryFile("w+t") as f:
    for entry in entries:
      f.write(json.dumps(entry))
      f.write("\n")
    f.seek(0)
    shifts = load_shift_history(pathlib.Path(f.name))
    assert len(shifts) > 0
