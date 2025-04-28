from __future__ import annotations

from pathlib import Path

from mcp.client.stdio import StdioServerParameters
from pydantic import BaseModel

from .utils import load_json


class Config(BaseModel):
    name: str
    instructions: str
    mcp_servers: dict[str, StdioServerParameters]

    @classmethod
    def from_json(cls, f: str | Path) -> Config:
        data = load_json(f)
        return cls.model_validate(data)
