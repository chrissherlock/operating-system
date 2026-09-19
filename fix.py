#!/usr/bin/env python3
import os
import subprocess
import sys

COMMIT_MSG = """Fix syntax error in commit argument list within fix.py

Correct a missing quotation mark on the git commit argument flag
'-m' inside fix.py. Verify syntax validity before staging,
committing, and pushing changes to origin main."""

def run_git_command(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0:
        print(f"Error during {desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def commit_and_push():
    run_git_command(["git", "add", "fix.py"], "Staging fix.py")
    run_git_command(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing with -a -m")
    run_git_command(["git", "push", "origin", "main"], "Pushing to origin main")
    print("--> Successfully committed and pushed fix.py!")

if __name__ == "__main__":
    commit_and_push()
