from dataclasses import dataclass
from typing import Optional

ENV_TOKEN_KEY = "GITHUB_TOKEN"

@dataclass
class Config:
    token: Optional[str] = None
