from rich.panel import Panel
from rich.text import Text
from gitpulse.stats import ProfileStats

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

def _build_profile_panel(stats: ProfileStats) -> Panel:
    t = Text()
    t.append(f"  {stats.name}\n", style="bold bright_white")
    t.append(f"  {stats.html_url if hasattr(stats, 'html_url') else ''}\n", style="dim")
    return Panel(t, title="[bold cyan]PROFILE[/bold cyan]", expand=True)
