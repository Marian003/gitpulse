import pytest
import httpx
import respx

from gitpulse.config import Config


@pytest.fixture
def config():
    return Config(token="test-token", api_base="https://api.github.com")


@respx.mock
@pytest.mark.asyncio
async def test_fetch_user_success(config):
    from gitpulse.api import GitHubClient
    respx.get("https://api.github.com/users/torvalds").mock(
        return_value=httpx.Response(200, json={"login": "torvalds", "name": "Linus"})
    )
    async with GitHubClient(config) as client:
        user = await client.fetch_user("torvalds")
    assert user["login"] == "torvalds"


@respx.mock
@pytest.mark.asyncio
async def test_fetch_user_not_found(config):
    from gitpulse.api import GitHubClient, UserNotFoundError
    respx.get("https://api.github.com/users/nobody").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    async with GitHubClient(config) as client:
        with pytest.raises(UserNotFoundError):
            await client.fetch_user("nobody")


@respx.mock
@pytest.mark.asyncio
async def test_rate_limit_error(config):
    from gitpulse.api import GitHubClient, RateLimitError
    respx.get("https://api.github.com/users/user").mock(
        return_value=httpx.Response(403, headers={"x-ratelimit-remaining": "0"}, json={})
    )
    async with GitHubClient(config) as client:
        with pytest.raises(RateLimitError):
            await client.fetch_user("user")


@respx.mock
@pytest.mark.asyncio
async def test_fetch_repos(config):
    from gitpulse.api import GitHubClient
    respx.get("https://api.github.com/users/user/repos").mock(
        return_value=httpx.Response(200, json=[{"name": "repo1"}, {"name": "repo2"}])
    )
    async with GitHubClient(config) as client:
        repos = await client.fetch_repos("user")
    assert len(repos) == 2


@respx.mock
@pytest.mark.asyncio
async def test_fetch_events(config):
    from gitpulse.api import GitHubClient
    respx.get("https://api.github.com/users/user/events/public").mock(
        return_value=httpx.Response(200, json=[{"type": "PushEvent"}])
    )
    async with GitHubClient(config) as client:
        events = await client.fetch_events("user")
    assert events[0]["type"] == "PushEvent"


@respx.mock
@pytest.mark.asyncio
async def test_fetch_all_concurrent(config):
    from gitpulse.api import GitHubClient
    respx.get("https://api.github.com/users/user").mock(
        return_value=httpx.Response(200, json={"login": "user"})
    )
    respx.get("https://api.github.com/users/user/repos").mock(
        return_value=httpx.Response(200, json=[])
    )
    respx.get("https://api.github.com/users/user/events/public").mock(
        return_value=httpx.Response(200, json=[])
    )
    async with GitHubClient(config) as client:
        user, repos, events = await client.fetch_all("user")
    assert user["login"] == "user"
    assert repos == []
    assert events == []
