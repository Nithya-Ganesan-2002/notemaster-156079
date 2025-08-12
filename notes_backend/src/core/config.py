from functools import lru_cache
import os
from typing import List
from urllib.parse import quote_plus

from pydantic import BaseModel, Field, ValidationError


class Settings(BaseModel):
    """Application settings sourced from environment variables."""

    mysql_url: str = Field(..., description="MySQL host or URL (without scheme). Example: localhost")
    mysql_user: str = Field(..., description="MySQL username")
    mysql_password: str = Field(..., description="MySQL password")
    mysql_db: str = Field(..., description="MySQL database name")
    mysql_port: int = Field(..., description="MySQL port (e.g. 3306)")

    # PUBLIC_INTERFACE
    def sqlalchemy_uri(self) -> str:
        """Build the SQLAlchemy connection URI for PyMySQL driver."""
        password = quote_plus(self.mysql_password) if self.mysql_password is not None else ""
        return (
            f"mysql+pymysql://{self.mysql_user}:{password}"
            f"@{self.mysql_url}:{self.mysql_port}/{self.mysql_db}?charset=utf8mb4"
        )


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and cache application settings from environment variables.

    Environment variables required:
    - MYSQL_URL
    - MYSQL_USER
    - MYSQL_PASSWORD
    - MYSQL_DB
    - MYSQL_PORT

    Returns:
        Settings: Validated application settings.

    Raises:
        RuntimeError: If required environment variables are missing or invalid.
    """
    missing: List[str] = []
    env = {
        "mysql_url": os.getenv("MYSQL_URL"),
        "mysql_user": os.getenv("MYSQL_USER"),
        "mysql_password": os.getenv("MYSQL_PASSWORD"),
        "mysql_db": os.getenv("MYSQL_DB"),
        "mysql_port": os.getenv("MYSQL_PORT"),
    }
    for k, v in env.items():
        if v is None or v == "":
            missing.append(k.upper())

    if missing:
        raise RuntimeError(
            "Missing required environment variables for database connection: "
            + ", ".join(missing)
        )

    try:
        return Settings(
            mysql_url=str(env["mysql_url"]),
            mysql_user=str(env["mysql_user"]),
            mysql_password=str(env["mysql_password"]),
            mysql_db=str(env["mysql_db"]),
            mysql_port=int(env["mysql_port"]),  # may raise ValueError
        )
    except (ValueError, ValidationError) as e:
        raise RuntimeError(f"Invalid database configuration: {e}") from e
