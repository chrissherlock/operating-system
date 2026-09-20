#!/usr/bin/env python3
# =====================================================================
# update_gen3_images.py: Insert Generation 3 images into Module 1 page
# =====================================================================
import os
import subprocess
import sys

def execute_image_addition():
    base_dir = "week01-operating-system-concepts"
    file_path = os.path.join(base_dir, "01-what-is-an-os-and-history.html")

    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The target text block for Generation 3
    target_text = """      <h3>Generation 3: ICs, Multiprogramming, &amp; Time-Sharing (1965–1980)</h3>
      <p>
        Integrated circuits (ICs) revolutionized computer architecture. The IBM System/360 introduced hardware architecture families capable of running both commercial and scientific workloads. To eliminate CPU idle time during slow I/O operations, <strong>multiprogramming</strong> was developed, alongside <strong>time-sharing</strong> systems enabling multiple interactive users.
      </p>"""

    # The new section including the image grid with attributions and captions
    replacement_text = """      <h3>Generation 3: ICs, Multiprogramming, &amp; Time-Sharing (1965–1980)</h3>
      <p>
        Integrated circuits (ICs) revolutionized computer architecture. The IBM System/360 introduced hardware architecture families capable of running both commercial and scientific workloads. To eliminate CPU idle time during slow I/O operations, <strong>multiprogramming</strong> was developed, alongside <strong>time-sharing</strong> systems enabling multiple interactive users.
      </p>
      <div class="image-grid">
        <div class="image-card">
          <img src="../images/integrated-circuit.jpeg" alt="Integrated Circuit">
          <span>Integrated Circuit Microchip<br><small>Wikimedia Commons contributors, CC BY-SA 3.0</small></span>
        </div>
        <div class="image-card">
          <img src="../images/system360.jpg" alt="IBM System/360">
          <span>IBM System/360 Mainframe at VW-Werk Wolfsburg (1973)<br><small>Bundesarchiv, B 145 Bild-F038812-0014 / Schaack, Lothar / CC-BY-SA 3.0</small></span>
        </div>
      </div>"""

    if target_text in content:
        new_content = content.replace(target_text, replacement_text)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Successfully added Generation 3 images to {file_path}")
    else:
        print("--> Target text for Generation 3 not found in file.")

    modified = [file_path]
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Add Generation 3 integrated circuit and IBM System/360 images with captions\n\n"
            "Update week01-operating-system-concepts/01-what-is-an-os-and-history.html to include\n"
            "the image-grid section for Generation 3 with Wikimedia Commons and Bundesarchiv attributions."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Generation 3 image integration successfully deployed!")

if __name__ == "__main__":
    execute_image_addition()
