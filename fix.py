#!/usr/bin/env python3
# =====================================================================
# fix.py: Update subtitle in 01-what-is-an-os-and-history.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "01-what-is-an-os-and-history.html"
)

OLD_SUBTITLE = '<p class="subtitle">Foundational Paradigms and the Five Computing Generations.</p>'
NEW_SUBTITLE = '<p class="subtitle">Core operating system abstractions, resource multiplexing, and architectural evolution from batch mainframes to ubiquitous computing.</p>'

def update_module_one_subtitle():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if OLD_SUBTITLE not in content:
        print("Notice: Target subtitle string not found or already updated.")
        return

    updated_content = content.replace(OLD_SUBTITLE, NEW_SUBTITLE, 1)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully updated subtitle in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Replace syllabus artifact with descriptive subtitle in Module 1\n\n"
            "Update the subtitle in 01-what-is-an-os-and-history.html to provide a\n"
            "clean conceptual overview of OS abstractions and computing evolution."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_module_one_subtitle()
