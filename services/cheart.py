from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.cheart import CHeartTable
from schemas.cheart import *

from db import get_db_session

class CHeartService:

    # 댓글 하트 관리
    def manageCHeart(self, manageCHeartInput: ManageCHeartInput, parent_id:str) -> Optional[CHeart]:
        """
        하트 관리
        --input
            - manageCHeartInput.comment_id: 댓글 아이디
        --output
            - CHeart: 하트 딕셔너리
        """
        db = get_db_session()

        Cheart = db.query(CHeartTable).filter(
            CHeartTable.comment_id == manageCHeartInput.comment_id,
            CHeartTable.parent_id == parent_id
        ).first()

        if Cheart is None:
            new_Cheart = CHeartTable(
                comment_id=manageCHeartInput.comment_id,
                parent_id = parent_id,
                createTime = datetime.now()
            )

            try:
                db.add(new_Cheart)
                db.commit()
                db.refresh(new_Cheart)
                return new_Cheart
            
            except Exception as e:
                db.rollback()
                raise e

        else:
            try:
                db.delete(Cheart)
                db.commit()
                return Cheart
            
            except Exception as e:
                db.rollback()
                raise e


    # 댓글 하트 생성
    def createCHeart(self,
                    createCHeartInput: CreateCHeartInput,
                    parent_id: str) -> Optional[CHeart]:
        """
        하트 생성
        --input
            - createCHeartInput.comment_id: 댓글 아이디
            - createCHeartInput.parent_id: 하트 누른 부모 아이디
        --output
            - CHeart: 하트 딕셔너리
        """
        db = get_db_session()
        try:
            Cheart = CHeartTable(
                comment_id=createCHeartInput.comment_id,
                parent_id = parent_id,
                createTime = datetime.now()
            )

            db.add(Cheart)
            db.commit()
            db.refresh(Cheart)

            return Cheart
        
        except Exception as e:
            db.rollback()
            raise (e)
        

    # 댓글 하트 삭제
    def deleteCHeart(self, deleteCHeartInput: DeleteCHeartInput, parent_id: str) -> Optional[CHeart]:
        """
        하트 삭제
        --input
            - deleteCHeartInput.comment_id: 댓글 아이디
            - deleteCHeartInput.parent_id: 하트 누른 부모 아이디
        --output
            - CHeart: 하트 딕셔너리
        """
        db = get_db_session()
        
        Cheart = db.query(CHeartTable).filter(
            CHeartTable.comment_id == deleteCHeartInput.comment_id,
            CHeartTable.parent_id == parent_id
        ).first()

        if Cheart is None:
            raise HTTPException(status_code=404, detail="Heart not found")
        
        try:
            db.delete(Cheart)
            db.commit()
            return Cheart
        
        except Exception as e:
            db.rollback()
            raise (e)