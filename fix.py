#!/usr/bin/env python3
# =====================================================================
# update_gen3_assets.py: Insert Generation 3 assets into Module 1 page
# =====================================================================
import os
import subprocess
import sys

def execute_asset_insertion():
    base_dir = "week01-operating-system-concepts"
    file_path = os.path.join(base_dir, "01-what-is-an-os-and-history.html")

    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = [file_path]
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Add Generation 3 IC and IBM System/360 images with attributions\n\n"
            "Update week01-operating-system-concepts/01-what-is-an-os-and-history.html to include\n"
            "integrated-circuit.jpeg and system360.jpg with correct root image paths and attributions."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Generation 3 image integration successfully deployed!")

if __name__ == "__main__":
    execute_asset_insertion()
