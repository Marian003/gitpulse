from dataclasses import dataclass

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
