from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.hospital import *

# 산모수첩 생성
class CreateHospitalInput(BaseModel):
    diary_id: int
    baby_id: str
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float] = None
    baby_cm: Optional[int] = None
    special: Optional[str] = None
    next_day: Optional[datetime] = None

class CreateHospitalOutput(BaseModel):
    success: int
    message: str
    hospital: Hospital


# 다이어리에 대한 전체 산모수첩 조회
class GetHospitalInput(BaseModel):
    diary_id: int
    start_time: datetime
    end_time: datetime

class GetHospitalOutput(BaseModel):
    success: int
    message: str
    hospitals: List[Hospital]


# 하나의 산모수첩 조회
class GetHospitalOutput(BaseModel):
    success: int
    message: str
    hospital: Hospital


# 산모수첩 수정
class UpdateHospitalInput(BaseModel):
    hospital_id: int
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float] = None
    baby_cm: Optional[int] = None
    special: Optional[str] = None
    next_day: Optional[datetime] = None

class UpdateHospitalOutput(BaseModel):
    success: int
    message: str
    hospital: Hospital


# 산모수첩 삭제
class DeleteHospitalOutput(BaseModel):
    success: bool
    message: str