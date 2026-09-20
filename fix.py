#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace week index label with home icon in navigation header
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

def update_header_with_home_icon():
    repo_root = "."
    modified_files = []

    # Styled pill template featuring a home symbol (🏠)
    pill_template = '<a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;">'

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

                # Match existing styled or unstyled navigation index links
                patterns_to_replace = [
                    rf'<a\s+href="index\.html"[^>]*>\s*(?:&larr;|&rarr;|&#8592;|&#8594;|🏠)?\s*{re.escape(week_title)}\s*</a>',
                    rf'<a\s+href="\./index\.html"[^>]*>\s*(?:&larr;|&rarr;|&#8592;|&#8594;|🏠)?\s*{re.escape(week_title)}\s*</a>',
                    rf'<span>\s*{re.escape(week_title)}\s*</span>'
                ]

                replaced = False
                for pat in patterns_to_replace:
                    if re.search(pat, new_content):
                        new_content = re.sub(pat, f'{pill_template}&#127968; {week_title}</a>', new_content)
                        updated = True
                        replaced = True
                        break

                if not replaced and week_title in new_content:
                    header_pattern = r'(<header[^>]*>.*?</header>|<nav[^>]*>.*?</nav>|<div[^>]*class="[^"]*nav[^"]*"[^>]*>.*?</div>)'
                    header_match = re.search(header_pattern, new_content, flags=re.DOTALL | re.IGNORECASE)
                    if header_match:
                        h_block = header_match.group(1)
                        if week_title in h_block:
                            new_h_block = h_block.replace(week_title, f'{pill_template}&#127968; {week_title}</a>')
                            new_content = new_content.replace(h_block, new_h_block)
                            updated = True

                if updated:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified_files.append(file_path)
                    print(f"--> Updated navigation header with home symbol in: {file_path}")

    if modified_files:
        try:
            subprocess.run(["git", "add", "fix.py"] + modified_files, check=True)
            commit_msg = (
                "Replace week index text label with home icon in navigation header\n\n"
                "Update all week module HTML files to display a home symbol (🏠) alongside\n"
                "the week title within the styled navigation pill link."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for home icon navigation headers!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> All week index navigation headers already use the home symbol.")

if __name__ == "__main__":
    update_header_with_home_icon()
