#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix SVG node text overflow in translation simulator
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_svg_node_overflow():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old SVG group structure for the 4 stages in translation simulator
    old_svg_stages = """            <!-- Stage 1: Virtual Address -->
            <g id="trans-node-va" transform="translate(30, 30)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">1. Virtual Address</text>
              <text id="trans-svg-va" x="90" y="48" fill="#0284c7" font-size="11" font-weight="700" text-anchor="middle">0x00403018</text>
              <text x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">CPU Instruction Bus</text>
            </g>

            <!-- Stage 2: Bit-Slicing Unit -->
            <g id="trans-node-slice" transform="translate(250, 30)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">2. Bit-Slicing Unit</text>
              <text id="trans-svg-slice" x="90" y="48" fill="#475569" font-size="10.5" font-weight="700" text-anchor="middle">VPN: 0x00403 | Off: 0x018</text>
              <text x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">Split bits [47:12] &amp; [11:0]</text>
            </g>

            <!-- Stage 3: MMU Page Table Lookup -->
            <g id="trans-node-mmu" transform="translate(470, 30)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">3. MMU Table Walk</text>
              <text id="trans-svg-mmu" x="90" y="48" fill="#475569" font-size="10.5" font-weight="700" text-anchor="middle">Lookup VPN → PFN</text>
              <text x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">Resolves to Frame 0x07B40</text>
            </g>

            <!-- Stage 4: Physical Address Assembly -->
            <g id="trans-node-pa" transform="translate(690, 30)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">4. Physical Address</text>
              <text id="trans-svg-pa" x="90" y="48" fill="#475569" font-size="10.5" font-weight="700" text-anchor="middle">0x07B40018</text>
              <text x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">Issued to DRAM Bus</text>
            </g>

            <!-- Inter-Stage Links -->
            <path d="M 210,75 L 245,75" stroke="#cbd5e1" stroke-width="2" />
            <path d="M 430,75 L 465,75" stroke="#cbd5e1" stroke-width="2" />
            <path d="M 650,75 L 685,75" stroke="#cbd5e1" stroke-width="2" />

            <!-- Offset Bypass Pass-Through Line -->
            <path id="trans-bypass-path" d="M 340,120 C 340,165 600,165 600,120" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />"""

    # New wider structure (width=200 per node, distributed across 920 canvas)
    new_svg_stages = """            <!-- Stage 1: Virtual Address -->
            <g id="trans-node-va" transform="translate(20, 30)">
              <rect x="0" y="0" width="200" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="100" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">1. Virtual Address</text>
              <text id="trans-svg-va" x="100" y="44" fill="#0284c7" font-size="11" font-weight="700" text-anchor="middle">0x00403018</text>
              <text x="100" y="62" fill="#64748b" font-size="9" text-anchor="middle">CPU Instruction Bus</text>
            </g>

            <!-- Stage 2: Bit-Slicing Unit -->
            <g id="trans-node-slice" transform="translate(240, 30)">
              <rect x="0" y="0" width="200" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="100" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">2. Bit-Slicing Unit</text>
              <text id="trans-svg-slice-vpn" x="100" y="42" fill="#475569" font-size="10" font-weight="700" text-anchor="middle">VPN: 0x00403</text>
              <text id="trans-svg-slice-off" x="100" y="58" fill="#059669" font-size="10" font-weight="700" text-anchor="middle">Offset: 0x018</text>
              <text x="100" y="74" fill="#64748b" font-size="8.5" text-anchor="middle">Split bits [47:12] &amp; [11:0]</text>
            </g>

            <!-- Stage 3: MMU Page Table Lookup -->
            <g id="trans-node-mmu" transform="translate(460, 30)">
              <rect x="0" y="0" width="200" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="100" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">3. MMU Table Walk</text>
              <text id="trans-svg-mmu" x="100" y="44" fill="#475569" font-size="10" font-weight="700" text-anchor="middle">Lookup VPN → PFN</text>
              <text x="100" y="62" fill="#64748b" font-size="9" text-anchor="middle">Resolves Frame 0x07B40</text>
            </g>

            <!-- Stage 4: Physical Address Assembly -->
            <g id="trans-node-pa" transform="translate(680, 30)">
              <rect x="0" y="0" width="200" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="100" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">4. Physical Address</text>
              <text id="trans-svg-pa" x="100" y="44" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">0x07B40018</text>
              <text x="100" y="62" fill="#64748b" font-size="9" text-anchor="middle">Issued to DRAM Bus</text>
            </g>

            <!-- Inter-Stage Links -->
            <path d="M 220,75 L 238,75" stroke="#cbd5e1" stroke-width="2" />
            <path d="M 440,75 L 458,75" stroke="#cbd5e1" stroke-width="2" />
            <path d="M 660,75 L 678,75" stroke="#cbd5e1" stroke-width="2" />

            <!-- Offset Bypass Pass-Through Line -->
            <path id="trans-bypass-path" d="M 340,120 C 340,165 560,165 560,120" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />"""

    if old_svg_stages in content:
        content = content.replace(old_svg_stages, new_svg_stages)
        print("--> Successfully widened SVG stage cards and split Bit-Slicing labels.")
    else:
        print("--> Warning: Exact SVG stages block not found; checking script rendering logic.")

    # Also update the JavaScript updater in the script block for trans-svg-slice
    old_js_update = 'document.getElementById("trans-svg-slice").textContent = "VPN: " + data.vpn + " | Off: " + data.offset.split(" ")[0];'
    new_js_update = """document.getElementById("trans-svg-slice-vpn").textContent = "VPN: " + data.vpn.split(" ")[0];
            document.getElementById("trans-svg-slice-off").textContent = "Offset: " + data.offset.split(" ")[0];"""

    if old_js_update in content:
        content = content.replace(old_js_update, new_js_update)
        print("--> Updated JavaScript text updaters for split slice labels.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix SVG box text overflow in Bit-Slicing Unit node\n\n"
            "Widen SVG stage cards and split long sub-labels across stacked lines\n"
            "within the address translation simulator in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for SVG node overflow fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_svg_node_overflow()
