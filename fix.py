#!/usr/bin/env python3
import os
import re
import subprocess
import sys

COMMIT_MSG = """Mark Module 9 (Working Set Model) as published in week09 index

Update week09-memory-management/index.html to transition Module 9 from
draft or in-progress status to published. Ensure the link to
09-working-set.html is enabled and active in the curriculum overview."""

def run_git_step(cmd, step_desc):
    print(f"--> {step_desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{step_desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0:
        print(f"Execution failed during {step_desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)
    return res.stdout.strip()

def mark_module_published(content):
    # Pattern 1: Target status badges or text associated with 09-working-set.html
    # Matches common badge variants: draft, pending, planned, in-progress, coming soon
    pattern_badge = r'(<a[^>]*href=["\']09-working-set\.html["\'][^>]*>[\s\S]*?)(<(?:span|div)[^>]*class=["\'][^"\']*(?:badge|tag|status)[^"\']*["\'][^>]*>)(.*?)(</(?:span|div)>)'

    def badge_repl(m):
        prefix = m.group(1)
        tag_open = m.group(2)
        tag_close = m.group(4)
        # Update badge class to completed/published style if needed
        updated_open = re.sub(r'\b(draft|pending|in-progress|todo|wip)\b', 'completed published', tag_open)
        return f"{prefix}{updated_open}Published{tag_close}"

    new_content, count = re.subn(pattern_badge, badge_repl, content, flags=re.IGNORECASE)

    # Pattern 2: Badge placed immediately before or around 09-working-set.html
    if count == 0:
        pattern_fallback = r'(09-working-set\.html[\s\S]{0,120}?<span[^>]*class=["\'][^"\']*badge[^"\']*["\'][^>]*>)(.*?)(</span>)'
        new_content, count = re.subn(pattern_fallback, r'\1Published\3', content, flags=re.IGNORECASE)

    # Pattern 3: Direct text status replacement near Module 9
    if count == 0:
        pattern_text = r'(9\.\s*The Working Set Model[\s\S]{0,160}?)(Draft|Planned|In Progress|Coming Soon|WIP)'
        new_content, count = re.subn(pattern_text, r'\1Published', content, flags=re.IGNORECASE)

    # If any disabled or inactive link class wraps the module, remove it
    new_content = re.sub(
        r'(class=["\'][^"\']*)\b(disabled|inactive|opacity-50)\b([^"\']*["\'][^>]*href=["\']09-working-set\.html["\'])',
        r'\1\3',
        new_content
    )

    return new_content, count

def update_index_file():
    index_path = "week09-memory-management/index.html"
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(index_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    updated_content, replacements = mark_module_published(original_content)

    if replacements == 0 and updated_content == original_content:
        print("Note: Could not find an unreleased badge pattern. Verifying file state...")
    else:
        print(f"Updated Module 9 publication status in {index_path}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    # Stage, commit using -a -m, and push
    run_git_step(["git", "add", index_path], f"Staging {index_path}")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing tracked changes with -a -m")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Successfully updated index, committed, and pushed to origin/main.")

def main():
    update_index_file()

if __name__ == "__main__":
    main()
