#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct Mars Pathfinder section title from Failure to Anomaly
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "01-concurrency-hazards-livelock-starvation.html"
)

def correct_pathfinder_title():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    old_heading = "<h4>2. The Mars Pathfinder Mission Failure (July 1997)</h4>"
    new_heading = "<h4>2. The Mars Pathfinder Priority Inversion Anomaly (July 1997)</h4>"

    if old_heading not in content:
        print("Warning: Old heading string not found exactly.")
        return False

    new_content = content.replace(old_heading, new_heading)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"--> Successfully updated Pathfinder title to 'Anomaly' in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if correct_pathfinder_title():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Correct Mars Pathfinder section title to reflect anomaly, not failure\n\n"
                "Rename subsection heading in Module 01 from 'Mission Failure' to\n"
                "'Priority Inversion Anomaly' to accurately characterize the spacecraft event."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
