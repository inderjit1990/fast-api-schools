from fastapi import FastAPI
# from app.core.database import Base, engine
from app.routes import master , tenant , admin , auth_master
from app.middleware.tenant import TenantMiddleware
from app.core.db_exceptions import db_integrity_error_handler
from sqlalchemy.exc import IntegrityError


# Base.metadata.create_all(bind=engine)


app = FastAPI(title="School API")

# 👇 Register DB error handler
app.add_exception_handler(
    IntegrityError,
    db_integrity_error_handler
)

app.add_middleware(TenantMiddleware)

app.include_router(master.router)
app.include_router(auth_master.router)
app.include_router(admin.router)
app.include_router(tenant.router)