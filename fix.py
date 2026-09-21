#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix half-encoded restart character in pipeline walkthrough
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_restart_character():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # The buggy entity syntax
    old_snippet = 'nextBtn.innerHTML = pipeIndex === list.length - 1 ? "Restart Walkthrough &↺;" : "Next Step &rarr;";'
    new_snippet = 'nextBtn.innerHTML = pipeIndex === list.length - 1 ? "Restart Walkthrough &#x21BA;" : "Next Step &rarr;";'

    # Also check the address translation walkthrough just in case it shared the same pattern
    old_trans_snippet = 'nextBtn.innerHTML = transIndex === list.length - 1 ? "Restart Walkthrough &↺;" : "Next Step &rarr;";'
    new_trans_snippet = 'nextBtn.innerHTML = transIndex === list.length - 1 ? "Restart Walkthrough &#x21BA;" : "Next Step &rarr;";'

    modified = content
    if old_snippet in modified:
        modified = modified.replace(old_snippet, new_snippet)
        print("--> Fixed pipeline restart button entity.")
    if old_trans_snippet in modified:
        modified = modified.replace(old_trans_snippet, new_trans_snippet)
        print("--> Fixed translation restart button entity.")

    if modified == content:
        # Fallback replacement if exact spacing differs
        modified = modified.replace("&↺;", "&#x21BA;")
        print("--> Replaced '&↺;' globally with '&#x21BA;'.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(modified)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix broken HTML entity encoding in pipeline restart button\n\n"
            "Correct the restart button innerHTML in 02-hardware-review.html by replacing\n"
            "the invalid '&↺;' entity syntax with a clean Unicode counterclockwise arrow."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for restart entity fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_restart_character()
