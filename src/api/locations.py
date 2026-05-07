from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import get_location_repository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.location import Location, LocationCreate, LocationUpdate

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/", response_model=List[Location])
async def get_locations(
    skip: int = 0,
    limit: int = 100,
    only_published: bool = True,
    repo: LocationRepository = Depends(get_location_repository)
):
    if only_published:
        return repo.get_published(skip=skip, limit=limit)
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{location_id}", response_model=Location)
async def get_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repository)
):
    location = repo.get_by_id(location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация не найдена"
        )
    return location

@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    repo: LocationRepository = Depends(get_location_repository)
):
    return repo.create(**location_data.model_dump())

@router.put("/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    repo: LocationRepository = Depends(get_location_repository)
):
    existing = repo.get_by_id(location_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация не найдена"
        )
    
    update_data = location_data.model_dump(exclude_unset=True)
    return repo.update(location_id, **update_data)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repository)
):
    deleted = repo.delete(location_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация не найдена"
        )
    return None