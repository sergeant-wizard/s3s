import json
import pathlib
from typing import Iterable


def load_existing_job_ids() -> Iterable[str]:
  for path in sorted(pathlib.Path("exports/coop_results").iterdir())[-50:]:
    yield json.loads(path.read_text())["data"]["coopHistoryDetail"]["id"]