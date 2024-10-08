from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from typing import Optional
from model.parent import ParentTable
from model.baby import BabyTable


# 산모수첩 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | pregn_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | baby_id   | varchar(255) | NO   | MUL | NULL    |                |
# | dname     | varchar(50)  | YES  |     | NULL    |                |
# | img       | varchar(255) | YES  |     | NULL    |                |
# | time      | datetime     | NO   |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class Pregnancy(BaseModel):
    pregn_id: int
    parent_id: str
    baby_id: str
    dname: Optional[str]
    img: Optional[str]
    time: DateTime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class PregnancyTable(DB_Base):
    __tablename__ = 'pregnancy'

    pregn_id = Column(Integer, primary_key=True,
                      nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    baby_id = Column(String(255), ForeignKey('baby.baby_id'), nullable=False)
    dname = Column(String(50), nullable=True)
    img = Column(String(255), nullable=True)
    time = Column(DateTime, nullable=False)

    parent = relationship(
        ParentTable, back_populates='pregnancy', passive_deletes=True)
    baby = relationship(
        BabyTable, back_populates='pregnancy', passive_deletes=True)
