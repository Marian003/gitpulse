![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

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


## What You Get

| Feature | Description |
|---------|-------------|
| Profile | Name, bio, followers |
| Languages | Top languages with bars |
| Repos | Stars, forks, top repos |
| Streak | Current and longest streaks |
| Commits | Recent commit messages |
