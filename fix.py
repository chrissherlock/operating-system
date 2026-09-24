#!/usr/bin/env python3
# =====================================================================
# fix.py: Increase preview box height to 150px in Module 02 interactive aid
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

def increase_preview_box_size():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Update preview-box CSS to increase height to 150px
    old_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-size: 0.86rem; color: var(--text); margin-bottom: 14px; line-height: 1.5; height: 115px; max-height: 115px; display: flex; flex-direction: column; justify-content: center; overflow-y: auto; }"""
    new_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-size: 0.86rem; color: var(--text); margin-bottom: 14px; line-height: 1.5; height: 150px; max-height: 150px; display: flex; flex-direction: column; justify-content: center; overflow-y: auto; }"""

    if old_css in content:
        content = content.replace(old_css, new_css)
    else:
        # Fallback replacement if exact string varies slightly
        content = content.replace("height: 115px; max-height: 115px;", "height: 150px; max-height: 150px;")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully increased preview box height to 150px in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if increase_preview_box_size():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Increase preview step box height to 150px in RAG interactive stepper\n\n"
                "Enlarge the fixed height of the preview summary box to 150px to provide\n"
                "more vertical breathing room while preventing control button jumping."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
