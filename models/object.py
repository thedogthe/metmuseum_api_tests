from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl


class Constituent(BaseModel):
    constituentID: int
    role: str
    name: str
    constituentULAN_URL: Optional[HttpUrl] = None
    constituentWikidata_URL: Optional[HttpUrl] = None
    gender: Optional[str] = None


class Measurement(BaseModel):
    elementName: str
    elementDescription: Optional[str] = None
    elementMeasurements: Dict[str, float]


class DimensionParsed(BaseModel):
    element: str
    dimensionType: str
    dimension: float


class Tag(BaseModel):
    term: str
    AAT_URL: Optional[HttpUrl] = None
    Wikidata_URL: Optional[HttpUrl] = None


class ArtObject(BaseModel):
    objectID: int
    isHighlight: bool
    accessionNumber: str
    accessionYear: str
    isPublicDomain: bool
    primaryImage: Optional[HttpUrl] = None
    primaryImageSmall: Optional[HttpUrl] = None
    additionalImages: Optional[List[HttpUrl]] = None
    constituents: Optional[List[Constituent]] = None
    department: str
    objectName: str
    title: str
    culture: Optional[str] = None
    period: Optional[str] = None
    dynasty: Optional[str] = None
    reign: Optional[str] = None
    portfolio: Optional[str] = None
    artistRole: Optional[str] = None
    artistPrefix: Optional[str] = None
    artistDisplayName: Optional[str] = None
    artistDisplayBio: Optional[str] = None
    artistSuffix: Optional[str] = None
    artistAlphaSort: Optional[str] = None
    artistNationality: Optional[str] = None
    artistBeginDate: Optional[str] = None
    artistEndDate: Optional[str] = None
    artistGender: Optional[str] = None
    artistWikidata_URL: Optional[HttpUrl] = None
    artistULAN_URL: Optional[HttpUrl] = None
    objectDate: str
    objectBeginDate: int
    objectEndDate: int
    medium: str
    dimensions: str
    dimensionsParsed: Optional[List[DimensionParsed]] = None
    measurements: Optional[List[Measurement]] = None
    creditLine: str
    geographyType: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    subregion: Optional[str] = None
    locale: Optional[str] = None
    locus: Optional[str] = None
    excavation: Optional[str] = None
    river: Optional[str] = None
    classification: Optional[str] = None
    rightsAndReproduction: Optional[str] = None
    linkResource: Optional[str] = None
    metadataDate: datetime
    repository: str
    objectURL: Optional[HttpUrl] = None
    tags: Optional[List[Tag]] = None
    objectWikidata_URL: Optional[HttpUrl] = None
    isTimelineWork: bool
    GalleryNumber: Optional[str] = None