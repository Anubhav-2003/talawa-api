"""
Script to check if the number of files submitted in a Pull Request exceeds 20.

Methodology:
    Analyses the text file generated after the git diff command.
    Checks the number of files modified in the PR branch by
    counting the lines in the file.
    Exits with an appropriate error message if the number of files exceeds 20.

NOTE:
    This script complies with Python 3 coding and documentation standards,
    including:
        1) Pylint
        2) Pydocstyle
        3) Pycodestyle
        4) Flake8
    Run these commands from the CLI to ensure the code is compliant
    for all your pull requests.
"""

import sys
import subprocess
import argparse


def get_changed_files(base_branch, pr_branch):
    """
    Get the list of changed files between branches.

    Args:
        base_branch (str): Base branch name.
        pr_branch (str): Pull request branch name.

    Returns:
        list: List of changed file names.
    """
    try:
        with subprocess.Popen(
            [
                "git",
                "diff",
                "--name-only",
                f"origin/{base_branch}...{pr_branch}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        ) as git_diff_process:
            git_diff_output, git_diff_error = git_diff_process.communicate()

            if git_diff_process.returncode != 0:
                print(f"Error: {git_diff_error}")
                return []

            changed_files = git_diff_output.splitlines()
            return changed_files
    except Exception as e:
        print(f"Error: {e}")
        return []


def main():
    """Execute checks on the changed files."""
    parser = argparse.ArgumentParser(description="Check the number of changed files.")
    parser.add_argument("base_branch", help="Base branch name")
    parser.add_argument("pr_branch", help="Pull request branch name")
    args = parser.parse_args()

    base_branch = args.base_branch
    pr_branch = args.pr_branch

    changed_files = get_changed_files(base_branch, pr_branch)
    if len(changed_files) > 20:
        print("Number of changed files exceeds 20.")
        sys.exit(1)


if __name__ == "__main__":
    main()
