#!/usr/bin/env python3
# =====================================================================
# fix.py: Style all navigation index links across the repository
# =====================================================================
import os
import re
import subprocess

WEEK_TITLE_MAP = {
    "week01-operating-system-concepts": "Week 1: Operating System Concepts",
    "week02-processes": "Week 2: Processes & Threads",
    "week03-process-scheduling": "Week 3: Process Scheduling",
    "week04-concurrency-and-mutual-exclusion": "Week 4: Concurrency & Mutual Exclusion",
    "week05-io-and-disk-scheduling": "Week 5: I/O & Disk Scheduling",
    "week06-synchronisation-and-deadlock": "Week 6: Synchronisation & Deadlock",
    "week09-memory-management": "Week 9: Memory Management",
    "week10-file-management": "Week 10: File Management",
    "week11-multiprocessor-scheduling-and-distributed-computing": "Week 11: Multiprocessors & Distributed Computing",
    "week11-multiprocessors": "Week 11: Multiprocessors",
    "week12-security": "Week 12: Security"
}

def style_all_navigation_links():
    repo_root = "."
    modified_files = []

    styled_anchor_template = '<a href="index.html" style="color: inherit; text-decoration: none;">'

    for root, dirs, files in os.walk(repo_root):
        dir_name = os.path.basename(root)
        week_title = WEEK_TITLE_MAP.get(dir_name)
        if not week_title:
            continue

        for file in files:
            if file.endswith(".html") and file != "index.html":
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                updated = False
                new_content = content

                # Replace any unstyled <a href="index.html"> tags in nav/header areas with styled ones
                # Also catch existing style variations and standardize them
                # First, fix existing malformed or unstyled anchor tags pointing to index.html
                unstyled_patterns = [
                    r'<a\s+href="index\.html"\s*>',
                    r'<a\s+href="\./index\.html"\s*>',
                    r'<a\s+href="index\.html"\s+style="[^"]*">',
                ]

                for pat in unstyled_patterns:
                    if re.search(pat, new_content):
                        new_content = re.sub(pat, styled_anchor_template, new_content)
                        updated = True

                # If the week title is present in the nav/header but not wrapped in an anchor at all, wrap it
                if week_title in new_content and 'href="index.html"' not in new_content:
                    header_pattern = r'(<header[^>]*>.*?</header>|<nav[^>]*>.*?</nav>|<div[^>]*class="[^"]*nav[^"]*"[^>]*>.*?</div>)'
                    header_match = re.search(header_pattern, new_content, flags=re.DOTALL | re.IGNORECASE)
                    if header_match:
                        h_block = header_match.group(1)
                        if week_title in h_block:
                            new_h_block = h_block.replace(week_title, f'{styled_anchor_template}{week_title}</a>')
                            new_content = new_content.replace(h_block, new_h_block)
                            updated = True

                if updated:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified_files.append(file_path)
                    print(f"--> Styled navigation index link in: {file_path}")

    if modified_files:
        try:
            subprocess.run(["git", "add", "fix.py"] + modified_files, check=True)
            commit_msg = (
                "Style navigation index links with inherit color and no decoration\n\n"
                "Update all week module HTML files to ensure navigation links pointing\n"
                "to index.html inherit parent typography styles and suppress underlines."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for styled navigation links!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> All module navigation links are already styled correctly.")

if __name__ == "__main__":
    style_all_navigation_links()
