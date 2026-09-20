#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix pyramid diagram contrast in Module 2 and sync
# =====================================================================
import os
import re
import subprocess

SVG_MEMORY_PYRAMID_CONTRAST = """
      <div style="display: flex; justify-content: center; margin: 24px 0;">
        <svg viewBox="0 0 760 390" width="100%" height="auto" style="max-width: 760px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="gradReg" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#0369a1" />
              <stop offset="100%" stop-color="#0284c7" />
            </linearGradient>
            <linearGradient id="gradCache" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#075985" />
              <stop offset="100%" stop-color="#0369a1" />
            </linearGradient>
            <linearGradient id="gradRAM" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#0c4a6e" />
              <stop offset="100%" stop-color="#075985" />
            </linearGradient>
            <linearGradient id="gradSSD" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#1e293b" />
              <stop offset="100%" stop-color="#334155" />
            </linearGradient>
            <linearGradient id="gradDisk" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#0f172a" />
              <stop offset="100%" stop-color="#1e293b" />
            </linearGradient>
            <marker id="arrowUp" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
              <path d="M0,6 L3,0 L6,6 Z" fill="#0284c7" />
            </marker>
            <marker id="arrowDown" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
              <path d="M0,0 L3,6 L6,0 Z" fill="#475569" />
            </marker>
          </defs>

          <!-- Pyramid Tiers with dark, deep gradients ensuring crisp white text contrast -->
          <!-- Tier 1: Registers -->
          <polygon points="380,25 330,85 430,85" fill="url(#gradReg)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="68" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Registers (&lt; 2 KB, &lt; 1 ns)</text>

          <!-- Tier 2: Cache Memory -->
          <polygon points="330,85 270,155 490,155 430,85" fill="url(#gradCache)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="128" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">L1 / L2 / L3 Caches (SRAM, 1–15 ns)</text>

          <!-- Tier 3: Main Memory -->
          <polygon points="270,155 200,230 560,230 490,155" fill="url(#gradRAM)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="200" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Main Memory (DRAM, 16–128 GB, 50–100 ns)</text>

          <!-- Tier 4: SSDs -->
          <polygon points="200,230 130,305 630,305 560,230" fill="url(#gradSSD)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="275" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Solid-State Drives (NVMe / Flash, 10–50 μs)</text>

          <!-- Tier 5: Magnetic Disks -->
          <polygon points="130,305 60,375 700,375 630,305" fill="url(#gradDisk)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="348" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Magnetic Disks / Archival (HDDs, 5–10 ms)</text>

          <!-- Left Indicator: Access Speed & Cost -->
          <line x1="45" y1="365" x2="45" y2="40" stroke="#0284c7" stroke-width="3" marker-end="url(#arrowUp)" />
          <text x="38" y="205" fill="#0284c7" font-size="11" font-weight="700" transform="rotate(-90 38 205)" text-anchor="middle">HIGHER ACCESS SPEED &amp; COST / BIT</text>

          <!-- Right Indicator: Capacity & Persistence -->
          <line x1="715" y1="40" x2="715" y2="365" stroke="#475569" stroke-width="3" marker-end="url(#arrowDown)" />
          <text x="723" y="205" fill="#475569" font-size="11" font-weight="700" transform="rotate(90 723 205)" text-anchor="middle">LARGER CAPACITY &amp; PERSISTENCE</text>
        </svg>
      </div>
"""

def update_pyramid_contrast():
    target_file = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace existing pyramid block inside #svg-memory-pyramid or regex match
    if '<div id="svg-memory-pyramid">' in content:
        pattern = r'<div id="svg-memory-pyramid">.*?</div>\s*</div>'
        replacement = f'<div id="svg-memory-pyramid">{SVG_MEMORY_PYRAMID_CONTRAST}</div>'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("--> Updated #svg-memory-pyramid with high-contrast palette.")
    else:
        # If the container id was omitted earlier, replace the raw SVG
        pattern = r'<div style="display: flex; justify-content: center; margin: 24px 0;">\s*<svg viewBox="0 0 760 380".*?</svg>\s*</div>'
        content = re.sub(pattern, SVG_MEMORY_PYRAMID_CONTRAST, content, flags=re.DOTALL)
        print("--> Replaced memory pyramid SVG with high-contrast palette.")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Git sync
    try:
        subprocess.run(["git", "add", "fix.py", target_file], check=True)
        commit_msg = (
            "Fix text contrast on memory hierarchy pyramid diagram in Module 2\n\n"
            "Update SVG text fills and gradient stops in week01-operating-system-concepts/02-hardware-review.html\n"
            "to prevent white text rendering against light slice backgrounds."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_pyramid_contrast()
