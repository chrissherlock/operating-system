#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace &bull; entities with literal Unicode bullets
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def remove_bull_entities():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace &bull; across SVG elements and script strings with Unicode bullet •
    if "&bull;" in content:
        new_content = content.replace("&bull;", "•")
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Successfully replaced &bull; with Unicode • in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Replace &bull; HTML entities with Unicode bullet characters in Module 2\n\n"
                "Convert raw &bull; entity strings in SVG text nodes and simulator script\n"
                "to standard Unicode bullets (•) to prevent literal text escaping."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No &bull; entities found in target file.")

if __name__ == "__main__":
    remove_bull_entities()
