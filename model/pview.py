from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from model.parent import ParentTable
from model.post import PostTable


# 조회수 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | view_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | post_id    | int(11)      | NO   | MUL | NULL    |                |
# | createTime | datetime     | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class PView(BaseModel):
    view_id: int
    parent_id: str
    post_id: int
    createTime: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class PViewTable(DB_Base):
    __tablename__ = 'pview'

    view_id = Column(Integer, primary_key=True,
                     nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)
    createTime = Column(DateTime, nullable=True)

    post = relationship(PostTable, backref='pview', passive_deletes=True)
    parent = relationship(ParentTable, backref='pview', passive_deletes=True)
