#!/usr/bin/env python3
# =====================================================================
# fix.py: Add interactive address translation simulator to Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

TRANSLATION_SIMULATOR_HTML = """      <!-- Interactive Directed Narrative Stepper: Bit-Slice & Offset Pass-Through Engine -->
      <div id="interactive-translation-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <!-- Header & Dimension Toggles -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Interactive Walkthrough: Address Translation &amp; Offset Pass-Through</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Trace how virtual address bits are sliced, translated, and combined into physical DRAM addresses.</p>
          </div>

          <!-- Dimension Toggles -->
          <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
            <span style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; padding: 0 6px;">Granularity:</span>
            <button id="trans-btn-4k" class="trans-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">4 KiB Standard Page</button>
            <button id="trans-btn-2m" class="trans-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">2 MiB Superpage</button>
            <button id="trans-btn-swap" class="trans-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Swapped Page</button>
          </div>
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
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Bit-Slice (VPN)</div>
            <div id="trans-stat-vpn" style="font-weight: 700; color: #0284c7; margin-top: 2px;">0x00403</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Page Offset</div>
            <div id="trans-stat-offset" style="font-weight: 700; color: #059669; margin-top: 2px;">0x018 (Unmodified)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Physical Frame (PFN)</div>
            <div id="trans-stat-pfn" style="font-weight: 700; color: #0369a1; margin-top: 2px;">0x07B40</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Final Physical Addr</div>
            <div id="trans-stat-pa" style="font-weight: 700; color: #7c3aed; margin-top: 2px;">0x07B40018</div>
          </div>
        </div>

        <!-- Synchronized SVG Visual Canvas -->
        <div style="display: flex; justify-content: center; margin-bottom: 20px; overflow-x: auto;">
          <svg id="trans-anim-svg" viewBox="0 0 920 260" width="100%" height="auto" style="max-width: 920px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <!-- Stage 1: Virtual Address -->
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
            <path id="trans-bypass-path" d="M 340,120 C 340,165 600,165 600,120" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="470" y="155" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified</text>

            <!-- Lower Topology Console -->
            <g transform="translate(30, 160)">
              <rect x="0" y="0" width="840" height="80" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="20" y="26" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: IDLE</text>
              <text id="trans-console-mid" x="20" y="48" fill="#0f172a" font-size="11" font-family="var(--font-mono)">
                Ready to trace virtual address translation and offset pass-through.
              </text>
              <text id="trans-console-sub" x="20" y="68" fill="#64748b" font-size="10" font-family="var(--font-mono)">
                MMU hardware operating in 4 KiB standard page mode.
              </text>
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
                step: "Step 1: Virtual Address Generation",
                phase: "1. Virtual Address Issued",
                va: "0x00403018",
                vpn: "0x00403",
                offset: "0x018",
                pfn: "Pending...",
                pa: "Pending...",
                activeStages: ["trans-node-va"],
                bypassActive: false,
                consoleTop: "TRANSLATION STEP 1 • VIRTUAL ADDRESS GENERATED",
                consoleMid: "CPU issues load instruction referencing virtual address 0x00403018.",
                consoleSub: "Address is ready for MMU bit-slicing and page table lookup.",
                inlinePreview: "We are at Step 1. The CPU generates virtual address 0x00403018. Next, the MMU slices the address into VPN and Page Offset. Click Next to advance to Step 2.",
                what: "The CPU execution unit issues a load instruction targeting virtual memory address <code>0x00403018</code>. This address is placed on the internal memory management bus.",
                why: "Applications operate entirely in virtual address spaces, completely isolated from physical DRAM hardware frames."
              },
              {
                step: "Step 2: Bit-Slicing (VPN & Offset Separation)",
                phase: "2. Address Bit-Slicing",
                va: "0x00403018",
                vpn: "0x00403 (Bits [47:12])",
                offset: "0x018 (Bits [11:0])",
                pfn: "Pending...",
                pa: "Pending...",
                activeStages: ["trans-node-slice"],
                bypassActive: true,
                consoleTop: "TRANSLATION STEP 2 • ADDRESS BIT-SLICING",
                consoleMid: "Hardware divides 0x00403018 into VPN (0x00403) and Page Offset (0x018).",
                consoleSub: "Lower 12 bits (0x018) enter pass-through wire; upper bits enter page table walker.",
                inlinePreview: "We are at Step 2. The address is split into VPN and Offset. Next, the MMU walks the page table to find the Physical Frame Number. Click Next to advance to Step 3.",
                what: "The MMU hardware bit-slices the address: the upper bits form the <strong>Virtual Page Number (VPN) <code>0x00403</code></strong>, while the lowest 12 bits form the <strong>Page Offset <code>0x018</code></strong>.",
                why: "Standard 4 KiB pages require exactly 12 bits for byte indexing ($2^{12} = 4096$ bytes), leaving the remaining upper bits for page table indexing."
              },
              {
                step: "Step 3: MMU Page Table Walk",
                phase: "3. Page Table Translation",
                va: "0x00403018",
                vpn: "0x00403",
                offset: "0x018",
                pfn: "0x07B40 (Resolved)",
                pa: "0x07B40018 (Assembled)",
                activeStages: ["trans-node-mmu"],
                bypassActive: true,
                consoleTop: "TRANSLATION STEP 3 • MMU PAGE TABLE WALK",
                consoleMid: "MMU indexes VPN 0x00403 into page tables, resolving Physical Frame Number 0x07B40.",
                consoleSub: "Page table entry confirms valid permissions (Present=1, R/W=1, User=1).",
                inlinePreview: "We are at Step 3. PFN 0x07B40 has been resolved. Next, the final physical address is assembled and issued to DRAM. Click Next to advance to Step 4.",
                what: "The MMU uses VPN <code>0x00403</code> to index into the process page table tree, discovering that this virtual page maps to <strong>Physical Frame Number (PFN) <code>0x07B40</code></strong>.",
                why: "Multi-level page tables allow non-contiguous physical RAM to appear as a smooth, continuous address space to every running application."
              },
              {
                step: "Step 4: Offset Pass-Through & Physical Address Assembly",
                phase: "4. Physical Address Issued",
                va: "0x00403018",
                vpn: "0x00403",
                offset: "0x018 (Unmodified)",
                pfn: "0x07B40",
                pa: "0x07B40018 (Complete)",
                activeStages: ["trans-node-pa"],
                bypassActive: true,
                consoleTop: "TRANSLATION STEP 4 • PHYSICAL ADDRESS ASSEMBLED",
                consoleMid: "Combining PFN 0x07B40000 + Offset 0x018 yields physical address 0x07B40018.",
                consoleSub: "Offset passed through 100% untouched. Translation complete and cached in TLB.",
                inlinePreview: "Translation complete! Physical address 0x07B40018 issued to DRAM bus. Click Reset to trace again.",
                what: "The PFN base <code>0x07B40000</code> is combined with the original offset <code>0x018</code>, which passed through completely unmodified, yielding final physical address <strong><code>0x07B40018</code></strong>.",
                why: "Because virtual page size matches physical frame size (4 KiB), the byte offset within the page is identical to the byte offset within the frame, eliminating recalculation overhead."
              }
            ],
            "2m": [
              {
                step: "Superpage Step 1: Virtual Address Issue",
                phase: "1. Superpage VA Issued",
                va: "0x00400000 (2MB Aligned)",
                vpn: "VPN[2:1]: 0x002",
                offset: "0x000 (21-bit Offset)",
                pfn: "Pending...",
                pa: "Pending...",
                activeStages: ["trans-node-va"],
                bypassActive: false,
                consoleTop: "2 MiB SUPERPAGE TRANSLATION • STEP 1",
                consoleMid: "CPU issues load for a large 2 MiB superpage mapping.",
                consoleSub: "Bypasses Level 3 Page Table for faster TLB coverage.",
                inlinePreview: "Superpage Step 1: VA issued. Next, slicing for 2 MiB superpages. Click Next to advance.",
                what: "The CPU targets a large 2 MiB memory region using a single contiguous superpage entry.",
                why: "Superpages reduce TLB pressure for large databases, virtual machines, and game engines by mapping 512 times more memory per TLB entry."
              },
              {
                step: "Superpage Step 2: 21-Bit Offset Pass-Through",
                phase: "2. Large Offset Slicing",
                va: "0x00400000",
                vpn: "VPN[2:1]: 0x002",
                offset: "0x000 (21 bits)",
                pfn: "Pending...",
                pa: "Pending...",
                activeStages: ["trans-node-slice"],
                bypassActive: true,
                consoleTop: "2 MiB SUPERPAGE TRANSLATION • STEP 2",
                consoleMid: "Lower 21 bits pass through completely unmodified as the superpage offset.",
                consoleSub: "Enables massive contiguous physical frame mapping.",
                inlinePreview: "Superpage Step 2: 21-bit offset isolated. Next, resolving base frame. Click Next to advance.",
                what: "Because a 2 MiB superpage spans $2^{21}$ bytes, the lowest 21 bits pass through untouched directly to physical memory.",
                why: "Larger offset pass-through windows eliminate intermediate table walks entirely for large memory buffers."
              },
              {
                step: "Superpage Step 3: PDE Direct Frame Resolution",
                phase: "3. Direct PDE Mapping",
                va: "0x00400000",
                vpn: "VPN[2:1]: 0x002",
                offset: "0x000",
                pfn: "0x04000 (2MB Frame)",
                pa: "0x08000000",
                activeStages: ["trans-node-mmu", "trans-node-pa"],
                bypassActive: true,
                consoleTop: "2 MiB SUPERPAGE TRANSLATION • STEP 3 (COMPLETE)",
                consoleMid: "Page Directory Entry (PDE) maps directly to physical 2 MiB frame 0x08000000.",
                consoleSub: "Superpage translation resolved in fewer MMU lookup cycles.",
                inlinePreview: "Superpage walkthrough complete! 2 MiB translation resolved. Click Reset to restart.",
                what: "The MMU resolves the translation directly at the Page Directory level, pointing to a massive 2 MiB physical DRAM frame.",
                why: "Stopping the page walk early at Level 2 eliminates memory latency and maximizes TLB efficiency."
              }
            ],
            "swap": [
              {
                step: "Swap Fault Step 1: Virtual Address Issued",
                phase: "1. Swapped VA Issued",
                va: "0x00705020",
                vpn: "0x00705",
                offset: "0x020",
                pfn: "None (Present=0)",
                pa: "Page Fault!",
                activeStages: ["trans-node-va", "trans-node-mmu"],
                bypassActive: false,
                consoleTop: "SWAPPED PAGE FAULT WALKTHROUGH • STEP 1",
                consoleMid: "CPU attempts to access virtual address 0x00705020.",
                consoleSub: "MMU inspects page table entry and discovers Present Bit = 0.",
                inlinePreview: "Swap Step 1: VA issued. Next, MMU detects Present=0 and triggers Page Fault trap. Click Next.",
                what: "An application thread tries to load from virtual address <code>0x00705020</code>, which has been evicted to disk swap storage.",
                why: "Demand paging allows systems to overcommit physical RAM by keeping inactive pages on disk."
              },
              {
                step: "Swap Fault Step 2: Kernel Trap & Disk Swap-In",
                phase: "2. Kernel Page Fault Trap",
                va: "0x00705020",
                vpn: "0x00705",
                offset: "0x020",
                pfn: "Frame Allocated: 0x09840",
                pa: "Resolved via Disk",
                activeStages: ["trans-node-slice"],
                bypassActive: true,
                consoleTop: "SWAPPED PAGE FAULT WALKTHROUGH • STEP 2",
                consoleMid: "CPU traps to OS kernel. Kernel allocates frame 0x09840 and reads disk swap.",
                consoleSub: "Data streamed from storage into RAM via DMA.",
                inlinePreview: "Swap Step 2: Kernel allocates frame and loads swap data. Next, updating PTE and restarting instruction. Click Next.",
                what: "The MMU triggers a Page Fault exception. The OS kernel allocates physical frame <code>0x09840</code> and reads the 4 KiB block from disk into RAM.",
                why: "Only the privileged supervisor kernel can access storage controllers and manage backing store swap files."
              },
              {
                step: "Swap Fault Step 3: PTE Update & Instruction Restart",
                phase: "3. Seamless Resume",
                va: "0x00705020",
                vpn: "0x00705",
                offset: "0x020 (Unmodified)",
                pfn: "0x09840",
                pa: "0x09840020 (Complete)",
                activeStages: ["trans-node-pa"],
                bypassActive: true,
                consoleTop: "SWAPPED PAGE FAULT WALKTHROUGH • STEP 3 (COMPLETE)",
                consoleMid: "Kernel sets Present=1 in PTE, flushes TLB, and restarts load instruction.",
                consoleSub: "Offset 0x020 passes through untouched to physical frame 0x09840020.",
                inlinePreview: "Swap walkthrough complete! Page successfully faulted in from disk. Click Reset to restart.",
                what: "The kernel updates the page table entry with Present=1 and frame <code>0x09840</code>, then restarts the instruction using unmodified offset <code>0x020</code>.",
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

            // Preview & Panes
            document.getElementById("trans-inline-preview").innerHTML = data.inlinePreview;
            document.getElementById("trans-desc-what").innerHTML = data.what;
            document.getElementById("trans-desc-why").innerHTML = data.why;

            // SVG labels
            document.getElementById("trans-svg-va").textContent = data.va;
            document.getElementById("trans-svg-slice").textContent = "VPN: " + data.vpn + " | Off: " + data.offset.split(" ")[0];
            document.getElementById("trans-svg-mmu").textContent = "PFN: " + data.pfn.split(" ")[0];
            document.getElementById("trans-svg-pa").textContent = data.pa.split(" ")[0];

            document.getElementById("trans-console-top").textContent = data.consoleTop;
            document.getElementById("trans-console-mid").textContent = data.consoleMid;
            document.getElementById("trans-console-sub").textContent = data.consoleSub;

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
            const allNodes = ["trans-node-va", "trans-node-slice", "trans-node-mmu", "trans-node-pa"];
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
            data.activeStages.forEach(id => {
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

def add_translation_simulator():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if "Interactive Walkthrough: Address Translation &amp; Offset Pass-Through" in content:
        print("--> Address translation simulator already present.")
        return

    # Target marker: right after the second address translation SVG diagram (the bit-slice diagram)
    # Let's locate the second diagram container in Section 3
    target_marker = '<!-- Bottom Label (Shifted Down) -->\n          <text x="40" y="180" fill="#0f172a" font-size="12" font-weight="700">PHYSICAL ADDRESS (Issued to DRAM Memory Bus)</text>'

    # Alternatively, let's find the end of the second diagram's svg block
    diagram_end_marker = '</svg>\n      </div>'

    # Let's search for the second diagram explicitly by looking for "PHYSICAL ADDRESS (Issued to DRAM Memory Bus)"
    pos = content.find("PHYSICAL ADDRESS (Issued to DRAM Memory Bus)")
    if pos != -1:
        # Find the closing tag of that svg container
        svg_close = content.find("</svg>", pos)
        if svg_close != -1:
            div_close = content.find("</div>", svg_close)
            if div_close != -1:
                insert_pos = div_close + 6
                content = content[:insert_pos] + "\n\n" + TRANSLATION_SIMULATOR_HTML + content[insert_pos:]
                print("--> Injected Address Translation simulator after the bit-slice diagram.")
            else:
                print("--> Error: Could not locate diagram container closing div.")
                return
        else:
            print("--> Error: Could not locate diagram closing svg tag.")
            return
    else:
        print("--> Error: Target bit-slice diagram header not found.")
        return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add interactive bit-slice and offset pass-through simulator to Module 2\n\n"
            "Embed a directed narrative stepper simulator for virtual-to-physical\n"
            "address translation and page offset pass-through in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for address translation simulator!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_translation_simulator()
