#!/usr/bin/env python3

import subprocess
import os


def run_command(cmd: list[str]) -> bool:
    result = subprocess.run(cmd)
    return result.returncode == 0


def git_has_changes() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() != ""


def auto_commit_and_push():
    if git_has_changes():
        subprocess.run(["git", "commit", "-am", "auto commit"])
        subprocess.run(["git", "push"])
    else:
        print("No changes to commit.")


def main():
    if run_command(["obsidian"]):
        auto_commit_and_push()


if __name__ == "__main__":
    main()

