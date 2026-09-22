#!/usr/bin/env python3
# =====================================================================
# fix.py: Link historical pioneer names to their Wikipedia articles
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

def embed_pioneer_links():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # 1. John von Neumann
    content = content.replace(
        "John von Neumann",
        '<a href="https://en.wikipedia.org/wiki/John_von_Neumann" target="_blank" rel="noopener">John von Neumann</a>'
    )
    # Avoid double-linking if already processed
    content = content.replace(
        '<a href="https://en.wikipedia.org/wiki/John_von_Neumann" target="_blank" rel="noopener"><a href="https://en.wikipedia.org/wiki/John_von_Neumann" target="_blank" rel="noopener">John von Neumann</a></a>',
        '<a href="https://en.wikipedia.org/wiki/John_von_Neumann" target="_blank" rel="noopener">John von Neumann</a>'
    )

    # 2. James Goodman
    content = content.replace(
        "James Goodman",
        '<a href="https://en.wikipedia.org/wiki/James_R._Goodman" target="_blank" rel="noopener">James Goodman</a>'
    )
    content = content.replace(
        '<a href="https://en.wikipedia.org/wiki/James_R._Goodman" target="_blank" rel="noopener"><a href="https://en.wikipedia.org/wiki/James_R._Goodman" target="_blank" rel="noopener">James Goodman</a></a>',
        '<a href="https://en.wikipedia.org/wiki/James_R._Goodman" target="_blank" rel="noopener">James Goodman</a>'
    )

    # 3. Tom Kilburn
    content = content.replace(
        "Tom Kilburn",
        '<a href="https://en.wikipedia.org/wiki/Tom_Kilburn" target="_blank" rel="noopener">Tom Kilburn</a>'
    )
    content = content.replace(
        '<a href="https://en.wikipedia.org/wiki/Tom_Kilburn" target="_blank" rel="noopener"><a href="https://en.wikipedia.org/wiki/Tom_Kilburn" target="_blank" rel="noopener">Tom Kilburn</a></a>',
        '<a href="https://en.wikipedia.org/wiki/Tom_Kilburn" target="_blank" rel="noopener">Tom Kilburn</a>'
    )

    # 4. John McCarthy
    content = content.replace(
        "John McCarthy",
        '<a href="https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)" target="_blank" rel="noopener">John McCarthy</a>'
    )
    content = content.replace(
        '<a href="https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)" target="_blank" rel="noopener"><a href="https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)" target="_blank" rel="noopener">John McCarthy</a></a>',
        '<a href="https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)" target="_blank" rel="noopener">John McCarthy</a>'
    )

    # 5. Butler Lampson
    content = content.replace(
        "Butler Lampson",
        '<a href="https://en.wikipedia.org/wiki/Butler_Lampson" target="_blank" rel="noopener">Butler Lampson</a>'
    )
    content = content.replace(
        '<a href="https://en.wikipedia.org/wiki/Butler_Lampson" target="_blank" rel="noopener"><a href="https://en.wikipedia.org/wiki/Butler_Lampson" target="_blank" rel="noopener">Butler Lampson</a></a>',
        '<a href="https://en.wikipedia.org/wiki/Butler_Lampson" target="_blank" rel="noopener">Butler Lampson</a>'
    )

    # 6. John Ousterhout
    content = content.replace(
        "John Ousterhout",
        '<a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" rel="noopener">John Ousterhout</a>'
    )
    content = content.replace(
        '<a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" rel="noopener"><a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" rel="noopener">John Ousterhout</a></a>',
        '<a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" rel="noopener">John Ousterhout</a>'
    )

    if content != original_content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Successfully added Wikipedia links to pioneers in {TARGET_FILE}.")
    else:
        print("--> No changes made; links may already be present.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add Wikipedia hyperlinks to historical pioneer names in Module 2\n\n"
            "Enhance historical and systems engineering aside boxes in\n"
            "02-hardware-review.html with direct links to respective Wikipedia articles."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    embed_pioneer_links()
