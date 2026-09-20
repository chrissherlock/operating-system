#!/usr/bin/env python3
# =====================================================================
# fix_ic_extension.py: Correct integrated circuit image file extension
# =====================================================================
import os
import subprocess
import sys

def execute_extension_correction():
    base_dir = "week01-operating-system-concepts"
    file_path = os.path.join(base_dir, "01-what-is-an-os-and-history.html")

    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Correct the extension to .jpg
    content = content.replace('src="../images/integrated-circuit.jpeg"', 'src="../images/integrated-circuit.jpg"')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    modified = [file_path]
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Fix integrated circuit image extension to .jpg in Module 1\n\n"
            "Update week01-operating-system-concepts/01-what-is-an-os-and-history.html to reference\n"
            "../images/integrated-circuit.jpg instead of .jpeg."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Extension correction successfully deployed!")

if __name__ == "__main__":
    execute_extension_correction()
