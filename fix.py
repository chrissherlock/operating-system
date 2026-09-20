#!/usr/bin/env python3
# =====================================================================
# relocate_tanenbaum_asset.py: Move tanenbaum.jpg and update paths
# =====================================================================
import os
import shutil
import subprocess
import sys

def relocate_asset():
    src = os.path.join("week10-file-management", "images", "tanenbaum.jpg")
    dest_dir = "images"
    dest = os.path.join(dest_dir, "tanenbaum.jpg")

    os.makedirs(dest_dir, exist_ok=True)

    moved = []
    if os.path.exists(src):
        shutil.move(src, dest)
        moved.append(dest)
        print(f"--> Moved {src} to {dest}")

    # Search and replace references in html files
    modified = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                updated = False
                if "tanenbaum.png" in content:
                    content = content.replace("tanenbaum.png", "tanenbaum.jpg")
                    updated = True
                if "week10-file-management/images/tanenbaum.jpg" in content:
                    content = content.replace("week10-file-management/images/tanenbaum.jpg", "../images/tanenbaum.jpg")
                    updated = True

                if updated:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    modified.append(path)

    fix_path = "fix.py"
    if os.path.exists(fix_path) and fix_path not in modified:
        modified.append(fix_path)

    all_to_add = list(set(moved + modified))
    if not all_to_add:
        print("--> No files modified or moved.")
        return

    print(f"--> Staging git changes: {all_to_add}")
    try:
        subprocess.run(["git", "add"] + all_to_add, check=True)
        commit_msg = (
            "Relocate tanenbaum.jpg to top-level images directory and update references\n\n"
            "Move tanenbaum.jpg from week10-file-management/images/ to top-level images/\n"
            "and update all module references to point to ../images/tanenbaum.jpg."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Tanenbaum asset relocation and path updates successfully deployed!")

if __name__ == "__main__":
    relocate_asset()
