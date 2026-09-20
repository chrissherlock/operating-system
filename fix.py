#!/usr/bin/env python3
# =====================================================================
# stage_and_commit_week1.py: Stage, commit, and push all Week 1 files
# =====================================================================
import os
import subprocess
import sys

def execute_git_sync():
    base_dir = "week01-operating-system-concepts"

    # List all files to ensure they are tracked and added
    files_to_add = [
        os.path.join(base_dir, "index.html"),
        os.path.join(base_dir, "01-what-is-an-os-and-history.html"),
        os.path.join(base_dir, "02-hardware-review.html"),
        os.path.join(base_dir, "03-os-concepts.html"),
        os.path.join(base_dir, "04-os-structure.html")
    ]

    print(f"--> Ensuring all files exist: {files_to_add}")
    for fp in files_to_add:
        if os.path.exists(fp):
            print(f"    [OK] Found {fp}")
        else:
            print(f"    [MISSING] {fp} not found!")

    fix_path = "fix.py"
    if os.path.exists(fix_path):
        files_to_add.append(fix_path)

    print(f"--> Staging and committing files...")
    try:
        subprocess.run(["git", "add"] + files_to_add, check=True)
        commit_msg = (
            "Add and sync all Week 1 module files and index portal\n\n"
            "Include index.html, 01-what-is-an-os-and-history.html, 02-hardware-review.html,\n"
            "03-os-concepts.html, and 04-os-structure.html in the repository."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> All Week 1 files successfully committed and pushed to origin main!")
    except Exception as e:
        print(f"--> Git sync note: {e}")

if __name__ == "__main__":
    execute_git_sync()
