import json
import pathlib
from typing import Iterator

import pandas

from .shift import Shift, find_shift
from .stage import Stage
from .types import CoopHistoryDetail


def load_jobs(path: pathlib.Path) -> Iterator[CoopHistoryDetail]:
  for job_result in path.iterdir():
    data = json.loads(job_result.read_text())
    yield CoopHistoryDetail.model_validate(data["data"]["coopHistoryDetail"])


def load_as_df(path: pathlib.Path, shifts: list[Shift]) -> pandas.DataFrame:
  def access_each_job(job: CoopHistoryDetail) -> list:
    try:
      first_wave_deliver_norm = job.waveResults[0].deliverNorm
    except IndexError:
      first_wave_deliver_norm = None
    
    shift = find_shift(Stage(job.coopStage.id), job.playedTime, shifts)
    if shift is None:
      shift_label = ""
    else:
      shift_label = shift.to_label()
    
    num_cleared_waves = 0
    for wave in job.waveResults:
      if wave.waveNumber == 4:
        continue
      if wave.teamDeliverCount >= wave.deliverNorm:
        num_cleared_waves += 1
    
    defeat_rank = pandas.Series(
      [job.myResult.defeatEnemyCount] + [mr.defeatEnemyCount for mr in job.memberResults]
    ).rank(ascending=False).iloc[0]

    try:
      defeat_ratio = job.myResult.defeatEnemyCount / (
        job.myResult.defeatEnemyCount + sum(mr.defeatEnemyCount for mr in job.memberResults)
      )
    except ZeroDivisionError:
      defeat_ratio = 0

    deliver_rank = pandas.Series(
      [job.myResult.goldenDeliverCount + job.myResult.goldenAssistCount] +
      [mr.goldenDeliverCount + mr.goldenAssistCount for mr in job.memberResults]
    ).rank(ascending=False).iloc[0]


    if job.afterGrade is not None:
      after_grade_name = job.afterGrade.name
    else:
      after_grade_name = ""

    return (
      job.playedTime,
      job.afterGradePoint,
      after_grade_name,
      job.coopStage.id,
      job.coopStage.name,
      job.dangerRate,
      job.resultWave,
      num_cleared_waves,
      first_wave_deliver_norm,
      shift_label,
      defeat_rank,
      deliver_rank,
      defeat_ratio,
    )

  return pandas.DataFrame(
    map(access_each_job, load_jobs(path)),
    columns=[
      "playedTime",
      "afterGradePoint",
      "afterGradeName",
      "stageId",
      "stageName",
      "dangerRate",
      "resultWave",
      "numClearedWaves",
      "firstWaveDeliverNorm",
      "shift",
      "defeatRank",
      "deliverRank",
      "defeatRatio",
    ]
  )


def load_members(path: pathlib.Path) -> Iterator[tuple]:
  def access_each_member(job: CoopHistoryDetail) -> Iterator[tuple]:
    for member in job.memberResults:
      yield (job.id, job.playedTime, member.player.name, member.player.nameId, member.deliverCount)
  
  for job in load_jobs(path):
    yield from access_each_member(job)


def load_members_as_df(path: pathlib.Path) -> pandas.DataFrame:
  return pandas.DataFrame(
    load_members(path),
    columns=["job_id", "job_time", "name", "nameId", "deliverCount"],
  )