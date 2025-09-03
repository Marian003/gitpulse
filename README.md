<!-- GitPulse -->
![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

<!-- GitPulse -->
![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

# GitPulse

Instantly see any GitHub user's profile stats in a beautiful terminal dashboard.

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

## Development

```bash
git clone https://github.com/Marian003/gitpulse
cd gitpulse
pip install -e ".[dev]"
pytest
```

## Configuration

Set `GITHUB_TOKEN` to authenticate and get higher rate limits:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```



## Screenshot

> Dashboard renders in your terminal with colors, bars, and tables.
