import asyncio
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

    async def _get(self, path: str, params: Optional[dict] = None) -> Any:
        assert self._client is not None
        last_exc: Exception = RuntimeError("No attempts made")
        for attempt in range(self._config.max_retries + 1):
            try:
                resp = await self._client.get(path, params=params)
            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < self._config.max_retries:
                    await asyncio.sleep(0.5 * (attempt + 1))
                continue
            if resp.status_code == 404:
                username = path.strip("/").split("/")[-1]
                raise UserNotFoundError(username)
            if resp.status_code == 403:
                raise RateLimitError()
            resp.raise_for_status()
            return resp.json()
        raise GitHubAPIError("Request timed out") from last_exc

    async def fetch_user(self, username: str) -> dict[str, Any]:
        return await self._get(f"/users/{username}")

    async def fetch_repos(self, username: str) -> list[dict[str, Any]]:
        return await self._get(f"/users/{username}/repos", params={"per_page": 100})
