#!/usr/bin/env python3
import os
import subprocess
import sys

def stage_and_commit_fix():
    filename = "fix.py"
    if not os.path.exists(filename):
        print(f"Notice: {filename} does not exist in working directory. Searching for alternate fix scripts...")
        # Search for any file matching fix*.py
        import glob
        candidates = glob.glob("fix*.py")
        if candidates:
            filename = candidates[0]
            print(f"--> Found candidate script: {filename}")
        else:
            print(f"Error: No fix script found to commit.", file=sys.stderr)
            sys.exit(1)

    print(f"--> Staging {filename}...")
    subprocess.run(["git", "add", filename], check=True)

    status_res = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if status_res.returncode == 0:
        print(f"--> {filename} is already staged/committed. No changes to commit.")
        return

    commit_msg = (
        "Track and commit repository utility fix script\n\n"
        f"Include {filename} in git version control tracking to preserve helper code\n"
        "used during curriculum verification and refactoring."
    )

    print("--> Committing changes...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("--> Pushing changes to origin main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(f"--> Successfully committed and pushed {filename}!")

if __name__ == "__main__":
    stage_and_commit_fix()
