#!/usr/bin/env python3
# =====================================================================
# embed_youtube_in_aside.py: Embed YouTube video into SMP aside box
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_SMP_WITH_VIDEO = r"""
        <!-- WIKIPEDIA ASIDE BOX WITH EMBEDDED VIDEO -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Symmetric Multiprocessing (SMP)</h4>
          <p style="margin-bottom: 8px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
            Symmetric Multiprocessing (SMP) evolved from early mainframe architectures such as the Burroughs D825 (1962) into commercial open-systems hardware pioneered by Sequent Computer Systems in the 1980s. Unlike asynchronous master-slave models where one CPU monopolizes kernel execution, SMP allows any processor to execute kernel code, service hardware interrupts, and schedule threads concurrently across a unified shared physical memory space.
          </p>

          <!-- Embedded YouTube Video Container -->
          <div style="margin: 14px 0; position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 6px; border: 1px solid #bae6fd;">
            <iframe src="https://www.youtube.com/embed/9wQEgm3FNxo" title="1964 Burroughs Computers Computer History (B5000, B280, BUIC D825)" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
          </div>
          <div style="font-size: 0.85rem; color: #475569; margin-bottom: 8px;">
            Watch on YouTube: <a href="https://www.youtube.com/watch?v=9wQEgm3FNxo" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">1964 Burroughs D825 Multiprocessing Documentary</a>
          </div>

          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Symmetric_multiprocessing" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Symmetric Multiprocessing on Wikipedia</a></li>
          </ul>
        </aside>"""

def update_video_embedding():
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
            content = content.replace(target, WIKI_ASIDE_SMP_WITH_VIDEO + "\n\n      " + target)
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
        "Embed Burroughs D825 historical computer history video into SMP aside box\n\n"
        "Update 01-multiprocessor-hardware.html to embed YouTube video 9wQEgm3FNxo\n"
        "directly within the Symmetric Multiprocessing (SMP) research aside box."
    )

    print("--> Committing changes...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("--> Pushing changes to origin main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> YouTube video embedding deployed successfully!")

if __name__ == "__main__":
    update_video_embedding()
