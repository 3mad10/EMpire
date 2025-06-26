from fastapi import APIRouter, HTTPException, Query, Path, status
from smart_solutions.app.schemas.solution import SolutionCreate, ImageCreate, VideoCreate, SolutionRead, VideoRead, TagRead, ImageRead
from smart_solutions.app.models.solution import Solution, Image, Video, Tag
from smart_solutions.app.core.deps import SessionDep
from sqlalchemy import text
from typing import Annotated
from uuid import UUID
from smart_solutions.app.core.config import settings


router = APIRouter(prefix="/solution", tags=["solution"])

"""
Create a solution and add it to database
Requirements:
    - The solutions must have at least one tag and optionally multiple tags
    - The Solution must have either an image or a video or multiple of both
    - The Solution must have a unique name if the solution is from the same user
    - Different Users can have solution names with the same name
    - if and only if the solution is added to the database return the solution
      with a status code HTTP_201_CREATED
    - if the creation of the solution failed due to a pydantic model 
      validation return status code HTTP_422_UNPROCESSABLE_ENTITY
    - if the User do not have permission to add a solution return status code HTTP_401_UNAUTHORIZED
    - if the creation of the solution failed due to no images nor videos 
      provided validation return status code HTTP_400_BAD_REQUEST with a description for the issue
    - If the provided tag is not a tag that exists in the websites return HTTP_400_BAD_REQUEST
    - if the video is not an actual video format return HTTP_400_BAD_REQUEST
"""
@router.post("/", response_model=SolutionRead,
             status_code=status.HTTP_201_CREATED)
async def create_solution(*, session: SessionDep, solution_in: SolutionCreate):
    if not solution_in.tags:
        raise HTTPException(status_code=400, detail="One or more tags must be added to the solution")
    for tag in solution_in.tags:
        tag = tag.lower()
        if tag not in settings.ALLOWED_TAGS:
            raise HTTPException(status_code=400, detail=f"tag : {tag} is not a part of the tags accepted tags accepted are : {settings.ALLOWED_TAGS}")
    if not solution_in.image and not solution_in.video:
        raise HTTPException(status_code=400, detail=f"Either an image or a video must be provided for the solution")

    solution = Solution(
        name=solution_in.name,
        description=solution_in.description,
    )

    if solution_in.image:
        solution.image = [Image(**img.dict()) for img in solution_in.image]
    if solution_in.video:
        solution.video = [Video(**vid.dict()) for vid in solution_in.video]
    if solution_in.tags:
        solution.tags = [Tag(name=tag.lower()) for tag in solution_in.tags]

    session.add(solution)
    session.commit()
    session.refresh(solution)
    return SolutionRead(
        id=solution.id,
        name=solution.name,
        description=solution.description,
        tags=[TagRead(name=tag.name) for tag in solution.tags],
        image=[ImageRead(url=img.url, name=img.name) for img in solution.image],
        video=[VideoRead(url=vid.url, name=vid.name) for vid in solution.video]
    )

@router.get("/", response_model=list[SolutionRead])
async def read_solutions(*, session: SessionDep,
                          offset: int = 0,
                          catagory: str = None,
                          limit: Annotated[int, Query(le=10)] = 10,):
    if not catagory:
        print("taaaaags : ", catagory)
        query = text("SELECT * FROM solution LIMIT :limit OFFSET :offset")
        results = session.execute(query, {"limit": limit,
                                          "offset": offset})
    else:
        tags = catagory.split(',')
        
        tags_available = [
            t["name"] for t in session.execute(text("SELECT tag.name FROM tag")).mappings().all()
        ]
        tags_tuple = tuple(tag for tag in tags if tag in tags_available)
        if not tags_tuple:
            return []  # No valid tags matched
        query = text("""SELECT DISTINCT solution.* FROM ((solution
                    INNER JOIN solutiontaglink ON solution.id = solutiontaglink.solution_id)
                    INNER JOIN tag ON tag.id = solutiontaglink.tag_id) 
                    WHERE tag.name IN :tags
                    LIMIT :limit OFFSET :offset""")
        results = session.execute(query, {"limit": limit,
                                          "offset": offset,
                                          "tags": tags_tuple})

    rows = results.mappings().all()
    solutions = []
    for row in rows:
        row = dict(row)  # now mutable
        row["tags"] = row["tags"].split(",") if row["tags"] else []
        row["tags"] = [TagRead(name=tag) for tag in row["tags"]]
        solutions.append(SolutionRead(**row))

    return solutions

@router.get("/{solution_id}")
async def read_solution(*, session: SessionDep,
                        solution_id: Annotated[UUID, Path()]):
    query = text("SELECT * FROM solution WHERE id = :solution_id")
    result = session.execute(query, {"solution_id": solution_id})
    result = result.mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    result_dict = dict(result)
    result_dict["tags"] = result_dict["tags"].split(",") if result_dict["tags"] else []
    return result_dict
