#!/usr/bin/env python3
# =====================================================================
# fix.py: Update navigation headers across all week directories
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

def update_navigation_headers():
    repo_root = "."
    modified_files = []

    for root, dirs, files in os.walk(repo_root):
        # Determine if this directory corresponds to a week
        dir_name = os.path.basename(root)
        week_title = WEEK_TITLE_MAP.get(dir_name)

        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                updated = False
                new_content = content

                # Replace generic nav header instances (e.g., "Week Index", "<span>Week Index</span>", etc.)
                patterns = [
                    r'(<span[^>]*>)\s*Week Index\s*(</span>)',
                    r'(<a[^>]*>\s*)Week Index(\s*</a>)',
                    r'(<div[^>]*>\s*)Week Index(\s*</div>)',
                    r'(<h[1-6][^>]*>\s*)Week Index(\s*</h[1-6]>)',
                    r'<span>Week Index</span>',
                    r'<div>Week Index</div>'
                ]

                # If we have a specific week title for this directory
                if week_title:
                    for pat in patterns:
                        if re.search(pat, new_content, flags=re.IGNORECASE):
                            new_content = re.sub(pat, rf'\1{week_title}\2' if '\\1' in pat else week_title, new_content, flags=re.IGNORECASE)
                            updated = True

                # Also catch generic breadcrumbs or titles saying "Week Index" if in root or unmapped
                if "Week Index" in new_content and not week_title:
                    new_content = new_content.replace("Week Index", "Course Overview")
                    updated = True

                if updated:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified_files.append(file_path)
                    print(f"--> Updated navigation header in: {file_path}")

    if modified_files:
        try:
            subprocess.run(["git", "add", "fix.py"] + modified_files, check=True)
            commit_msg = (
                "Update navigation headers across repository to display specific week titles\n\n"
                "Replace generic 'Week Index' strings in HTML navigation bars and breadcrumbs\n"
                "across all week directories with explicit week names (e.g., Week 1, Week 9)."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for navigation headers!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No navigation header updates needed or files already synchronized.")

if __name__ == "__main__":
    update_navigation_headers()
