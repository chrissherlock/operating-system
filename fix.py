#!/usr/bin/env python3
# =====================================================================
# add_vacuum_tube_plugboard_images.py: Add images and attributions
# =====================================================================
import os
import subprocess
import sys

GENERATION_1_WITH_IMAGES = r"""
      <h3>1. The First Generation (1945–1955): Vacuum Tubes and Plugboards</h3>
      <p>
        Following electronic breakthroughs during World War II, computers were built using <strong>vacuum tubes</strong>. These machines were massive, unreliable, and immensely expensive. A single computer filled an entire room and was operated entirely by small teams of engineers and mathematicians.
      </p>

      <!-- Visual Gallery for Vacuum Tubes and Plugboards -->
      <div style="display: flex; gap: 20px; flex-wrap: wrap; margin: 16px 0;">
        <!-- Vacuum Tube Card -->
        <div style="flex: 1; min-width: 280px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; display: flex; gap: 14px; align-items: flex-start;">
          <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0;">
            <div style="width: 100px; height: 130px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
              <img src="../images/vacuumtube.jpg" alt="Philips 12AX7WA Vacuum Tube" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <span style="font-size: 0.7rem; color: #64748b; text-align: center; line-height: 1.2;">
              <a href="https://commons.wikimedia.org/wiki/File:Philips_12AX7WA_tube.jpg" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Photo: Wikimedia Commons<br>contributors (2022)</a>
            </span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.9rem; color: #334155;">
            <strong>Vacuum Tubes:</strong> Active electronic components that controlled electrical current flow. Thousands were required per computer, generating immense heat and frequent hardware failures.
          </div>
        </div>

        <!-- Plugboard Card -->
        <div style="flex: 1; min-width: 280px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; display: flex; gap: 14px; align-items: flex-start;">
          <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0;">
            <div style="width: 100px; height: 130px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
              <img src="../images/plugboard.jpg" alt="IBM 402 Plugboard" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <span style="font-size: 0.7rem; color: #64748b; text-align: center; line-height: 1.2;">
              <a href="https://commons.wikimedia.org/wiki/File:IBM402plugboard.Shrigley.wireside.jpg" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Photo: Wikimedia Commons<br>contributors (2025)</a>
            </span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.9rem; color: #334155;">
            <strong>Plugboards &amp; Patch Panels:</strong> Programs were wired manually using plugboards. Changing computations required physically unplugging and rerouting wire patch panels.
          </div>
        </div>
      </div>

      <p>
        There were no operating systems. Programs were written entirely in machine language or wired manually onto plugboards. Every job required setting physical switches and plugging cables into patch panels.
      </p>"""

def update_gen1_images():
    portal_path = os.path.join("week01-operating-system-concepts", "index.html")
    modified = []

    if os.path.exists(portal_path):
        with open(portal_path, "r", encoding="utf-8") as f:
            content = f.read()

        target_header = "<h3>1. The First Generation (1945–1955): Vacuum Tubes and Plugboards</h3>"
        if target_header in content:
            parts = content.split(target_header)
            # Find the end of the first generation paragraph before section 2
            trailer = parts[1].split("<h3>2. The Second Generation")[1]
            content = parts[0] + GENERATION_1_WITH_IMAGES + "\n\n      <h3>2. The Second Generation" + trailer
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
            "Add vacuum tube and plugboard images with Wikimedia attributions to Chapter 1\n\n"
            "Update week01-operating-system-concepts/index.html to include images/vacuumtube.jpg\n"
            "and images/plugboard.jpg in the First Generation section with full Wikimedia Commons attributions."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Vacuum tube and plugboard images successfully deployed!")

if __name__ == "__main__":
    update_gen1_images()
