from pydantic import BaseModel, HttpUrl, Field
from uuid import UUID
from typing import List, Optional


class ImageCreate(BaseModel):
    url: HttpUrl
    name: str


class ImageRead(ImageCreate):
    url: HttpUrl
    name: str
    model_config = {
        "from_attributes": True
    }


class VideoCreate(BaseModel):
    url: HttpUrl
    name: str


class VideoRead(VideoCreate):

    model_config = {
        "from_attributes": True
    }


class SolutionCreate(BaseModel):
    name: str
    description: Optional[str] = Field(default=None, examples=["Detect cars in Image"])
    tags: Optional[List[str]] = []
    image: Optional[List[ImageCreate]] = []
    video: Optional[List[VideoCreate]] = []


class TagRead(BaseModel):
    name: str


class SolutionRead(BaseModel):
    id: UUID
    name: str
    description: str
    tags: List[TagRead] = []
    image: List[ImageRead] = []
    video: List[VideoRead] = []

    model_config = {
        "from_attributes": True
    }

