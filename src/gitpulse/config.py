import os
from dataclasses import dataclass
from typing import Optional

ENV_TOKEN_KEY = "GITHUB_TOKEN"

@dataclass
class Config:
    token: Optional[str] = None
    timeout: float = 15.0
    max_retries: int = 2

    @property
    def headers(self) -> dict:
        h = {"Accept": "application/vnd.github+json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

def resolve_token(token_flag: Optional[str] = None) -> Optional[str]:
    if token_flag:
        return token_flag
    return os.environ.get(ENV_TOKEN_KEY) or None
