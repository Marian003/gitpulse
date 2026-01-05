from __future__ import annotations

import json
from typing import Any

from rich import print as rprint
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
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
    "C#": "magenta",
    "Ruby": "bright_red",
    "PHP": "bright_magenta",
    "Swift": "bright_yellow",
    "Kotlin": "bright_magenta",
    "Scala": "red",
    "Shell": "green",
    "HTML": "bright_red",
    "CSS": "bright_blue",
    "Dart": "cyan",
    "Elixir": "magenta",
    "Haskell": "bright_magenta",
    "Lua": "blue",
    "R": "bright_blue",
    "Julia": "bright_green",
    "Zig": "bright_yellow",  # added 2026
}
DEFAULT_LANG_COLOR = "bright_white"
BAR_FULL = "\u2588"
BAR_EMPTY = "\u2591"

# Width of the language bar chart in characters
BAR_WIDTH = 12


# Private helpers
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
        bio = stats.bio[:60] + ("\u2026" if len(stats.bio) > 60 else "")
        t.append(f"  {bio}\n", style="italic dim")
    if stats.location:
        t.append(f"  \U0001f4cd {stats.location}\n")
    t.append(f"\n  \U0001f465 {stats.followers:,} followers  \u00b7  {stats.following:,} following\n")
    t.append(f"  \U0001f4e6 {stats.public_repos} public repos\n")
    t.append(f"\n  \U0001f517 {stats.html_url}\n", style="dim")
    return Panel(t, title="[bold cyan]PROFILE[/bold cyan]", border_style="bright_cyan", expand=True)


def _build_streak_panel(stats: ProfileStats) -> Panel:
    s = stats.streak
    t = Text()
    t.append("\n  \U0001f525 Current streak:  ", style="bold")
    t.append(f"{s.current_streak} days\n", style="bold bright_yellow")
    t.append("  \U0001f3c5 Longest streak:  ", style="bold")
    t.append(f"{s.longest_streak} days\n", style="bold bright_green")
    t.append("  \U0001f4ca Active days:     ", style="bold")
    t.append(f"{s.active_days}\n", style="bold")
    t.append("\n  (based on public push events)\n\n", style="dim italic")
    return Panel(t, title="[bold yellow]STREAK[/bold yellow]", border_style="yellow", expand=True)


def _build_languages_panel(stats: ProfileStats) -> Panel:
    if not stats.languages:
        return Panel(
            Text("  No language data available for this user.", style="dim"),
            title="[bold green]LANGUAGES[/bold green]",
            border_style="green",
            expand=True,
        )
    t = Text()
    t.append("\n")
    for lang in stats.languages:
        color = LANG_COLORS.get(lang.name, DEFAULT_LANG_COLOR)
        name_padded = lang.name[:12].ljust(12)
        t.append(f"  {name_padded} ", style=f"bold {color}")
        t.append_text(_lang_bar(lang.percentage, color))
        t.append(f"  {lang.percentage:5.1f}% \n")
    return Panel(t, title="[bold green]LANGUAGES[/bold green]", border_style="green", expand=True)


def _build_repos_panel(stats: ProfileStats) -> Panel:
    rs = stats.repo_stats
    t = Text()
    t.append("\n  \u2b50 Total stars:    ", style="bold")
    t.append(f"{rs.total_stars:,}\n", style="bold bright_yellow")
    t.append("  \U0001f374 Total forks:    ", style="bold")
    t.append(f"{rs.total_forks:,}\n", style="bold bright_cyan")
    t.append("\n  \U0001f3c6 Most starred:\n", style="bold")
    t.append(f"     {rs.most_starred_name}")
    t.append(f"  \u2b50{rs.most_starred_stars:,}\n", style="bright_yellow")
    t.append("  \U0001f500 Most forked:\n", style="bold")
    t.append(f"     {rs.most_forked_name}")
    t.append(f"  \U0001f374{rs.most_forked_forks:,}\n", style="bright_cyan")
    return Panel(t, title="[bold magenta]REPOSITORIES[/bold magenta]", expand=True)


def _build_commits_table(stats: ProfileStats) -> Table:
    table = Table(
        show_header=True,
        header_style="bold bright_white",
        border_style="dim",
        expand=True,
        title="[bold blue]RECENT COMMITS[/bold blue]",
        title_justify="left",
    )
    table.add_column("SHA", style="dim cyan", width=8, no_wrap=True)
    table.add_column("Repo", style="bright_cyan", width=20, no_wrap=True)
    table.add_column("Message", style="white", min_width=30)
    table.add_column("Date", style="dim", width=12, no_wrap=True)

    if not stats.recent_commits:
                table.add_row("--", "--", "No recent public commits found", "--")
    else:
        for c in stats.recent_commits:
            msg = c.message[:60] + ("\u2026" if len(c.message) > 60 else "")
            table.add_row(c.sha, c.repo, msg, c.date)

    return table


def render_dashboard(stats: ProfileStats) -> None:
    """Render the full GitPulse terminal dashboard."""
    console.print()

    header = Text(justify="center")
    header.append("\u26a1 GitPulse", style="bold bright_yellow")
    header.append("  \u2014  ", style="dim")
    header.append(f"@{stats.username[:30]}", style="bold bright_cyan")
    console.print(Panel(header, style="bold bright_yellow"))

    console.print(
        Columns(
            [_build_profile_panel(stats), _build_streak_panel(stats)],
            equal=True,
            expand=True,
        )
    )
    console.print(
        Columns(
            [_build_languages_panel(stats), _build_repos_panel(stats)],
            equal=True,
            expand=True,
        )
    )
    console.print(Rule(style="dim"))
    console.print(_build_commits_table(stats))
    console.print()


def render_json(data: Any) -> None:
    rprint(json.dumps(data, indent=2, default=str))


