from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_public_db
from app.models.classes import Classes
from app.schemas.tenant import ClassCreate

router = APIRouter(prefix="/tenant", tags=["Schools"])


@router.post("/class/create")
def create_class(
    class_data: ClassCreate,
    db: Session = Depends(get_public_db),
):
    db_class = Classes(**class_data.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)

    return {
        "id": db_class.id,
        "name": db_class.name,
    }


# @router.get("/schools")
# def list_schools(db: Session = Depends(get_public_db)):
#     schools = db.query(School).all()
#     if not schools:
#         raise HTTPException(status_code=404, detail="School not found")

#     result = []
#     for school in schools:
#         active_session = next(
#             (s for s in school.sessions if s.is_active),
#             None
#         )

#         result.append({
#             "id": school.id,
#             "name": school.name,
#             "subdomain": school.subdomain,
#             "active_session": (
#                 {
#                     "id": active_session.id,
#                     "session_year": active_session.session_year,
#                     "schema_name": active_session.schema_name,
#                 }
#                 if active_session else None
#             )
#         })

#     return result



# @router.get("/school/{school_id}")
# def get_school(school_id: int, db: Session = Depends(get_public_db)):
#     school = db.query(School).filter(School.id == school_id).first()
#     if not school:
#         raise HTTPException(status_code=404, detail="School not found")
#     return school