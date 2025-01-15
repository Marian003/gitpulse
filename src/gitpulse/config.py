import os
from dataclasses import dataclass
from typing import Optional

ENV_TOKEN_KEY = "GITHUB_TOKEN"

@dataclass
class Config:
    token: Optional[str] = None

def resolve_token(token_flag: Optional[str] = None) -> Optional[str]:
    if token_flag:
        return token_flag
    return os.environ.get(ENV_TOKEN_KEY) or None
