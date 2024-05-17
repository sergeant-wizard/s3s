from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AfterGrade(BaseModel):
  name: str
  id: str


class Image(BaseModel):
  url: str


class Badge(BaseModel):
  id: str
  image: Optional[Image]


class TextColor(BaseModel):
  a: float
  b: float
  g: float
  r: float


class Background(BaseModel):
  textColor: TextColor
  image: Image
  id: str


class Nameplate(BaseModel):
  badges: list[Optional[Badge]]
  background: Background


class Uniform(BaseModel):
  name: str
  image: Image
  id: str

class Player(BaseModel):
  __isPlayer: str
  byname: str
  name: str
  nameId: str
  nameplate: Nameplate
  uniform: Uniform
  id: str
  species: str


class Weapon(BaseModel):
  name: str
  image: Image


class SpecialWeapon(BaseModel):
  name: str
  image: Image
  weaponId: int


class SpecialWeapon2(BaseModel):
  name: str
  image: Image
  id: str


class MyResult(BaseModel):
  player: Player
  weapons: list[Weapon]
  specialWeapon: Optional[SpecialWeapon]
  defeatEnemyCount: int
  deliverCount: int
  goldenAssistCount: int
  goldenDeliverCount: int
  rescueCount: int
  rescuedCount: int


class MemberResult(BaseModel):
  player: Player
  weapons: list[Weapon]
  specialWeapon: Optional[SpecialWeapon]
  defeatEnemyCount: int
  deliverCount: int
  goldenAssistCount: int
  goldenDeliverCount: int
  rescueCount: int
  rescuedCount: int


class Boss(BaseModel):
  name: str
  id: str
  image: Image


class BossResult(BaseModel):
  hasDefeatBoss: bool
  boss: Boss
  

class Enemy(BaseModel):
  name: str
  image: Image
  id: str


class EnemyResult(BaseModel):
  defeatCount: int
  teamDefeatCount: int
  popCount: int
  enemy: Enemy


class EventWave(BaseModel):
  name: str
  id: str


class WaveResult(BaseModel):
  waveNumber: int
  waterLevel: int
  eventWave: Optional[EventWave]
  deliverNorm: Optional[int]
  goldenPopCount: int
  teamDeliverCount: Optional[int]
  specialWeapons: list[SpecialWeapon2]


class CoopStage(BaseModel):
  name: str
  image: Image
  id: str


class Scale(BaseModel):
  gold: int
  silver: int
  bronze: int


class HistoryDetail(BaseModel):
  id: str


class CoopHistoryDetail(BaseModel):
  __typename: str
  id: str
  afterGrade: Optional[AfterGrade]
  myResult: MyResult
  memberResults: list[MemberResult]
  bossResult: Optional[BossResult]
  enemyResults: list[EnemyResult]
  waveResults: list[WaveResult]
  resultWave: int
  playedTime: datetime
  rule: str
  coopStage: CoopStage
  dangerRate: float
  scenarioCode: Optional[str]
  smellMeter: Optional[int]
  weapons: list[Weapon]
  afterGradePoint: Optional[int]
  scale: Optional[Scale]
  jobPoint: int
  jobScore: int
  jobRate: float
  jobBonus: int
  nextHistoryDetail: Optional[HistoryDetail]
  previousHistoryDetail: Optional[HistoryDetail]