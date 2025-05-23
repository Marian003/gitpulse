# GitPulse

Beautiful terminal dashboard for GitHub profile stats.

## Installation

```bash
pip install gitpulse
```

## Usage

```bash
gitpulse torvalds
gitpulse torvalds --token ghp_xxx
gitpulse torvalds --json
```

## Tech Stack

- [Typer](https://typer.tiangolo.com/) â€” CLI framework
- [Rich](https://rich.readthedocs.io/) â€” terminal formatting
- [httpx](https://www.python-httpx.org/) â€” async HTTP client
