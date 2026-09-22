#!/usr/bin/env python3
# =====================================================================
# fix.py: Remove subtitle paragraph from 01-what-is-an-os-and-history.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "01-what-is-an-os-and-history.html"
)

SUBTITLE_LINE = '      <p class="subtitle">Core operating system abstractions, resource multiplexing, and architectural evolution from batch mainframes to ubiquitous computing.</p>\n'

def remove_subtitle():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if SUBTITLE_LINE in content:
        content = content.replace(SUBTITLE_LINE, "")
    else:
        # Fallback if whitespace differs
        import re
        content = re.sub(
            r'\s*<p class="subtitle">Core operating system abstractions, resource multiplexing, and architectural evolution from batch mainframes to ubiquitous computing\.</p>',
            "",
            content
        )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully removed subtitle from {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Remove subtitle element from Module 1 header\n\n"
            "Delete the subtitle paragraph in 01-what-is-an-os-and-history.html so\n"
            "the document flows directly from the h1 heading into the module body."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    remove_subtitle()
