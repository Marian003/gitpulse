from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console

from gitpulse import __version__
from gitpulse.api import GitHubAPIError, GitHubClient, RateLimitError, UserNotFoundError
from gitpulse.config import Config, resolve_token
from gitpulse.dashboard import render_dashboard, render_json
from gitpulse.stats import build_profile_stats

app = typer.Typer(
    name="gitpulse",
    help="Beautiful terminal dashboard for any GitHub user's profile stats.",
    add_completion=False,
)

console = Console()
err_console = Console(stderr=True)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"[bold]GitPulse[/bold] v{__version__}")
        raise typer.Exit()


@app.command()
def main(
    username: str = typer.Argument(..., help="GitHub username to look up"),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        "-t",
        help="GitHub personal access token (or set GITHUB_TOKEN env var)",
        envvar="GITHUB_TOKEN",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Output raw JSON instead of the dashboard"
    ),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of recent commits to show"),
    no_forks: bool = typer.Option(False, "--no-forks", help="Exclude forked repos from stats"),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Fetch GitHub profile stats and render a terminal dashboard."""
    resolved_token = resolve_token(token)
    config = Config(token=resolved_token)

    async def _run() -> None:
        async with GitHubClient(config) as client:
            with console.status(
                f"[bold cyan]Loading stats for "
                f"[bright_yellow]@{username}[/bright_yellow]...[/bold cyan]"
            ):
                data = await client.fetch_all(username)

            if json_output:
                payload = {"user": data[0], "repos": data[1], "events": data[2]}
                render_json(payload)
            else:
                stats = build_profile_stats(data)
                render_dashboard(stats)

    try:
        asyncio.run(_run())
    except UserNotFoundError as exc:
        err_console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(1)
    except RateLimitError as exc:
        err_console.print(f"[bold red]Rate limited:[/bold red] {exc}")
        raise typer.Exit(1)
    except GitHubAPIError as exc:
        err_console.print(f"[bold red]API error:[/bold red] {exc}")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        err_console.print("\n[dim]Interrupted.[/dim]")
        raise typer.Exit(130)
