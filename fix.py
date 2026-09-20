#!/usr/bin/env python3
# =====================================================================
# fix.py: Shift DMA stream text label down to clear the dashed line
# =====================================================================
import os
import re
import subprocess

REFINED_DMA_SVG = """
        <svg viewBox="0 0 880 305" width="100%" height="auto" style="max-width: 880px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="dmaArrow" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
            </marker>
          </defs>

          <!-- CPU Box -->
          <rect x="40" y="30" width="150" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="115" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">CPU Core</text>
          <text x="115" y="82" fill="#64748b" font-size="10" text-anchor="middle">1. Sets up DMA transfer</text>

          <!-- DMA Controller Box -->
          <rect x="310" y="30" width="180" height="70" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
          <text x="400" y="62" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">DMA Controller</text>
          <text x="400" y="82" fill="#e0f2fe" font-size="10" text-anchor="middle">2. Manages direct bus flow</text>

          <!-- RAM Box -->
          <rect x="600" y="30" width="150" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="675" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">Main Memory</text>
          <text x="675" y="82" fill="#64748b" font-size="10" text-anchor="middle">Buffer Destination</text>

          <!-- System Bus Bar -->
          <rect x="40" y="145" width="710" height="24" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" />
          <text x="395" y="161" fill="#475569" font-size="11" font-weight="bold" text-anchor="middle">SYSTEM &amp; MEMORY BUS (PCIe / DMI / Memory Channels)</text>

          <!-- Device Controller -->
          <rect x="310" y="210" width="180" height="60" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" />
          <text x="400" y="236" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">Device Controller</text>
          <text x="400" y="254" fill="#64748b" font-size="10" text-anchor="middle">(NVMe / Disk / NIC)</text>

          <!-- Vertical Interconnect Bus Drops -->
          <line x1="115" y1="100" x2="115" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="400" y1="100" x2="400" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="675" y1="100" x2="675" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="400" y1="169" x2="400" y2="210" stroke="#64748b" stroke-width="2" />

          <!-- Bulk Data Flow Curve - Enters side port of Main Memory at (750, 65) -->
          <path d="M 490,240 C 650,240 780,210 780,110 C 780,65 765,65 756,65" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="6,3" marker-end="url(#dmaArrow)" />

          <!-- Label cleanly positioned underneath the dashed path with zero overlap -->
          <rect x="535" y="252" width="210" height="34" rx="4" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1" />
          <text x="640" y="267" fill="#0284c7" font-size="10" font-weight="bold" text-anchor="middle">Direct Memory Stream</text>
          <text x="640" y="280" fill="#0369a1" font-size="9" text-anchor="middle">(Bypasses CPU)</text>
        </svg>
"""

def adjust_dma_label_offset():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<svg viewBox="0 0 880 290".*?</svg>'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, REFINED_DMA_SVG.strip(), content, flags=re.DOTALL)
        print("--> Repositioned DMA label underneath the dashed path.")
    else:
        fallback_pattern = r'(<h3>Three Fundamental I/O Approaches</h3>.*?<div class="diagram-container">)\s*<svg.*?</svg>'
        if re.search(fallback_pattern, content, flags=re.DOTALL):
            content = re.sub(fallback_pattern, f"\\1\n{REFINED_DMA_SVG.strip()}", content, flags=re.DOTALL)
            print("--> Replaced DMA diagram via fallback pattern.")
        else:
            print("--> DMA SVG not found.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Shift DMA stream label down to prevent overlap with dashed data path\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html to lower\n"
            "the Direct Memory Stream text block beneath the trajectory of the curve."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    adjust_dma_label_offset()
