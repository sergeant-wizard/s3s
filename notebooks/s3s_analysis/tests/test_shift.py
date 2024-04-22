import datetime

from ..shift import Shift, find_shift
from ..stage import Stage

def test_to_label() -> None:
  test_shift = Shift(start=datetime.datetime(2024, 4, 10, 9), stage=Stage.aramaki)
  assert test_shift.to_label() == '04/10アラマキ砦'


def test_is_in() -> None:
  test_shift = Shift(start=datetime.datetime(2024, 4, 10, 9), stage=Stage.aramaki)
  assert test_shift.is_in(Stage.donbrako, datetime.datetime(2024, 4, 10, 10)) is False
  assert test_shift.is_in(Stage.aramaki, datetime.datetime(2024, 4, 10, 10)) is True
  assert test_shift.is_in(Stage.aramaki, datetime.datetime(2024, 4, 12, 10)) is False


def test_find_shift() -> None:
  tz_jst = datetime.timezone(datetime.timedelta(hours=9))
  timestamp = datetime.datetime.fromisoformat("2024-04-18T11:12:57Z")
  test_shift = Shift(
    start=datetime.datetime(2024, 4, 18, 17, tzinfo=tz_jst),
    stage=Stage.aramaki,
  )
  assert test_shift.is_in(Stage.aramaki, timestamp) is True
  assert find_shift(Stage.aramaki, timestamp, [test_shift]) is not None