#!/usr/bin/env python3
# =====================================================================
# fix.py: Strip textbook chapter cites and syllabus labels from modules
# =====================================================================
import os
import re
import subprocess

TARGET_FILES = [
    os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html"),
    os.path.join("week01-operating-system-concepts", "02-hardware-review.html"),
    os.path.join("week01-operating-system-concepts", "03-os-concepts.html"),
    os.path.join("week01-operating-system-concepts", "04-os-structure.html"),
]

def clean_textbook_citations(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}: file not found.")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # 1. Clean subtitles
    content = content.replace(
        '<p class="subtitle">Tanenbaum Chapter 1.1 &amp; 1.2: Foundational Paradigms and the Five Computing Generations.</p>',
        '<p class="subtitle">Foundational Paradigms and the Five Computing Generations.</p>'
    )
    content = content.replace(
        '<p class="subtitle">Tanenbaum Chapter 1.3: Processors, Memory Hierarchy, Disks, I/O Devices, Buses, and Booting.</p>',
        '<p class="subtitle">Processors, Memory Hierarchy, Disks, I/O Devices, Buses, and Booting.</p>'
    )

    # 2. Clean headings containing chapter citations
    content = content.replace(
        '<h2>Foundational Paradigms (Tanenbaum Chapter 1.1)</h2>',
        '<h2>Foundational Paradigms</h2>'
    )
    content = content.replace(
        '<h2>Historical Evolution &amp; Computing Generations (Tanenbaum Chapter 1.2)</h2>',
        '<h2>Historical Evolution &amp; Computing Generations</h2>'
    )

    # 3. Clean prose references in 03-os-concepts.html
    content = re.sub(
        r"Drawing from Tanenbaum's foundational taxonomy,\s*",
        "",
        content
    )

    # 4. Remove any remaining generic chapter reference patterns in headings or subtitles
    content = re.sub(r"\s*\(Tanenbaum Chapter [0-9.]+\)", "", content)
    content = re.sub(r"Tanenbaum Chapter [0-9.]+(&amp;|\s*and\s*)[0-9.]+:\s*", "", content)
    content = re.sub(r"Tanenbaum Chapter [0-9.]+:\s*", "", content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Stripped textbook citations from {file_path}")
        return True
    else:
        print(f"--> No textbook citations found in {file_path}")
        return False

def run_citation_cleanup():
    modified = []
    for file_path in TARGET_FILES:
        if clean_textbook_citations(file_path):
            modified.append(file_path)

    if modified:
        try:
            subprocess.run(["git", "add", "fix.py"] + modified, check=True)
            commit_msg = (
                "Remove external textbook chapter citations across Week 1 modules\n\n"
                "Strip chapter pointers and syllabus cross-references (e.g., Tanenbaum\n"
                "Chapter 1.1/1.2/1.3) from titles, subtitles, and headings across all\n"
                "Week 1 HTML modules."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")

if __name__ == "__main__":
    run_citation_cleanup()
