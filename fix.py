#!/usr/bin/env python3
# =====================================================================
# add_gen4_images.py: Add Macintosh and Windows 95 cards to Generation 4
# =====================================================================
import os
import subprocess

def execute_image_addition():
    file_path = os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    target_marker = "</ul>"
    pos = content.find(target_marker)
    if pos != -1:
        insert_pos = pos + len(target_marker)

        image_grid_block = """
      <div class="image-grid" style="margin-top: 16px;">
        <div class="image-card">
          <img src="../images/macintosh-128k.png" alt="Macintosh 128k">
          <span>
            <strong>Macintosh 128k</strong><br>
            Early personal computer with graphical desktop interface.<br>
            <small><a href="https://en.wikipedia.org/wiki/Macintosh_128k" target="_blank" rel="noopener">Wikipedia: Macintosh 128k</a></small><br>
            <small><a href="https://commons.wikimedia.org/w/index.php?title=File:Macintosh_128k_transparency.png&oldid=1086425807" target="_blank" rel="noopener">Wikimedia Commons File Record</a></small><br>
            <small>Author: Wikimedia Commons contributors</small>
          </span>
        </div>
        <div class="image-card">
          <img src="../images/windows-95-first-run.png" alt="Windows 95 First Run">
          <span>
            <strong>Windows 95</strong><br>
            Desktop operating system environment.<br>
            <small><a href="https://en.wikipedia.org/wiki/File:Windows_95_at_first_run.png" target="_blank" rel="noopener">Wikipedia File: Windows 95 at first run</a></small><br>
            <small>Source: Wikipedia contributors</small>
          </span>
        </div>
      </div>"""

        content = content[:insert_pos] + image_grid_block + content[insert_pos:]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("--> Generation 4 image cards successfully added.")

    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add Macintosh 128k and Windows 95 image cards to Generation 4 in Module 1"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git note: {e}")

if __name__ == "__main__":
    execute_image_addition()
