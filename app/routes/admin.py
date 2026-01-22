from app.tasks.tenant_tasks import provision_tenant_schema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_public_db
from app.models import groups , sessions , schools
from app.schemas.master import SchoolCreate, GroupCreate, SchoolSessionCreate, SchoolResponse, SchoolStatusUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/group/create")
def create_group(payload: GroupCreate, db: Session = Depends(get_public_db)):
    Group = groups.Group
    db_group = Group(**payload.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return {
        "id": db_group.id,
        "name": db_group.name,
        "mobile": db_group.mobile,
    }


@router.post("/school/create")
def create_school(
    payload: SchoolCreate,
    db: Session = Depends(get_public_db),
):
    schoolModel = schools.School
    db_school = schoolModel(**payload.dict())
    db_school.user_name = db_school.generate_username()
    db.add(db_school)
    db.commit()
    db.refresh(db_school)

    return {
        "id": db_school.id,
        "name": db_school.name,
        "subdomain": db_school.subdomain,
        "user_name": db_school.user_name,
    }


@router.post("/school-session/create")
def create_school_session(
    payload: SchoolSessionCreate,
    db: Session = Depends(get_public_db),
):
    db_school_session = sessions.SchoolSession(**payload.dict())
    db_school_session.schema_name = db_school_session.generate_schemaname()
    db.add(db_school_session)
    db.commit()
    db.refresh(db_school_session)

    return {
        "id": db_school_session.id,
        "school_id": db_school_session.school_id,
        "session_year": db_school_session.session_year,
        "schema_name": db_school_session.schema_name,
        "is_active": db_school_session.is_active,
    }


@router.get("/schools")
def list_schools(db: Session = Depends(get_public_db)):
    schoolModel = schools.School
    schoolRecords = db.query(schoolModel).all()
    if not schoolRecords:
        raise HTTPException(status_code=404, detail="School not found")

    result = []
    for school in schoolRecords:
        active_session = next(
            (s for s in school.sessions if s.is_active),
            None
        )

        result.append({
            "id": school.id,
            "name": school.name,
            "subdomain": school.subdomain,
            "active_session": (
                {
                    "id": active_session.id,
                    "session_year": active_session.session_year,
                    "schema_name": active_session.schema_name,
                }
                if active_session else None
            )
        })

    return result



@router.get("/school/{school_id}", response_model= SchoolResponse)
def get_school(school_id: int, db: Session = Depends(get_public_db)):
    schoolModel = schools.School
    school = db.query(schoolModel).filter(schoolModel.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.get("/school/{school_id}/{status}")
def active_school(school_id:int, status: str, db: Session = Depends(get_public_db)):
    schoolModel = schools.School
    school = db.query(schoolModel).filter(schoolModel.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    school.status = status
    db.commit()
    db.refresh(school)

     # 2️⃣ Get active session
    active_session = next(
        (s for s in school.sessions if s.is_active),
        None
    )

    if not active_session:
        raise HTTPException(status_code=400, detail="No active session")
    
    schema_name = active_session.schema_name
    # 3️⃣ Trigger Celery task
    provision_tenant_schema.delay(schema_name)

    return {
        "message": "School activated",
        "schema": schema_name,
        "task": "schema provisioning started",
    }
