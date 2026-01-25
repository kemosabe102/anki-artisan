#!/usr/bin/env python
"""Git commit history analysis for churn metrics.

Analyzes git repository commits within a time window to extract:
- Commits per file
- Unique authors per file
- Lines changed per file

Usage:
    uv run python git_churn.py --repo-path . --output-file churn.json --days 90 --branch main
"""

from __future__ import annotations

import sys


def _check_gitpython_installed() -> None:
    """Check if gitpython is installed, exit with helpful message if not."""
    try:
        import git  # noqa: F401
    except ImportError:
        print("=" * 60, file=sys.stderr)
        print("ERROR: Missing required dependency: gitpython", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(file=sys.stderr)
        print("Install with:", file=sys.stderr)
        print("  pip install gitpython>=3.1", file=sys.stderr)
        print(file=sys.stderr)
        print("Or install all tech debt dependencies:", file=sys.stderr)
        print("  pip install radon>=6.0 gitpython>=3.1 pylint>=3.0", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        sys.exit(1)


_check_gitpython_installed()

import argparse  # noqa: E402
import json  # noqa: E402
from dataclasses import asdict, dataclass  # noqa: E402
from datetime import datetime, timedelta  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import TYPE_CHECKING  # noqa: E402

if TYPE_CHECKING:
    pass  # git types imported at runtime


@dataclass
class FileStat:
    """Statistics for a single file's git history."""

    path: str
    commits: int
    authors: int
    lines_changed: int


@dataclass
class ChurnSummary:
    """Summary of churn analysis."""

    total_commits: int
    unique_authors: int
    hottest_file: str
    time_window_days: int


@dataclass
class ChurnResult:
    """Complete result of churn analysis."""

    files: list[FileStat]
    summary: ChurnSummary


def analyze_churn(
    repo_path: str | Path,
    days: int = 90,
    branch: str = "main",
) -> ChurnResult:
    """Analyze git commit history within a time window.

    Args:
        repo_path: Path to the git repository root.
        days: Number of days to look back (default: 90).
        branch: Branch to analyze (default: main).

    Returns:
        ChurnResult with file statistics and summary.

    Raises:
        ValueError: If repo_path is not a valid git repository.
    """
    try:
        from git import InvalidGitRepositoryError, Repo
    except ImportError as e:
        raise ImportError(
            "gitpython is required. Install with: uv add gitpython"
        ) from e

    repo_path = Path(repo_path).resolve()

    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError as e:
        raise ValueError(f"Not a valid git repository: {repo_path}") from e

    # Handle empty repositories gracefully
    if repo.head.is_detached or not repo.heads:
        return ChurnResult(
            files=[],
            summary=ChurnSummary(
                total_commits=0,
                unique_authors=0,
                hottest_file="",
                time_window_days=days,
            ),
        )

    # Calculate cutoff date
    since_date = datetime.now() - timedelta(days=days)

    # Track per-file metrics
    file_commits: dict[str, int] = {}
    file_authors: dict[str, set[str]] = {}
    file_lines: dict[str, int] = {}
    all_authors: set[str] = set()
    total_commits = 0

    # Iterate through commits on the branch within the time window
    try:
        commits = list(repo.iter_commits(branch, since=since_date))
    except Exception:
        # Branch may not exist or repo has no commits
        return ChurnResult(
            files=[],
            summary=ChurnSummary(
                total_commits=0,
                unique_authors=0,
                hottest_file="",
                time_window_days=days,
            ),
        )

    for commit in commits:
        total_commits += 1
        author = commit.author.email if commit.author else "unknown"
        all_authors.add(author)

        # Get stats for each file in the commit
        try:
            stats = commit.stats.files
        except Exception:
            # Some commits may not have accessible stats
            continue

        for file_path, stat in stats.items():
            # Initialize tracking for new files
            if file_path not in file_commits:
                file_commits[file_path] = 0
                file_authors[file_path] = set()
                file_lines[file_path] = 0

            # Update metrics
            file_commits[file_path] += 1
            file_authors[file_path].add(author)
            file_lines[file_path] += stat.get("insertions", 0) + stat.get(
                "deletions", 0
            )

    # Build file statistics sorted by commit count (descending)
    file_stats: list[FileStat] = []
    for path in sorted(
        file_commits.keys(), key=lambda p: file_commits[p], reverse=True
    ):
        file_stats.append(
            FileStat(
                path=path,
                commits=file_commits[path],
                authors=len(file_authors[path]),
                lines_changed=file_lines[path],
            )
        )

    # Find hottest file
    hottest_file = file_stats[0].path if file_stats else ""

    return ChurnResult(
        files=file_stats,
        summary=ChurnSummary(
            total_commits=total_commits,
            unique_authors=len(all_authors),
            hottest_file=hottest_file,
            time_window_days=days,
        ),
    )


def result_to_dict(result: ChurnResult) -> dict:
    """Convert ChurnResult to JSON-serializable dictionary."""
    return {
        "files": [asdict(f) for f in result.files],
        "summary": asdict(result.summary),
    }


def main() -> int:
    """CLI entry point for git churn analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze git commit history for churn metrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python git_churn.py --repo-path . --output-file churn.json
    python git_churn.py --repo-path /path/to/repo --days 180 --branch develop
        """,
    )
    parser.add_argument(
        "--repo-path",
        type=str,
        required=True,
        help="Path to the git repository",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Path for output JSON file",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Number of days to analyze (default: 90)",
    )
    parser.add_argument(
        "--branch",
        type=str,
        default="main",
        help="Branch to analyze (default: main)",
    )

    args = parser.parse_args()

    try:
        result = analyze_churn(
            repo_path=args.repo_path,
            days=args.days,
            branch=args.branch,
        )

        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result_to_dict(result), f, indent=2)

        print(f"Churn analysis written to: {output_path}")
        print(f"  Total commits: {result.summary.total_commits}")
        print(f"  Unique authors: {result.summary.unique_authors}")
        print(f"  Files analyzed: {len(result.files)}")
        if result.summary.hottest_file:
            print(f"  Hottest file: {result.summary.hottest_file}")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
