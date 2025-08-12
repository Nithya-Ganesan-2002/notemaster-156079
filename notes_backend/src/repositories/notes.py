from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from src.models.note import Note
from src.schemas.note import NoteCreate, NoteUpdate


class NoteRepository:
    """Repository encapsulating CRUD operations for Note."""

    def __init__(self, session: Session) -> None:
        self.session = session

    # PUBLIC_INTERFACE
    def get(self, note_id: int) -> Optional[Note]:
        """Fetch a single note by ID."""
        return self.session.get(Note, note_id)

    # PUBLIC_INTERFACE
    def list(self, offset: int = 0, limit: int = 100) -> List[Note]:
        """List notes with pagination."""
        statement = select(Note).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    # PUBLIC_INTERFACE
    def create(self, payload: NoteCreate) -> Note:
        """Create and persist a new note from payload."""
        note = Note(title=payload.title, content=payload.content)
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    # PUBLIC_INTERFACE
    def update(self, note: Note, payload: NoteUpdate) -> Note:
        """Update fields on the provided note entity and persist changes."""
        if payload.title is not None:
            note.title = payload.title
        if payload.content is not None:
            note.content = payload.content
        note.updated_at = datetime.utcnow()
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    # PUBLIC_INTERFACE
    def delete(self, note: Note) -> None:
        """Delete the provided note entity."""
        self.session.delete(note)
        self.session.commit()
