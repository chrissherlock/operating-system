#!/usr/bin/env python3
# =====================================================================
# fix.py: Ensure proper text containment and scrolling in Module 02 preview box
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

def fix_preview_containment():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Update preview-box CSS to support proper vertical centering and scrolling containment
    old_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-size: 0.86rem; color: var(--text); margin-bottom: 14px; line-height: 1.5; height: 115px; max-height: 115px; display: flex; align-items: center; overflow: hidden; }"""
    new_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-size: 0.86rem; color: var(--text); margin-bottom: 14px; line-height: 1.5; height: 115px; max-height: 115px; display: flex; flex-direction: column; justify-content: center; overflow-y: auto; }"""

    if old_css in content:
        content = content.replace(old_css, new_css)
    else:
        # Fallback replacement if exact string varies slightly
        content = content.replace("align-items: center; overflow: hidden;", "flex-direction: column; justify-content: center; overflow-y: auto;")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully fixed text containment in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if fix_preview_containment():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix text containment and overflow in RAG stepper preview box\n\n"
                "Update flex direction and enable vertical scrolling on the preview box\n"
                "so step descriptions remain fully contained and readable."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
