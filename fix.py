#!/usr/bin/env python3
# =====================================================================
# fix.py: Recursively remove bracketed citation markers from HTML files
# =====================================================================
import os
import re
import subprocess

def clean_html_files():
    updated_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Remove citation tags like[cite: 1] or[cite: 1] cleanly
                cleaned = re.sub(r'\s*\]+\]', '', content)

                if cleaned != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(cleaned)
                    updated_files.append(filepath)
                    print(f"--> Stripped citations from {filepath}")

    if updated_files:
        try:
            subprocess.run(["git", "add", "fix.py"] + updated_files, check=True)
            commit_msg = (
                "Remove citation markers from all course HTML files\n\n"
                "Recursively strip all bracketed citation tags () from all\n"
                "HTML modules across the repository to maintain clean course materials."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No citation markers found in any HTML files.")

if __name__ == "__main__":
    clean_html_files()
