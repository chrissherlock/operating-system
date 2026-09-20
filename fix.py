#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace phrasing in Module 2 interactive widget
# =====================================================================
import os
import subprocess

def update_widget_label():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    target_phrase = "Pedagogical Insight (Why This Matters)"
    replacement_phrase = "Why The System Does This"

    if target_phrase in content:
        content = content.replace(target_phrase, replacement_phrase)
        print(f"--> Replaced '{target_phrase}' with '{replacement_phrase}'.")
    else:
        print("--> Target phrase not found or already updated.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Replace awkward pedagogical phrasing in Module 2 interactive widget\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html to replace\n"
            "'Pedagogical Insight' label with clear 'Why The System Does This' header."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_widget_label()
