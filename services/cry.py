from fastapi import UploadFile
from typing import List, Optional, Union
from datetime import datetime
from sqlalchemy import func, text
import os
import pandas as pd
import numpy as np
from sqlalchemy.dialects import mysql

from model.cry_state import CryState
from constants.path import *
from model.parent import Parent
from model.types.cry_state import CryStateType
from db import get_db_session
from services.cry_predict import cry_predict
from utils import save_log


class CryService:
    def __init__(self):
        self.model = CryState

    async def predict(self, file: UploadFile, uid: str) -> dict:
        content = await file.read()

        curtime = datetime.now()
        timestamp = curtime.strftime("%Y%m%d-%H%M%S")
        save_filename = f"{uid}_{timestamp}.wav"
        file_path = os.path.join(BABY_CRY_DATASET_DIR, save_filename)
        with open(file_path, 'wb') as f:
            f.write(content)

        # get predictMap
        print(f'response state:')
        predictMap = await cry_predict(content)
        for key in predictMap:
            print(f'{key}: {predictMap[key]}')

        return {
            "time": curtime.strftime("%Y-%m-%d %H:%M:%S"),
            "filename": file.filename,
            'predictMap': predictMap,
            "intensity": 'medium',
            'audioURL': timestamp,
        }

    async def _inspect(self, df: pd.DataFrame) -> dict:
        # 1. 주로 우는 시간대 분석
        cry_freq_hour = df['time'].dt.hour.value_counts().sort_index()

        # 2. 일별 울음 빈도 분석
        cry_freq_date = df[['id']].groupby(
            df['time'].dt.date).count().reset_index()
        cry_freq_date['time'] = cry_freq_date['time'].astype(str)

        # 3. 울음 원인 빈도 분석
        type_freq = df['type'].value_counts()
        type_freq.sort_values(ascending=True, inplace=True)

        # 4. 울음 원인에 따른 울음 지속시간 분석
        duration_of_type = df[['type', 'duration']].groupby('type').mean()
        duration_of_type.sort_values(by='duration', inplace=True)

        min_value = duration_of_type['duration'].min().astype(int)
        duration_of_type['duration'] -= min_value
        bar_percent = (duration_of_type['duration'] /
                       duration_of_type['duration'].max()).round(3)

        return {
            'cry_freq_hour': cry_freq_hour.tolist(),
            'cry_freq_date': {
                'date': cry_freq_date['time'].tolist(),
                'freqs': cry_freq_date['id'].tolist()
            },
            'type_freq': type_freq.to_dict(),
            'duration_of_type': {
                'type': duration_of_type.index.tolist(),
                'duration': duration_of_type['duration'].round(3).tolist(),
                'bar_percent': bar_percent.tolist()
            }
        }

    async def inspect(self, baby_id: str, start_date: datetime, end_date: datetime) -> Optional[dict]:
        db = get_db_session()
        try:
            query = db.query(self.model).filter(
                self.model.babyId == baby_id,
                self.model.time >= start_date,
                self.model.time <= end_date
            )
            sql_query = query.statement.compile(
                dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})

            df = pd.read_sql(sql_query, db.connection())
            res = await self._inspect(df)

            file_name = f"{baby_id}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"
            save_log(os.path.join(CRY_INSPECT_LOG_DIR,
                     f'{file_name}.json'), res)
            res['logId'] = file_name
            return res

        except Exception as e:
            print(e)
            return None