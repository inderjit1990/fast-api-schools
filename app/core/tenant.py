from fastapi import Request
from sqlalchemy.orm import Session
from app.models import schools

def get_tenant_schema(request: Request, db: Session) -> str:
    host = request.headers.get("host")
    SchoolModel = schools.School

    if host in ["127.0.0.1:8001", "127.0.0.1", "localhost:8001", "localhost"]:
        print("🏠 PRIMARY DOMAIN → Using MASTER DB (public schema)")
        return "public"

    domain = host.split(":")[0]
    cnt  = domain.count(".")

    # subdomain case: school1.example.com
    if domain.count(".") >= 2:
        subdomain = domain.split(".")[0]
        school = db.query(SchoolModel).filter(
            SchoolModel.subdomain == subdomain,
            SchoolModel.is_active == True
        ).first()
    else:
        # custom domain
        school = db.query(SchoolModel).filter(
            SchoolModel.custom_domain == domain,
            SchoolModel.is_active == True
        ).first()

    if not school:
        raise Exception("Schema not found")

    print(f"School: {school.name}")

    active_session = next(
        (s for s in school.sessions if s.is_active),
        None
    )

    if not active_session:
        raise Exception(f"No active session found for school {school.name}")

    print(
        f"  ✅ Active Session: {active_session.session_year} "
        f"(schema={active_session.schema_name})"
    )

    print(
        f"🏫 SCHOOL [{school.name}] → Using SCHEMA: {active_session.schema_name}"
    )
    sname = f"schema_{active_session.schema_name}"
    print(f"Schema Name: {sname}")
    return sname
