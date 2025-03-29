from pydantic import BaseModel
from typing import List

class Department(BaseModel):
    departmentId: int
    displayName: str

class DepartmentsResponse(BaseModel):
    departments: List[Department]
