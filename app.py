#!/usr/bin/env python
"""
Simplified entry point for the Conduit API.
Run with: python app.py
"""
import asyncio
import os

import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine

from conduit.core.config import get_app_settings
from conduit.infrastructure.models import Base


async def init_db() -> None:
    """Initialize the database by creating all tables."""
    settings = get_app_settings()
    engine = create_async_engine(settings.sql_db_uri)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print(f"Database initialized: {settings.sql_db_uri}")


def main() -> None:
    """Main entry point."""
    os.environ.setdefault("APP_ENV", "dev")

    asyncio.run(init_db())

    uvicorn.run("conduit.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
