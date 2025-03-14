from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from gitpulse.stats import ProfileStats

console = Console()

LANG_COLORS: dict[str, str] = {
    "Python": "yellow",
    "JavaScript": "bright_yellow",
    "TypeScript": "blue",
    "Go": "cyan",
    "Rust": "red",
    "Java": "bright_red",
    "C": "white",
    "C++": "bright_white",
    "Ruby": "bright_red",
    "Shell": "green",
}
DEFAULT_LANG_COLOR = "bright_white"
BAR_FULL = "â–ˆ"
BAR_EMPTY = "â–‘"
BAR_WIDTH = 12

def _lang_bar(percentage: float, color: str) -> Text:
    filled = round(percentage / 100 * BAR_WIDTH)
    empty = BAR_WIDTH - filled
    t = Text()
    t.append(BAR_FULL * filled, style=f"bold {color}")
    t.append(BAR_EMPTY * empty, style="dim")
    return t

def _build_profile_panel(stats: ProfileStats) -> Panel:
    t = Text()
    t.append(f"  {stats.name}\n", style="bold bright_white")
    if stats.bio:
        t.append(f"  {stats.bio}\n", style="italic dim")
    t.append(f"\n  Followers: {stats.followers}  Following: {stats.following}\n")
    t.append(f"  Public repos: {stats.public_repos}\n")
    return Panel(t, title="[bold cyan]PROFILE[/bold cyan]", expand=True)

def _build_languages_panel(stats: ProfileStats) -> Panel:
    if not stats.languages:
        return Panel(Text("  No language data."), title="[bold green]LANGUAGES[/bold green]", expand=True)
    t = Text()
    t.append("\n")
    for lang in stats.languages:
        color = LANG_COLORS.get(lang.name, DEFAULT_LANG_COLOR)
        t.append(f"  {lang.name:<12} ", style=f"bold {color}")
        t.append_text(_lang_bar(lang.percentage, color))
        t.append(f"  {lang.percentage:5.1f}%\n")
    return Panel(t, title="[bold green]LANGUAGES[/bold green]", expand=True)

def _build_repos_panel(stats: ProfileStats) -> Panel:
    rs = stats.repo_stats
    t = Text()
    t.append(f"\n  Total stars: {rs.total_stars}\n")
    t.append(f"  Total forks: {rs.total_forks}\n")
    t.append(f"\n  Most starred: {rs.most_starred_name} ({rs.most_starred_stars})\n")
    t.append(f"  Most forked: {rs.most_forked_name} ({rs.most_forked_forks})\n")
    return Panel(t, title="[bold magenta]REPOSITORIES[/bold magenta]", expand=True)

def _build_streak_panel(stats: ProfileStats) -> Panel:
    s = stats.streak
    t = Text()
    t.append(f"\n  Current streak: {s.current_streak} days\n")
    t.append(f"  Longest streak: {s.longest_streak} days\n")
    return Panel(t, title="[bold yellow]STREAK[/bold yellow]", expand=True)

def _build_commits_table(stats: ProfileStats) -> Table:
    table = Table(show_header=True, expand=True, title="[bold blue]RECENT COMMITS[/bold blue]")
    table.add_column("SHA", width=8)
    table.add_column("Message")
    table.add_column("Date", width=12)
    for c in stats.recent_commits:
        table.add_row(c.sha, c.message, c.date)
    return table
