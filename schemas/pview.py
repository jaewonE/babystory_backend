from pydantic import BaseModel
from typing import Optional, List

from model.pview import *

class CreatePViewInput(BaseModel):
    post_id: int

class CreatePViewOutput(BaseModel):
    success: int
    pview: Optional[PView]

class DeletePViewInput(BaseModel):
    post_id: int

class DeletePViewOutput(BaseModel):
    success: int
    pview: Optional[PView]