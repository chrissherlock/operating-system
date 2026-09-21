#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace narrative headers with clear technical labels
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def update_preview_labels():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace narrative headers with clean technical labels across simulators
    content = content.replace(
        'Active Story Chapter &amp; Next Plot Point:',
        'Stage Explanation:'
    )
    content = content.replace(
        'Active Story Chapter & Next Plot Point:',
        'Stage Explanation:'
    )
    content = content.replace(
        'Where We Are &amp; What Happens Next Click:',
        'Stage Explanation:'
    )
    content = content.replace(
        'Where We Are & What Happens Next Click:',
        'Stage Explanation:'
    )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("--> Updated preview headers to 'Stage Explanation:'.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Replace narrative labels with Stage Explanation in interactive walkthroughs\n\n"
            "Update 02-hardware-review.html preview headers to use clear, direct technical\n"
            "labeling ('Stage Explanation:') instead of story metaphors."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for label update!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_preview_labels()
