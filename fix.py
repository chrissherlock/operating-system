#!/usr/bin/env python3
# =====================================================================
# fix.py: Recursively inject house emoji into all index navigation links
# =====================================================================
import os
import re
import subprocess

def inject_house_icon_globally():
    updated_files = []

    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                def check_and_insert(match):
                    tag_attrs = match.group(1)
                    link_text = match.group(2)
                    if "&#127968;" not in link_text:
                        return f'<a {tag_attrs}>&#127968; {link_text}</a>'
                    return match.group(0)

                # Match any anchor tag pointing to an index file
                pattern = r'<a\s+([^>]*href="[^"]*index\.html"[^>]*)>([^<]+)</a>'
                new_content = re.sub(pattern, check_and_insert, content)

                # Match parent overview links
                pattern_overview = r'<a\s+([^>]*href="[^"]*\.\./index\.html"[^>]*)>([^<]+)</a>'
                new_content = re.sub(pattern_overview, check_and_insert, new_content)

                if new_content != original_content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    updated_files.append(filepath)
                    print(f"--> Added house icon to {filepath}")

    if updated_files:
        try:
            subprocess.run(["git", "add", "fix.py"] + updated_files, check=True)
            commit_msg = (
                "Add house icon to all index and overview navigation links\n\n"
                "Recursively scan all HTML files across the repository to ensure\n"
                "every index or overview navigation link includes the house emoji (&#127968;)."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> All index links already contain the house icon.")

if __name__ == "__main__":
    inject_house_icon_globally()
