from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class GroupCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15,
        pattern=r"^\d+$",
        description="Mobile number with digits only"
    )


class SchoolCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    subdomain: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-z0-9-]+$",
        description="Lowercase letters, numbers, hyphen"
    )
    password: str = Field(..., min_length=8)
    address: str = Field(..., min_length=5, max_length=255)
    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        pattern=r"^\d+$"
    )
    email: EmailStr
    custom_domain: Optional[str] = Field(
        None,
        max_length=255
    )
    group_id: int = Field(..., gt=0)


class SchoolSessionCreate(BaseModel):
    school_id: int = Field(..., gt=0)
    session_year: int = Field(
        ...,
        ge=2000,
        le=2100,
        description="Academic year"
    )
    # schema_name: str = Field(
    #     ...,
    #     pattern=r"^[a-z0-9_]+$",
    #     max_length=63,
    #     description="Postgres schema name"
    # )
    # is_active: bool = True


class AdminCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15,
        pattern=r"^\d+$"
    )
    password: str = Field(..., min_length=8)
    email: EmailStr
    role: str = Field(
        ...,
        pattern=r"^(admin|staff|superadmin)$",
        description="Allowed roles"
    )

class SchoolStatusUpdate(BaseModel):
    school_id: int
    status : str = Field(
        ...,
        pattern=r"^(Active|Inactive|Pending)$",
        description="School status"
    )

    sessions: List["SchoolSessionResponse"] = []
    groups: Optional["GroupResponse"] = None


    class Config:
        from_attributes = True  # 👈 IMPORTANT (Pydantic v2)


class SchoolResponse(BaseModel):
    id: int
    name: str
    subdomain: str | None
    email: EmailStr
    phone: str
    user_name: str
    is_active: bool
    created_at: datetime

    sessions: List["SchoolSessionResponse"] = []
    groups: Optional["GroupResponse"] = None


    class Config:
        from_attributes = True  # 👈 IMPORTANT (Pydantic v2)


class SchoolSessionResponse(BaseModel):
    id: int
    school_id: int
    session_year: int
    schema_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # 👈 IMPORTANT (Pydantic v2)

class GroupResponse(BaseModel):
    id: int
    name: str
    mobile: str

    class Config:
        from_attributes = True  # 👈 IMPORTANT (Pydantic v2)
