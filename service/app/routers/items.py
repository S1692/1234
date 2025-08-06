"""Routes related to item CRUD operations."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from ..repositories.item_repository import ItemRepository
from ..core.db import get_session
from ..models.item import Item


class ItemCreate(BaseModel):
    name: str


class ItemRead(BaseModel):
    id: int
    name: str
    created_at: str


router = APIRouter(prefix="/items", tags=["items"])

item_repo = ItemRepository()


@router.get("/", response_model=List[ItemRead], summary="List items")
async def list_items(session: AsyncSession = Depends(get_session)) -> List[ItemRead]:
    """Return all items from the database."""
    items: List[Item] = await item_repo.get_all(session)
    return [ItemRead(id=i.id, name=i.name, created_at=i.created_at.isoformat()) for i in items]


@router.post(
    "/",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create new item",
)
async def create_item(
    item_in: ItemCreate, session: AsyncSession = Depends(get_session)
) -> ItemRead:
    """Create a new item with the provided name."""
    if not item_in.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name field is required",
        )
    item: Item = await item_repo.create(session, name=item_in.name)
    return ItemRead(id=item.id, name=item.name, created_at=item.created_at.isoformat())


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
async def delete_item(
    item_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    """Delete an item by its ID. Returns 404 if not found."""
    item = await item_repo.delete(session, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    # Return 204 No Content on successful deletion
    return None
