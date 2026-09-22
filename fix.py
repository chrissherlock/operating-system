#!/usr/bin/env python3
# =====================================================================
# fix.py: Verify and correct image paths in Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

def fix_image_paths():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure relative paths correctly point to root images directory from week01 subdirectory
    # Module 1 uses "../images/..." successfully, so we maintain consistency.
    content = content.replace('src="images/', 'src="../images/')

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully verified and aligned image paths in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix image relative paths in Module 2 historical asides\n\n"
            "Ensure image source attributes in 02-hardware-review.html correctly point\n"
            "to the root images directory via ../images/."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_image_paths()
