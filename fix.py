#!/usr/bin/env python3
# =====================================================================
# fix.py: Precisely link first body occurrence of pioneers, avoiding headers
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

def apply_precise_pioneer_links():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Strip all existing Wikipedia anchor tags around these names to ensure a clean slate
    wiki_urls = [
        "https://en.wikipedia.org/wiki/John_von_Neumann",
        "https://en.wikipedia.org/wiki/James_R._Goodman",
        "https://en.wikipedia.org/wiki/Tom_Kilburn",
        "https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)",
        "https://en.wikipedia.org/wiki/Butler_Lampson",
        "https://en.wikipedia.org/wiki/John_Ousterhout"
    ]
    for url in wiki_urls:
        content = re.sub(rf'<a\s+[^>]*href="{re.escape(url)}"[^>]*>([^<]+)</a>', r'\1', content)

    # 2. Define precise target replacements in body paragraphs only (avoiding headings and <strong> titles)
    # We target the exact sentence where they are first introduced in the body text.

    # John von Neumann
    target_vn = "Before John von Neumann formalized"
    replacement_vn = 'Before <a href="https://en.wikipedia.org/wiki/John_von_Neumann" target="_blank" rel="noopener">John von Neumann</a> formalized'
    if target_vn in content:
        content = content.replace(target_vn, replacement_vn, 1)

    # James Goodman (in the paragraph text: "Goodman solved this")
    target_jg = "Goodman solved this by introducing"
    replacement_jg = '<a href="https://en.wikipedia.org/wiki/James_R._Goodman" target="_blank" rel="noopener">Goodman</a> solved this by introducing'
    if target_jg in content:
        content = content.replace(target_jg, replacement_jg, 1)

    # Tom Kilburn
    target_tk = "led by Tom Kilburn and David Edwards"
    replacement_tk = 'led by <a href="https://en.wikipedia.org/wiki/Tom_Kilburn" target="_blank" rel="noopener">Tom Kilburn</a> and David Edwards'
    if target_tk in content:
        content = content.replace(target_tk, replacement_tk, 1)

    # John McCarthy
    target_jm = "In 1963, John McCarthy championed"
    replacement_jm = 'In 1963, <a href="https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)" target="_blank" rel="noopener">John McCarthy</a> championed'
    if target_jm in content:
        content = content.replace(target_jm, replacement_jm, 1)

    # Butler Lampson
    target_bl = "Turing Award winner Butler Lampson emphasized"
    replacement_bl = 'Turing Award winner <a href="https://en.wikipedia.org/wiki/Butler_Lampson" target="_blank" rel="noopener">Butler Lampson</a> emphasized'
    if target_bl in content:
        content = content.replace(target_bl, replacement_bl, 1)

    # John Ousterhout
    target_jo = "In his landmark paper, John Ousterhout observed"
    replacement_jo = 'In his landmark paper, <a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" rel="noopener">John Ousterhout</a> observed'
    if target_jo in content:
        content = content.replace(target_jo, replacement_jo, 1)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully applied precise pioneer Wikipedia links in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Precisely link first body occurrence of pioneers, avoiding headers\n\n"
            "Target exact body sentence introductions in 02-hardware-review.html\n"
            "while leaving headings and strong header titles unlinked."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    apply_precise_pioneer_links()
