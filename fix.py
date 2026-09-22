#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject house emoji into navigation buttons across course files
# =====================================================================
import os
import subprocess

def add_house_icon_to_nav():
    updated_files = []

    # Walk through repository directories
    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                # Replace standard overview text links with house emoji if missing
                # e.g., <a href="index.html">Week 1: Operating System Concepts</a>
                # or similar overview pointers
                if "&#127968;" not in content:
                    # Target course overview or index links
                    content = content.replace(
                        'href="index.html">Week 1: Operating System Concepts</a>',
                        'href="index.html">&#127968; Week 1: Operating System Concepts</a>'
                    )
                    content = content.replace(
                        'href="../index.html">Week 1: Operating System Concepts</a>',
                        'href="../index.html">&#127968; Week 1: Operating System Concepts</a>'
                    )
                    content = content.replace(
                        'href="../index.html">&larr; Back to Course Overview</a>',
                        'href="../index.html">&#127968; Back to Course Overview</a>'
                    )

                if content != original_content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    updated_files.append(filepath)
                    print(f"--> Added house icon to nav in {filepath}")

    if updated_files:
        try:
            subprocess.run(["git", "add", "fix.py"] + updated_files, check=True)
            commit_msg = (
                "Add house icon emoji to home navigation links across all module files\n\n"
                "Update module navigation bars in Week 1 and Week 2 HTML files to feature\n"
                "the house character (&#127968;) on root course overview links."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No navigation links required updating.")

if __name__ == "__main__":
    add_house_icon_to_nav()
