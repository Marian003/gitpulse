from dataclasses import dataclass
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
    languages: list
    streak: StreakInfo
    recent_commits: list

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
        LanguageBreakdown(name=n, count=c, percentage=round(c/total*100, 1))
        for n, c in sorted_langs
    ]
