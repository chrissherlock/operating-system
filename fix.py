#!/usr/bin/env python3
# =====================================================================
# fix.py: Add visual retirement indicators to pipeline SVG
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def add_retirement_visuals():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update renderPipeState in 02-hardware-review.html to apply emerald styling to WB when retiring
    old_render_highlight = """            // Highlight active stages with vivid orange pop
            data.activeStages.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                const rect = el.querySelector("rect");
                if (rect) {
                  rect.setAttribute("stroke", "#ea580c");
                  rect.setAttribute("stroke-width", "2.5");
                  rect.setAttribute("fill", "#fff7ed");
                  rect.style.filter = "drop-shadow(0 0 5px rgba(234, 88, 12, 0.35))";
                }
              }
            });"""

    new_render_highlight = """            // Highlight active stages: Orange for compute/fetch/decode, Emerald Green for Writeback/Retire
            data.activeStages.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                const rect = el.querySelector("rect");
                if (rect) {
                  if (id === "pipe-node-wb" && data.retired !== "0 / 4") {
                    // Visually pop retired stage in vibrant emerald green
                    rect.setAttribute("stroke", "#059669");
                    rect.setAttribute("stroke-width", "3");
                    rect.setAttribute("fill", "#ecfdf5");
                    rect.style.filter = "drop-shadow(0 0 6px rgba(5, 150, 105, 0.4))";
                  } else {
                    rect.setAttribute("stroke", "#ea580c");
                    rect.setAttribute("stroke-width", "2.5");
                    rect.setAttribute("fill", "#fff7ed");
                    rect.style.filter = "drop-shadow(0 0 5px rgba(234, 88, 12, 0.35))";
                  }
                }
              }
            });"""

    content = content.replace(old_render_highlight, new_render_highlight)

    # 2. Add an explicit visual badge inside the Stage 4 Writeback container in SVG
    # Change Stage 4 label to show "(WB &bull; RETIRE)"
    content = content.replace(
        '<text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Stage 4: WRITEBACK (WB)</text>',
        '<text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Stage 4: WRITEBACK / RETIRE</text>'
    )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Added retirement stage visual indicators in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add emerald retirement indicators to instruction throughput SVG\n\n"
            "Visually differentiate in-flight active stages (orange) from retired\n"
            "commit events (emerald green) in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_retirement_visuals()
