#!/usr/bin/env python3
# =====================================================================
# fix.py: Standardize Module 3 interactive simulator title
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

def standardize_simulator_title():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    old_title = "Interactive Simulator: Process Lifecycle Walkthrough"
    new_title = "Interactive Walkthrough: Process Lifecycle Engine"

    if old_title in content:
        content = content.replace(old_title, new_title)
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Successfully updated simulator title in {TARGET_FILE}.")
    else:
        print("--> Title already updated or not found.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Standardize simulator title format in Module 3\n\n"
            "Update 03-os-concepts.html to use 'Interactive Walkthrough: Process Lifecycle'\n"
            "for consistency with Module 2."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    standardize_simulator_title()
