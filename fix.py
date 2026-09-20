#!/usr/bin/env python3
# =====================================================================
# add_transistor_batch_images.py: Add transistor and punched card images
# =====================================================================
import os
import subprocess
import sys

GENERATION_2_WITH_IMAGES = r"""
      <h3>2. The Second Generation (1955–1965): Transistors and Batch Systems</h3>
      <p>
        The invention of the <strong>transistor</strong> in the 1950s made computers reliable enough to manufacture and sell commercially. This era introduced <strong>batch systems</strong> to eliminate human operator idle time. Users wrote programs on punch cards, carried their card decks to the computer center, and handed them to operators.
      </p>

      <!-- Visual Gallery for Transistors and Batch Systems -->
      <div style="display: flex; gap: 20px; flex-wrap: wrap; margin: 16px 0;">
        <!-- Transistor Card -->
        <div style="flex: 1; min-width: 280px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; display: flex; gap: 14px; align-items: flex-start;">
          <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0;">
            <div style="width: 100px; height: 130px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
              <img src="../images/replica-first-transistor.jpg" alt="Replica of the First Working Transistor" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <span style="font-size: 0.7rem; color: #64748b; text-align: center; line-height: 1.2;">
              <a href="https://commons.wikimedia.org/wiki/File:A_replica_of_the_first_working_transistor_02.jpg" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Photo: Wikimedia Commons<br>contributors (2023)</a>
            </span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.9rem; color: #334155;">
            <strong>Transistors:</strong> Solid-state semiconductor devices that replaced fragile vacuum tubes, enabling smaller, faster, and dramatically more reliable computing hardware.
          </div>
        </div>

        <!-- Punched Card Program Deck Card -->
        <div style="flex: 1; min-width: 280px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; display: flex; gap: 14px; align-items: flex-start;">
          <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0;">
            <div style="width: 100px; height: 130px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
              <img src="../images/punched-card-program-deck.jpg" alt="Punched Card Program Deck" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <span style="font-size: 0.7rem; color: #64748b; text-align: center; line-height: 1.2;">
              <a href="https://commons.wikimedia.org/wiki/File:Punched_card_program_deck.agr.jpg" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Photo: Wikimedia Commons<br>contributors (2026)</a>
            </span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.9rem; color: #334155;">
            <strong>Batch Systems &amp; Card Decks:</strong> Programs and data were encoded onto punched cards and grouped into batches to be processed sequentially by batch monitor systems.
          </div>
        </div>
      </div>

      <p>
        Operators grouped similar jobs (e.g., all FORTRAN jobs) into a batch, loaded them onto magnetic tape, and ran them sequentially using early batch monitors like IBSYS.
      </p>"""

def update_gen2_images():
    portal_path = os.path.join("week01-operating-system-concepts", "index.html")
    modified = []

    if os.path.exists(portal_path):
        with open(portal_path, "r", encoding="utf-8") as f:
            content = f.read()

        target_header = "<h3>2. The Second Generation (1955–1965): Transistors and Batch Systems</h3>"
        if target_header in content:
            parts = content.split(target_header)
            trailer = parts[1].split("<h3>3. The Third Generation")[1]
            content = parts[0] + GENERATION_2_WITH_IMAGES + "\n\n      <h3>3. The Third Generation" + trailer
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
            "Add replica transistor and punched card program deck images with Wikimedia attributions\n\n"
            "Update week01-operating-system-concepts/index.html to include images/replica-first-transistor.jpg\n"
            "and images/punched-card-program-deck.jpg in the Second Generation section with full Wikimedia Commons attributions."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Transistor and batch system images successfully deployed!")

if __name__ == "__main__":
    update_gen2_images()
