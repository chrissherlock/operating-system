#!/usr/bin/env python3
# =====================================================================
# fix.py: Reroute DMA curve to eliminate overlap with the memory bus line
# =====================================================================
import os
import re
import subprocess

REFINED_DMA_SVG = """
        <svg viewBox="0 0 760 290" width="100%" height="auto" style="max-width: 760px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="dmaArrow" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
            </marker>
          </defs>

          <!-- CPU Box -->
          <rect x="30" y="30" width="140" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="100" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">CPU Core</text>
          <text x="100" y="82" fill="#64748b" font-size="10" text-anchor="middle">1. Sets up DMA transfer</text>

          <!-- DMA Controller Box -->
          <rect x="290" y="30" width="170" height="70" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
          <text x="375" y="62" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">DMA Controller</text>
          <text x="375" y="82" fill="#e0f2fe" font-size="10" text-anchor="middle">2. Manages direct bus flow</text>

          <!-- RAM Box -->
          <rect x="560" y="30" width="140" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="630" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">Main Memory</text>
          <text x="630" y="82" fill="#64748b" font-size="10" text-anchor="middle">Buffer Destination</text>

          <!-- System Bus Bar -->
          <rect x="30" y="145" width="670" height="24" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" />
          <text x="365" y="161" fill="#475569" font-size="11" font-weight="bold" text-anchor="middle">SYSTEM &amp; MEMORY BUS (PCIe / DMI / Memory Channels)</text>

          <!-- Device Controller -->
          <rect x="290" y="210" width="170" height="60" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" />
          <text x="375" y="236" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">Device Controller</text>
          <text x="375" y="254" fill="#64748b" font-size="10" text-anchor="middle">(NVMe / Disk / NIC)</text>

          <!-- Vertical Interconnect Bus Drops -->
          <line x1="100" y1="100" x2="100" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="375" y1="100" x2="375" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="630" y1="100" x2="630" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="375" y1="169" x2="375" y2="210" stroke="#64748b" stroke-width="2" />

          <!-- Bulk Data Flow Curve - Routed to enter side port of Main Memory at (700, 65) -->
          <path d="M 460,240 C 620,240 735,210 735,110 C 735,65 715,65 706,65" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="6,3" marker-end="url(#dmaArrow)" />
          <text x="590" y="260" fill="#0284c7" font-size="10" font-weight="bold">Direct Memory Stream (Bypasses CPU)</text>
        </svg>
"""

def adjust_dma_diagram_path():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate DMA diagram SVG pattern and substitute
    dma_pattern = r'<svg viewBox="0 0 740 280".*?</svg>'
    if re.search(dma_pattern, content, flags=re.DOTALL):
        content = re.sub(dma_pattern, REFINED_DMA_SVG.strip(), content, flags=re.DOTALL)
        print("--> Updated DMA diagram path to prevent line overlap.")
    else:
        # Fallback if viewBox already varied
        fallback_pattern = r'(<h3>Three Fundamental I/O Approaches</h3>.*?<div class="diagram-container">)\s*<svg.*?</svg>'
        if re.search(fallback_pattern, content, flags=re.DOTALL):
            content = re.sub(fallback_pattern, f"\\1\n{REFINED_DMA_SVG.strip()}", content, flags=re.DOTALL)
            print("--> Replaced DMA diagram via fallback pattern.")
        else:
            print("--> DMA SVG container not found.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Reroute DMA data stream curve in Module 2 to prevent bus line overlap\n\n"
            "Adjust coordinates of dashed DMA memory path in 02-hardware-review.html\n"
            "to land on the memory side port instead of overwriting the bus drop line."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    adjust_dma_diagram_path()
