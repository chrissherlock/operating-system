#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject cross-architecture (x86-64, ARM64, RISC-V) MMU stepper
# =====================================================================
import os
import re
import subprocess

MMU_SIMULATOR_COMPONENT = """
      <!-- Interactive Directed Narrative Stepper: MMU & Address Translation -->
      <div id="interactive-mmu-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <!-- Header & Architecture Selectors -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Guided Walkthrough: Cross-Architecture MMU &amp; Page Fault Lifecycle</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Observe address translation, page walks, and trap registers across x86-64, ARM64, and RISC-V silicon.</p>
          </div>

          <!-- Dual Selectors: Architecture & Scenario -->
          <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px;">
            <!-- Arch Selector -->
            <div style="display: flex; align-items: center; gap: 4px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
              <span style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #475569; padding: 0 4px;">Arch:</span>
              <button id="btn-mmu-x86" class="mmu-arch-btn" style="padding: 4px 10px; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">x86-64</button>
              <button id="btn-mmu-arm" class="mmu-arch-btn" style="padding: 4px 10px; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">ARM64 (AArch64)</button>
              <button id="btn-mmu-riscv" class="mmu-arch-btn" style="padding: 4px 10px; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">RISC-V (Sv39)</button>
            </div>

            <!-- Scenario Selector -->
            <div style="display: flex; align-items: center; gap: 4px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
              <span style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #475569; padding: 0 4px;">Scenario:</span>
              <button id="btn-mmu-scen-walk" class="mmu-scen-btn" style="padding: 4px 10px; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">TLB Miss &amp; Walk</button>
              <button id="btn-mmu-scen-fault" class="mmu-scen-btn" style="padding: 4px 10px; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Page Fault &amp; Swap</button>
            </div>
          </div>
        </div>

        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">How to Use This Simulator</div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            <li><strong>Toggle CPU Architectures:</strong> Switch between <code>x86-64</code>, <code>ARM64 (AArch64)</code>, and <code>RISC-V (Sv39)</code> to compare hardware root registers (<code>CR3</code> vs <code>TTBR0_EL1</code> vs <code>satp</code>) and exception traps (<code>CR2</code> vs <code>FAR_EL1</code> vs <code>stval</code>).</li>
            <li><strong>Select the Memory Scenario:</strong> Trace a cold <code>TLB Miss &amp; Walk</code> resolving via page directories or a supervisor <code>Page Fault &amp; Swap</code> resolution.</li>
            <li><strong>Preview Upcoming Actions:</strong> Read the adjacent action pane before advancing to anticipate hardware and operating system state changes.</li>
          </ol>
        </div>

        <!-- Controls & Adjacent Next Step Card -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="mmu-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step &rarr;</button>
            <div style="display: flex; gap: 8px;">
              <button id="mmu-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">&larr; Prev</button>
              <button id="mmu-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Upcoming Action When You Click Next:</div>
            <div id="mmu-inline-next-desc" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">Loading step information...</div>
          </div>
        </div>

        <!-- Telemetry State Bar -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.8rem;">
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Virtual Address</div>
            <div id="mmu-status-vaddr" style="font-weight: 700; color: #0f172a; margin-top: 2px;">0x00403018</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">VPN / Offset</div>
            <div id="mmu-status-vpn" style="font-weight: 700; color: #0284c7; margin-top: 2px;">VPN: 0x00403 | 0x018</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Root Register</div>
            <div id="mmu-status-root" style="font-weight: 700; color: #0f172a; margin-top: 2px;">CR3: 0x1A4000</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Fault Register</div>
            <div id="mmu-status-faultreg" style="font-weight: 700; color: #475569; margin-top: 2px;">CR2: Clean</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Physical Target</div>
            <div id="mmu-status-paddr" style="font-weight: 700; color: #0369a1; margin-top: 2px;">Translating...</div>
          </div>
        </div>

        <!-- SVG Architecture Canvas -->
        <div style="display: flex; justify-content: center; margin-bottom: 20px; overflow-x: auto;">
          <svg id="mmu-anim-svg" viewBox="0 0 940 280" width="100%" height="auto" style="max-width: 940px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <!-- Interconnect Bus Bar -->
            <rect x="25" y="130" width="890" height="20" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" />
            <text x="470" y="144" fill="#475569" font-size="10" font-weight="700" text-anchor="middle">CPU INTERNAL &amp; SYSTEM MEMORY INTERCONNECT</text>

            <!-- Node 1: CPU Execution Core (x: 25, w: 165) -->
            <g id="mmu-node-cpu" transform="translate(25, 30)">
              <rect x="0" y="0" width="165" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="82" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">1. CPU Core</text>
              <text id="mmu-node1-sub" x="82" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Issues Memory Load</text>
              <text id="mmu-node1-val" x="82" y="56" fill="#0284c7" font-size="9" text-anchor="middle">VA: 0x00403018</text>
            </g>

            <!-- Node 2: On-Die TLB Cache (x: 210, w: 165) -->
            <g id="mmu-node-tlb" transform="translate(210, 30)">
              <rect x="0" y="0" width="165" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="82" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">2. On-Die TLB</text>
              <text id="mmu-node2-state" x="82" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Tag Array Search</text>
              <text id="mmu-node2-tag" x="82" y="56" fill="#0284c7" font-size="9" text-anchor="middle">VPN Tag Matching</text>
            </g>

            <!-- Node 3: Page Table Walker / Hardware MMU (x: 395, w: 165) -->
            <g id="mmu-node-ptw" transform="translate(395, 30)">
              <rect x="0" y="0" width="165" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text id="mmu-node3-title" x="82" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">3. Page Table Walker</text>
              <text id="mmu-node3-sub" x="82" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Root: CR3 / TTBR0</text>
              <text id="mmu-node3-detail" x="82" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Traverses Tree in RAM</text>
            </g>

            <!-- Node 4: Physical DRAM (x: 580, w: 165) -->
            <g id="mmu-node-ram" transform="translate(580, 30)">
              <rect x="0" y="0" width="165" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text id="mmu-node4-title" x="82" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">4. Physical RAM</text>
              <text id="mmu-node4-sub" x="82" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Target Page Frame</text>
              <text id="mmu-node4-detail" x="82" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Frame: 0x07B4000</text>
            </g>

            <!-- Node 5: Disk Backing Store / Swap (x: 765, w: 150) -->
            <g id="mmu-node-disk" transform="translate(765, 30)">
              <rect x="0" y="0" width="150" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text id="mmu-node5-title" x="75" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">5. Swap / Disk</text>
              <text id="mmu-node5-sub" x="75" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Backing Store File</text>
              <text id="mmu-node5-detail" x="75" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Inactive in Hit</text>
            </g>

            <!-- Vertical Bus Drops -->
            <line id="mmu-line-1" x1="107" y1="95" x2="107" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="mmu-line-2" x1="292" y1="95" x2="292" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="mmu-line-3" x1="477" y1="95" x2="477" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="mmu-line-4" x1="662" y1="95" x2="662" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="mmu-line-5" x1="840" y1="95" x2="840" y2="130" stroke="#cbd5e1" stroke-width="2" />

            <!-- Dynamic Bottom Mapping Console -->
            <g transform="translate(25, 175)">
              <rect x="0" y="0" width="890" height="85" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text x="20" y="25" fill="#0369a1" font-size="11" font-weight="700">ACTIVE TRANSLATION STAGE &amp; BUS STATUS</text>
              <text id="mmu-flow-title" x="20" y="48" fill="#0f172a" font-size="11" font-family="var(--font-mono)">
                CPU issues virtual load &rarr; MMU evaluates TLB tag cache.
              </text>
              <text id="mmu-flow-sub" x="20" y="68" fill="#64748b" font-size="10" font-family="var(--font-mono)">
                Initial request staged. Checking on-die cache lines.
              </text>
            </g>
          </svg>
        </div>

        <!-- Paired Analytical Panes -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <!-- What Is Happening -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">What Is Happening</div>
            <div id="mmu-desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <!-- Why The System Does This -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="mmu-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const crossArchData = {
            "x86": {
              name: "x86-64",
              rootName: "CR3",
              faultName: "CR2",
              levels: "4-Level (PML4 &rarr; PDPT &rarr; PD &rarr; PT)",
              walk: [
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: Clean",
                  paddr: "Translating...",
                  activeNode: "mmu-node-cpu",
                  activeLine: "mmu-line-1",
                  btnNextText: "Next: Query TLB &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The MMU will query the L1/L2 data TLB tag array to see if VPN 0x00403 is already cached.",
                  flowTitle: "x86-64 INSTRUCTION FETCH &rarr; Splitting 48-bit Canonical Virtual Address",
                  flowSub: "CPU decodes MOV RAX, [0x00403018]. Bits [47:12] define VPN; bits [11:0] define page offset.",
                  what: "An application executes a load instruction from heap address <code>0x00403018</code>. The x86-64 core decomposes the 48-bit address into a 36-bit Virtual Page Number (<code>0x00403</code>) and a 12-bit Page Offset (<code>0x018</code>).",
                  why: "Separating page index from intra-page byte offset allows hardware to manage memory allocation in standardized 4 KiB units while maintaining precise single-byte addressing."
                },
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: Clean",
                  paddr: "Translating...",
                  activeNode: "mmu-node-tlb",
                  activeLine: "mmu-line-2",
                  btnNextText: "Next: Walk 4-Level Page Table &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The hardware MMU page table walker will load root physical address from register CR3 and traverse DRAM.",
                  flowTitle: "x86-64 TLB TAG COMPARISON &rarr; Cache Miss Detected",
                  flowSub: "VPN 0x00403 is absent in L1/L2 TLB. MMU initiates a hardware walk using root pointer in CR3.",
                  what: "The MMU checks the on-die TLB. The tag comparison fails to find VPN <code>0x00403</code>. The hardware signals a <strong>TLB Miss</strong> and activates the hardware page table walker.",
                  why: "The TLB is kept small (typically 64 to 1536 entries) to maintain single-cycle associative lookup speeds. Uncached entries require walking the multi-level page table stored in main memory."
                },
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: Clean",
                  paddr: "Base: 0x07B40000",
                  activeNode: "mmu-node-ptw",
                  activeLine: "mmu-line-3",
                  btnNextText: "Next: Read Physical DRAM &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The MMU will append offset 0x018 to physical frame base 0x07B40000 and insert the translation into the TLB.",
                  flowTitle: "x86-64 HARDWARE WALK &rarr; PML4 &rarr; PDPT &rarr; PD &rarr; PT Entry Found",
                  flowSub: "MMU reads Page Table Entry in RAM: Physical Frame 0x07B40 with Present=1, R/W=1, User=1.",
                  what: "The MMU reads root physical pointer <code>0x1A4000</code> from register <strong>CR3</strong>. It walks the 4-level tree (PML4 &rarr; PDPT &rarr; PD &rarr; PT). The final Page Table Entry yields <strong>Physical Frame Number 0x07B40</strong> with Present=1 and User/Supervisor=1.",
                  why: "Hierarchical page tables permit sparse address spaces: unallocated 2 MiB or 1 GiB virtual address ranges require zero page tables, conserving physical RAM."
                },
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: Clean",
                  paddr: "0x07B40018",
                  activeNode: "mmu-node-ram",
                  activeLine: "mmu-line-4",
                  btnNextText: "Restart Walkthrough &#8634;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "Translation complete. The mapping is now cached in the TLB for single-cycle future access.",
                  flowTitle: "x86-64 PHYSICAL ACCESS &rarr; Issuing 0x07B40018 to Memory Bus",
                  flowSub: "MMU inserts translation into TLB and loads 64-bit word from DRAM into RAX.",
                  what: "The MMU combines frame address <code>0x07B40000</code> with the original 12-bit offset <code>0x018</code> to generate physical address <code>0x07B40018</code>. It caches the mapping in the TLB and reads the data from DRAM.",
                  why: "Inserting the translation into the TLB guarantees that subsequent instruction executions accessing this 4 KiB page resolve in a single clock cycle without touching RAM page tables."
                }
              ],
              fault: [
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: Clean",
                  paddr: "None (P=0)",
                  activeNode: "mmu-node-cpu",
                  activeLine: "mmu-line-1",
                  btnNextText: "Next: Walk Page Table &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The MMU will walk the page table and check the Present bit in the PTE.",
                  flowTitle: "x86-64 MEMORY ACCESS &rarr; Accessing Evicted / Swapped Virtual Page",
                  flowSub: "Application references heap address 0x00705020. Data currently resides in swap storage.",
                  what: "An application thread accesses address <code>0x00705020</code> in a memory region whose page was previously evicted to disk swap by the operating system kernel.",
                  why: "Operating systems overcommit memory: inactive pages are written to backing store storage so active processes can make use of high-speed DRAM."
                },
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: 0x00705020",
                  paddr: "TRAP to Kernel",
                  activeNode: "mmu-node-ptw",
                  activeLine: "mmu-line-3",
                  btnNextText: "Next: Fire Page Fault (Int 14) &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The CPU will store the faulting virtual address in register CR2 and invoke Interrupt 14 in the kernel IDT.",
                  flowTitle: "x86-64 MMU EXCEPTION &rarr; Present Bit = 0 Triggers Interrupt 14",
                  flowSub: "Hardware stores faulting address in CR2 and transfers control to kernel page fault handler.",
                  what: "The MMU walks the page tables and finds that <strong>Present Bit = 0</strong> in the PTE. The MMU halts execution, places faulting address <code>0x00705020</code> into register <strong>CR2</strong>, pushes an error code, and fires <strong>Interrupt 14</strong>.",
                  why: "Hardware cannot perform file system operations or disk I/O. The MMU must trap into the supervisor kernel so the OS can allocate a physical frame and retrieve data from storage."
                },
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: 0x00705020",
                  paddr: "Allocating Frame...",
                  activeNode: "mmu-node-disk",
                  activeLine: "mmu-line-5",
                  btnNextText: "Next: Swap In from Storage &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The kernel storage driver will allocate a physical frame and read the 4 KiB block from disk into memory.",
                  flowTitle: "x86-64 KERNEL PAGE FAULT HANDLER &rarr; Swap File Read",
                  flowSub: "OS allocates physical Frame 0x09210 and initiates NVMe/SATA DMA block transfer.",
                  what: "The kernel page fault handler reads register <strong>CR2</strong>, confirms the address is valid in the process memory map, allocates a free physical frame (<code>0x09210</code>), and issues a read command to swap storage.",
                  why: "Demand paging allows systems to run workloads larger than installed physical RAM by treating disk storage as a slower extension of the memory hierarchy."
                },
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "CR3: 0x1A4000",
                  faultreg: "CR2: Clean",
                  paddr: "0x09210020",
                  activeNode: "mmu-node-ram",
                  activeLine: "mmu-line-4",
                  btnNextText: "Restart Walkthrough &#8634;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The kernel executes IRET. The CPU seamlessly retries the faulting instruction with the page resident in RAM.",
                  flowTitle: "x86-64 PTE UPDATE &rarr; Setting Present=1 &amp; Issuing IRET",
                  flowSub: "PTE points to Frame 0x09210. CPU returns to user mode and restarts instruction.",
                  what: "Storage transfer completes. The kernel writes physical frame <code>0x09210</code> into the PTE, sets <strong>Present Bit = 1</strong>, executes <code>INVLPG</code> to clear stale TLB entries, and issues <code>IRET</code>. The CPU restarts the faulting instruction transparently.",
                  why: "Demand paging is fully transparent to user software. The application experiences a temporary I/O stall, but requires no custom error-handling logic."
                }
              ]
            },
            "arm": {
              name: "ARM64 (AArch64)",
              rootName: "TTBR0_EL1",
              faultName: "FAR_EL1",
              levels: "4-Level Translation (L0 &rarr; L1 &rarr; L2 &rarr; L3)",
              walk: [
                {
                  vaddr: "0x00000000403018",
                  vpn: "VPN: 0x0000403 | Off: 0x018",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: Clean",
                  paddr: "Translating...",
                  activeNode: "mmu-node-cpu",
                  activeLine: "mmu-line-1",
                  btnNextText: "Next: Query Micro-TLB &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The ARM64 MMU will query the L1/L2 Unified TLB using the ASID tagged in TTBR0_EL1.",
                  flowTitle: "ARM64 INSTRUCTION FETCH &rarr; Evaluating TTBR0_EL1 User Range",
                  flowSub: "CPU decodes LDR X0, [X1]. Bit 63=0 selects TTBR0_EL1 (User Space) over TTBR1_EL1 (Kernel Space).",
                  what: "An ARM64 core decodes an instruction loading from address <code>0x00000000403018</code>. Because the top address bits are 0, the MMU knows this address belongs to user space and selects <strong>TTBR0_EL1</strong> (Translation Table Base Register 0).",
                  why: "ARM64 cleanly splits the virtual address space in hardware: user addresses use TTBR0_EL1, while supervisor addresses use TTBR1_EL1, eliminating the need to flush kernel mappings on user context switches."
                },
                {
                  vaddr: "0x00000000403018",
                  vpn: "VPN: 0x0000403 | Off: 0x018",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: Clean",
                  paddr: "Translating...",
                  activeNode: "mmu-node-tlb",
                  activeLine: "mmu-line-2",
                  btnNextText: "Next: Walk Translation Tables &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The ARM64 MMU translation table walk unit will load table base from TTBR0_EL1.",
                  flowTitle: "ARM64 TLB LOOKUP &rarr; Tag Miss with ASID Filtering",
                  flowSub: "TLB tag check fails for VPN 0x0000403 with current ASID. Hardware triggers translation table walk.",
                  what: "The ARM64 MMU searches the TLB. The entry is not present for the current <strong>ASID (Address Space ID)</strong>. The hardware flags a TLB miss and begins a translation table walk.",
                  why: "ARM64 embeds the process ASID directly in the TLB tag. Multiple processes can share the TLB simultaneously without entries colliding or requiring flushes across context switches."
                },
                {
                  vaddr: "0x00000000403018",
                  vpn: "VPN: 0x0000403 | Off: 0x018",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: Clean",
                  paddr: "Base: 0x08C20000",
                  activeNode: "mmu-node-ptw",
                  activeLine: "mmu-line-3",
                  btnNextText: "Next: Read Physical DRAM &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The MMU will append offset 0x018 to the resolved physical base and insert the descriptor into the TLB.",
                  flowTitle: "ARM64 TABLE WALK &rarr; Levels 0 &rarr; 1 &rarr; 2 &rarr; 3 Page Descriptor",
                  flowSub: "MMU reads Level 3 Descriptor: Physical Output Address 0x08C20000, Valid Bit=1, AF=1.",
                  what: "The MMU reads the Level 0 base table from <strong>TTBR0_EL1</strong> (physical address <code>0x2B8000</code>) and traverses translation levels L0 &rarr; L1 &rarr; L2 &rarr; L3. The Level 3 descriptor yields <strong>Physical Address 0x08C20000</strong> with Valid=1.",
                  why: "ARM64 page tables support configurable translation granule sizes (4 KiB, 16 KiB, or 64 KiB), allowing operating systems to choose optimal trade-offs between mapping granularity and table overhead."
                },
                {
                  vaddr: "0x00000000403018",
                  vpn: "VPN: 0x0000403 | Off: 0x018",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: Clean",
                  paddr: "0x08C20018",
                  activeNode: "mmu-node-ram",
                  activeLine: "mmu-line-4",
                  btnNextText: "Restart Walkthrough &#8634;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "Translation complete. The mapping is cached in the ARM64 TLB with its active ASID tag.",
                  flowTitle: "ARM64 PHYSICAL ACCESS &rarr; Emitting 0x08C20018 over Interconnect",
                  flowSub: "Data loaded from DRAM into register X0. Translation cached in L1 Data TLB.",
                  what: "The MMU combines the physical page address with offset <code>0x018</code> to form <code>0x08C20018</code>. The CPU fetches the data from physical DRAM into register <code>X0</code> and caches the translation in the TLB.",
                  why: "Caching both the physical translation and memory attributes (Normal vs Device memory, inner/outer shareability) guarantees future accesses bypass table walks completely."
                }
              ],
              fault: [
                {
                  vaddr: "0x00000000705020",
                  vpn: "VPN: 0x0000705 | Off: 0x020",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: Clean",
                  paddr: "None (Valid=0)",
                  activeNode: "mmu-node-cpu",
                  activeLine: "mmu-line-1",
                  btnNextText: "Next: Walk Translation Table &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The ARM64 MMU will evaluate the translation descriptor and discover Valid Bit = 0.",
                  flowTitle: "ARM64 MEMORY ACCESS &rarr; Accessing Non-Resident Virtual Address",
                  flowSub: "Application accesses 0x00000000705020. Data is currently paged out to disk backing store.",
                  what: "A user thread running at Exception Level 0 (EL0) accesses address <code>0x00000000705020</code>, referencing a virtual page currently not resident in physical memory.",
                  why: "Paging enables efficient memory sharing and dynamic allocation on memory-constrained mobile and server ARM64 architectures."
                },
                {
                  vaddr: "0x00000000705020",
                  vpn: "VPN: 0x0000705 | Off: 0x020",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: 0x00000000705020",
                  paddr: "TRAP to EL1",
                  activeNode: "mmu-node-ptw",
                  activeLine: "mmu-line-3",
                  btnNextText: "Next: Fire Translation Fault &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The CPU will store the faulting address in FAR_EL1 and syndrome code in ESR_EL1, trapping to EL1.",
                  flowTitle: "ARM64 TRANSLATION FAULT &rarr; Exception Raised to EL1 (Kernel)",
                  flowSub: "Hardware populates FAR_EL1 with faulting address and ESR_EL1 with exception syndrome.",
                  what: "The MMU walks the table and finds the Level 3 descriptor has <strong>Bit 0 (Valid) = 0</strong>. The CPU halts execution, saves the address to <strong>FAR_EL1</strong> (Fault Address Register), writes the cause into <strong>ESR_EL1</strong>, and traps to kernel mode at EL1.",
                  why: "ARM64 categorizes faults cleanly: ESR_EL1 details whether the fault was a translation fault, permission fault, or access flag fault, speeding up kernel dispatching."
                },
                {
                  vaddr: "0x00000000705020",
                  vpn: "VPN: 0x0000705 | Off: 0x020",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: 0x00000000705020",
                  paddr: "Allocating Frame...",
                  activeNode: "mmu-node-disk",
                  activeLine: "mmu-line-5",
                  btnNextText: "Next: Swap In from Storage &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The kernel disk driver will stream the page from storage into a newly allocated RAM frame.",
                  flowTitle: "ARM64 KERNEL FAULT DISPATCH &rarr; Reading Storage Swap",
                  flowSub: "Kernel reads FAR_EL1, allocates physical frame 0x09530000, and triggers DMA block read.",
                  what: "The kernel reads <strong>FAR_EL1</strong> to identify the missing address, allocates physical RAM frame <code>0x09530000</code>, and initiates a DMA transfer from storage backing store into memory.",
                  why: "Demand paging allows the OS to run large binaries by loading only executable sections as they are touched by the instruction pointer."
                },
                {
                  vaddr: "0x00000000705020",
                  vpn: "VPN: 0x0000705 | Off: 0x020",
                  root: "TTBR0_EL1: 0x2B8000",
                  faultreg: "FAR_EL1: Clean",
                  paddr: "0x09530020",
                  activeNode: "mmu-node-ram",
                  activeLine: "mmu-line-4",
                  btnNextText: "Restart Walkthrough &#8634;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The kernel executes ERET. The CPU transparently restarts the instruction at EL0 with the page now in RAM.",
                  flowTitle: "ARM64 DESCRIPTOR UPDATE &rarr; TLBI Invalidation &amp; ERET",
                  flowSub: "Kernel sets Valid=1 in Level 3 descriptor, executes TLBI to flush stale tags, and returns via ERET.",
                  what: "Storage transfer completes. The kernel sets Valid=1 in the Level 3 descriptor, executes <code>TLBI VAE1IS</code> to invalidate any stale TLB lines, and issues <code>ERET</code>. The CPU returns to EL0 and restarts the load instruction.",
                  why: "The application resumes without ever knowing a disk read occurred. Hardware and kernel collaboration provides seamless virtual memory abstraction."
                }
              ]
            },
            "riscv": {
              name: "RISC-V (Sv39)",
              rootName: "satp",
              faultName: "stval",
              levels: "3-Level Translation (VPN[2] &rarr; VPN[1] &rarr; VPN[0])",
              walk: [
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: Clean",
                  paddr: "Translating...",
                  activeNode: "mmu-node-cpu",
                  activeLine: "mmu-line-1",
                  btnNextText: "Next: Query TLB &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The RISC-V MMU will check the translation cache for the VPN and ASID stored in satp.",
                  flowTitle: "RISC-V Sv39 FETCH &rarr; Decomposing 39-bit Virtual Address",
                  flowSub: "Address decomposes into three 9-bit VPN fields (VPN[2], VPN[1], VPN[0]) and 12-bit offset.",
                  what: "A user program executing in U-mode issues a load from address <code>0x00403018</code>. Under RISC-V <strong>Sv39</strong> virtual memory, the 39-bit address is split into three 9-bit page directory indexes and a 12-bit offset.",
                  why: "RISC-V uses modular address sizes (Sv39, Sv48, Sv57). Sv39 provides a 512 GiB virtual address space with small 3-level page tables, ideal for efficient embedded and server silicon."
                },
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: Clean",
                  paddr: "Translating...",
                  activeNode: "mmu-node-tlb",
                  activeLine: "mmu-line-2",
                  btnNextText: "Next: Walk Sv39 Page Table &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The hardware will read the root page table physical address from the satp register.",
                  flowTitle: "RISC-V TLB SEARCH &rarr; Cache Miss Detected",
                  flowSub: "No matching tag found in TLB. Hardware activates multi-level page table walk.",
                  what: "The MMU searches the TLB. The tag comparison fails. The MMU raises a TLB miss and begins walking the Sv39 page tables in memory.",
                  why: "Caching translations avoids repeated memory reads. A miss forces the hardware to read up to three 64-bit page table entries from RAM."
                },
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: Clean",
                  paddr: "Base: 0x08E10000",
                  activeNode: "mmu-node-ptw",
                  activeLine: "mmu-line-3",
                  btnNextText: "Next: Read Physical DRAM &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The MMU will append offset 0x018 to the resolved PPN and insert the entry into the TLB.",
                  flowTitle: "RISC-V Sv39 WALK &rarr; Traverses Level 2 &rarr; 1 &rarr; 0 PTEs",
                  flowSub: "Hardware locates leaf PTE: PPN 0x08E10, Valid=1, Readable=1, User=1.",
                  what: "The MMU reads the root Physical Page Number from register <strong>satp</strong> (Supervisor Address Translation and Protection). It traverses indexes VPN[2] &rarr; VPN[1] &rarr; VPN[0]. The leaf entry reveals <strong>Physical Page Number 0x08E10</strong> with Valid=1 and User=1.",
                  why: "RISC-V allows non-leaf PTEs to be marked as valid leaves, providing native hardware support for 2 MiB (megapage) and 1 GiB (gigapage) superpages without extra hardware complexity."
                },
                {
                  vaddr: "0x00403018",
                  vpn: "VPN: 0x00403 | Off: 0x018",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: Clean",
                  paddr: "0x08E10018",
                  activeNode: "mmu-node-ram",
                  activeLine: "mmu-line-4",
                  btnNextText: "Restart Walkthrough &#8634;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "Translation complete. Translation cached in RISC-V TLB.",
                  flowTitle: "RISC-V PHYSICAL ACCESS &rarr; Issuing 0x08E10018 to Bus",
                  flowSub: "DRAM returns data word into CPU register. TLB caches mapping.",
                  what: "The MMU appends offset <code>0x018</code> to physical base <code>0x08E10000</code>, creating physical address <code>0x08E10018</code>. The CPU loads data from RAM and stores the translation in the TLB.",
                  why: "Future accesses to this 4 KiB range will hit the TLB, bypassing memory reads until an <code>sfence.vma</code> instruction invalidates the cache."
                }
              ],
              fault: [
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: Clean",
                  paddr: "None (Valid=0)",
                  activeNode: "mmu-node-cpu",
                  activeLine: "mmu-line-1",
                  btnNextText: "Next: Walk Page Table &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The MMU will walk the Sv39 page table and inspect the leaf PTE Valid bit.",
                  flowTitle: "RISC-V MEMORY ACCESS &rarr; Accessing Swapped Address",
                  flowSub: "Application references address 0x00705020 in unmapped/swapped memory space.",
                  what: "An unprivileged application thread running in U-mode attempts to load from address <code>0x00705020</code>. The data is currently stored in disk swap.",
                  why: "Virtual memory isolates processes and permits memory overcommit across desktop and server RISC-V implementations."
                },
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: 0x00705020",
                  paddr: "TRAP to S-mode",
                  activeNode: "mmu-node-ptw",
                  activeLine: "mmu-line-3",
                  btnNextText: "Next: Fire Page Fault (Cause 13) &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The CPU will store the fault address into stval and raise Load Page Fault (Cause 13) to S-mode.",
                  flowTitle: "RISC-V EXCEPTION &rarr; Load Page Fault (scause = 13)",
                  flowSub: "MMU halts walk. CPU records faulting address in stval and traps to supervisor.",
                  what: "The MMU finds <strong>Bit 0 (Valid) = 0</strong> in the PTE. The CPU writes faulting address <code>0x00705020</code> into register <strong>stval</strong> (Supervisor Trap Value), sets <strong>scause</strong> to 13 (Load Page Fault), and transfers control to the S-mode kernel.",
                  why: "RISC-V separates trap value (stval) from trap reason (scause), giving supervisor software an unambiguous, clean interface to diagnose memory faults."
                },
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: 0x00705020",
                  paddr: "Allocating Frame...",
                  activeNode: "mmu-node-disk",
                  activeLine: "mmu-line-5",
                  btnNextText: "Next: Swap In from Storage &rarr;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The supervisor kernel will allocate a physical frame and issue a storage transfer.",
                  flowTitle: "RISC-V KERNEL TRAP DISPATCH &rarr; Reading Swap Storage",
                  flowSub: "OS inspects stval, allocates Frame 0x09840, and starts disk block read.",
                  what: "The S-mode kernel reads <strong>stval</strong>, allocates physical memory frame <code>0x09840000</code>, and initiates a DMA transfer from storage backing store.",
                  why: "The operating system transparently handles page allocation while application execution remains paused."
                },
                {
                  vaddr: "0x00705020",
                  vpn: "VPN: 0x00705 | Off: 0x020",
                  root: "satp: 0x800000000008A100",
                  faultreg: "stval: Clean",
                  paddr: "0x09840020",
                  activeNode: "mmu-node-ram",
                  activeLine: "mmu-line-4",
                  btnNextText: "Restart Walkthrough &#8634;",
                  btnPrevText: "&larr; Prev",
                  inlineNext: "The kernel executes sret. The CPU transparently restarts the faulting load instruction.",
                  flowTitle: "RISC-V PTE UPDATE &rarr; sfence.vma &amp; sret Execution",
                  flowSub: "PTE updated with Frame 0x09840, Valid=1. CPU flushes TLB and returns via sret.",
                  what: "The storage transfer completes. The kernel writes PPN <code>0x09840</code> into the PTE, sets <strong>Valid = 1</strong>, executes <code>sfence.vma</code> to synchronize the TLB, and issues <code>sret</code>. The CPU returns to U-mode and restarts the instruction.",
                  why: "The application resumes seamlessly without knowing a disk transfer occurred. Hardware and kernel collaborate to preserve the illusion of infinite memory."
                }
              ]
            }
          };

          let currentArch = "x86";
          let currentScen = "walk";
          let stepIndex = 0;

          function renderState() {
            const archObj = crossArchData[currentArch];
            const data = archObj[currentScen][stepIndex];

            document.getElementById("mmu-status-vaddr").textContent = data.vaddr;
            document.getElementById("mmu-status-vpn").textContent = data.vpn;
            document.getElementById("mmu-status-root").textContent = data.root;
            document.getElementById("mmu-status-faultreg").textContent = data.faultreg;
            document.getElementById("mmu-status-paddr").textContent = data.paddr;

            document.getElementById("mmu-inline-next-desc").innerHTML = data.inlineNext;
            document.getElementById("mmu-desc-what").innerHTML = data.what;
            document.getElementById("mmu-desc-why").innerHTML = data.why;

            document.getElementById("mmu-flow-title").innerHTML = data.flowTitle;
            document.getElementById("mmu-flow-sub").innerHTML = data.flowSub;

            document.getElementById("mmu-node1-val").textContent = "VA: " + data.vaddr;
            document.getElementById("mmu-node3-sub").textContent = "Root: " + archObj.rootName;

            const nextBtn = document.getElementById("mmu-next-btn");
            const prevBtn = document.getElementById("mmu-prev-btn");

            if (nextBtn) nextBtn.innerHTML = data.btnNextText;
            if (prevBtn) {
              prevBtn.innerHTML = data.btnPrevText;
              prevBtn.style.opacity = stepIndex === 0 ? "0.5" : "1.0";
              prevBtn.style.cursor = stepIndex === 0 ? "not-allowed" : "pointer";
            }

            const allNodes = ["mmu-node-cpu", "mmu-node-tlb", "mmu-node-ptw", "mmu-node-ram", "mmu-node-disk"];
            allNodes.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                const rect = el.querySelector("rect");
                if (rect) {
                  rect.setAttribute("stroke", "#cbd5e1");
                  rect.setAttribute("stroke-width", "1.5");
                  rect.setAttribute("fill", "#ffffff");
                }
              }
            });

            const allLines = ["mmu-line-1", "mmu-line-2", "mmu-line-3", "mmu-line-4", "mmu-line-5"];
            allLines.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#cbd5e1");
                el.setAttribute("stroke-width", "2");
              }
            });

            const activeNodeEl = document.getElementById(data.activeNode);
            if (activeNodeEl) {
              const rect = activeNodeEl.querySelector("rect");
              if (rect) {
                rect.setAttribute("stroke", "#0284c7");
                rect.setAttribute("stroke-width", "2.5");
                rect.setAttribute("fill", "#f0f9ff");
              }
            }

            const activeLineEl = document.getElementById(data.activeLine);
            if (activeLineEl) {
              activeLineEl.setAttribute("stroke", "#0284c7");
              activeLineEl.setAttribute("stroke-width", "3");
            }
          }

          function setArch(archKey) {
            currentArch = archKey;
            stepIndex = 0;
            const buttons = {
              "x86": document.getElementById("btn-mmu-x86"),
              "arm": document.getElementById("btn-mmu-arm"),
              "riscv": document.getElementById("btn-mmu-riscv")
            };
            Object.keys(buttons).forEach(key => {
              const btn = buttons[key];
              if (btn) {
                if (key === archKey) {
                  btn.style.background = "#0284c7";
                  btn.style.color = "#ffffff";
                } else {
                  btn.style.background = "transparent";
                  btn.style.color = "#475569";
                }
              }
            });
            renderState();
          }

          function setScen(scenKey) {
            currentScen = scenKey;
            stepIndex = 0;
            const btnWalk = document.getElementById("btn-mmu-scen-walk");
            const btnFault = document.getElementById("btn-mmu-scen-fault");
            if (scenKey === "walk") {
              btnWalk.style.background = "#0284c7";
              btnWalk.style.color = "#ffffff";
              btnFault.style.background = "transparent";
              btnFault.style.color = "#475569";
            } else {
              btnFault.style.background = "#0284c7";
              btnFault.style.color = "#ffffff";
              btnWalk.style.background = "transparent";
              btnWalk.style.color = "#475569";
            }
            renderState();
          }

          document.getElementById("btn-mmu-x86").addEventListener("click", () => setArch("x86"));
          document.getElementById("btn-mmu-arm").addEventListener("click", () => setArch("arm"));
          document.getElementById("btn-mmu-riscv").addEventListener("click", () => setArch("riscv"));

          document.getElementById("btn-mmu-scen-walk").addEventListener("click", () => setScen("walk"));
          document.getElementById("btn-mmu-scen-fault").addEventListener("click", () => setScen("fault"));

          document.getElementById("mmu-next-btn").addEventListener("click", function() {
            const list = crossArchData[currentArch][currentScen];
            if (stepIndex < list.length - 1) {
              stepIndex++;
            } else {
              stepIndex = 0;
            }
            renderState();
          });

          document.getElementById("mmu-prev-btn").addEventListener("click", function() {
            if (stepIndex > 0) {
              stepIndex--;
              renderState();
            }
          });

          document.getElementById("mmu-reset-btn").addEventListener("click", function() {
            stepIndex = 0;
            renderState();
          });

          renderState();
        })();
      </script>
"""

def update_mmu_simulator_component():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<div id="interactive-mmu-simulator".*?</script>'
    match = re.search(pattern, content, flags=re.DOTALL)

    if match:
        start, end = match.span()
        content = content[:start] + MMU_SIMULATOR_COMPONENT.strip() + content[end:]
        print("--> Injected cross-architecture MMU simulator (x86-64, ARM64, RISC-V).")
    else:
        print("--> Interactive MMU simulator container not found.")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Integrate multi-ISA comparative toggle for x86-64, ARM64, and RISC-V\n\n"
            "Enhance MMU interactive simulator in 02-hardware-review.html with ISA\n"
            "switching across CR3/CR2, TTBR/FAR, and satp/stval translation pipelines."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_mmu_simulator_component()
