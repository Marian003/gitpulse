<!-- GitPulse -->
![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![CI](https://github.com/Marian003/gitpulse/actions/workflows/ci.yml/badge.svg)

<!-- GitPulse -->
![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![CI](https://github.com/Marian003/gitpulse/actions/workflows/ci.yml/badge.svg)

# GitPulse

Instantly see any GitHub user's profile stats in a beautiful terminal dashboard.

## Installation

```bash
pip install gitpulse

# Latest from GitHub:
pip install git+https://github.com/Marian003/gitpulse.git

# Or from source:
git clone https://github.com/Marian003/gitpulse
cd gitpulse
pip install -e .
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


## Environment Variables

- GITHUB_TOKEN - GitHub personal access token for higher rate limits


## Rate Limits

Without a token: 60 requests/hour. With token: 5000 requests/hour.


## Contributing

Pull requests welcome. Please run pytest and 
uff check src/ before submitting.


## Error Handling

GitPulse shows clear messages for: user not found, rate limit exceeded, network errors.
