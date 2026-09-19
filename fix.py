#!/usr/bin/env python3
import os
import subprocess
import sys

def execute_git_command(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0 and "nothing to commit" not in res.stdout and "nothing to commit" not in res.stderr:
        print(f"Error during {desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def execute_fix():
    html_file = os.path.join("week10-file-management", "03-filesystem-implementation.html")

    print(f"--> Reading {html_file}...")
    if not os.path.exists(html_file):
        print(f"Error: Could not find {html_file}", file=sys.stderr)
        sys.exit(1)

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace any malformed or raw rarr occurrences with proper &rarr; entity or unicode arrow →
    # Let's ensure proper &rarr; entity formatting or use the literal unicode character '→' which avoids entity encoding bugs entirely.
    updated_content = content.replace("&rarr;", "→")

    print(f"--> Writing corrected content back to {html_file}...")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_content)

    commit_msg = (
        "Fix raw rarr entity rendering in 03-filesystem-implementation.html\n\n"
        "Replace raw or malformed &rarr; text occurrences with proper unicode "
        "arrow characters (→) to ensure clean browser rendering."
    )

    execute_git_command(["git", "add", html_file], "Staging fixed HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing fix")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Fix deployed successfully!")

if __name__ == "__main__":
    execute_fix()
