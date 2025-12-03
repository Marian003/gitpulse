# Helper factories for building test fixtures
# These avoid repetition across test classes
from typing import Any


def _make_repo(language: str | None = "Python", stars: int = 0, forks: int = 0) -> dict[str, Any]:
    return {
        "language": language,
        "stargazers_count": stars,
        "forks_count": forks,
        "name": "test-repo",
    }


def _make_push_event(date_str: str = "2024-06-01T10:00:00Z", commits: list | None = None) -> dict:
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

    def test_skip_forked_repo(self):
        from gitpulse.stats import compute_languages
        repos = [_make_repo("Python"), {"language": "Go", "fork": True}]
        result = compute_languages(repos)
        assert result[0].name == "Python"
        assert len(result) == 1

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

    def test_percentage_sums_near_100(self):
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
            _make_push_event("2024-06-01T10:00:00Z"),
            _make_push_event("2025-06-02T10:00:00Z"),
            _make_push_event("2025-06-03T10:00:00Z"),
        ]
        result = compute_streak(events)
        assert result.longest_streak == 3

    def test_streak_broken_by_gap(self):
        from gitpulse.stats import compute_streak
        events = [
            _make_push_event("2024-06-01T10:00:00Z"),
            _make_push_event("2025-06-03T10:00:00Z"),  # gap on Jun 2
        ]
        result = compute_streak(events)
        assert result.longest_streak == 1

    def test_empty_events(self):
        from gitpulse.stats import compute_streak
        result = compute_streak([])
        assert result.current_streak == 0
        assert result.longest_streak == 0

    def test_non_push_events_ignored(self):
        from gitpulse.stats import compute_streak
        events = [{"type": "WatchEvent", "created_at": "2024-06-01T10:00:00Z"}]
        result = compute_streak(events)
        assert result.current_streak == 0


class TestExtractRecentCommits:
    def test_basic_extraction(self):
        from gitpulse.stats import extract_recent_commits
        events = [_make_push_event()]
        result = extract_recent_commits(events)
        assert len(result) == 1
        assert result[0].sha == "abc1234"
        assert result[0].message == "test commit"

    def test_limit_respected(self):
        from gitpulse.stats import extract_recent_commits
        events = [_make_push_event() for _ in range(20)]
        result = extract_recent_commits(events, limit=5)
        assert len(result) == 5

    def test_long_message_truncated(self):
        from gitpulse.stats import extract_recent_commits
        long_msg = "x" * 100
        events = [_make_push_event(commits=[{"sha": "abc1234", "message": long_msg}])]
        result = extract_recent_commits(events)
        assert len(result[0].message) <= 72

    def test_single_day_streak(self):
        from gitpulse.stats import compute_streak
        events = [_make_push_event("2024-06-01T10:00:00Z")]
        result = compute_streak(events)
        assert result.longest_streak == 1
        assert result.active_days == 1


class TestEdgeCases:
    def test_single_repo(self):
        from gitpulse.stats import compute_repo_stats
        repos = [_make_repo("Python", stars=10, forks=2)]
        result = compute_repo_stats(repos)
        assert result.total_repos == 1
        assert result.most_starred_name == "test-repo"

    def test_user_with_no_bio(self):
        from gitpulse.stats import build_profile_stats
        user = {"login": "user", "name": "Test", "bio": None, "followers": 0,
                "following": 0, "public_repos": 0, "avatar_url": "", "html_url": ""}
        result = build_profile_stats((user, [], []))
        assert result.bio is None

    def test_zero_star_repos(self):
        from gitpulse.stats import compute_repo_stats
        repos = [_make_repo(stars=0), _make_repo(stars=0)]
        result = compute_repo_stats(repos)
        assert result.total_stars == 0

