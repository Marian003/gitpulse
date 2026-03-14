from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Config:
    """Configuration for the GitPulse API client."""

    token: Optional[str] = None
    api_base: str = "https://api.github.com"
    timeout: float = 10.0
    max_retries: int = 2

    @property
    def headers(self) -> dict[str, str]:
        h = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h


def resolve_token(token_flag: Optional[str] = None) -> Optional[str]:
    """Return token: flag takes priority, then GITHUB_TOKEN env var."""
    if token_flag:
        return token_flag
    env_token = os.environ.get("GITHUB_TOKEN")  # check standard env var
    return env_token if env_token else None
