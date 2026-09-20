#!/usr/bin/env python3
# =====================================================================
# fix.py: Ensure every module HTML file across all weeks links to index.html
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

def ensure_all_navigation_links():
    repo_root = "."
    modified_files = []

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

                # Check if an index link already exists in the navigation context
                if 'href="index.html"' in new_content or f"href='./index.html'" in new_content:
                    # Check if the week title is present; if so, verify if it's inside an <a> tag
                    if week_title in new_content:
                        # If the exact string appears outside an <a> tag, wrap it
                        # Simple heuristic: replace plain week title with hyperlinked version if not already wrapped
                        linked_str = f'<a href="index.html" style="color: inherit; text-decoration: none;">{week_title}</a>'
                        if linked_str not in new_content:
                            new_content = new_content.replace(week_title, linked_str)
                            updated = True
                else:
                    # No index link found at all; search for navigation header block or breadcrumb and inject link
                    nav_pattern = r'(<nav[^>]*>.*?</nav>)'
                    match = re.search(nav_pattern, new_content, flags=re.DOTALL)
                    if match:
                        nav_block = match.group(1)
                        if week_title in nav_block:
                            linked_nav = nav_block.replace(
                                week_title,
                                f'<a href="index.html" style="color: inherit; text-decoration: none;">{week_title}</a>'
                            )
                            new_content = new_content.replace(nav_block, linked_nav)
                            updated = True
                        else:
                            # Inject week title link into nav if title wasn't found verbatim
                            linked_nav = re.sub(r'(<span>|<div>)([^<]*)(</span>|</div>)', rf'\1<a href="index.html" style="color: inherit; text-decoration: none;">{week_title}</a>\3', nav_block, count=1)
                            if linked_nav != nav_block:
                                new_content = new_content.replace(nav_block, linked_nav)
                                updated = True
                    else:
                        # Fallback: if no <nav> tag, replace week title anywhere in header/body top
                        if week_title in new_content:
                            new_content = new_content.replace(
                                week_title,
                                f'<a href="index.html" style="color: inherit; text-decoration: none;">{week_title}</a>'
                            )
                            updated = True

                if updated:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified_files.append(file_path)
                    print(f"--> Ensured navigation header links to index.html in: {file_path}")

    if modified_files:
        try:
            subprocess.run(["git", "add", "fix.py"] + modified_files, check=True)
            commit_msg = (
                "Ensure all module navigation headers link to index.html across repository\n\n"
                "Walk all week directories and wrap unlinked navigation header titles\n"
                "in anchor tags pointing to index.html in every module HTML file."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for all navigation links!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> All module navigation headers are already correctly linked to index.html.")

if __name__ == "__main__":
    ensure_all_navigation_links()
