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

    def test_empty_repos(self):
        from gitpulse.stats import compute_languages
        assert compute_languages([]) == []

    def test_none_language_skipped(self):
        from gitpulse.stats import compute_languages
        repos = [_make_repo(None), _make_repo("Python")]
        result = compute_languages(repos)
        assert len(result) == 1
        assert result[0].name == "Python"

    def test_top_n_limit(self):
        from gitpulse.stats import compute_languages
        repos = [_make_repo(str(i)) for i in range(10)]
        result = compute_languages(repos, top_n=3)
        assert len(result) == 3

    def test_percentage_sums_to_100(self):
        from gitpulse.stats import compute_languages
        repos = [_make_repo("Python"), _make_repo("Go"), _make_repo("Rust")]
        result = compute_languages(repos, top_n=3)
        total = sum(r.percentage for r in result)
        assert abs(total - 100.0) < 0.5


class TestComputeRepoStats:
    def test_aggregation(self):
        from gitpulse.stats import compute_repo_stats
        repos = [_make_repo(stars=5, forks=2), _make_repo(stars=3, forks=1)]
        result = compute_repo_stats(repos)
        assert result.total_stars == 8
        assert result.total_forks == 3
        assert result.total_repos == 2

    def test_empty_repos(self):
        from gitpulse.stats import compute_repo_stats
        result = compute_repo_stats([])
        assert result.total_stars == 0
        assert result.total_repos == 0


class TestComputeStreak:
    def test_consecutive_days(self):
        from gitpulse.stats import compute_streak
        events = [
            _make_push_event("2025-06-01T10:00:00Z"),
            _make_push_event("2025-06-02T10:00:00Z"),
            _make_push_event("2025-06-03T10:00:00Z"),
        ]
        result = compute_streak(events)
        assert result.longest_streak == 3
