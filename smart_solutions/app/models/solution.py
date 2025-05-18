from sqlmodel import Field, SQLModel, Relationship
import uuid
from typing import List, Optional


class Image(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    solution_id: uuid.UUID = Field(foreign_key="solution.id")
    solution: Optional["Solution"] = Relationship(back_populates="image")
    url: str
    name: str


class Video(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    solution_id: uuid.UUID = Field(foreign_key="solution.id")
    solution: Optional["Solution"] = Relationship(back_populates="video")
    url: str
    name: str


class SolutionTagLink(SQLModel, table=True):
    solution_id: uuid.UUID = Field(foreign_key="solution.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    solutions: List["Solution"] = Relationship(back_populates="tags",
                                               link_model=SolutionTagLink)


class Solution(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          primary_key=True)
    name: str = Field(min_length=3, nullable=False)
    description: str = Field(nullable=False)
    image: List[Image] = Relationship(back_populates="solution")
    video: List[Video] = Relationship(back_populates="solution")
    tags: List[Tag] = Relationship(back_populates="solutions",
                                   link_model=SolutionTagLink)


Image.update_forward_refs()
Video.update_forward_refs()
