#!/usr/bin/env python3
# =====================================================================
# add_ousterhout_image.py: Embed John Ousterhout's image into Gang Aside
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_GANG_WITH_IMAGE = r"""
        <!-- WIKIPEDIA ASIDE BOX WITH PORTRAIT -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Gang Scheduling</h4>

          <div style="display: flex; gap: 14px; align-items: flex-start; margin-bottom: 10px;">
            <div style="flex-shrink: 0; width: 85px; height: 105px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
              <img src="https://upload.wikimedia.org/wikipedia/commons/e/e0/John_Ousterhout_by_Christopher_Michel.jpg" alt="John Ousterhout Portrait" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
              Gang scheduling was pioneered by <strong>John Ousterhout</strong> in 1982 to address the coordination failure of independent thread schedulers on parallel hardware. By scheduling related threads across multiple cores simultaneously (a two-dimensional matrix of Cores $\times$ Time Quanta), gang scheduling prevents preemption delays and blocking when cooperating threads communicate.
            </p>
          </div>

          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Gang_scheduling" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Gang Scheduling on Wikipedia</a></li>
          </ul>
        </aside>"""

def update_gang_aside():
    mod2 = os.path.join("week11-multiprocessors", "02-multiprocessor-scheduling.html")
    modified = []

    if os.path.exists(mod2):
        with open(mod2, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove existing Gang aside if present
        if "Historical Summary &amp; Further Reading: Gang Scheduling" in content:
            parts = content.split("<!-- WIKIPEDIA ASIDE BOX")
            content = parts[0] + parts[1].split("</aside>", 1)[1]

        target = "<!-- GUIDED WALKTHROUGH"
        if target in content:
            content = content.replace(target, WIKI_ASIDE_GANG_WITH_IMAGE + "\n\n      " + target, 1)
            with open(mod2, "w", encoding="utf-8") as f:
                f.write(content)
            modified.append(mod2)

    # Synchronize fix.py
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    if not modified:
        print("--> No files modified.")
        return

    print(f"--> Staging modified files: {modified}")
    subprocess.run(["git", "add"] + modified, check=True)

    commit_msg = (
        "Add John Ousterhout portrait image to Gang Scheduling aside box\n\n"
        "Embed portrait image of John Ousterhout into the Gang Scheduling historical\n"
        "summary box in 02-multiprocessor-scheduling.html."
    )

    print("--> Committing changes...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("--> Pushing changes to origin main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> John Ousterhout image successfully added to Gang Scheduling aside!")

if __name__ == "__main__":
    update_gang_aside()
