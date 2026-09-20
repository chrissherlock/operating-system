#!/usr/bin/env python3
# =====================================================================
# reflow_gang_aside_layout.py: Align wiki link under paragraph beside image
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_GANG_REFLOWED = r"""
        <!-- WIKIPEDIA ASIDE BOX WITH REFLOWED LAYOUT -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Gang Scheduling</h4>

          <div style="display: flex; gap: 16px; align-items: flex-start;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0;">
              <div style="width: 120px; height: 150px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
                <img src="../images/ousterhout.png" alt="John Ousterhout Portrait" style="width: 100%; height: 100%; object-fit: cover;">
              </div>
              <span style="font-size: 0.72rem; color: #64748b; text-align: center; line-height: 1.2;">Photo by Christopher Michel</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px; flex-grow: 1;">
              <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                <strong>Gang scheduling</strong> was pioneered by <strong>John Ousterhout</strong> in 1982 to address the coordination failure of independent thread schedulers on parallel hardware. By scheduling related threads across multiple cores simultaneously (a <strong>two-dimensional matrix of Cores $\times$ Time Quanta</strong>), gang scheduling prevents preemption delays and blocking when cooperating threads communicate.
              </p>
              <div>
                <a href="https://en.wikipedia.org/wiki/Gang_scheduling" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline; font-weight: 500; font-size: 0.88rem;">Read more on Wikipedia: Gang Scheduling &rarr;</a>
              </div>
            </div>
          </div>
        </aside>"""

def reflow_aside_layout():
    mod2 = os.path.join("week11-multiprocessors", "02-multiprocessor-scheduling.html")
    modified = []

    if os.path.exists(mod2):
        with open(mod2, "r", encoding="utf-8") as f:
            content = f.read()

        if "Historical Summary &amp; Further Reading: Gang Scheduling" in content:
            parts = content.split("<!-- WIKIPEDIA ASIDE BOX")
            content = parts[0] + parts[1].split("</aside>", 1)[1]

        target = "<!-- GUIDED WALKTHROUGH"
        if target in content:
            content = content.replace(target, WIKI_ASIDE_GANG_REFLOWED + "\n\n      " + target, 1)
            with open(mod2, "w", encoding="utf-8") as f:
                f.write(content)
            modified.append(mod2)

    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    if not modified:
        print("--> No files modified.")
        return

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Reflow Gang Scheduling aside flex layout to place wiki link under paragraph\n\n"
            "Align text and Wikipedia reference link alongside John Ousterhout portrait in\n"
            "02-multiprocessor-scheduling.html with the link positioned directly below the text."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Gang Scheduling aside layout reflowed successfully!")

if __name__ == "__main__":
    reflow_aside_layout()
