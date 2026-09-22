#!/usr/bin/env python3
# =====================================================================
# fix.py: Standardize inline preview header label to Stage Explanation
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

def fix_preview_label():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the header label inside the interactive pipeline simulator
    old_label = '<div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase;">Upcoming Transition:</div>'
    new_label = '<div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase;">Stage Explanation:</div>'

    if old_label in content:
        content = content.replace(old_label, new_label)
    elif new_label not in content:
        # Fallback search and replace if minor attribute differences exist
        import re
        content = re.sub(
            r'<div[^>]*>Upcoming Transition:</div>',
            new_label,
            content,
            flags=re.IGNORECASE
        )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully standardized inline preview label to 'Stage Explanation:' in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Standardize inline preview label to Stage Explanation in pipeline stepper\n\n"
            "Update 02-hardware-review.html so the header above the narrative inline\n"
            "preview box correctly displays 'Stage Explanation:' across all modes."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_preview_label()
