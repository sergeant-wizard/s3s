import json
import pathlib
from ..types import CoopHistoryDetail


def test_coop_history_detail() -> None:
  current_dir = pathlib.Path(__file__).parent
  data_path = current_dir / "example.json"
  detail = CoopHistoryDetail.model_validate(json.loads(data_path.read_text())["data"]["coopHistoryDetail"])
  assert isinstance(detail.afterGradePoint, int)
