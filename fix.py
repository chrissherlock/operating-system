#!/usr/bin/env python3
# =====================================================================
# fix.py: Add hierarchical page table walk visualization diagram
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

HIERARCHICAL_TABLE_DIAGRAM_HTML = """      <!-- Graphical Hierarchical Page Table Walk Visualization -->
      <div style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Visual Diagram: 4-Level Hierarchical Page Table Walk</h3>
          <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Graphical tree view of how the MMU traverses memory from root register CR3 down to the physical frame.</p>
        </div>

        <div style="display: flex; justify-content: center; overflow-x: auto;">
          <svg viewBox="0 0 920 340" width="100%" height="100%" style="max-width: 920px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="arrowTable" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
              </marker>
              <marker id="arrowTableActive" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#ea580c" />
              </marker>
            </defs>

            <!-- Root Register CR3 -->
            <g transform="translate(30, 125)">
              <rect x="0" y="0" width="140" height="70" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" />
              <text x="70" y="24" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">CPU Root Register</text>
              <text x="70" y="44" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">CR3 Register</text>
              <text x="70" y="60" fill="#64748b" font-size="9" text-anchor="middle">Base: 0x1A4000</text>
            </g>

            <!-- Level 4: PML4 Table -->
            <g id="table-node-pml4" transform="translate(220, 30)">
              <rect x="0" y="0" width="140" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="70" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">PML4 Table</text>
              <text x="70" y="38" fill="#64748b" font-size="9" text-anchor="middle">Index: VPN[3]</text>
              <text x="70" y="50" fill="#0284c7" font-size="9" text-anchor="middle">Entry → PDPT</text>
            </g>

            <!-- Level 3: PDPT -->
            <g id="table-node-pdpt" transform="translate(390, 30)">
              <rect x="0" y="0" width="140" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="70" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">PDPT Table</text>
              <text x="70" y="38" fill="#64748b" font-size="9" text-anchor="middle">Index: VPN[2]</text>
              <text x="70" y="50" fill="#0284c7" font-size="9" text-anchor="middle">Entry → PD</text>
            </g>

            <!-- Level 2: Page Directory (PD) -->
            <g id="table-node-pd" transform="translate(560, 30)">
              <rect x="0" y="0" width="140" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="70" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Page Directory</text>
              <text x="70" y="38" fill="#64748b" font-size="9" text-anchor="middle">Index: VPN[1]</text>
              <text x="70" y="50" fill="#0284c7" font-size="9" text-anchor="middle">Entry → PT</text>
            </g>

            <!-- Level 1: Page Table (PT) -->
            <g id="table-node-pt" transform="translate(730, 30)">
              <rect x="0" y="0" width="160" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="80" y="22" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Page Table (PT)</text>
              <text x="80" y="38" fill="#64748b" font-size="9" text-anchor="middle">Index: VPN[0] (0x00403)</text>
              <text x="80" y="50" fill="#059669" font-size="9" font-weight="700" text-anchor="middle">Leaf PTE → PFN 0x07B40</text>
            </g>

            <!-- Physical Frame Target Box -->
            <g id="table-node-frame" transform="translate(730, 230)">
              <rect x="0" y="0" width="160" height="70" rx="6" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
              <text x="80" y="24" fill="#065f46" font-size="11" font-weight="700" text-anchor="middle">Physical DRAM Frame</text>
              <text x="80" y="44" fill="#059669" font-size="12" font-weight="700" text-anchor="middle">Frame: 0x07B40</text>
              <text x="80" y="60" fill="#047857" font-size="9" text-anchor="middle">+ Offset 0x018 = Addr</text>
            </g>

            <!-- Connecting Tree Paths -->
            <!-- CR3 to PML4 -->
            <path d="M 170,160 C 195,160 190,60 220,60" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowTable)" />
            <!-- PML4 to PDPT -->
            <path d="M 360,60 L 390,60" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowTable)" />
            <!-- PDPT to PD -->
            <path d="M 530,60 L 560,60" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowTable)" />
            <!-- PD to PT -->
            <path d="M 700,60 L 730,60" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowTable)" />
            <!-- PT Leaf down to Physical Frame -->
            <path d="M 810,90 L 810,230" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowTable)" />
            <text x="825" y="165" fill="#059669" font-size="9.5" font-weight="700">Resolved PFN</text>

            <!-- Explanatory Callout Box Below Tree -->
            <g transform="translate(30, 230)">
              <rect x="0" y="0" width="670" height="70" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text x="15" y="25" fill="#0369a1" font-size="11" font-weight="700">HOW HIERARCHICAL PAGING WORKS:</text>
              <text x="15" y="45" fill="#1e293b" font-size="10" font-family="var(--font-mono)">
                Each table lookup consumes one DRAM memory access unless cached in the TLB.
              </text>
              <text x="15" y="60" fill="#64748b" font-size="9.5" font-family="var(--font-mono)">
                Unallocated virtual memory ranges omit entire subtrees, saving gigabytes of physical RAM.
              </text>
            </g>
          </svg>
        </div>
      </div>"""

def add_hierarchical_table_diagram():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if "Visual Diagram: 4-Level Hierarchical Page Table Walk" in content:
        print("--> Hierarchical table walk diagram already present.")
        return

    # Target marker: right after the translation simulator block
    sim_end_marker = '<!-- Paired Analytical Panes -->\n        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">'

    # Let's find the closing div of the interactive translation simulator
    # We can search for the second occurrence of <script> after Section 3 or look for the end of the translation simulator div
    target_pos = content.find("Interactive Walkthrough: Address Translation &amp; Offset Pass-Through")
    if target_pos != -1:
        # Find the script block closing tag for this simulator
        script_close = content.find("</script>", target_pos)
        if script_close != -1:
            insert_pos = script_close + 9
            content = content[:insert_pos] + "\n\n" + HIERARCHICAL_TABLE_DIAGRAM_HTML + content[insert_pos:]
            print("--> Successfully injected hierarchical table diagram after translation simulator.")
        else:
            print("--> Error: Could not locate script closing tag for translation simulator.")
            return
    else:
        print("--> Error: Could not locate translation simulator header.")
        return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add hierarchical page table walk visual diagram to Module 2\n\n"
            "Embed an interactive graphical SVG tree diagram illustrating multi-level\n"
            "page table walks beneath the address translation simulator in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for hierarchical table diagram!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_hierarchical_table_diagram()
