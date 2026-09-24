#!/usr/bin/env python3
# =====================================================================
# fix.py: Lock preview box dimensions to eliminate stepper button jumping
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

def fix_button_jumping():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the preview-box CSS rule with a strictly locked height
    old_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 12px; font-size: 0.82rem; color: var(--text); margin-bottom: 14px; line-height: 1.45; min-height: 72px; display: flex; align-items: center; }"""
    new_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 12px; font-size: 0.82rem; color: var(--text); margin-bottom: 14px; line-height: 1.45; height: 85px; max-height: 85px; display: flex; align-items: center; overflow: hidden; }"""

    if old_css in content:
        content = content.replace(old_css, new_css)
    else:
        # Fallback replacement if exact string varies slightly
        content = content.replace("min-height: 72px; display: flex; align-items: center;", "height: 85px; max-height: 85px; display: flex; align-items: center; overflow: hidden;")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully locked preview box height in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if fix_button_jumping():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Lock preview box height to prevent stepper button jumping\n\n"
                "Enforce rigid height constraints and overflow handling on the preview box\n"
                "so the control buttons remain completely stationary across all steps."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
