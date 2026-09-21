#!/usr/bin/env python3
# =====================================================================
# fix.py: Final cleanup of HTML errors, borders, and duplicate comments
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def final_html_cleanup():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix invalid hex color code typo (#d8b4te -> #d8b4fe)
    content = content.replace("border: 1px solid #d8b4te;", "border: 1px solid #d8b4fe;")

    # 2. Clean up duplicated translation simulator comment headers
    redundant_comments = """      <!-- Interactive Directed Narrative Stepper: Bit-Slice & Offset Pass-Through Engine -->
      <!-- Interactive Directed Narrative Stepper: Bit-Slice & Synchronized Page Table Walk Engine -->
      <!-- Interactive Directed Narrative Stepper: Bit-Slice & Synchronized Page Table Walk Engine -->"""

    clean_comment = "      <!-- Interactive Directed Narrative Stepper: Synchronized Page Table Walk Engine -->"

    if redundant_comments in content:
        content = content.replace(redundant_comments, clean_comment)
        print("--> Cleaned up redundant stacked comment headers.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully cleaned up {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix HTML border hex typo and remove duplicate comment headers\n\n"
            "Correct #d8b4te to #d8b4fe and deduplicate stacked stepper comments\n"
            "within 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for HTML cleanup!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    final_html_cleanup()
