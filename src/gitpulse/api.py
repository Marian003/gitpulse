from typing import Any, Optional
import httpx
from gitpulse.config import Config

class GitHubAPIError(Exception):
    """Base exception for GitHub API errors."""

class UserNotFoundError(GitHubAPIError):
    def __init__(self, username: str) -> None:
        super().__init__(f"GitHub user '{username}' not found.")
        self.username = username

class RateLimitError(GitHubAPIError):
    def __init__(self) -> None:
        super().__init__("GitHub API rate limit exceeded.")

class GitHubClient:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "GitHubClient":
        self._client = httpx.AsyncClient(
            headers=self._config.headers,
            timeout=self._config.timeout,
        )
        return self

    async def __aexit__(self, *_: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def _get(self, path: str) -> Any:
        assert self._client is not None
        resp = await self._client.get(path)
        return resp.json()
