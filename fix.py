#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand page table entry density in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

EXPANDED_TABLE_SIMULATOR_HTML = """      <!-- Interactive Directed Narrative Stepper: Bit-Slice & Synchronized Page Table Walk Engine -->
      <div id="interactive-translation-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <!-- Header & Dimension Toggles -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Interactive Walkthrough: Synchronized Page Table Walk &amp; Offset Pass-Through</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Trace how the MMU steps through multi-level page table entries (PTEs) in DRAM in real time.</p>
          </div>

          <!-- Dimension Toggles -->
          <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
            <span style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; padding: 0 6px;">Granularity:</span>
            <button id="trans-btn-4k" class="trans-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">4 KiB Standard Page</button>
            <button id="trans-btn-2m" class="trans-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">2 MiB Superpage</button>
            <button id="trans-btn-swap" class="trans-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Swapped Page</button>
          </div>
        </div>

        <!-- Instructions & Scenario Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">The Scenario: Tracing a 4 KiB Virtual-to-Physical Translation</div>
          <p style="margin: 0 0 8px 0; color: #1e293b; font-size: 0.9rem; line-height: 1.5;">
            We are tracing how the MMU translates virtual address <strong><code>0x00403018</code></strong> into physical DRAM address <strong><code>0x07B40018</code></strong> across synchronized page table entries:
          </p>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; margin-bottom: 10px;">
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #0284c7; font-family: var(--font-mono);">1. Multi-Level Page Walk</strong>
              <div style="color: #64748b; margin-top: 2px;">MMU traverses CR3 → PML4 → PDPT → PD → PT entries in DRAM.</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #059669; font-family: var(--font-mono);">2. Offset Pass-Through</strong>
              <div style="color: #64748b; margin-top: 2px;">Lower 12 bits (<code>0x018</code>) bypass translation entirely, passing through unmodified.</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #7c3aed; font-family: var(--font-mono);">3. Frame Assembly (PFN)</strong>
              <div style="color: #64748b; margin-top: 2px;">Combined with Physical Frame Number (<code>0x07B40</code>) to form the final physical address.</div>
            </div>
          </div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.84rem; line-height: 1.5;">
            <li><strong>Synchronized Table Matrix:</strong> Observe how the expanded graphical table entries illuminate sequentially as each step of the table walk executes.</li>
            <li><strong>Granularity Toggles:</strong> Switch between modes to compare standard pages, superpages, and page faults.</li>
          </ol>
        </div>

        <!-- Action Controls & Foreshadowed Preview Panel -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="trans-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step →</button>
            <div style="display: flex; gap: 8px;">
              <button id="trans-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">← Prev</button>
              <button id="trans-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Where We Are &amp; What Happens Next Click:</div>
            <div id="trans-inline-preview" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">Loading translation state...</div>
          </div>
        </div>

        <!-- Live State Telemetry Bar -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.8rem;">
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Virtual Address</div>
            <div id="trans-stat-va" style="font-weight: 700; color: #0f172a; margin-top: 2px;">0x00403018</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Active Table Walk</div>
            <div id="trans-stat-vpn" style="font-weight: 700; color: #0284c7; margin-top: 2px;">CR3 Root</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Page Offset</div>
            <div id="trans-stat-offset" style="font-weight: 700; color: #059669; margin-top: 2px;">0x018 (Bypass)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Physical Frame (PFN)</div>
            <div id="trans-stat-pfn" style="font-weight: 700; color: #0369a1; margin-top: 2px;">Pending...</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Final Physical Addr</div>
            <div id="trans-stat-pa" style="font-weight: 700; color: #7c3aed; margin-top: 2px;">Pending...</div>
          </div>
        </div>

        <!-- Synchronized SVG Visual Canvas: Expanded Matrix Table Walk -->
        <div style="display: flex; justify-content: center; margin-bottom: 20px; overflow-x: auto;">
          <svg id="trans-anim-svg" viewBox="0 0 940 340" width="100%" height="100%" style="max-width: 940px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="marker-trans-blue" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
              </marker>
            </defs>

            <!-- CR3 Root Register Node -->
            <g id="trans-node-cr3" transform="translate(25, 110)">
              <rect x="0" y="0" width="120" height="70" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="60" y="24" fill="#0369a1" font-size="10" font-weight="700" text-anchor="middle">Root Register</text>
              <text x="60" y="44" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">CR3</text>
              <text x="60" y="60" fill="#64748b" font-size="9" text-anchor="middle">0x1A4000</text>
            </g>

            <!-- Table 1: PML4 Table (Expanded Density) -->
            <g id="trans-node-pml4" transform="translate(180, 50)">
              <rect x="0" y="0" width="130" height="190" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="65" y="18" fill="#0f172a" font-size="10.5" font-weight="700" text-anchor="middle">PML4 Table</text>
              <rect x="10" y="28" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="41" fill="#64748b" font-size="8.5" text-anchor="middle">Index 0: Unused</text>
              <rect x="10" y="52" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="65" fill="#64748b" font-size="8.5" text-anchor="middle">Index 1: Unused</text>
              <rect x="10" y="76" width="110" height="26" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="1" />
              <text x="65" y="93" fill="#0284c7" font-size="9" font-weight="700" text-anchor="middle">Index 2: 0x2B100</text>
              <rect x="10" y="106" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="119" fill="#64748b" font-size="8.5" text-anchor="middle">Index 3: Unused</text>
              <rect x="10" y="130" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="143" fill="#64748b" font-size="8.5" text-anchor="middle">Index 4: Unused</text>
              <rect x="10" y="154" width="110" height="22" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="169" fill="#64748b" font-size="8.5" text-anchor="middle">... (512 Entries)</text>
            </g>

            <!-- Table 2: PDPT Table (Expanded Density) -->
            <g id="trans-node-pdpt" transform="translate(345, 50)">
              <rect x="0" y="0" width="130" height="190" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="65" y="18" fill="#0f172a" font-size="10.5" font-weight="700" text-anchor="middle">PDPT Table</text>
              <rect x="10" y="28" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="41" fill="#64748b" font-size="8.5" text-anchor="middle">Index 0: Unused</text>
              <rect x="10" y="52" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="65" fill="#64748b" font-size="8.5" text-anchor="middle">Index 1: Unused</text>
              <rect x="10" y="76" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="89" fill="#64748b" font-size="8.5" text-anchor="middle">Index 2: Unused</text>
              <rect x="10" y="100" width="110" height="26" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="1" />
              <text x="65" y="117" fill="#0284c7" font-size="9" font-weight="700" text-anchor="middle">Index 3: 0x3C200</text>
              <rect x="10" y="130" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="143" fill="#64748b" font-size="8.5" text-anchor="middle">Index 4: Unused</text>
              <rect x="10" y="154" width="110" height="22" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="169" fill="#64748b" font-size="8.5" text-anchor="middle">... (512 Entries)</text>
            </g>

            <!-- Table 3: Page Directory (PD) (Expanded Density) -->
            <g id="trans-node-pd" transform="translate(510, 50)">
              <rect x="0" y="0" width="130" height="190" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="65" y="18" fill="#0f172a" font-size="10.5" font-weight="700" text-anchor="middle">Page Directory</text>
              <rect x="10" y="28" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="41" fill="#64748b" font-size="8.5" text-anchor="middle">Index 0: Unused</text>
              <rect x="10" y="52" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="65" fill="#64748b" font-size="8.5" text-anchor="middle">Index 1: Unused</text>
              <rect x="10" y="76" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="89" fill="#64748b" font-size="8.5" text-anchor="middle">Index 2: Unused</text>
              <rect x="10" y="100" width="110" height="26" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="1" />
              <text x="65" y="117" fill="#0284c7" font-size="9" font-weight="700" text-anchor="middle">Index 3: 0x4D300</text>
              <rect x="10" y="130" width="110" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="143" fill="#64748b" font-size="8.5" text-anchor="middle">Index 4: Unused</text>
              <rect x="10" y="154" width="110" height="22" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="65" y="169" fill="#64748b" font-size="8.5" text-anchor="middle">... (512 Entries)</text>
            </g>

            <!-- Table 4: Page Table (PT) (Expanded Density) -->
            <g id="trans-node-pt" transform="translate(675, 50)">
              <rect x="0" y="0" width="140" height="190" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="70" y="18" fill="#0f172a" font-size="10.5" font-weight="700" text-anchor="middle">Page Table (PT)</text>
              <rect x="10" y="28" width="120" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="70" y="41" fill="#64748b" font-size="8.5" text-anchor="middle">VPN 0x00401: Unused</text>
              <rect x="10" y="52" width="120" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="70" y="65" fill="#64748b" font-size="8.5" text-anchor="middle">VPN 0x00402: Unused</text>
              <rect x="10" y="76" width="120" height="26" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="1" />
              <text x="70" y="93" fill="#0284c7" font-size="9" font-weight="700" text-anchor="middle">VPN 0x00403: 0x07B40</text>
              <rect x="10" y="106" width="120" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="70" y="119" fill="#64748b" font-size="8.5" text-anchor="middle">VPN 0x00404: Unused</text>
              <rect x="10" y="130" width="120" height="20" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="70" y="143" fill="#64748b" font-size="8.5" text-anchor="middle">VPN 0x00405: Unused</text>
              <rect x="10" y="154" width="120" height="22" rx="3" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="70" y="169" fill="#64748b" font-size="8.5" text-anchor="middle">... (512 Entries)</text>
            </g>

            <!-- Connecting Flow Paths -->
            <path id="trans-path-1" d="M 145,145 L 175,145" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-trans-blue)" />
            <path id="trans-path-2" d="M 310,145 L 340,145" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-trans-blue)" />
            <path id="trans-path-3" d="M 475,145 L 505,145" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-trans-blue)" />
            <path id="trans-path-4" d="M 640,145 L 670,145" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-trans-blue)" />

            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,290 400,290 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="278" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 290)">
              <rect x="0" y="0" width="890" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="15" y="25" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: READY</text>
            </g>
          </svg>
        </div>

        <!-- Paired Analytical Panes -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Detailed Mechanics: What Is Happening</div>
            <div id="trans-desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="trans-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const transStorylines = {
            "4k": [
              {
                step: "Step 1: CR3 Root Lookup & PML4 Table",
                phase: "1. CR3 → PML4 Lookup",
                va: "0x00403018",
                vpn: "CR3 Root Lookup",
                offset: "0x018",
                pfn: "Pending...",
                pa: "Pending...",
                activeNodes: ["trans-node-cr3", "trans-node-pml4"],
                activePaths: ["trans-path-1"],
                bypassActive: false,
                consoleTop: "TRANSLATION STEP 1 • CR3 ROOT REGISTER TO PML4 TABLE",
                what: "The MMU reads the root page table physical address <code>0x1A4000</code> from control register <strong>CR3</strong>. It indexes into the PML4 table, locating entry 2 which points to the PDPT table at <code>0x2B100</code>.",
                why: "CR3 anchors the process's complete virtual address space, ensuring complete memory isolation between running applications."
              },
              {
                step: "Step 2: PDPT Table Traversal",
                phase: "2. PML4 → PDPT Traversal",
                va: "0x00403018",
                vpn: "PDPT Indexing",
                offset: "0x018",
                pfn: "Pending...",
                pa: "Pending...",
                activeNodes: ["trans-node-pml4", "trans-node-pdpt"],
                activePaths: ["trans-path-2"],
                bypassActive: false,
                consoleTop: "TRANSLATION STEP 2 • PML4 ENTRY TO PDPT TABLE",
                what: "Using the address found in PML4, the MMU accesses the Page Directory Pointer Table (PDPT) in DRAM, selecting Entry 3 which points to the Page Directory at <code>0x3C200</code>.",
                why: "Multi-level hierarchies allow operating systems to omit unused memory regions entirely, conserving physical DRAM."
              },
              {
                step: "Step 3: Page Directory Traversal",
                phase: "3. PDPT → Page Directory",
                va: "0x00403018",
                vpn: "Page Directory Indexing",
                offset: "0x018",
                pfn: "Pending...",
                pa: "Pending...",
                activeNodes: ["trans-node-pdpt", "trans-node-pd"],
                activePaths: ["trans-path-3"],
                bypassActive: false,
                consoleTop: "TRANSLATION STEP 3 • PDPT ENTRY TO PAGE DIRECTORY",
                what: "The MMU accesses the Page Directory (PD) in DRAM, reading Entry 3 which points to the base address of the Page Table at <code>0x4D300</code>.",
                why: "Staging memory lookups across directory trees keeps individual page tables compact (4 KiB per table)."
              },
              {
                step: "Step 4: Page Table Leaf Resolution",
                phase: "4. Page Directory → Page Table Leaf",
                va: "0x00403018",
                vpn: "VPN 0x00403 Resolved",
                offset: "0x018",
                pfn: "0x07B40",
                pa: "0x07B40018",
                activeNodes: ["trans-node-pd", "trans-node-pt"],
                activePaths: ["trans-path-4"],
                bypassActive: true,
                consoleTop: "TRANSLATION STEP 4 • PAGE TABLE LEAF PTE RESOLUTION",
                what: "The MMU reads the final Page Table (PT), indexing Virtual Page Number <code>0x00403</code>. The leaf Page Table Entry (PTE) yields <strong>Physical Frame Number <code>0x07B40</code></strong>.",
                why: "The leaf PTE encodes permission metadata (Present, Read/Write, User/Supervisor) alongside the physical frame number."
              },
              {
                step: "Step 5: Offset Pass-Through & Physical Address Assembly",
                phase: "5. Physical Address Assembled",
                va: "0x00403018",
                vpn: "VPN 0x00403",
                offset: "0x018 (Unmodified)",
                pfn: "0x07B40",
                pa: "0x07B40018 (Complete)",
                activeNodes: ["trans-node-pt"],
                activePaths: [],
                bypassActive: true,
                consoleTop: "TRANSLATION STEP 5 • OFFSET PASS-THROUGH & DRAM BUS ISSUE (COMPLETE)",
                what: "The lowest 12 bits (<code>0x018</code>) pass through completely unmodified, combining with PFN <code>0x07B40000</code> to issue final physical address <strong><code>0x07B40018</code></strong> to the DRAM bus.",
                why: "Because virtual page size matches physical frame size, intra-page byte offsets remain 100% identical in physical memory, eliminating calculation overhead."
              }
            ],
            "2m": [
              {
                step: "Superpage Step 1: CR3 to PML4",
                phase: "1. CR3 Root Lookup",
                va: "0x00400000 (2MB)",
                vpn: "Superpage Root",
                offset: "0x000",
                pfn: "Pending...",
                pa: "Pending...",
                activeNodes: ["trans-node-cr3", "trans-node-pml4"],
                activePaths: ["trans-path-1"],
                bypassActive: false,
                consoleTop: "2 MiB SUPERPAGE WALK • STEP 1",
                what: "The MMU accesses CR3 and checks PML4 for a 2 MiB superpage mapping.",
                why: "Superpages reduce TLB pressure for large memory-intensive applications."
              },
              {
                step: "Superpage Step 2: Direct PDE Frame Mapping",
                phase: "2. Direct Superpage Resolution",
                va: "0x00400000 (2MB)",
                vpn: "PDE Superpage Entry",
                offset: "0x000 (21 bits)",
                pfn: "0x04000 (2MB Frame)",
                pa: "0x08000000",
                activeNodes: ["trans-node-pdpt", "trans-node-pd"],
                activePaths: ["trans-path-2", "trans-path-3"],
                bypassActive: true,
                consoleTop: "2 MiB SUPERPAGE WALK • STEP 2 (COMPLETE)",
                what: "The Page Directory Entry (PDE) maps directly to a massive 2 MiB physical DRAM frame, bypassing the final Page Table walk entirely.",
                why: "Stopping the page walk early at Level 2 maximizes TLB efficiency and reduces DRAM access latency."
              }
            ],
            "swap": [
              {
                step: "Swap Step 1: Page Table Walk to Swapped PTE",
                phase: "1. Swapped PTE Located",
                va: "0x00705020",
                vpn: "VPN 0x00705",
                offset: "0x020",
                pfn: "None (Present=0)",
                pa: "Page Fault!",
                activeNodes: ["trans-node-cr3", "trans-node-pml4", "trans-node-pdpt", "trans-node-pd", "trans-node-pt"],
                activePaths: ["trans-path-1", "trans-path-2", "trans-path-3", "trans-path-4"],
                bypassActive: false,
                consoleTop: "SWAPPED PAGE FAULT WALK • STEP 1",
                what: "The MMU completes the page table walk for virtual address <code>0x00705020</code> but discovers <strong>Present Bit = 0</strong> in the leaf PTE.",
                why: "Demand paging allows systems to overcommit physical RAM by evicting inactive pages to disk swap."
              },
              {
                step: "Swap Step 2: Kernel Frame Allocation & Swap-In",
                phase: "2. Kernel Fault Resolution",
                va: "0x00705020",
                vpn: "VPN 0x00705",
                offset: "0x020",
                pfn: "0x09840 (Allocated)",
                pa: "0x09840020 (Complete)",
                activeNodes: ["trans-node-pt"],
                activePaths: [],
                bypassActive: true,
                consoleTop: "SWAPPED PAGE FAULT WALK • STEP 2 (COMPLETE)",
                what: "The CPU traps into the kernel page fault handler. The OS allocates frame <code>0x09840</code>, reads data from disk swap, updates the PTE to Present=1, and restarts the instruction.",
                why: "The application resumes execution seamlessly, unaware that its memory page was temporarily stored on disk."
              }
            ]
          };

          let currentTransMode = "4k";
          let transIndex = 0;

          function renderTransState() {
            const list = transStorylines[currentTransMode];
            const data = list[transIndex];

            // Telemetry
            document.getElementById("trans-stat-va").textContent = data.va;
            document.getElementById("trans-stat-vpn").textContent = data.vpn;
            document.getElementById("trans-stat-offset").textContent = data.offset;
            document.getElementById("trans-stat-pfn").textContent = data.pfn;
            document.getElementById("trans-stat-pa").textContent = data.pa;

            // Panes
            document.getElementById("trans-inline-preview").innerHTML = data.step + " completed. Click Next to continue.";
            document.getElementById("trans-desc-what").innerHTML = data.what;
            document.getElementById("trans-desc-why").innerHTML = data.why;
            document.getElementById("trans-console-top").textContent = data.consoleTop;

            // Buttons
            const nextBtn = document.getElementById("trans-next-btn");
            const prevBtn = document.getElementById("trans-prev-btn");

            if (nextBtn) {
              nextBtn.innerHTML = transIndex === list.length - 1 ? "Restart Walkthrough ↺" : "Next Step →";
            }
            if (prevBtn) {
              prevBtn.style.opacity = transIndex === 0 ? "0.5" : "1.0";
              prevBtn.style.cursor = transIndex === 0 ? "not-allowed" : "pointer";
            }

            // Reset SVG nodes
            const allNodes = ["trans-node-cr3", "trans-node-pml4", "trans-node-pdpt", "trans-node-pd", "trans-node-pt"];
            allNodes.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                const rect = el.querySelector("rect");
                if (rect) {
                  rect.setAttribute("stroke", "#cbd5e1");
                  rect.setAttribute("stroke-width", "1.5");
                  rect.setAttribute("fill", "#ffffff");
                  rect.style.filter = "none";
                }
              }
            });

            // Highlight active nodes
            data.activeNodes.forEach(id => {
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
            });

            // Reset paths
            const allPaths = ["trans-path-1", "trans-path-2", "trans-path-3", "trans-path-4"];
            allPaths.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#cbd5e1");
                el.setAttribute("stroke-width", "2");
              }
            });

            // Highlight active paths
            data.activePaths.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#ea580c");
                el.setAttribute("stroke-width", "3");
              }
            });

            // Bypass line glow
            const bypassPath = document.getElementById("trans-bypass-path");
            const bypassLabel = document.getElementById("trans-bypass-label");
            if (bypassPath && bypassLabel) {
              if (data.bypassActive) {
                bypassPath.setAttribute("stroke", "#059669");
                bypassPath.setAttribute("stroke-width", "2.5");
                bypassPath.setAttribute("stroke-dasharray", "none");
                bypassLabel.setAttribute("fill", "#059669");
                bypassLabel.setAttribute("font-weight", "700");
              } else {
                bypassPath.setAttribute("stroke", "#cbd5e1");
                bypassPath.setAttribute("stroke-width", "2");
                bypassPath.setAttribute("stroke-dasharray", "4,4");
                bypassLabel.setAttribute("fill", "#64748b");
                bypassLabel.setAttribute("font-weight", "400");
              }
            }
          }

          function setTransMode(modeKey) {
            currentTransMode = modeKey;
            transIndex = 0;
            const buttons = {
              "4k": document.getElementById("trans-btn-4k"),
              "2m": document.getElementById("trans-btn-2m"),
              "swap": document.getElementById("trans-btn-swap")
            };
            Object.keys(buttons).forEach(k => {
              const btn = buttons[k];
              if (btn) {
                if (k === modeKey) {
                  btn.style.background = "#0284c7";
                  btn.style.color = "#ffffff";
                } else {
                  btn.style.background = "transparent";
                  btn.style.color = "#475569";
                }
              }
            });
            renderTransState();
          }

          document.getElementById("trans-btn-4k").addEventListener("click", () => setTransMode("4k"));
          document.getElementById("trans-btn-2m").addEventListener("click", () => setTransMode("2m"));
          document.getElementById("trans-btn-swap").addEventListener("click", () => setTransMode("swap"));

          document.getElementById("trans-next-btn").addEventListener("click", function() {
            const list = transStorylines[currentTransMode];
            if (transIndex < list.length - 1) {
              transIndex++;
            } else {
              transIndex = 0;
            }
            renderTransState();
          });

          document.getElementById("trans-prev-btn").addEventListener("click", function() {
            if (transIndex > 0) {
              transIndex--;
              renderTransState();
            }
          });

          document.getElementById("trans-reset-btn").addEventListener("click", function() {
            transIndex = 0;
            renderTransState();
          });

          renderTransState();
        })();
      </script>"""

def update_expanded_table_simulator():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = '<div id="interactive-translation-simulator"'
    start_pos = content.find(start_marker)

    if start_pos != -1:
        section4_marker = '<h2>4. Disks, I/O Devices'
        end_pos = content.find(section4_marker, start_pos)
        if end_pos != -1:
            content = content[:start_pos] + EXPANDED_TABLE_SIMULATOR_HTML + "\n\n      " + content[end_pos:]
            print("--> Updated translation simulator with expanded high-density tables.")
        else:
            print("--> Error: Could not locate Section 4 boundary.")
            return
    else:
        print("--> Error: Could not locate interactive translation simulator in target file.")
        return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand page table entry density in Module 2 translation simulator\n\n"
            "Increase the number of visible rows in the PML4, PDPT, Page Directory,\n"
            "and Page Table SVG nodes within 02-hardware-review.html for a realistic view."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for expanded table density!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_expanded_table_simulator()
