#!/usr/bin/env python3
# =====================================================================
# fix.py: Clean up leaked escaped quotes in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_leaked_quotes():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace leaked escaped quotes with standard quotes
    new_content = content.replace(r'\"', '"').replace(r'\\"', '"')

    if new_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Cleaned up leaked escaped quotes in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix leaked escaped quotes in Module 2 privilege deep dive\n\n"
                "Remove literal escaped quotes (\\\") from the privilege hierarchies\n"
                "callout box within 02-hardware-review.html."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No leaked escaped quotes found.")

if __name__ == "__main__":
    fix_leaked_quotes()
