#!/usr/bin/env python3
# =====================================================================
# fix_video_sizing_and_player.py: Responsive thumbnail & error fix
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_SMP_RESPONSIVE_CARD = r"""
        <!-- WIKIPEDIA ASIDE BOX WITH RESPONSIVE VIDEO THUMBNAIL CARD -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Symmetric Multiprocessing (SMP)</h4>
          <p style="margin-bottom: 10px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
            Symmetric Multiprocessing (SMP) evolved from early mainframe architectures such as the Burroughs D825 (1962) into commercial open-systems hardware pioneered by Sequent Computer Systems in the 1980s. Unlike asynchronous master-slave models where one CPU monopolizes kernel execution, SMP allows any processor to execute kernel code, service hardware interrupts, and schedule threads concurrently across a unified shared physical memory space.
          </p>

          <!-- Compact Responsive Video Preview Card -->
          <div style="display: flex; align-items: center; gap: 14px; background: #ffffff; border: 1px solid #bae6fd; border-radius: 6px; padding: 10px 14px; margin: 12px 0; max-width: 540px;">
            <div style="flex-shrink: 0; position: relative; width: 110px; height: 65px; background: #0f172a; border-radius: 4px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
              <img src="https://img.youtube.com/vi/9wQEgm3FNxo/hqdefault.jpg" alt="Burroughs D825 Video Thumbnail" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.85;">
              <div style="position: absolute; width: 28px; height: 28px; background: rgba(2, 132, 199, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #ffffff; font-size: 12px; font-weight: bold;">&#9658;</div>
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 3px;">
              <div style="font-weight: 600; font-size: 0.88rem; color: #0f172a;">1964 Burroughs Computers &amp; D825 Multiprocessing</div>
              <div style="font-size: 0.78rem; color: #64748b;">Computer History Archives Project (CHAP) &bull; 21 mins</div>
              <a href="https://www.youtube.com/watch?v=9wQEgm3FNxo" target="_blank" rel="noopener" style="font-size: 0.82rem; color: #0284c7; text-decoration: underline; font-weight: 500;">Watch Documentary on YouTube &rarr;</a>
            </div>
          </div>

          <ul style="margin-left: 20px; margin-top: 10px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Symmetric_multiprocessing" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Symmetric Multiprocessing on Wikipedia</a></li>
          </ul>
        </aside>"""

def update_responsive_card():
    mod1 = os.path.join("week11-multiprocessors", "01-multiprocessor-hardware.html")
    modified = []

    if os.path.exists(mod1):
        with open(mod1, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove existing SMP aside if present
        if "Historical Summary &amp; Further Reading: Symmetric Multiprocessing (SMP)" in content:
            parts = content.split("<!-- WIKIPEDIA ASIDE BOX")
            content = parts[0] + parts[1].split("</aside>", 1)[1]

        target = "<!-- GUIDED WALKTHROUGH 4: OS ARCHITECTURES -->"
        if target in content:
            content = content.replace(target, WIKI_ASIDE_SMP_RESPONSIVE_CARD + "\n\n      " + target)
            with open(mod1, "w", encoding="utf-8") as f:
                f.write(content)
            modified.append(mod1)

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
        "Replace oversized YouTube iframe with responsive thumbnail card in SMP aside\n\n"
        "Fix video player configuration errors and reduce component sizing in the\n"
        "Symmetric Multiprocessing (SMP) research aside box across Week 11 modules."
    )

    print("--> Committing changes...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("--> Pushing changes to origin main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> Responsive video card deployed successfully!")

if __name__ == "__main__":
    update_responsive_card()
