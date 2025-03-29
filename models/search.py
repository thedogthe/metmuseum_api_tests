from typing import List, Optional
from pydantic import BaseModel


# Модель для параметров запроса 
class SearchRequestParams(BaseModel):
    q: Optional[str] = None
    isHighlight: Optional[bool] = None
    title: Optional[bool] = None
    tags: Optional[bool] = None
    departmentId: Optional[int] = None
    isOnView: Optional[bool] = None
    artistOrCulture: Optional[bool] = None
    medium: Optional[str] = None  # Можно было бы List[str] с кастомным валидатором
    hasImages: Optional[bool] = None
    geoLocation: Optional[str] = None  # Можно было бы List[str] с кастомным валидатором
    dateBegin: Optional[int] = None
    dateEnd: Optional[int] = None


# Модель для ответа API
class SearchResponse(BaseModel):
    total: int
    objectIDs: List[int] = []