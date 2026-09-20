#!/usr/bin/env python3
# =====================================================================
# use_local_ousterhout_image.py: Use local images/ousterhout.png asset
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_GANG_LOCAL_IMG = r"""
        <!-- WIKIPEDIA ASIDE BOX WITH LOCAL PORTRAIT ASSET -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Gang Scheduling</h4>

          <div style="display: flex; gap: 14px; align-items: flex-start; margin-bottom: 10px;">
            <div style="flex-shrink: 0; width: 85px; height: 105px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
              <img src="../images/ousterhout.png" alt="John Ousterhout Portrait" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
              Gang scheduling was pioneered by <strong>John Ousterhout</strong> in 1982 to address the coordination failure of independent thread schedulers on parallel hardware. By scheduling related threads across multiple cores simultaneously (a two-dimensional matrix of Cores $\times$ Time Quanta), gang scheduling prevents preemption delays and blocking when cooperating threads communicate.
            </p>
          </div>

          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Gang_scheduling" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Gang Scheduling on Wikipedia</a></li>
          </ul>
        </aside>"""

def update_gang_local_asset():
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
            content = content.replace(target, WIKI_ASIDE_GANG_LOCAL_IMG + "\n\n      " + target, 1)
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
    try:
        subprocess.run(["git", "add"] + modified, check=True)
    except Exception:
        pass

    commit_msg = (
        "Use local images/ousterhout.png asset in Gang Scheduling aside box\n\n"
        "Update 02-multiprocessor-scheduling.html to reference the local repository\n"
        "asset images/ousterhout.png for John Ousterhout's portrait."
    )

    print("--> Committing changes...")
    try:
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Local asset image successfully configured in Gang Scheduling aside!")

if __name__ == "__main__":
    update_gang_local_asset()
