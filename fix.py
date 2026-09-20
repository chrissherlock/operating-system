#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject uniform Previous, Index, and Next navigation bars
# =====================================================================
import os
import re
import subprocess

NAV_CSS = """
<style id="module-nav-styles">
  .module-nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 1100px;
    margin: 0 auto 16px auto;
    gap: 12px;
    box-sizing: border-box;
  }
  .module-nav-bar.bottom {
    margin-top: 24px;
    margin-bottom: 24px;
  }
  .module-nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    text-decoration: none;
    color: #0284c7;
    background-color: #f0f9ff;
    border: 1px solid #bae6fd;
    padding: 7px 13px;
    border-radius: 6px;
    transition: all 0.15s ease;
  }
  .module-nav-btn:hover {
    background-color: #0284c7;
    color: #ffffff;
  }
  .module-nav-placeholder {
    visibility: hidden;
    padding: 7px 13px;
    font-size: 0.85rem;
  }
</style>
"""

def scan_week_modules(directory_path):
    files = sorted([
        f for f in os.listdir(directory_path)
        if f.endswith(".html") and f != "index.html" and not f.startswith(".")
    ])
    return files

def extract_page_title(content, fallback_filename):
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        title = re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()
        return title
    title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    if title_match:
        raw = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
        cleaned = raw.split("--")[0].split("-")[0].strip()
        if cleaned:
            return cleaned
    return fallback_filename.replace(".html", "").replace("-", " ").title()

def build_nav_markup(prev_file, prev_title, next_file, next_title, bottom=False):
    css_class = "module-nav-bar bottom" if bottom else "module-nav-bar"

    if prev_file:
        prev_link = (
            f'<a href="{prev_file}" class="module-nav-btn">&larr; Previous: {prev_title}</a>'
        )
    else:
        prev_link = '<span class="module-nav-placeholder">&larr; Previous</span>'

    index_link = '<a href="index.html" class="module-nav-btn">Week Index</a>'

    if next_file:
        next_link = (
            f'<a href="{next_file}" class="module-nav-btn">Next: {next_title} &rarr;</a>'
        )
    else:
        next_link = '<span class="module-nav-placeholder">Next &rarr;</span>'

    return (
        f'<nav class="{css_class}">\n'
        f'  {prev_link}\n'
        f'  {index_link}\n'
        f'  {next_link}\n'
        f'</nav>'
    )

def clean_legacy_navigation(content):
    # Strip any previously inserted nav blocks or styles
    content = re.sub(r'<style id="module-nav-styles">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<nav class="module-nav-bar.*?/nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="nav-back".*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="nav-container".*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="nav-bar".*?</div>', '', content, flags=re.DOTALL)
    return content

def update_page_nav(file_path, prev_file, prev_title, next_file, next_title):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = clean_legacy_navigation(content)

    # Ensure CSS is present before </head>
    if "</head>" in content:
        content = content.replace("</head>", f"{NAV_CSS}\n</head>", 1)
    else:
        content = f"{NAV_CSS}\n{content}"

    top_nav = build_nav_markup(prev_file, prev_title, next_file, next_title, bottom=False)
    bottom_nav = build_nav_markup(prev_file, prev_title, next_file, next_title, bottom=True)

    # Insert top navigation right after <body> or right before <main>
    if "<main" in content:
        content = re.sub(r"(<main[^>]*>)", f"{top_nav}\n\\1", content, count=1)
    elif "<body" in content:
        content = re.sub(r"(<body[^>]*>)", f"\\1\n{top_nav}", content, count=1)

    # Insert bottom navigation right after </main> or right before </body>
    if "</main>" in content:
        content = content.replace("</main>", f"{bottom_nav}\n</main>", 1)
    elif "</body>" in content:
        content = content.replace("</body>", f"{bottom_nav}\n</body>", 1)
    else:
        content = f"{content}\n{bottom_nav}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def execute_site_nav_update():
    repo_root = "."
    modified_files = ["fix.py"]

    week_dirs = sorted([
        d for d in os.listdir(repo_root)
        if os.path.isdir(d) and d.startswith("week")
    ])

    for week in week_dirs:
        week_path = os.path.join(repo_root, week)
        modules = scan_week_modules(week_path)
        if not modules:
            continue

        # Cache titles
        titles = {}
        for m in modules:
            m_path = os.path.join(week_path, m)
            with open(m_path, "r", encoding="utf-8", errors="ignore") as f:
                titles[m] = extract_page_title(f.read(), m)

        # Update each module with previous, index, and next
        for idx, current_file in enumerate(modules):
            current_path = os.path.join(week_path, current_file)

            prev_file = modules[idx - 1] if idx > 0 else None
            prev_title = titles.get(prev_file, "") if prev_file else ""

            next_file = modules[idx + 1] if idx < len(modules) - 1 else None
            next_title = titles.get(next_file, "") if next_file else ""

            update_page_nav(current_path, prev_file, prev_title, next_file, next_title)
            modified_files.append(current_path)
            print(f"--> Updated navigation for: {current_path}")

    # Stage, commit, and push
    try:
        print(f"--> Staging {len(modified_files)} files...")
        # Add week folders and fix.py
        subprocess.run(["git", "add", "fix.py"] + week_dirs, check=True)
        commit_msg = (
            "Add uniform previous, index, and next navigation across all week pages\n\n"
            "Update fix.py to crawl week directories, calculate linear reading order,\n"
            "and insert consistent top and bottom navigation bars across all modules."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_site_nav_update()
