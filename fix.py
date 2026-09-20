#!/usr/bin/env python3
# =====================================================================
# fix.py: Force exact heading correction and nav sync in 03-os-concepts.html
# =====================================================================
import os
import re
import subprocess

def run_fix():
    file_path = os.path.join("week01-operating-system-concepts", "03-os-concepts.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    week_title = "Week 1: Operating System Concepts"
    pill_template = '<a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;">'
    home_pill = f'{pill_template}&#127968; {week_title}</a>'

    correct_nav = f'''<nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
    <a href="02-hardware-review.html" class="module-nav-btn">&larr; Previous: 02. Hardware Review</a>
    {home_pill}
    <a href="04-os-structure.html" class="module-nav-btn">Next: 04. OS Structure &rarr;</a>
  </nav>'''

    modified = content

    # Direct string replacements for common bad variations
    bad_snippets = [
        "<h2>04. Operating System Concepts</h2>",
        "<h2>4. Operating System Concepts</h2>",
        "<h1>04. Operating System Concepts</h1>",
        "<h1>4. Operating System Concepts</h1>",
        "<h2>04. OS Concepts</h2>",
        "<h2>3. Operating System Concepts</h2>" # just in case
    ]
    for bad in bad_snippets:
        if bad in modified:
            modified = modified.replace(bad, "<h2>03. Operating System Concepts</h2>")

    # Regex fallback to catch any variations in tag attributes or spacing
    modified = re.sub(
        r'<h[123][^>]*>\s*(?:0?4|[4])\.\s*Operating System Concepts\s*</h[123]>',
        '<h2>03. Operating System Concepts</h2>',
        modified,
        flags=re.IGNORECASE
    )

    # Force update the navigation bar block
    if '<nav class="module-nav-bar">' in modified:
        start_idx = modified.find('<nav class="module-nav-bar">')
        end_idx = modified.find('</nav>', start_idx) + 6
        modified = modified[:start_idx] + correct_nav + modified[end_idx:]
    else:
        body_match = re.search(r'(<body[^>]*>)', modified, flags=re.IGNORECASE)
        if body_match:
            modified = modified.replace(body_match.group(1), f'{body_match.group(1)}\n  {correct_nav}')

    if modified != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"--> Successfully forced correction in {file_path}")

        try:
            subprocess.run(["git", "add", "fix.py", file_path], check=True)
            commit_msg = (
                "Force heading correction to 03. Operating System Concepts in 03-os-concepts.html\n\n"
                "Replace incorrect 04/4 numbering in 03-os-concepts.html heading with 03\n"
                "and update navigation bar."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Warning: Exact heading match not replaced. Debugging file headings:")
        found_headings = re.findall(r'<h[123][^>]*>.*?</h[123]>', modified, flags=re.DOTALL)
        for h in found_headings[:5]:
            print(f"   Found heading: {h}")

if __name__ == "__main__":
    run_fix()
