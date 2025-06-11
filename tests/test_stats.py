from typing import Any


def _make_repo(language: str | None = "Python", stars: int = 0, forks: int = 0) -> dict[str, Any]:
    return {
        "language": language,
        "stargazers_count": stars,
        "forks_count": forks,
        "name": "test-repo",
    }


def _make_push_event(date_str: str = "2025-06-01T10:00:00Z", commits: list | None = None) -> dict:
    return {
        "type": "PushEvent",
        "created_at": date_str,
        "repo": {"name": "user/repo"},
        "payload": {"commits": commits or [{"sha": "abc1234", "message": "test commit"}]},
    }


class TestComputeLanguages:
    def test_basic_counting(self):
        from gitpulse.stats import compute_languages
        repos = [_make_repo("Python"), _make_repo("Python"), _make_repo("Go")]
        result = compute_languages(repos)
        assert result[0].name == "Python"
        assert result[0].count == 2
