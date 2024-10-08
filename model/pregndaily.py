from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, TEXT
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.pregnancy import PregnancyTable


# 산모수첩 ( 일기 ) 테이블
# +----------+--------------+------+-----+---------+----------------+
# | Field    | Type         | Null | Key | Default | Extra          |
# +----------+--------------+------+-----+---------+----------------+
# | daily_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | pregn_id | int(11)      | NO   | MUL | NULL    |                |
# | daily    | datetime     | NO   |     | NULL    |                |
# | title    | varchar(50)  | NO   |     | NULL    |                |
# | picture  | varchar(255) | YES  |     | NULL    |                |
# | post     | text         | YES  |     | NULL    |                |
# +----------+--------------+------+-----+---------+----------------+


class Pregndaily(BaseModel):
    daily_id: int
    pregn_id: int
    daily: datetime
    title: str
    picture: Optional[str]
    post: Optional[str]

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class PregndailyTable(DB_Base):
    __tablename__ = 'pregndaily'

    daily_id = Column(Integer, primary_key=True,
                      nullable=False, autoincrement=True)
    pregn_id = Column(Integer, ForeignKey(
        'pregnancy.pregn_id'), nullable=False)
    daily = Column(DateTime, nullable=False)
    title = Column(String(50), nullable=False)
    picture = Column(String(255), nullable=True)
    post = Column(TEXT, nullable=True)

    pregnancy = relationship(
        PregnancyTable, back_populates='pregndaily', passive_deletes=True)
