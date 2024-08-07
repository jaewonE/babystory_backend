from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.post import *



# 게시물 생성
class CreatePostInput(BaseModel):
    reveal: int
    title: str
    content: str
    hashList: Optional[str]

class CreatePostOutput(BaseModel):
    post: Optional[Post]



# 게시물 사진
class UploadPhotoOutput(BaseModel):
    success: bool



# 게시물 수정
class UpdatePostInput(BaseModel):
    post_id: int
    reveal: int
    title: str
    content: str
    hashList: Optional[str]

class UpdatePostOutput(BaseModel):
    success: int
    post: Post



# 게시물 삭제
class DeletePostInput(BaseModel):
    post_id: int

class DeletePostOutput(BaseModel):
    success: int
    post: Optional[Post]