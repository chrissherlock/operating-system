#!/usr/bin/env python3
# =====================================================================
# fix.py: Align week index header link styling with pagination buttons
# =====================================================================
os_import = __import__('os')
re_import = __import__('re')
subprocess_import = __import__('subprocess')

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

def align_navigation_pill_styling():
    repo_root = "."
    modified_files = []

    # Styled pill template matching pagination buttons
    pill_template = '<a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;">'

    for root, dirs, files in os_import.walk(repo_root):
        dir_name = os_import.path.basename(root)
        week_title = WEEK_TITLE_MAP.get(dir_name)
        if not week_title:
            continue

        for file in files:
            if file.endswith(".html") and file != "index.html":
                file_path = os_import.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                updated = False
                new_content = content

                # Replace any existing index.html anchor tag in nav/header with the pill-styled version
                # Or wrap the week title if unstyled
                old_anchor_patterns = [
                    rf'<a\s+href="index\.html"\s+style="[^"]*">\s*{re_import.escape(week_title)}\s*</a>',
                    rf'<a\s+href="index\.html"\s*>\s*{re_import.escape(week_title)}\s*</a>',
                    rf'<a\s+href="\./index\.html"\s*>\s*{re_import.escape(week_title)}\s*</a>'
                ]

                replaced = False
                for pat in old_anchor_patterns:
                    if re_import.search(pat, new_content):
                        new_content = re_import.sub(pat, f'{pill_template}&larr; {week_title}</a>', new_content)
                        updated = True
                        replaced = True
                        break

                if not replaced and week_title in new_content:
                    # Target header/nav block
                    header_pattern = r'(<header[^>]*>.*?</header>|<nav[^>]*>.*?</nav>|<div[^>]*class="[^"]*nav[^"]*"[^>]*>.*?</div>)'
                    header_match = re_import.search(header_pattern, new_content, flags=re_import.DOTALL | re_import.IGNORECASE)
                    if header_match:
                        h_block = header_match.group(1)
                        if week_title in h_block:
                            new_h_block = h_block.replace(week_title, f'{pill_template}&larr; {week_title}</a>')
                            new_content = new_content.replace(h_block, new_h_block)
                            updated = True

                if updated:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified_files.append(file_path)
                    print(f"--> Aligned navigation header pill styling in: {file_path}")

    if modified_files:
        try:
            subprocess_import.run(["git", "add", "fix.py"] + modified_files, check=True)
            commit_msg = (
                "Align week index navigation header styling with pagination buttons\n\n"
                "Update module HTML files across all week directories so the center week\n"
                "index link matches the styled pill format of the previous/next buttons."
            )
            subprocess_import.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess_import.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for pill-styled navigation headers!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> All week index navigation headers are already styled as pills.")

if __name__ == "__main__":
    align_navigation_pill_styling()
