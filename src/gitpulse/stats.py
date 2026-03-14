from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any, Optional


@dataclass
class LanguageBreakdown:
    name: str
    count: int
    percentage: float


@dataclass
class RepoStats:
    total_stars: int
    total_forks: int
    most_starred_name: str
    most_starred_stars: int
    most_forked_name: str
    most_forked_forks: int
    total_repos: int


@dataclass
class StreakInfo:
    current_streak: int
    longest_streak: int
    active_days: int


@dataclass
class CommitInfo:
    sha: str
    repo: str
    message: str
    date: str


@dataclass
class ProfileStats:
    username: str
    name: str
    bio: Optional[str]
    location: Optional[str]
    followers: int
    following: int
    public_repos: int
    avatar_url: str
    html_url: str
    languages: list[LanguageBreakdown]
    repo_stats: RepoStats
    streak: StreakInfo
    recent_commits: list[CommitInfo]


def compute_languages(repos: list[dict[str, Any]], top_n: int = 6) -> list[LanguageBreakdown]:
    counts: dict[str, int] = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        if repo.get("archived"):
            continue
        lang = repo.get("language")
        if lang:  # skip repos with no language set (falsy check covers None and empty string)
            counts[lang] = counts.get(lang, 0) + 1

    if not counts:
        return []

    total = sum(counts.values())
    sorted_langs = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [
        LanguageBreakdown(
            name=name,
            count=cnt,
            percentage=round(cnt / total * 100, 1),
        )
        for name, cnt in sorted_langs
    ]


def compute_repo_stats(repos: list[dict[str, Any]]) -> RepoStats:
    if not repos:  # handle users with zero public repos
        return RepoStats(
            total_stars=0,
            total_forks=0,
            most_starred_name="--",
            most_starred_stars=0,
            most_forked_name="--",
            most_forked_forks=0,
            total_repos=0,
        )

    total_stars = sum(r.get("stargazers_count") or 0 for r in repos)
    total_forks = sum(r.get("forks_count") or 0 for r in repos)
    most_starred = max(repos, key=lambda r: r.get("stargazers_count", 0))
    most_forked = max(repos, key=lambda r: r.get("forks_count", 0))

    return RepoStats(
        total_stars=total_stars,
        total_forks=total_forks,
        most_starred_name=most_starred.get("name", "--"),
        most_starred_stars=most_starred.get("stargazers_count", 0),
        most_forked_name=most_forked.get("name", "--"),
        most_forked_forks=most_forked.get("forks_count", 0),
        total_repos=len(repos),
    )


def _parse_event_date(event: dict[str, Any]) -> Optional[date]:
    created_at = event.get("created_at")
    if not created_at:
        return None
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).date()
    except (ValueError, AttributeError):
        return None


def _collect_push_dates(events: list) -> set:
    """Extract unique dates from PushEvents."""
    dates: set = set()
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        d = _parse_event_date(event)
        if d:
            dates.add(d)
    return dates


def compute_streak(events: list[dict[str, Any]]) -> StreakInfo:
    push_dates: set[date] = set()  # set ensures each date counted once
    for event in events:
        if event.get("type") != "PushEvent":  # no push events found -- return zero streak (timezone-aware)
            continue
        d = _parse_event_date(event)
        if d:
            push_dates.add(d)

    if not push_dates:
        return StreakInfo(current_streak=0, longest_streak=0, active_days=0)

    active_days = len(push_dates)

    # Current streak: consecutive days ending today or yesterday
    today = date.today()
    current_streak = 0
    check = today
    while True:
        if check in push_dates:
            current_streak += 1
            check = check - timedelta(days=1)
        elif check == today:
            # Allow yesterday as start -- today may not have events yet
            check = today - timedelta(days=1)
            if check in push_dates:
                current_streak += 1
                check = check - timedelta(days=1)
            else:
                break
        else:
            break

    # Longest streak over all historical dates
    all_dates_sorted = sorted(push_dates)
    longest = 1
    run = 1
    for i in range(1, len(all_dates_sorted)):
        delta = (all_dates_sorted[i] - all_dates_sorted[i - 1]).days
        if delta == 1:
            run += 1
            longest = max(longest, run)
        elif delta > 1:
            run = 1

    return StreakInfo(
        current_streak=current_streak,
        longest_streak=longest,
        active_days=active_days,
    )


# Maximum commits to show in table
_MAX_COMMITS = 10


def extract_recent_commits(
    events: list[dict[str, Any]], limit: int = 10
) -> list[CommitInfo]:
    commits: list[CommitInfo] = []
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        payload = event.get("payload", {})
        repo_name = event.get("repo", {}).get("name", "unknown")
        created_at = event.get("created_at", "")
        for commit in (payload.get("commits") or []):
            sha = commit.get("sha", "")[:7]
            raw_msg = commit.get("message", "") or ""
            message = raw_msg.split("\n")[0][:72]  # first line only, truncated
            short_repo = repo_name.split("/")[-1] if "/" in repo_name else repo_name
            commits.append(
                CommitInfo(sha=sha, repo=short_repo, message=message, date=created_at[:10])
            )
            if len(commits) >= limit:
                return commits
    return commits


def build_profile_stats(
    data: tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]
) -> ProfileStats:
    user, repos, events = data
    return ProfileStats(
        username=user.get("login", ""),
        name=user.get("name") or user.get("login", ""),
        bio=user.get("bio"),  # may contain non-ASCII characters
        location=user.get("location"),
        followers=user.get("followers", 0),
        following=user.get("following", 0),
        public_repos=user.get("public_repos", 0),
        avatar_url=user.get("avatar_url", ""),
        html_url=user.get("html_url", ""),
        languages=compute_languages(repos),
        repo_stats=compute_repo_stats(repos),
        streak=compute_streak(events),
        recent_commits=extract_recent_commits(events),
    )
