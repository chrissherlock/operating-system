#!/usr/bin/env python3
import subprocess
import sys

def commit_everything():
    print("--> Checking git status...")
    status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
    if not status_res.stdout.strip():
        print("--> Working directory is already completely clean.")
        return

    print("--> Staging all modified and untracked files...")
    subprocess.run(["git", "add", "-A"], check=True)

    commit_msg = (
        "Commit and push all remaining working directory changes\n\n"
        "Stage and commit all leftover modified files across the repository\n"
        "to ensure a completely clean working tree."
    )

    print("--> Committing changes...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("--> Pushing to origin main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> All working directory changes successfully committed and pushed!")

if __name__ == "__main__":
    commit_everything()
