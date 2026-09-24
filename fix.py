#!/usr/bin/env python3
# =====================================================================
# fix.py: Stabilize stepper button positioning by fixing preview box height
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

def stabilize_stepper_buttons():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Update CSS definition for preview-box to include a stable min-height
    old_preview_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 12px; font-size: 0.82rem; color: var(--text); margin-bottom: 14px; line-height: 1.45; }"""
    new_preview_css = """.preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 12px; font-size: 0.82rem; color: var(--text); margin-bottom: 14px; line-height: 1.45; min-height: 72px; display: flex; align-items: center; }"""

    if old_preview_css in content:
        content = content.replace(old_preview_css, new_preview_css)
    else:
        # Fallback search if spacing differs slightly
        content = content.replace(
            "padding: 12px; font-size: 0.82rem; color: var(--text); margin-bottom: 14px;",
            "padding: 12px; font-size: 0.82rem; color: var(--text); margin-bottom: 14px; min-height: 72px; display: flex; align-items: center;"
        )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully stabilized button positioning in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if stabilize_stepper_buttons():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix button vertical shifting in RAG interactive stepper controls\n\n"
                "Add fixed min-height to preview summary box to prevent Prev and Next buttons\n"
                "from jumping or shifting vertically when switching steps."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
