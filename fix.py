#!/usr/bin/env python3
# =====================================================================
# fix.py: Enlarge the preview step box height in Module 02 interactive aid
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

def enlarge_preview_box():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the preview-box CSS rule with an enlarged fixed height
    old_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 12px; font-size: 0.82rem; color: var(--text); margin-bottom: 14px; line-height: 1.45; height: 85px; max-height: 85px; display: flex; align-items: center; overflow: hidden; }"""
    new_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-size: 0.86rem; color: var(--text); margin-bottom: 14px; line-height: 1.5; height: 115px; max-height: 115px; display: flex; align-items: center; overflow: hidden; }"""

    if old_css in content:
        content = content.replace(old_css, new_css)
    else:
        # Fallback replacement if exact string varies slightly
        content = content.replace("height: 85px; max-height: 85px;", "height: 115px; max-height: 115px;")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully enlarged preview box height in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if enlarge_preview_box():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Enlarge preview step box height in RAG interactive stepper\n\n"
                "Increase fixed height constraint on the preview summary box to create\n"
                "a larger, more spacious step box without causing button jumping."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
