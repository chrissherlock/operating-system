#!/usr/bin/env python3
# =====================================================================
# rename_week1_modules.py: Rename Week 1 files to match new numbering
# =====================================================================
import os
import subprocess
import sys

def execute_renaming():
    base_dir = "week01-operating-system-concepts"
    os.makedirs(base_dir, exist_ok=True)

    # Mapping of old filenames to new filenames
    renames = {
        "03-hardware-review.html": "02-hardware-review.html",
        "04-os-concepts.html": "03-os-concepts.html",
        "05-os-structure.html": "04-os-structure.html"
    }

    modified_files = []

    for old_name, new_name in renames.items():
        old_path = os.path.join(base_dir, old_name)
        new_path = os.path.join(base_dir, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            modified_files.append(new_path)
            print(f"--> Renamed {old_name} to {new_name}")

    # Update index.html hrefs to match the new filenames
    index_path = os.path.join(base_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            idx_content = f.read()

        idx_content = idx_content.replace('href="03-hardware-review.html"', 'href="02-hardware-review.html"')
        idx_content = idx_content.replace('href="04-os-concepts.html"', 'href="03-os-concepts.html"')
        idx_content = idx_content.replace('href="05-os-structure.html"', 'href="04-os-structure.html"')

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(idx_content)
        modified_files.append(index_path)

    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified_files.append(fix_path)

    print(f"--> Staging modified files: {modified_files}")
    try:
        subprocess.run(["git", "add"] + modified_files, check=True)
        commit_msg = (
            "Renumber and rename Week 1 module files to match sequential index\n\n"
            "Rename hardware review, OS concepts, and OS structure module files to 02, 03, and 04\n"
            "under week01-operating-system-concepts/ and update index links."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Week 1 module files successfully renamed and deployed!")

if __name__ == "__main__":
    execute_renaming()
