"""
Centralized configuration loader.

Only responsibility:
- Load environment variables
- Expose DB connection settings
"""

from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class PostgresConfig:
    host: str
    port: int
    database: str
    user: str
    password: str


@dataclass(frozen=True)
class HFConfig:
    token: str | None


def load_postgres_config() -> PostgresConfig:
    """
    Load PostgreSQL configuration from environment variables.
    """
    return PostgresConfig(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def load_hf_config() -> HFConfig:
    """
    Load Hugging Face configuration from environment variables.
    """
    return HFConfig(
        token=os.getenv("HF_TOKEN")
    )
