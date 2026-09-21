#!/usr/bin/env python3
# =====================================================================
# fix.py: Add inline Wikipedia links for Booth encoding & Wallace tree
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def add_multiplier_wiki_links():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Target the Cycle 5 "why" text inside pipeStorylines.pipeline
    old_snippet = "typically using Booth encoding and Wallace tree adders"

    booth_url = "https://en.wikipedia.org/wiki/Booth%27s_multiplication_algorithm"
    wallace_url = "https://en.wikipedia.org/wiki/Wallace_tree"
    link_style = "color: #0284c7; text-decoration: underline;"

    new_snippet = (
        f'typically using <a href=\\"{booth_url}\\" target=\\"_blank\\" rel=\\"noopener noreferrer\\" '
        f'style=\\"{link_style}\\">Booth encoding</a> and '
        f'<a href=\\"{wallace_url}\\" target=\\"_blank\\" rel=\\"noopener noreferrer\\" '
        f'style=\\"{link_style}\\">Wallace tree adders</a>'
    )

    if old_snippet in content:
        content = content.replace(old_snippet, new_snippet)
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Added Wikipedia links for Booth encoding and Wallace trees in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Add inline Wikipedia links for Booth encoding and Wallace trees\n\n"
                "Link hardware multiplication terms to Wikipedia in the Cycle 5 pipeline\n"
                "analytical pane in 02-hardware-review.html for optional deeper reading."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Target snippet already updated or not found.")

if __name__ == "__main__":
    add_multiplier_wiki_links()
