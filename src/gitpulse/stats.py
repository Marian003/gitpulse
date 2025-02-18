from dataclasses import dataclass
from typing import Optional

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
