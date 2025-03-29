from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class ObjectIDsResponse(BaseModel):
    total: int
    objectIDs: List[int] = []

# Модель для параметров запроса
class ObjectIDsRequestParams(BaseModel):
    metadataDate: Optional[date] = None
    departmentIds: Optional[str] = None  