from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    """Shared fields for Note create/update."""
    title: str = Field(max_length=255, description="Short title for the note")
    content: str = Field(description="Full note content.")


class NoteCreate(NoteBase):
    """Payload for creating a new note."""
    pass


class NoteUpdate(SQLModel):
    """Payload for updating an existing note; all fields optional."""
    title: Optional[str] = Field(default=None, max_length=255, description="Short title for the note")
    content: Optional[str] = Field(default=None, description="Full note content.")


class NoteRead(SQLModel):
    """Response model for notes."""
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
