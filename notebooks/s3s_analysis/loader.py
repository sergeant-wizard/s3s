import json
import pathlib
from typing import Iterator

import pandas

from .types import CoopHistoryDetail


def load_jobs(path: pathlib.Path) -> Iterator[CoopHistoryDetail]:
  for job_result in path.iterdir():
    data = json.loads(job_result.read_text())
    yield CoopHistoryDetail.model_validate(data["data"]["coopHistoryDetail"])


def load_as_df(path: pathlib.Path) -> pandas.DataFrame:
  def access_each_job(job: CoopHistoryDetail) -> list:
    try:
      first_wave_deliver_norm = job.waveResults[0].deliverNorm
    except IndexError:
      first_wave_deliver_norm = None

    return (
      job.playedTime,
      job.afterGradePoint,
      job.coopStage.id,
      job.coopStage.name,
      job.dangerRate,
      first_wave_deliver_norm,
    )

  return pandas.DataFrame(
    map(access_each_job, load_jobs(path)),
    columns=[
      "playedTime",
      "afterGradePoint",
      "stageId",
      "stageName",
      "dangerRate",
      "firstWaveDeliverNorm",
    ]
  )


def load_members(path: pathlib.Path) -> Iterator[tuple]:
  def access_each_member(job: CoopHistoryDetail) -> Iterator[tuple]:
    for member in job.memberResults:
      yield (job.id, member.player.name, member.deliverCount)
  
  for job in load_jobs(path):
    yield from access_each_member(job)


def load_members_as_df(path: pathlib.Path) -> pandas.DataFrame:
  return pandas.DataFrame(
    load_members(path),
    columns=["job_id", "name", "deliverCount"],
  )