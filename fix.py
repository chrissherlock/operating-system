#!/usr/bin/env python3
import os
import re
import subprocess
import sys

def modify_root_index():
    target_file = "index.html"
    if not os.path.exists(target_file):
        print(f"Error: Could not find {target_file} in current directory.", file=sys.stderr)
        return False

    print(f"--> Reading {target_file}...")
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean up the duplicate text in Week 9 description if present
    duplicate_pattern = r"page replacement algorithms \(Clock / Second-Chance\),\s*and\s*page replacement algorithms \(Clock / Second-Chance\),\s*and"
    if re.search(duplicate_pattern, content):
        content = re.sub(duplicate_pattern, "page replacement algorithms (Clock / Second-Chance), and", content)
        print("--> Fixed duplicated text in memory management description.")

    # 2. Update Week 11 Card: activate link and update description/tags
    # Match Week 11 section/card block
    week11_pattern = r'(<a[^>]*href=["\'](?:#|week11[^"\']*)["\'][^>]*>[\s\S]*?Week 11[\s\S]*?</a>|<div[^>]*class=["\'][^"\']*card[^"\']*["\'][^>]*>[\s\S]*?Week 11[\s\S]*?</div>)'

    # Replacement card matching the dashboard's design language
    new_week11_card = r"""<a href="week11-multiprocessors/index.html" class="module-card">
        <span class="module-tag">Week 11 &bull; Chapter 8</span>
        <h3 class="module-title">Multiprocessor Systems &amp; Distributed Computing</h3>
        <p class="module-desc">
          Multiprocessor hardware models (UMA, NUMA), cache coherence protocols (MESI), and multiprocessor OS types (Symmetric Multiprocessing). Explores gang scheduling, multicomputer interconnect topologies, Remote Procedure Calls (RPC), Distributed Shared Memory (DSM), and distributed middleware architectures.
        </p>
        <div class="topics-list">
          <span class="topic-pill">SMP &bull; UMA/NUMA</span>
          <span class="topic-pill">MESI Coherence</span>
          <span class="topic-pill">Gang Scheduling</span>
          <span class="topic-pill">RPC &bull; DSM</span>
          <span class="topic-pill">Distributed Middleware</span>
        </div>
      </a>"""

    # If the file uses <a> tags with class module-card or similar, replace or update
    match = re.search(r'(<a[^>]*href=[^>]*>[\s\S]*?Week 11[\s\S]*?</a>)', content)
    if match:
        content = content[:match.start()] + new_week11_card + content[match.end():]
        print("--> Replaced existing Week 11 card link.")
    else:
        # Check if it was an inactive div
        match_div = re.search(r'(<div[^>]*>[\s\S]*?Week 11[\s\S]*?</div>\s*</div>)', content)
        if match_div:
            content = content[:match_div.start()] + new_week11_card + content[match_div.end():]
            print("--> Activated Week 11 card from container block.")
        else:
            print("Notice: Standard Week 11 card pattern not directly matched; checking generic week11 marker...")
            content = re.sub(r'href=["\']#["\'](?=[^>]*Week 11)', 'href="week11-multiprocessors/index.html"', content)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("--> Successfully updated root index.html!")
    return True

def run_git_deployment():
    target_file = "index.html"
    print("--> Staging index.html...")
    subprocess.run(["git", "add", target_file], check=True)

    status_res = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if status_res.returncode == 0:
        print("--> No staged changes detected in index.html. Exiting.")
        return

    print("--> Committing changes...")
    commit_msg = (
        "Update root dashboard index to activate Week 11 and fix typo\n\n"
        "Update index.html to link Week 11 to week11-multiprocessors/index.html with\n"
        "Chapter 8 multiprocessor topics, and clean up duplicate text in the\n"
        "memory management description."
    )
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> Deployment of root dashboard complete!")

if __name__ == "__main__":
    if modify_root_index():
        run_git_deployment()
