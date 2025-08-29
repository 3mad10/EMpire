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
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    images: Optional[List[ImageCreate]] = []
    videos: Optional[List[VideoCreate]] = []
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Car Detector",
                    "tags": ["detection", "tracking"],
                    "description": "Detect cars in an image",
                    "images": [
                        {
                         "name": "On road detection",
                         "url": "https://www.mouser.mx/blog/Portals/11/Vehicle%20Detection%20AI_Theme%20Image_min.jpg"
                        },
                        {
                         "name": "On road detection 2",
                         "url": "https://user-images.githubusercontent.com/86667690/127769547-9aff5cea-4778-423e-b410-b4ebc18f0011.png"
                        },
                    ],
                    "video": []
                 }
            ]
        }
    }


class TagRead(BaseModel):
    name: str


class SolutionRead(BaseModel):
    id: UUID
    name: str
    owner: str
    description: str
    tags: List[TagRead] = []
    images: List[ImageRead] = []
    videos: List[VideoRead] = []

    model_config = {
        "from_attributes": True
    }
