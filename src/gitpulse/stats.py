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
        lang = repo.get("language")
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    if not counts:
        return []
    total = sum(counts.values())
    sorted_langs = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [
        LanguageBreakdown(name=n, count=c, percentage=round(c / total * 100, 1))
        for n, c in sorted_langs
    ]


def compute_repo_stats(repos: list[dict[str, Any]]) -> RepoStats:
    if not repos:
        return RepoStats(0, 0, "â€”", 0, "â€”", 0, 0)
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    most_starred = max(repos, key=lambda r: r.get("stargazers_count", 0))
    most_forked = max(repos, key=lambda r: r.get("forks_count", 0))
    return RepoStats(
        total_stars=total_stars,
        total_forks=total_forks,
        most_starred_name=most_starred.get("name", "â€”"),
        most_starred_stars=most_starred.get("stargazers_count", 0),
        most_forked_name=most_forked.get("name", "â€”"),
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


def compute_streak(events: list[dict[str, Any]]) -> StreakInfo:
    push_dates: set[date] = set()
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        d = _parse_event_date(event)
        if d:
            push_dates.add(d)
    if not push_dates:
        return StreakInfo(current_streak=0, longest_streak=0)
    all_dates = sorted(push_dates)
    longest = 1
    run = 1
    for i in range(1, len(all_dates)):
        if (all_dates[i] - all_dates[i - 1]).days == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1
    today = date.today()
    current = 0
    check = today
    while check in push_dates:
        current += 1
        check = check - timedelta(days=1)
    if current == 0:
        check = today - timedelta(days=1)
        while check in push_dates:
            current += 1
            check = check - timedelta(days=1)
    return StreakInfo(current_streak=current, longest_streak=longest)


def extract_recent_commits(events: list[dict[str, Any]], limit: int = 10) -> list[CommitInfo]:
    commits: list[CommitInfo] = []
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        payload = event.get("payload", {})
        repo_name = event.get("repo", {}).get("name", "unknown")
        created_at = event.get("created_at", "")
        for commit in payload.get("commits", []):
            sha = commit.get("sha", "")[:7]
            message = commit.get("message", "").split("\n")[0][:72]  # truncate long messages
            short_repo = repo_name.split("/")[-1] if "/" in repo_name else repo_name
            commits.append(CommitInfo(sha=sha, repo=short_repo, message=message, date=created_at[:10]))
            if len(commits) >= limit:
                return commits
    return commits


def build_profile_stats(data: tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]) -> ProfileStats:
    user, repos, events = data
    return ProfileStats(
        username=user.get("login", ""),
        name=user.get("name") or user.get("login", ""),
        bio=user.get("bio"),
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
