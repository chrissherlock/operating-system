#!/usr/bin/env python3
# =====================================================================
# fix.py: Redesign memory hierarchy diagram with clear text contrast
# =====================================================================
import os
import re
import subprocess

REFINED_MEMORY_DIAGRAM = """
      <div style="display: flex; justify-content: center; margin: 28px 0;">
        <svg viewBox="0 0 820 440" width="100%" height="auto" style="max-width: 820px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrowSpeed" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
              <path d="M0,8 L4,0 L8,8 Z" fill="#0284c7" />
            </marker>
            <marker id="arrowCapacity" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
              <path d="M0,0 L4,8 L8,0 Z" fill="#334155" />
            </marker>
          </defs>

          <!-- Left Axis: Speed & Cost -->
          <line x1="50" y1="400" x2="50" y2="40" stroke="#0284c7" stroke-width="3" marker-end="url(#arrowSpeed)" />
          <text x="40" y="220" fill="#0284c7" font-size="12" font-weight="700" transform="rotate(-90 40 220)" text-anchor="middle">FASTER ACCESS &amp; HIGHER COST / BIT</text>

          <!-- Tier 1: CPU Registers -->
          <g transform="translate(100, 30)">
            <rect x="180" y="0" width="200" height="54" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
            <text x="280" y="26" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">CPU Registers</text>
            <text x="280" y="44" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">&lt; 2 KB | &lt; 1 ns</text>

            <line x1="390" y1="27" x2="430" y2="27" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="440" y="8" width="240" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
            <text x="450" y="32" fill="#0f172a" font-size="11" font-weight="600">Registers on CPU core die</text>
          </g>

          <!-- Tier 2: Cache Memory -->
          <g transform="translate(100, 105)">
            <rect x="140" y="0" width="280" height="54" rx="6" fill="#0369a1" stroke="#075985" stroke-width="2" />
            <text x="280" y="26" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">L1 / L2 / L3 Caches</text>
            <text x="280" y="44" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">64 KB – 64 MB | 1 – 15 ns</text>

            <line x1="430" y1="27" x2="470" y2="27" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="480" y="8" width="240" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
            <text x="490" y="32" fill="#0f172a" font-size="11" font-weight="600">On-die static RAM (SRAM)</text>
          </g>

          <!-- Tier 3: Main Memory -->
          <g transform="translate(100, 180)">
            <rect x="100" y="0" width="360" height="54" rx="6" fill="#075985" stroke="#0c4a6e" stroke-width="2" />
            <text x="280" y="26" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Main Memory (DRAM)</text>
            <text x="280" y="44" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">16 GB – 128 GB | 50 – 100 ns</text>

            <line x1="470" y1="27" x2="510" y2="27" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="520" y="8" width="240" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
            <text x="530" y="32" fill="#0f172a" font-size="11" font-weight="600">Volatile system RAM modules</text>
          </g>

          <!-- Tier 4: Solid-State Drives -->
          <g transform="translate(100, 255)">
            <rect x="60" y="0" width="440" height="54" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2" />
            <text x="280" y="26" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Solid-State Drives (NVMe / SSD)</text>
            <text x="280" y="44" fill="#e2e8f0" font-size="11" font-weight="600" text-anchor="middle">512 GB – 4 TB | 10 – 50 μs</text>

            <line x1="510" y1="27" x2="550" y2="27" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="560" y="8" width="220" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
            <text x="570" y="32" fill="#0f172a" font-size="11" font-weight="600">Non-volatile NAND Flash</text>
          </g>

          <!-- Tier 5: Magnetic Disks -->
          <g transform="translate(100, 330)">
            <rect x="20" y="0" width="520" height="54" rx="6" fill="#0f172a" stroke="#1e293b" stroke-width="2" />
            <text x="280" y="26" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Magnetic Hard Disks (HDD)</text>
            <text x="280" y="44" fill="#cbd5e1" font-size="11" font-weight="600" text-anchor="middle">1 TB – 20 TB | 5 – 10 ms</text>

            <line x1="550" y1="27" x2="590" y2="27" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="600" y="8" width="200" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
            <text x="610" y="32" fill="#0f172a" font-size="11" font-weight="600">Rotational disk platters</text>
          </g>

          <!-- Right Axis: Capacity & Persistence -->
          <line x1="810" y1="40" x2="810" y2="400" stroke="#334155" stroke-width="3" marker-end="url(#arrowCapacity)" />
          <text x="818" y="220" fill="#334155" font-size="12" font-weight="700" transform="rotate(90 818 220)" text-anchor="middle">LARGER STORAGE CAPACITY &amp; PERSISTENCE</text>
        </svg>
      </div>
"""

def execute_diagram_overhaul():
    target_file = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace old pyramid container
    pattern_container = r'<div id="svg-memory-pyramid">.*?</div>\s*</div>'
    if re.search(pattern_container, content, flags=re.DOTALL):
        content = re.sub(pattern_container, f'<div id="svg-memory-pyramid">{REFINED_MEMORY_DIAGRAM}</div>', content, flags=re.DOTALL)
        print("--> Replaced #svg-memory-pyramid with high-contrast tiered diagram.")
    else:
        # Fallback regex for raw svg replacement
        pattern_raw = r'<div style="display: flex; justify-content: center; margin: 24px 0;">\s*<svg viewBox="0 0 760 390".*?</svg>\s*</div>'
        content = re.sub(pattern_raw, REFINED_MEMORY_DIAGRAM, content, flags=re.DOTALL)
        print("--> Replaced raw SVG with high-contrast tiered diagram.")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Git stage, commit, and push
    try:
        subprocess.run(["git", "add", "fix.py", target_file], check=True)
        commit_msg = (
            "Redesign memory hierarchy diagram in Module 2 for high contrast\n\n"
            "Replace polygon slice pyramid with stepped horizontal tier layout in\n"
            "week01-operating-system-concepts/02-hardware-review.html to prevent clipping."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_diagram_overhaul()
