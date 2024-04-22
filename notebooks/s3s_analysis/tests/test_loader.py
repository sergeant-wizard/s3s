import pathlib

import pandas

from ..types import CoopHistoryDetail
from ..loader import load_as_df, load_jobs


export_dir = pathlib.Path(__file__).parents[3] / "exports/coop_results"


def test_load_jobs() -> None:
  for job in load_jobs(export_dir):
    assert isinstance(job, CoopHistoryDetail)


def test_load_as_df() -> None:
  df = load_as_df(export_dir)
  assert isinstance(df, pandas.DataFrame)
  assert "playedTime" in df.columns
  