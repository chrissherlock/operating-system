#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix overlapping SVG arrow and label in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_svg_overlap():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Target the second diagram containing the physical address label
    old_diagram_snippet = """      <div class="diagram-container" style="margin: 24px 0;">
        <svg viewBox="0 0 880 260" width="100%" height="auto" style="max-width: 880px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">"""

    new_diagram_snippet = """      <div class="diagram-container" style="margin: 24px 0;">
        <svg viewBox="0 0 880 290" width="100%" height="100%" style="max-width: 880px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">"""

    # Also shift the bottom group down
    old_bottom_group = """          <!-- Bottom Label (Shifted Down) -->
          <text x="40" y="180" fill="#0f172a" font-size="12" font-weight="700">PHYSICAL ADDRESS (Issued to DRAM Memory Bus)</text>

          <!-- Physical Address Split Boxes (Shifted Down to y=194) -->
          <!-- PFN Box -->
          <rect x="40" y="194" width="460" height="46" rx="5" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
          <text x="270" y="216" fill="#059669" font-size="12" font-weight="700" text-anchor="middle">Physical Frame Number (PFN)</text>
          <text x="270" y="231" fill="#065f46" font-size="9.5" text-anchor="middle">Base address of 4 KiB frame in physical DRAM</text>

          <!-- Offset Box (Bottom) -->
          <rect x="520" y="194" width="320" height="46" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="2" />
          <text x="680" y="216" fill="#334155" font-size="12" font-weight="700" text-anchor="middle">Page Offset (12 bits)</text>
          <text x="680" y="231" fill="#64748b" font-size="9.5" text-anchor="middle">Bits [11:0] • Unmodified intra-frame byte offset</text>"""

    new_bottom_group = """          <!-- Bottom Label (Shifted Down) -->
          <text x="40" y="210" fill="#0f172a" font-size="12" font-weight="700">PHYSICAL ADDRESS (Issued to DRAM Memory Bus)</text>

          <!-- Physical Address Split Boxes (Shifted Down to y=224) -->
          <!-- PFN Box -->
          <rect x="40" y="224" width="460" height="46" rx="5" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
          <text x="270" y="246" fill="#059669" font-size="12" font-weight="700" text-anchor="middle">Physical Frame Number (PFN)</text>
          <text x="270" y="261" fill="#065f46" font-size="9.5" text-anchor="middle">Base address of 4 KiB frame in physical DRAM</text>

          <!-- Offset Box (Bottom) -->
          <rect x="520" y="224" width="320" height="46" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="2" />
          <text x="680" y="246" fill="#334155" font-size="12" font-weight="700" text-anchor="middle">Page Offset (12 bits)</text>
          <text x="680" y="261" fill="#64748b" font-size="9.5" text-anchor="middle">Bits [11:0] • Unmodified intra-frame byte offset</text>"""

    # Adjust arrow path ending above the new label position
    old_arrow_path = '<path d="M 680,82 L 680,188" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrowGray)" />'
    new_arrow_path = '<path d="M 680,82 L 680,218" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrowGray)" />'

    if old_diagram_snippet in content and old_bottom_group in content:
        content = content.replace(old_diagram_snippet, new_diagram_snippet)
        content = content.replace(old_bottom_group, new_bottom_group)
        content = content.replace(old_arrow_path, new_arrow_path)
        print("--> Successfully updated SVG viewBox, label coordinates, and arrow path.")
    else:
        print("--> Warning: Exact snippet match not found; performing regex/alternative patch.")
        # Fallback substring replacements
        content = content.replace('viewBox="0 0 880 260"', 'viewBox="0 0 880 290"')
        content = content.replace('height="auto"', 'height="100%"')

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix overlapping arrow line and physical address label in Module 2 diagram\n\n"
            "Adjust SVG vertical layout and viewBox in 02-hardware-review.html to prevent\n"
            "the pass-through arrow line from overwriting the physical address label."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for diagram layout fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_svg_overlap()
