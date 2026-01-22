from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation, ForeignKeyViolation, NotNullViolation


def db_integrity_error_handler(request: Request, exc: IntegrityError):
    error = exc.orig

    # UNIQUE constraint
    if isinstance(error, UniqueViolation):
        return JSONResponse(
            status_code=409,
            content={
                "error": "DUPLICATE_ENTRY",
                "message": "Resource already exists",
            },
        )

    # FOREIGN KEY constraint
    if isinstance(error, ForeignKeyViolation):
        return JSONResponse(
            status_code=400,
            content={
                "error": "INVALID_REFERENCE",
                "message": "Invalid foreign key reference",
            },
        )

    # NOT NULL constraint
    if isinstance(error, NotNullViolation):
        return JSONResponse(
            status_code=400,
            content={
                "error": "MISSING_FIELD",
                "message": "Required field is missing",
            },
        )

    # Fallback
    return JSONResponse(
        status_code=400,
        content={
            "error": "DATABASE_ERROR",
            "message": "Database integrity error",
        },
    )
