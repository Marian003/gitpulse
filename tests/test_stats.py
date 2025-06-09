from typing import Any


def _make_repo(language: str | None = "Python", stars: int = 0, forks: int = 0) -> dict[str, Any]:
    return {
        "language": language,
        "stargazers_count": stars,
        "forks_count": forks,
        "name": "test-repo",
    }
