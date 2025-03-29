from pydantic import BaseModel
from typing import List

class ObjectList(BaseModel):
    total: int
    objectIDs: List[int]
