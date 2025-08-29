from fastapi import APIRouter, HTTPException, Query, Path, status
from smart_solutions.app.schemas.solution import (
    SolutionCreate,
    ImageCreate,
    VideoCreate,
    SolutionRead,
    VideoRead,
    TagRead,
    ImageRead
)
from smart_solutions.app.models.solution import (
    Solution,
    Image,
    Video,
    Tag,
    SolutionTagLink
)
from smart_solutions.app.models.user import User
from smart_solutions.app.schemas.user import UserPublic
from smart_solutions.app.api.deps import SessionDep, CurrentUser
from sqlalchemy import text
from typing import Annotated
from uuid import UUID
from smart_solutions.app.core.config import settings
from sqlmodel import func, select, delete
from smart_solutions.app.crud.user import get_user_by_id

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
async def create_solution(*, session: SessionDep, solution_in: SolutionCreate, current_user: CurrentUser):
    print("heeeereeee")
    if not solution_in.tags:
        raise HTTPException(status_code=400, detail="One or more tags must be added to the solution")
    for tag in solution_in.tags:
        tag = tag.lower()
        if tag not in settings.ALLOWED_TAGS:
            raise HTTPException(status_code=400, detail=f"tag : {tag} is not a part of the tags accepted tags accepted are : {settings.ALLOWED_TAGS}")
    if not solution_in.images and not solution_in.videos:
        raise HTTPException(status_code=400, detail=f"Either an image or a video must be provided for the solution")

    solution = Solution(
        name=solution_in.name,
        description=solution_in.description,
        owner=current_user
    )

    if solution_in.images:
        solution.images = [Image(**img.dict()) for img in solution_in.images]
    if solution_in.videos:
        solution.videos = [Video(**vid.dict()) for vid in solution_in.videos]
    if solution_in.tags:
        tags = []
        for tag in solution_in.tags:
            existing_tag = session.query(Tag).filter(Tag.name == tag.lower()).first()
            if existing_tag:
                tags.append(existing_tag)
            else:
                new_tag = Tag(name=tag.lower())
                session.add(new_tag)
                session.flush()
                tags.append(new_tag)
        solution.tags = tags

    session.add(solution)
    session.commit()
    session.refresh(solution)
    print("created soln : ", solution)
    return SolutionRead(
        id=solution.id,
        name=solution.name,
        description=solution.description,
        tags=[TagRead(name=tag.name) for tag in solution.tags],
        images=[ImageRead(url=img.url, name=img.name) for img in solution.images],
        videos=[VideoRead(url=vid.url, name=vid.name) for vid in solution.videos]
    )

@router.get("/", response_model=list[SolutionRead])
async def read_solutions(*, session: SessionDep,
                          offset: int = 0,
                          category: str = None,
                          limit: Annotated[int, Query(le=10)] = 10,):
    if not category:
        # When no category filter, get all solutions with their related data
        query = select(Solution).offset(offset).limit(limit)
        results = session.exec(query).all()
        
        # Load tags, images, and videos for each solution
        solutions = []
        for solution in results:
            # Get tags for this solution
            tags_query = (
                select(Tag)
                .join(SolutionTagLink, Tag.id == SolutionTagLink.tag_id)
                .where(SolutionTagLink.solution_id == solution.id)
            )
            tags = session.exec(tags_query).all()
            
            # Get images for this solution (assuming you have a SolutionImage model)
            images_query = select(Image).where(Image.solution_id == solution.id)
            images = session.exec(images_query).all()
            print("imagesssss : ", images)
            # Get videos for this solution (assuming you have a SolutionVideo model)
            videos_query = select(Video).where(Video.solution_id == solution.id)
            videos = session.exec(videos_query).all()
            
            select(User)
            # Create SolutionRead object with all related data
            solution_data = {
                **solution.__dict__,
                "tags": [TagRead(**tag.__dict__) for tag in tags],
                "images": [ImageRead(**img.__dict__) for img in images],
                "videos": [VideoRead(**vid.__dict__) for vid in videos]
            }
            solutions.append(SolutionRead(**solution_data))
    else:
        # When filtering by category/tags
        tags = category.split(',')
        tags_available = [
            t.name for t in session.exec(select(Tag)).all()
        ]
        valid_tags = [tag for tag in tags if tag in tags_available]
        if not valid_tags:
            return []
        # Get solutions that have any of the specified tags
        query = (
            select(Solution)
            .join(SolutionTagLink, Solution.id == SolutionTagLink.solution_id)
            .join(Tag, Tag.id == SolutionTagLink.tag_id)
            .where(Tag.name.in_(valid_tags))
            .distinct()
            .offset(offset)
            .limit(limit)
        )
        results = session.exec(query).all()
        # Load related data for filtered solutions
        solutions = []
        for solution in results:
            # Get all tags for this solution
            tags_query = (
                select(Tag)
                .join(SolutionTagLink, Tag.id == SolutionTagLink.tag_id)
                .where(SolutionTagLink.solution_id == solution.id)
            )
            tags = session.exec(tags_query).all()
            # Get images
            images_query = select(Image).where(Image.solution_id == solution.id)
            images = session.exec(images_query).all()
            # Get videos
            videos_query = select(Video).where(Video.solution_id == solution.id)
            videos = session.exec(videos_query).all()

            user = get_user_by_id(session=session, id=solution.owner_id)
            user = UserPublic.model_validate(user, from_attributes=True)
            solution_data = {
                **solution.__dict__,
                "tags": [TagRead(**tag.__dict__) for tag in tags],
                "images": [ImageRead(**img.__dict__) for img in images],
                "videos": [VideoRead(**vid.__dict__) for vid in videos],
                "owner": user.name
            }
            solutions.append(SolutionRead(**solution_data))

    return solutions

@router.get("/{solution_id}")
async def read_solution(*, session: SessionDep,
                        solution_id: Annotated[UUID, Path()]):
    result = session.execute(select(Solution)
                               .join(SolutionTagLink, Solution.id == SolutionTagLink.solution_id)
                               .join(Tag, Tag.id == SolutionTagLink.tag_id)).first()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    # print("resultttttt : ", result)

    tags_query = (
                select(Tag)
                .join(SolutionTagLink, Tag.id == SolutionTagLink.tag_id)
                .where(SolutionTagLink.solution_id == solution_id)
            )
    tags = session.exec(tags_query).all()
    # Get images
    images_query = select(Image).where(Image.solution_id == solution_id)
    images = session.exec(images_query).all()
    # Get videos
    videos_query = select(Video).where(Video.solution_id == solution_id)
    videos = session.exec(videos_query).all()
    solution_data = result[0].model_dump()
    solution = {
        **solution_data,
        "tags": [TagRead(**tag.__dict__) for tag in tags],
        "images": [ImageRead(**img.__dict__) for img in images],
        "videos": [VideoRead(**vid.__dict__) for vid in videos]
    }
    # print("soln : ", solution)
    return SolutionRead(**solution)
