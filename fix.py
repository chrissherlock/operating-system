#!/usr/bin/env python3
# =====================================================================
# fix.py: Link "landmark 1990 paper" text to Ousterhout's paper
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

PAPER_URL = "https://www.mcs.anl.gov/~ketan/Papers/whyos.pdf"

def link_ousterhout_paper():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    target_phrase = "landmark 1990 paper"
    linked_phrase = f'<a href="{PAPER_URL}" target="_blank" rel="noopener">landmark 1990 paper</a>'

    if target_phrase in content and linked_phrase not in content:
        content = content.replace(target_phrase, linked_phrase, 1)
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Successfully linked 'landmark 1990 paper' in {TARGET_FILE}.")
    else:
        print("--> Target phrase already linked or not found.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Link landmark 1990 paper text to John Ousterhout's USENIX paper\n\n"
            "Add an external hyperlink pointing to the PDF of John Ousterhout's 1990\n"
            "paper in the systems engineering aside box of 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    link_ousterhout_paper()
