#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace &rarr; and &larr; entities with native Unicode arrows
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def sanitize_arrow_entities():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacements for entity leaks
    replacements = [
        ("&rarr;", "→"),
        ("&larr;", "←"),
        ("&times;", "×"),
    ]

    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Replaced all &rarr; and &larr; entities with Unicode arrows in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Replace &rarr; and &larr; HTML entities with native Unicode arrows\n\n"
                "Eliminate raw &rarr; and &larr; entities in JavaScript objects and button\n"
                "labels in 02-hardware-review.html to prevent textContent escaping bugs."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No &rarr; or &larr; entities found.")

if __name__ == "__main__":
    sanitize_arrow_entities()
