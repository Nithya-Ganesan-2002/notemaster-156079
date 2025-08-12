from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session

from src.db.session import get_session
from src.repositories.notes import NoteRepository
from src.schemas.note import NoteCreate, NoteRead, NoteUpdate

router = APIRouter(prefix="/notes", tags=["Notes"])


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[NoteRead],
    summary="List notes",
    description="Retrieve a paginated list of notes.",
    responses={
        200: {"description": "List of notes returned successfully."}
    },
)
def list_notes(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, gt=0, le=500, description="Max items to return"),
    session: Session = Depends(get_session),
):
    """List notes with pagination."""
    repo = NoteRepository(session)
    return repo.list(offset=offset, limit=limit)


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=NoteRead,
    summary="Get note",
    description="Retrieve a single note by its ID.",
    responses={
        200: {"description": "Note returned successfully."},
        404: {"description": "Note not found."},
    },
)
def get_note(
    note_id: int = Path(..., ge=1, description="ID of the note"),
    session: Session = Depends(get_session),
):
    """Fetch a note by ID."""
    repo = NoteRepository(session)
    note = repo.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note.",
    responses={
        201: {"description": "Note created successfully."},
        422: {"description": "Validation error."},
    },
)
def create_note(
    payload: NoteCreate,
    session: Session = Depends(get_session),
):
    """Create a note."""
    repo = NoteRepository(session)
    return repo.create(payload)


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=NoteRead,
    summary="Update note",
    description="Replace an existing note's content and/or title.",
    responses={
        200: {"description": "Note updated successfully."},
        404: {"description": "Note not found."},
        422: {"description": "Validation error."},
    },
)
def update_note(
    note_id: int = Path(..., ge=1, description="ID of the note"),
    payload: NoteUpdate = ...,
    session: Session = Depends(get_session),
):
    """Update an existing note (full update)."""
    repo = NoteRepository(session)
    note = repo.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    # For PUT, require at least one field present; enforce minimal behavior
    if payload.title is None and payload.content is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No fields to update")
    return repo.update(note, payload)


# PUBLIC_INTERFACE
@router.patch(
    "/{note_id}",
    response_model=NoteRead,
    summary="Partially update note",
    description="Partially update fields on an existing note.",
    responses={
        200: {"description": "Note updated successfully."},
        404: {"description": "Note not found."},
        422: {"description": "Validation error."},
    },
)
def patch_note(
    note_id: int = Path(..., ge=1, description="ID of the note"),
    payload: NoteUpdate = ...,
    session: Session = Depends(get_session),
):
    """Partially update an existing note."""
    repo = NoteRepository(session)
    note = repo.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if payload.title is None and payload.content is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No fields to update")
    return repo.update(note, payload)


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note by its ID.",
    responses={
        204: {"description": "Note deleted successfully."},
        404: {"description": "Note not found."},
    },
)
def delete_note(
    note_id: int = Path(..., ge=1, description="ID of the note"),
    session: Session = Depends(get_session),
):
    """Delete a note by ID."""
    repo = NoteRepository(session)
    note = repo.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    repo.delete(note)
    # 204 responses should not return a body; FastAPI will handle empty response.
    return None
