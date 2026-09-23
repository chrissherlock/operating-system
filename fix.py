#!/usr/bin/env python3
# =====================================================================
# fix.py: Remove unused Week 2 modules and placeholders
# =====================================================================
import os
import subprocess

TARGET_DIR = "week02-processes"

OBSOLETE_FILES = [
    "01-limited-direct-execution.html",
    "02-process-api.html",
    "03-cpu-scheduling.html",
    "04-mlfq.html",
    "placeholder.html"
]

def remove_obsolete_files():
    removed_paths = ["fix.py"]
    for filename in OBSOLETE_FILES:
        filepath = os.path.join(TARGET_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            removed_paths.append(filepath)
            print(f"--> Removed obsolete file: {filepath}")
        else:
            print(f"--> File not found (already removed): {filepath}")

    try:
        subprocess.run(["git", "add", "fix.py"], check=True)
        for filepath in removed_paths:
            if filepath != "fix.py":
                subprocess.run(["git", "rm", filepath], check=True)

        commit_msg = (
            "Remove obsolete Week 2 modules and placeholders\n\n"
            "Clean up week02-processes directory by removing unused sub-modules and\n"
            "placeholders, leaving the precise four-module MOS 2.1-2.2 and OSTEP Ch 4 set."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git cleanup and sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    remove_obsolete_files()
