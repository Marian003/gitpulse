from typing import Any, Optional
import httpx
from gitpulse.config import Config

class GitHubClient:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._client: Optional[httpx.AsyncClient] = None
