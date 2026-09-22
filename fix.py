#!/usr/bin/env python3
# =====================================================================
# fix.py: Add Butler Lampson image card to Systems Engineering aside
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

REBUILT_LAMPSON_ASIDE = """      <!-- Historical Aside: Butler Lampson & John Ousterhout -->
      <div class="aside-box" style="border-left-color: #d97706; background: #fffbeb; margin: 20px 0;">
        <strong style="color: #b45309; font-size: 1rem;">Systems Engineering: Lampson's Laws &amp; Ousterhout's Law</strong>

        <div style="display: flex; gap: 16px; align-items: flex-start; margin-top: 10px; flex-wrap: wrap;">
          <!-- Left: Compact Image Card -->
          <div class="image-card" style="max-width: 170px; width: 100%; flex-shrink: 0; margin: 0; background: #ffffff;">
            <img src="../images/butler-lampson.jpg" alt="Butler Lampson, Royal Society" style="height: 110px; width: 100%; object-fit: cover;">
            <span>
              <strong>Butler Lampson</strong><br>
              <small><a href="https://commons.wikimedia.org/w/index.php?title=File:Butler_Lampson_Royal_Society_(cropped).jpg&oldid=1102221289" target="_blank" rel="noopener">Wikimedia Record</a></small><br>
              <small>Author: Wikimedia Commons</small>
            </span>
          </div>

          <!-- Right: Text Content -->
          <div style="flex: 1; min-width: 260px;">
            <p style="margin: 0; color: #334155; line-height: 1.55;">
              Turing Award winner Butler Lampson emphasized a core rule of operating system design: <strong>separation of policy from mechanism</strong>. The hardware provides mechanisms (like MMU page walks or timer traps), while the OS establishes policies (like scheduling algorithms or eviction rules). Mixing them leads to brittle architectures.
            </p>
          </div>
        </div>

        <div style="margin-top: 12px; background: #ffffff; border: 1px solid #fde68a; border-left: 3px solid #d97706; padding: 10px 14px; border-radius: 0 4px 4px 0; font-size: 0.85rem;">
          <strong style="color: #b45309;">John Ousterhout &amp; The Memory Latency Wall</strong>
          <p style="margin: 4px 0 0 0; color: #475569; line-height: 1.5;">
            In his landmark 1990 paper, John Ousterhout observed that while CPU clock speeds were scaling exponentially, memory and storage bus latency lagged severely behind. This reality explains why hardware architectural breakthroughs like Translation Lookaside Buffers (TLBs), DMA controllers, and superpages are vital to preventing CPU starvation.
          </p>
        </div>
      </div>"""

def update_lampson_aside_markup():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- Historical Aside: Butler Lampson & John Ousterhout -->"
    next_section_marker = "<h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>"

    if start_marker not in content or next_section_marker not in content:
        print("Error: Could not locate Lampson aside boundaries in Module 2.")
        return

    parts = content.split(start_marker, 1)
    remainder = parts[1].split(next_section_marker, 1)

    updated_content = f"{parts[0]}{REBUILT_LAMPSON_ASIDE}\n\n    {next_section_marker}{remainder[1]}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully added Butler Lampson image card to {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add Butler Lampson image card and attribution to systems aside\n\n"
            "Embed images/butler-lampson.jpg into the Systems Engineering aside in\n"
            "02-hardware-review.html with clean flexbox layout and complete metadata."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_lampson_aside_markup()
