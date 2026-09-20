#!/usr/bin/env python3
# =====================================================================
# fix_tanenbaum_filename.py: Correct image filename to tanenbaum.png
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_TANENBAUM_CORRECT = r"""
        <!-- WIKIPEDIA ASIDE BOX WITH CORRECT FILENAME -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Operating System Foundations</h4>

          <div style="display: flex; gap: 16px; align-items: flex-start; margin-bottom: 12px;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0;">
              <div style="width: 120px; height: 150px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
                <img src="../images/tanenbaum.png" alt="Andrew S. Tanenbaum Portrait" style="width: 100%; height: 100%; object-fit: cover;">
              </div>
              <span style="font-size: 0.72rem; color: #64748b; text-align: center; line-height: 1.2;">Photo by Andrew S. Tanenbaum</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px; flex-grow: 1;">
              <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                The concept of the operating system as both an <strong>extended machine</strong> and a <strong>resource manager</strong> was formalized in foundational computer science literature by authors such as <a href="https://en.wikipedia.org/wiki/Andrew_S._Tanenbaum" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline; font-weight: 600;">Andrew S. Tanenbaum</a>. By hiding hardware intricacies and arbitrating resource contention, the OS provides a stable, secure foundation for all user applications.
              </p>
              <div>
                <a href="https://en.wikipedia.org/wiki/Operating_system" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline; font-weight: 500; font-size: 0.88rem;">Read more on Wikipedia: Operating System &rarr;</a>
              </div>
            </div>
          </div>
        </aside>"""

def fix_tanenbaum_asset_filename():
    portal_path = os.path.join("week01-operating-system-concepts", "index.html")
    modified = []

    if os.path.exists(portal_path):
        with open(portal_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "Historical Summary &amp; Further Reading: Operating System Foundations" in content:
            parts = content.split("<!-- WIKIPEDIA ASIDE BOX WITH TANENBAUM PORTRAIT -->")
            if len(parts) > 1:
                content = parts[0] + parts[1].split("</aside>", 1)[1]
            else:
                parts = content.split("<!-- WIKIPEDIA ASIDE BOX")
                content = parts[0] + parts[1].split("</aside>", 1)[1]

        target = "<!-- SECTION 1.2: HISTORY OF OPERATING SYSTEMS -->"
        if target in content:
            content = content.replace(target, WIKI_ASIDE_TANENBAUM_CORRECT + "\n\n    " + target, 1)
            with open(portal_path, "w", encoding="utf-8") as f:
                f.write(content)
            modified.append(portal_path)

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
            "Correct image filename reference from tanenbaum.jpeg to tanenbaum.png\n\n"
            "Update week01-operating-system-concepts/index.html to reference the correct\n"
            "asset filename images/tanenbaum.png in the Andrew S. Tanenbaum research aside box."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Tanenbaum filename correction successfully deployed!")

if __name__ == "__main__":
    fix_tanenbaum_asset_filename()
