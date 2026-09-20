#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix clipping on the right side of memory hierarchy SVG
# =====================================================================
import os
import re
import subprocess

REFINED_MEMORY_DIAGRAM = """
      <div style="display: flex; justify-content: center; margin: 28px 0; width: 100%; overflow-x: auto;">
        <svg viewBox="0 0 960 430" width="100%" height="auto" style="max-width: 960px; min-width: 650px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrowSpeed" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
              <path d="M0,8 L4,0 L8,8 Z" fill="#0284c7" />
            </marker>
            <marker id="arrowCapacity" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
              <path d="M0,0 L4,8 L8,0 Z" fill="#334155" />
            </marker>
          </defs>

          <!-- Left Axis: Speed & Cost -->
          <line x1="45" y1="390" x2="45" y2="35" stroke="#0284c7" stroke-width="3" marker-end="url(#arrowSpeed)" />
          <text x="35" y="215" fill="#0284c7" font-size="11" font-weight="700" transform="rotate(-90 35 215)" text-anchor="middle">FASTER ACCESS &amp; HIGHER COST / BIT</text>

          <!-- Tier 1: CPU Registers -->
          <g transform="translate(70, 25)">
            <rect x="180" y="0" width="280" height="52" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
            <text x="320" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">CPU Registers</text>
            <text x="320" y="42" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">&lt; 2 KB | &lt; 1 ns</text>

            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Internal registers on CPU core</text>
          </g>

          <!-- Tier 2: Cache Memory -->
          <g transform="translate(70, 97)">
            <rect x="140" y="0" width="320" height="52" rx="6" fill="#0369a1" stroke="#075985" stroke-width="2" />
            <text x="300" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">L1 / L2 / L3 Caches (SRAM)</text>
            <text x="300" y="42" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">64 KB – 64 MB | 1 – 15 ns</text>

            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">On-die static RAM cache</text>
          </g>

          <!-- Tier 3: Main Memory -->
          <g transform="translate(70, 169)">
            <rect x="100" y="0" width="360" height="52" rx="6" fill="#075985" stroke="#0c4a6e" stroke-width="2" />
            <text x="280" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Main Memory (DRAM)</text>
            <text x="280" y="42" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">16 GB – 128 GB | 50 – 100 ns</text>

            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Primary volatile system RAM</text>
          </g>

          <!-- Tier 4: Solid-State Drives -->
          <g transform="translate(70, 241)">
            <rect x="60" y="0" width="400" height="52" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2" />
            <text x="260" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Solid-State Drives (NVMe / SSD)</text>
            <text x="260" y="42" fill="#e2e8f0" font-size="11" font-weight="600" text-anchor="middle">512 GB – 4 TB | 10 – 50 μs</text>

            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Non-volatile NAND flash storage</text>
          </g>

          <!-- Tier 5: Magnetic Disks -->
          <g transform="translate(70, 313)">
            <rect x="20" y="0" width="440" height="52" rx="6" fill="#0f172a" stroke="#1e293b" stroke-width="2" />
            <text x="240" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Magnetic Hard Disks (HDD)</text>
            <text x="240" y="42" fill="#cbd5e1" font-size="11" font-weight="600" text-anchor="middle">1 TB – 20 TB | 5 – 10 ms</text>

            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Secondary rotational storage</text>
          </g>

          <!-- Right Axis: Capacity & Persistence (comfortably inside viewBox at x=895) -->
          <line x1="895" y1="35" x2="895" y2="390" stroke="#334155" stroke-width="3" marker-end="url(#arrowCapacity)" />
          <text x="912" y="215" fill="#334155" font-size="11" font-weight="700" transform="rotate(90 912 215)" text-anchor="middle">LARGER STORAGE CAPACITY &amp; PERSISTENCE</text>
        </svg>
      </div>
"""

def execute_svg_boundary_fix():
    target_file = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<div id="svg-memory-pyramid">.*?</div>\s*</div>'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, f'<div id="svg-memory-pyramid">{REFINED_MEMORY_DIAGRAM}</div>', content, flags=re.DOTALL)
        print("--> Replaced #svg-memory-pyramid with widened boundary diagram.")
    else:
        pattern_fallback = r'<div style="display: flex; justify-content: center; margin: 28px 0;">\s*<svg viewBox="0 0 820 440".*?</svg>\s*</div>'
        content = re.sub(pattern_fallback, REFINED_MEMORY_DIAGRAM, content, flags=re.DOTALL)
        print("--> Replaced fallback SVG with widened boundary diagram.")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", target_file], check=True)
        commit_msg = (
            "Fix right-hand clipping on memory hierarchy SVG in Module 2\n\n"
            "Expand SVG viewBox width to 960 and adjust element coordinates in\n"
            "week01-operating-system-concepts/02-hardware-review.html to prevent axis cutoff."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_svg_boundary_fix()
