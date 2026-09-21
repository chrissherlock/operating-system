#!/usr/bin/env python3
# =====================================================================
# fix.py: Clean up stray markdown bold markers in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_stray_markdown():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the malformed markdown bold pattern with clean HTML strong tags
    old_pattern = "using only **Ring 0 (Kernel)** and **Ring 3 (User)**."
    # Wait, in the actual HTML snippet it was written as **Ring 0 (Kernel)** without a closing ** pair or similar
    # Let's search for any stray ** near Ring 0 / Ring 3 in the footnote

    new_content = content.replace("using only **Ring 0 (Kernel)** and **Ring 3 (User)**.", "using only <strong>Ring 0 (Kernel)</strong> and <strong>Ring 3 (User)</strong>.")
    # Also catch any general stray double asterisks in that block
    new_content = new_content.replace("**Ring 0 (Kernel)**", "<strong>Ring 0 (Kernel)</strong>")
    new_content = new_content.replace("**Ring 3 (User)**", "<strong>Ring 3 (User)</strong>")

    # Generic cleanup of stray ** in the footnote paragraph
    footnote_target_snippet = "using only **Ring 0 (Kernel)"
    if footnote_target_snippet in new_content:
        new_content = new_content.replace("using only **Ring 0 (Kernel)", "using only <strong>Ring 0 (Kernel)</strong>")

    if new_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Cleaned up stray markdown syntax in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix stray markdown bold markers in Module 2 historical footnote\n\n"
                "Remove stray ** bold markers from the Rings 1 and 2 historical footnote\n"
                "within 02-hardware-review.html."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No stray markdown markers found.")

if __name__ == "__main__":
    fix_stray_markdown()
