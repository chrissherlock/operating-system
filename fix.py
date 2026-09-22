#!/usr/bin/env python3
# =====================================================================
# fix.py: Update Process Lifecycle Walkthrough preview label
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

def fix_lifecycle_preview_label():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace "Upcoming Transition:" or variants with "Stage Explanation:" in Module 3
    new_label = '<div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase;">Stage Explanation:</div>'

    updated_content = re.sub(
        r'<div[^>]*>(?:Upcoming Transition|Upcoming State|Next State)[^<]*</div>',
        new_label,
        content,
        flags=re.IGNORECASE
    )

    if updated_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"--> Successfully updated lifecycle simulator label in {TARGET_FILE}.")
    else:
        print("--> Notice: Label pattern already updated or not found in Module 3.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Change Upcoming Transition to Stage Explanation in lifecycle simulator\n\n"
            "Update 03-os-concepts.html so the interactive Process Lifecycle Walkthrough\n"
            "uses 'Stage Explanation:' instead of 'Upcoming Transition:'."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_lifecycle_preview_label()
