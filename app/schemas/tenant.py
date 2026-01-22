from pydantic import BaseModel


class ClassCreate(BaseModel):
    name: str


class SectionCreate(BaseModel):
    name: str
    class_id: int

class studentCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    class_id: int
    section_id: int

class SchoolProfileCreate(BaseModel):
    name: str
    school_id: int
    mobile: int
    address: str