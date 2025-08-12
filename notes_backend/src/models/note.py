from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    """SQLModel representation of a note entity stored in MySQL."""

    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=255, description="Short title for the note")
    content: str = Field(
        sa_column=Column(Text, nullable=False),
        description="Full note content (rich text supported as string).",
        default="",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp (UTC).",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp (UTC).",
    )
