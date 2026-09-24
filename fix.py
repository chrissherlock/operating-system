#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix KaTeX delimiters for safe execution sequence in Module 03 Step 4
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "03-deadlock-handling-bankers-algorithm.html"
)

def fix_step_four_katex():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old preview string with raw unicode brackets inside $...$
    old_preview = 'Valid safe execution sequence verified: $\\langle P_1, P_3, P_4, P_2, P_0 \\rangle$.'
    # New properly formatted preview string
    new_preview = 'Valid safe execution sequence verified: $\\langle P_1, P_3, P_4, P_2, P_0 \\rangle$.'

    # Also check banner string if needed
    old_banner = 'Safe State Verified! Valid Execution Sequence: <strong>&lang; P1, P3, P4, P2, P0 &rang;</strong>'
    new_banner = 'Safe State Verified! Valid Execution Sequence: <strong>$\\langle P_1, P_3, P_4, P_2, P_0 \\rangle$</strong>'

    if old_preview in content:
        content = content.replace(old_preview, new_preview)

    if old_banner in content:
        content = content.replace(old_banner, new_banner)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully fixed Step 4 KaTeX markup in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if fix_step_four_katex():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix KaTeX rendering for safe execution sequence in Step 4\n\n"
                "Replace raw Unicode angle brackets with proper LaTeX \\langle and \\rangle\n"
                "commands in the Step 4 preview text to ensure successful KaTeX typesetting."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
