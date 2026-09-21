#!/usr/bin/env python3
# =====================================================================
# fix.py: Add paired analytical panes to instruction throughput simulator
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

PIPELINE_SIM_HTML = """      <!-- Interactive Directed Narrative Stepper: Pipelining, Superscalar, & Multicore -->
      <div id="interactive-pipeline-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <!-- Header & Architecture Dimension Toggles -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Interactive Walkthrough: Instruction Throughput Engine</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Step through sequential vector operations across standard pipelined, superscalar, and multicore execution.</p>
          </div>

          <!-- Dimension Toggles -->
          <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
            <span style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; padding: 0 6px;">Architecture:</span>
            <button id="pipe-btn-pipeline" class="pipe-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">Pipelined (4-Stage)</button>
            <button id="pipe-btn-superscalar" class="pipe-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Dual-Issue Superscalar</button>
            <button id="pipe-btn-multicore" class="pipe-mode-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Dual-Core Multicore</button>
          </div>
        </div>

        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">Workload Scenario &amp; Instructions</div>
          <p style="margin: 0 0 6px 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            Tracking the execution of four instructions computing a vector dot-product term:
            <code>I1: LOAD R1, [A]</code> &bull; <code>I2: LOAD R2, [B]</code> &bull; <code>I3: MUL R3, R1, R2</code> &bull; <code>I4: ADD R4, R4, R3</code>.
          </p>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.85rem; line-height: 1.5;">
            <li><strong>Foreshadowed Step Navigation:</strong> Check the preview box next to the controls to see what instruction transition occurs before clicking.</li>
            <li><strong>Live Telemetry:</strong> Observe how Instructions Per Cycle (IPC) scales from 1.0 IPC in a clean pipeline up to 2.0 IPC in dual-issue superscalar and multicore execution.</li>
            <li><strong>Hazard &amp; Core Allocation:</strong> Watch how data hazards (e.g., <code>I3</code> depending on <code>R1</code> and <code>R2</code>) resolve via data forwarding vs. independent core thread dispatching.</li>
          </ol>
        </div>

        <!-- Action Controls & Foreshadowed Preview Panel -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="pipe-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step &rarr;</button>
            <div style="display: flex; gap: 8px;">
              <button id="pipe-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">&larr; Prev</button>
              <button id="pipe-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Where We Are &amp; What Happens Next Click:</div>
            <div id="pipe-inline-preview" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">Loading pipeline state...</div>
          </div>
        </div>

        <!-- Live State Telemetry Bar -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.8rem;">
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Clock Cycle</div>
            <div id="pipe-stat-cycle" style="font-weight: 700; color: #0f172a; margin-top: 2px;">Cycle 1</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Execution Phase</div>
            <div id="pipe-stat-phase" style="font-weight: 700; color: #0284c7; margin-top: 2px;">Pipeline Fill</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Instructions Retired</div>
            <div id="pipe-stat-retired" style="font-weight: 700; color: #059669; margin-top: 2px;">0 / 4</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Throughput (IPC)</div>
            <div id="pipe-stat-ipc" style="font-weight: 700; color: #0369a1; margin-top: 2px;">0.00 IPC</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Hazard Status</div>
            <div id="pipe-stat-hazard" style="font-weight: 700; color: #166534; margin-top: 2px;">None (Clean Fill)</div>
          </div>
        </div>

        <!-- Synchronized SVG Visual Canvas -->
        <div style="display: flex; justify-content: center; margin-bottom: 20px; overflow-x: auto;">
          <svg id="pipe-anim-svg" viewBox="0 0 920 280" width="100%" height="auto" style="max-width: 920px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <!-- Stage Containers -->
            <!-- Stage 1: Fetch -->
            <g id="pipe-node-fetch" transform="translate(30, 40)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Stage 1: FETCH (IF)</text>
              <text id="pipe-fetch-instr" x="90" y="48" fill="#0284c7" font-size="11" font-weight="700" text-anchor="middle">I1: LOAD R1, [A]</text>
              <text id="pipe-fetch-sub" x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">PC = 0x00401000</text>
            </g>

            <!-- Stage 2: Decode -->
            <g id="pipe-node-decode" transform="translate(250, 40)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Stage 2: DECODE (ID)</text>
              <text id="pipe-decode-instr" x="90" y="48" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">Empty (Bubble)</text>
              <text id="pipe-decode-sub" x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">Read Registers / Opcode</text>
            </g>

            <!-- Stage 3: Execute -->
            <g id="pipe-node-exec" transform="translate(470, 40)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Stage 3: EXECUTE (EX)</text>
              <text id="pipe-exec-instr" x="90" y="48" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">Empty (Bubble)</text>
              <text id="pipe-exec-sub" x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">ALU / Address Gen</text>
            </g>

            <!-- Stage 4: Writeback -->
            <g id="pipe-node-wb" transform="translate(690, 40)">
              <rect x="0" y="0" width="180" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="90" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Stage 4: WRITEBACK (WB)</text>
              <text id="pipe-wb-instr" x="90" y="48" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">Empty (Bubble)</text>
              <text id="pipe-wb-sub" x="90" y="68" fill="#64748b" font-size="9.5" text-anchor="middle">Update Register File</text>
            </g>

            <!-- Inter-Stage Pipeline Latches -->
            <path id="pipe-flow-1" d="M 210,85 L 245,85" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="pipe-flow-2" d="M 430,85 L 465,85" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="pipe-flow-3" d="M 650,85 L 685,85" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />

            <!-- Bypass / Data Forwarding Line (EX to EX / ID) -->
            <path id="pipe-forwarding-path" d="M 560,130 C 560,165 340,165 340,135" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="pipe-forward-label" x="450" y="160" fill="#64748b" font-size="9.5" text-anchor="middle">Data Forwarding Bypass (Bypasses WB)</text>

            <!-- Lower Topology Console -->
            <g transform="translate(30, 180)">
              <rect x="0" y="0" width="840" height="80" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="pipe-console-top" x="20" y="26" fill="#0369a1" font-size="11" font-weight="700">EXECUTION HARDWARE TOPOLOGY: SINGLE-CORE PIPELINE</text>
              <text id="pipe-console-mid" x="20" y="48" fill="#0f172a" font-size="11" font-family="var(--font-mono)">
                Cycle 1: Fetching Instruction I1 into IF Stage.
              </text>
              <text id="pipe-console-sub" x="20" y="68" fill="#64748b" font-size="10" font-family="var(--font-mono)">
                Core 0 &bull; 4 pipeline stages clocked in lockstep &bull; Latches primed.
              </text>
            </g>
          </svg>
        </div>

        <!-- Paired Analytical Panes -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Detailed Mechanics: What Is Happening</div>
            <div id="pipe-desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Behind the Curtain: Why The System Does This</div>
            <div id="pipe-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const pipeStorylines = {
            pipeline: [
              {
                cycle: "Cycle 1",
                phase: "Pipeline Fill (Stage 1 Active)",
                retired: "0 / 4",
                ipc: "0.00 IPC",
                hazard: "None (Pipeline Priming)",
                fetch: "I1: LOAD R1, [A]",
                decode: "Empty (Bubble)",
                exec: "Empty (Bubble)",
                wb: "Empty (Bubble)",
                activeStages: ["pipe-node-fetch"],
                forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE &bull; CLOCK CYCLE 1",
                consoleMid: "I1 is fetched from memory address 0x00401000 into the Instruction Register.",
                consoleSub: "Downstream pipeline latches are currently empty as execution begins.",
                inlinePreview: "We are at Cycle 1. I1 has been fetched into the core. Next, I1 moves into the Decode stage while the Fetch stage retrieves I2. Click Next to advance to Cycle 2.",
                what: "The CPU begins execution by asserting Program Counter <code>0x00401000</code> on the instruction bus. The machine code for <code>I1: LOAD R1, [A]</code> is latched into the Instruction Fetch (IF) register. Hardware automatically increments <code>PC &larr; PC + 4</code>. The Decode, Execute, and Writeback stages hold uninitialized bubbles.",
                why: "Dividing instruction processing into discrete stages decoupled by edge-triggered D flip-flops isolates path delays. The clock frequency only needs to accommodate the propagation delay of the longest individual stage rather than the entire instruction execution cycle."
              },
              {
                cycle: "Cycle 2",
                phase: "Pipeline Fill (Stages 1-2 Active)",
                retired: "0 / 4",
                ipc: "0.00 IPC",
                hazard: "None (Independent Loads)",
                fetch: "I2: LOAD R2, [B]",
                decode: "I1: LOAD R1, [A]",
                exec: "Empty (Bubble)",
                wb: "Empty (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"],
                forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE &bull; CLOCK CYCLE 2",
                consoleMid: "I1 enters Decode (ID); I2 enters Fetch (IF). Two instructions in flight.",
                consoleSub: "Hardware decodes LOAD opcode while fetching the next sequential word.",
                inlinePreview: "We are at Cycle 2. I1 is decoding and I2 is fetching. Next, I1 executes its memory address calculation, I2 decodes, and I3 (MUL) is fetched. Click Next to advance to Cycle 3.",
                what: "On the rising clock edge, <code>I1</code> shifts across the inter-stage latch into the <strong>Instruction Decode (ID)</strong> stage, where the control unit extracts opcode bits and designates <code>R1</code> as the writeback target. Concurrently, the <strong>Fetch (IF)</strong> stage pulls <code>I2: LOAD R2, [B]</code> from the cache bus.",
                why: "Functional units operate concurrently without structural collision: the L1 instruction cache port services <code>I2</code> while the control unit decoder evaluates <code>I1</code>. Pipelining increases instruction throughput by keeping independent hardware blocks concurrently utilized."
              },
              {
                cycle: "Cycle 3",
                phase: "Pipeline Fill & Hazard Detection",
                retired: "0 / 4",
                ipc: "0.00 IPC",
                hazard: "RAW Hazard Detected (I3 needs R1)",
                fetch: "I3: MUL R3, R1, R2",
                decode: "I2: LOAD R2, [B]",
                exec: "I1: LOAD R1, [A]",
                wb: "Empty (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode", "pipe-node-exec"],
                forwardingActive: true,
                consoleTop: "STANDARD 4-STAGE PIPELINE &bull; CLOCK CYCLE 3",
                consoleMid: "I1 executes address calculation; I2 decodes; I3 (MUL) is fetched into the core.",
                consoleSub: "Hazard unit detects I3 depends on R1 and R2 &rarr; primes forwarding bypass.",
                inlinePreview: "We are at Cycle 3. I1 is executing and I3 detects a data dependency on R1. Next, the pipeline fills completely, I1 completes writeback, and data forwarding provides R1 to I3 without stalling. Click Next to advance to Cycle 4.",
                what: "<code>I1</code> moves to the <strong>Execute (EX)</strong> stage, calculating the effective memory address for <code>[A]</code>. <code>I2</code> enters Decode, and <code>I3: MUL R3, R1, R2</code> is fetched. The core's hazard detection unit identifies a <strong>Read-After-Write (RAW)</strong> dependency: <code>I3</code> requires <code>R1</code> before <code>I1</code> has updated the register file.",
                why: "Without bypass hardware, the processor would be forced to stall (insert bubbles) for two clock cycles until <code>I1</code> reached Writeback. The hardware primes internal multiplexer bypass buses (forwarding paths) to route the calculated value directly from the ALU/Memory output into <code>I3</code>'s input latches."
              },
              {
                cycle: "Cycle 4",
                phase: "Steady State (Full Pipeline)",
                retired: "1 / 4",
                ipc: "0.25 IPC",
                hazard: "Forwarding Active (EX &rarr; ID)",
                fetch: "I4: ADD R4, R4, R3",
                decode: "I3: MUL R3, R1, R2",
                exec: "I2: LOAD R2, [B]",
                wb: "I1: LOAD R1, [A]",
                activeStages: ["pipe-node-fetch", "pipe-node-decode", "pipe-node-exec", "pipe-node-wb"],
                forwardingActive: true,
                consoleTop: "STANDARD 4-STAGE PIPELINE &bull; CLOCK CYCLE 4 (FULL PIPELINE)",
                consoleMid: "I1 writes back R1; I2 executes; I3 decodes with forwarded operands; I4 enters Fetch.",
                consoleSub: "First instruction retires. The pipeline reaches full steady-state utilization.",
                inlinePreview: "We are at Cycle 4. All four stages are occupied and I1 has retired. Next, I2 writes back R2 and I3 enters the ALU for multiplication. Click Next to advance to Cycle 5.",
                what: "All 4 stages are now occupied simultaneously. <code>I1</code> writes its retrieved data word into general-purpose register <code>R1</code> and officially <strong>retires</strong>. <code>I2</code> executes address generation in EX, <code>I3</code> decodes, and <code>I4: ADD R4, R4, R3</code> enters the Fetch stage.",
                why: "The pipeline has completed its fill latency. From this point forward, until the instruction stream is exhausted or interrupted by branch mispredictions or cache misses, the core retires exactly one instruction every single clock cycle (1.0 IPC)."
              },
              {
                cycle: "Cycle 5",
                phase: "Pipeline Drain (Steady Retiring)",
                retired: "2 / 4",
                ipc: "0.40 IPC",
                hazard: "Forwarding Active (MUL result)",
                fetch: "Drained",
                decode: "I4: ADD R4, R4, R3",
                exec: "I3: MUL R3, R1, R2",
                wb: "I2: LOAD R2, [B]",
                activeStages: ["pipe-node-decode", "pipe-node-exec", "pipe-node-wb"],
                forwardingActive: true,
                consoleTop: "STANDARD 4-STAGE PIPELINE &bull; CLOCK CYCLE 5",
                consoleMid: "I2 writes back R2; I3 multiplies R1*R2 in ALU; I4 decodes. I1 and I2 retired.",
                consoleSub: "No new instructions fetched. Remaining operations drain down the pipe.",
                inlinePreview: "We are at Cycle 5. I2 has retired and I3 is multiplying in the ALU. Next, I3 writes back product R3 and I4 executes addition. Click Next to advance to Cycle 6.",
                what: "<code>I2</code> writes back into register <code>R2</code> and retires. <code>I3</code> enters the ALU multiplier array to compute <code>R1 &times; R2</code>. <code>I4</code> decodes in ID, and the Fetch stage drains to idle as the 4-instruction block has been fully fetched.",
                why: "Multiplication circuits are deeply pipelined (typically using Booth encoding and Wallace tree adders). Staging ensures the clock frequency remains high without letting multi-bit multiplication stall upstream stages."
              },
              {
                cycle: "Cycle 6",
                phase: "Pipeline Drain (Final Stages)",
                retired: "3 / 4",
                ipc: "0.50 IPC",
                hazard: "None",
                fetch: "Drained",
                decode: "Drained",
                exec: "I4: ADD R4, R4, R3",
                wb: "I3: MUL R3, R1, R2",
                activeStages: ["pipe-node-exec", "pipe-node-wb"],
                forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE &bull; CLOCK CYCLE 6",
                consoleMid: "I3 writes back R3; I4 adds R4 + R3 in ALU. 3 of 4 instructions retired.",
                consoleSub: "Pipeline nears completion. Accumulator stage computing final sum.",
                inlinePreview: "We are at Cycle 6. I3 has retired and I4 is in the ALU. Next, I4 writes back to R4 and retires, completing the 4-instruction sequence. Click Next to finish.",
                what: "<code>I3</code> writes its computed product into register <code>R3</code> and retires. <code>I4</code> executes in the ALU, adding <code>R3</code> directly into accumulator register <code>R4</code>.",
                why: "Forwarding allowed <code>I4</code> to begin execution in the exact cycle following <code>I3</code>'s ALU phase, eliminating register file latency."
              },
              {
                cycle: "Cycle 7",
                phase: "Workload Complete",
                retired: "4 / 4",
                ipc: "0.57 IPC (Avg across drain)",
                hazard: "None",
                fetch: "Idle",
                decode: "Idle",
                exec: "Idle",
                wb: "I4: ADD R4, R4, R3",
                activeStages: ["pipe-node-wb"],
                forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE &bull; CLOCK CYCLE 7 (COMPLETE)",
                consoleMid: "I4 writes back final sum to R4. All 4 instructions successfully retired.",
                consoleSub: "Total execution: 7 cycles for 4 instructions (vs 16 cycles non-pipelined).",
                inlinePreview: "Walkthrough complete! 4 instructions finished in 7 cycles (saving 9 cycles over non-pipelined execution). Click Reset or toggle to Superscalar mode to see parallel issue.",
                what: "<code>I4</code> writes back into <code>R4</code>. All 4 instructions are officially retired. Total execution time was 7 clock cycles, compared to 16 cycles on an unpipelined architecture ($4 \\times 4$).",
                why: "The pipelining speedup theorem states that speedup approaches the number of pipeline stages ($k=4$) as $N \\to \\infty$. For long vector loops, this pipeline achieves a near 400% speedup over sequential execution."
              }
            ],
            superscalar: [
              {
                cycle: "Cycle 1",
                phase: "Dual-Issue Fetch & Decode",
                retired: "0 / 4",
                ipc: "0.00 IPC",
                hazard: "None (Parallel Fetch)",
                fetch: "I1 &amp; I2 (Dual-Issue)",
                decode: "Empty (Bubble)",
                exec: "Empty (Bubble)",
                wb: "Empty (Bubble)",
                activeStages: ["pipe-node-fetch"],
                forwardingActive: false,
                consoleTop: "DUAL-ISSUE SUPERSCALAR &bull; CLOCK CYCLE 1",
                consoleMid: "Wide 64-byte fetcher reads both I1 (LOAD R1) and I2 (LOAD R2) simultaneously.",
                consoleSub: "Dual instruction queues primed &bull; Superscalar issue logic checks dependency matrix.",
                inlinePreview: "We are at Cycle 1. The superscalar core fetched both I1 and I2 simultaneously. Next, both instructions decode in parallel while I3 and I4 are fetched together. Click Next to advance to Cycle 2.",
                what: "The CPU's wide instruction fetch unit pulls 64 bits from the L1 instruction cache, loading <strong>both</strong> <code>I1: LOAD R1, [A]</code> and <code>I2: LOAD R2, [B]</code> simultaneously into dual instruction queues in a single cycle.",
                why: "A single pipeline is bound by the theoretical ceiling of 1.0 IPC. Superscalar designs duplicate execution paths to fetch, decode, and issue multiple instructions per cycle, achieving $IPC > 1.0$."
              },
              {
                cycle: "Cycle 2",
                phase: "Dual Execute (Load Units 1 &amp; 2)",
                retired: "0 / 4",
                ipc: "0.00 IPC",
                hazard: "Dual Issue Matrix Check",
                fetch: "I3 &amp; I4 (Dual-Issue)",
                decode: "I1 &amp; I2 (Dual Decode)",
                exec: "Empty (Bubble)",
                wb: "Empty (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"],
                forwardingActive: false,
                consoleTop: "DUAL-ISSUE SUPERSCALAR &bull; CLOCK CYCLE 2",
                consoleMid: "I1 & I2 decode simultaneously; I3 (MUL) and I4 (ADD) enter dual fetchers.",
                consoleSub: "Scoreboard validates I1 and I2 have no memory address conflicts.",
                inlinePreview: "We are at Cycle 2. I1 and I2 are decoding while I3 and I4 are fetching. Next, I1 and I2 execute in dual load ports while I3 and I4 decode. Click Next to advance to Cycle 3.",
                what: "Dual instruction decoders process <code>I1</code> and <code>I2</code> in parallel. Simultaneously, <code>I3: MUL R3, R1, R2</code> and <code>I4: ADD R4, R4, R3</code> are fetched side-by-side. The hardware scoreboard confirms <code>I1</code> and <code>I2</code> target different registers (<code>R1</code> vs <code>R2</code>) and can execute concurrently.",
                why: "Superscalar issue logic uses dependency matrices to confirm instruction independence. Because <code>I1</code> and <code>I2</code> do not share registers or memory addresses, they can proceed without structural serialization."
              },
              {
                cycle: "Cycle 3",
                phase: "Parallel Execution & Retiring",
                retired: "2 / 4",
                ipc: "1.00 IPC (2 Retires this cycle)",
                hazard: "Cross-Pipeline Forwarding",
                fetch: "Drained",
                decode: "I3 &amp; I4 (Dual Decode)",
                exec: "I1 &amp; I2 (Dual Load)",
                wb: "Empty (Bubble)",
                activeStages: ["pipe-node-decode", "pipe-node-exec"],
                forwardingActive: true,
                consoleTop: "DUAL-ISSUE SUPERSCALAR &bull; CLOCK CYCLE 3",
                consoleMid: "Dual execution units service I1 & I2. Both loads complete and forward to ALU.",
                consoleSub: "Reorder Buffer (ROB) tracks in-flight instructions for in-order retirement.",
                inlinePreview: "We are at Cycle 3. I1 and I2 are executing in parallel load ports. Next, both I1 and I2 retire together (2.0 IPC peak!) while I3 executes in the multiplier. Click Next to advance to Cycle 4.",
                what: "<code>I1</code> and <code>I2</code> execute in parallel on separate memory load ports. Their loaded values are forwarded immediately across an internal bypass crossbar into the integer execution units for <code>I3</code> and <code>I4</code>.",
                why: "Superscalar architectures use dual-ported or banked L1 data caches so two distinct memory loads can be serviced simultaneously without causing a cache port structural hazard."
              },
              {
                cycle: "Cycle 4",
                phase: "Dual Retirement (Workload Finished)",
                retired: "4 / 4",
                ipc: "1.00 IPC (4 Insts in 4 Cycles)",
                hazard: "None",
                fetch: "Idle",
                decode: "Idle",
                exec: "I3 (MUL) &amp; I4 (ADD)",
                wb: "I1 &amp; I2 Retired",
                activeStages: ["pipe-node-exec", "pipe-node-wb"],
                forwardingActive: false,
                consoleTop: "DUAL-ISSUE SUPERSCALAR &bull; CLOCK CYCLE 4 (COMPLETE)",
                consoleMid: "I3 and I4 finish execution and retire simultaneously. All 4 instructions complete.",
                consoleSub: "Total execution: 4 clock cycles for 4 instructions (Peak Throughput: 2.0 IPC).",
                inlinePreview: "Walkthrough complete! 4 instructions finished in only 4 clock cycles (nearly twice as fast as the single pipeline). Click Reset or toggle to Multicore mode.",
                what: "<code>I3</code> and <code>I4</code> complete execution and retire together through the Reorder Buffer (ROB). All 4 instructions finish in just 4 clock cycles.",
                why: "Dual-issue superscalar execution completes the workload in 4 cycles instead of 7 cycles, demonstrating that parallel dispatching overcomes the single-issue pipeline limit."
              }
            ],
            multicore: [
              {
                cycle: "Cycle 1",
                phase: "Thread Partitioning across Cores",
                retired: "0 / 4",
                ipc: "0.00 IPC",
                hazard: "None (Independent Threads)",
                fetch: "Core 0: I1 | Core 1: I2",
                decode: "Empty (Both Cores)",
                exec: "Empty (Both Cores)",
                wb: "Empty (Both Cores)",
                activeStages: ["pipe-node-fetch"],
                forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR &bull; CLOCK CYCLE 1",
                consoleMid: "OS thread scheduler dispatches Iteration A to Core 0 and Iteration B to Core 1.",
                consoleSub: "Two independent silicon cores each with private L1/L2 caches and separate pipelines.",
                inlinePreview: "We are at Cycle 1. Core 0 and Core 1 have each fetched independent loop iterations simultaneously. Next, both cores decode in parallel. Click Next to advance to Cycle 2.",
                what: "The operating system divides the workload across two complete, physically separate CPU cores. <strong>Core 0</strong> fetches <code>I1 (Iteration A)</code> while <strong>Core 1</strong> fetches <code>I2 (Iteration B)</code>.",
                why: "Unlike superscalar cores that share a single register file and dispatch scheduler, multicore systems feature completely separate execution pipelines, eliminating register dependency stalls across threads."
              },
              {
                cycle: "Cycle 2",
                phase: "Parallel Execution on Separate Dies",
                retired: "0 / 4",
                ipc: "0.00 IPC",
                hazard: "None (Private Core Cache)",
                fetch: "Core 0: I3 | Core 1: I4",
                decode: "Core 0: I1 | Core 1: I2",
                exec: "Empty (Both Cores)",
                wb: "Empty (Both Cores)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"],
                forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR &bull; CLOCK CYCLE 2",
                consoleMid: "Core 0 decodes I1 while Core 1 decodes I2; each core fetches its next thread op.",
                consoleSub: "MESI cache coherency protocol snoops shared L3 cache to guarantee memory consistency.",
                inlinePreview: "We are at Cycle 2. Both cores are decoding their respective thread instructions. Next, Core 0 and Core 1 execute memory loads in their private L1 caches. Click Next to advance to Cycle 3.",
                what: "Both cores decode their instructions simultaneously. Core 0's private L1 cache services <code>I1</code>, while Core 1's private L1 cache services <code>I2</code>.",
                why: "Each core has dedicated L1 instruction and data caches. Memory access on Core 0 does not contend with or slow down memory access on Core 1."
              },
              {
                cycle: "Cycle 3",
                phase: "Parallel Compute & Cache Snooping",
                retired: "2 / 4",
                ipc: "0.67 IPC (2 Cores Retiring)",
                hazard: "MESI Bus Snooping Clean",
                fetch: "Drained",
                decode: "Core 0: I3 | Core 1: I4",
                exec: "Core 0: I1 | Core 1: I2",
                wb: "Empty (Both Cores)",
                activeStages: ["pipe-node-decode", "pipe-node-exec"],
                forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR &bull; CLOCK CYCLE 3",
                consoleMid: "Core 0 and Core 1 retire loads simultaneously. Both threads advance to arithmetic.",
                consoleSub: "Hardware cache coherence snoops shared interconnect; no false sharing detected.",
                inlinePreview: "We are at Cycle 3. Both cores have finished their memory loads. Next, Core 0 executes multiplication while Core 1 executes addition, retiring both threads. Click Next to finish.",
                what: "Both cores execute in parallel. Core 0 completes its load for Iteration A, and Core 1 completes its load for Iteration B. Both instructions retire across the two cores.",
                why: "Multicore architectures scale throughput without increasing clock frequencies, avoiding the thermal and power limits (the 'power wall') of high-frequency single cores."
              },
              {
                cycle: "Cycle 4",
                phase: "Symmetric Multiprocessing Complete",
                retired: "4 / 4",
                ipc: "1.00 IPC (Dual Core Throughput)",
                hazard: "None",
                fetch: "Idle",
                decode: "Idle",
                exec: "Core 0: I3 | Core 1: I4",
                wb: "Core 0 &amp; Core 1 Retired",
                activeStages: ["pipe-node-exec", "pipe-node-wb"],
                forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR &bull; CLOCK CYCLE 4 (COMPLETE)",
                consoleMid: "Core 0 and Core 1 complete their workloads in parallel. Symmetric threads finished.",
                consoleSub: "True thread-level parallelism (TLP) achieved across independent hardware cores.",
                inlinePreview: "Walkthrough complete! Two independent physical cores executed the workload in parallel. Click Reset or switch back to Pipelined or Superscalar modes to compare.",
                what: "Core 0 and Core 1 complete their arithmetic calculations and retire their respective threads. The parallel vector calculations finish in 4 clock cycles.",
                why: "True hardware parallelism enables the operating system to achieve high system throughput across multiple independent processes or multithreaded applications."
              }
            ]
          };

          let currentPipeMode = "pipeline";
          let pipeIndex = 0;

          function renderPipeState() {
            const list = pipeStorylines[currentPipeMode];
            const data = list[pipeIndex];

            // Telemetry
            document.getElementById("pipe-stat-cycle").textContent = data.cycle;
            document.getElementById("pipe-stat-phase").textContent = data.phase;
            document.getElementById("pipe-stat-retired").textContent = data.retired;
            document.getElementById("pipe-stat-ipc").textContent = data.ipc;
            document.getElementById("pipe-stat-hazard").textContent = data.hazard;

            // Foreshadowed preview & analytical panes
            document.getElementById("pipe-inline-preview").innerHTML = data.inlinePreview;
            document.getElementById("pipe-desc-what").innerHTML = data.what;
            document.getElementById("pipe-desc-why").innerHTML = data.why;

            // SVG textual elements
            document.getElementById("pipe-fetch-instr").innerHTML = data.fetch;
            document.getElementById("pipe-decode-instr").innerHTML = data.decode;
            document.getElementById("pipe-exec-instr").innerHTML = data.exec;
            document.getElementById("pipe-wb-instr").innerHTML = data.wb;

            document.getElementById("pipe-console-top").textContent = data.consoleTop;
            document.getElementById("pipe-console-mid").textContent = data.consoleMid;
            document.getElementById("pipe-console-sub").textContent = data.consoleSub;

            // Buttons
            const nextBtn = document.getElementById("pipe-next-btn");
            const prevBtn = document.getElementById("pipe-prev-btn");

            if (nextBtn) {
              nextBtn.innerHTML = pipeIndex === list.length - 1 ? "Restart Walkthrough &#8634;" : "Next Step &rarr;";
            }
            if (prevBtn) {
              prevBtn.style.opacity = pipeIndex === 0 ? "0.5" : "1.0";
              prevBtn.style.cursor = pipeIndex === 0 ? "not-allowed" : "pointer";
            }

            // Reset SVG stage highlighting
            const allStages = ["pipe-node-fetch", "pipe-node-decode", "pipe-node-exec", "pipe-node-wb"];
            allStages.forEach(id => {
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

            // Highlight active stages with vivid orange pop
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

            // Forwarding path glow
            const fwdPath = document.getElementById("pipe-forwarding-path");
            const fwdLabel = document.getElementById("pipe-forward-label");
            if (fwdPath && fwdLabel) {
              if (data.forwardingActive) {
                fwdPath.setAttribute("stroke", "#0284c7");
                fwdPath.setAttribute("stroke-width", "2.5");
                fwdPath.setAttribute("stroke-dasharray", "none");
                fwdLabel.setAttribute("fill", "#0284c7");
                fwdLabel.setAttribute("font-weight", "700");
              } else {
                fwdPath.setAttribute("stroke", "#cbd5e1");
                fwdPath.setAttribute("stroke-width", "2");
                fwdPath.setAttribute("stroke-dasharray", "4,4");
                fwdLabel.setAttribute("fill", "#64748b");
                fwdLabel.setAttribute("font-weight", "400");
              }
            }
          }

          function setPipeMode(modeKey) {
            currentPipeMode = modeKey;
            pipeIndex = 0;
            const buttons = {
              "pipeline": document.getElementById("pipe-btn-pipeline"),
              "superscalar": document.getElementById("pipe-btn-superscalar"),
              "multicore": document.getElementById("pipe-btn-multicore")
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
            renderPipeState();
          }

          document.getElementById("pipe-btn-pipeline").addEventListener("click", () => setPipeMode("pipeline"));
          document.getElementById("pipe-btn-superscalar").addEventListener("click", () => setPipeMode("superscalar"));
          document.getElementById("pipe-btn-multicore").addEventListener("click", () => setPipeMode("multicore"));

          document.getElementById("pipe-next-btn").addEventListener("click", function() {
            const list = pipeStorylines[currentPipeMode];
            if (pipeIndex < list.length - 1) {
              pipeIndex++;
            } else {
              pipeIndex = 0;
            }
            renderPipeState();
          });

          document.getElementById("pipe-prev-btn").addEventListener("click", function() {
            if (pipeIndex > 0) {
              pipeIndex--;
              renderPipeState();
            }
          });

          document.getElementById("pipe-reset-btn").addEventListener("click", function() {
            pipeIndex = 0;
            renderPipeState();
          });

          renderPipeState();
        })();
      </script>"""

def inject_pipeline_walkthrough():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if existing simulator is installed; if so, replace it cleanly
    old_sim_pattern = r'<!-- Interactive Directed Narrative Stepper: Pipelining.*?<\/script>'
    match = re.search(old_sim_pattern, content, flags=re.DOTALL)
    if match:
        content = content[:match.start()] + PIPELINE_SIM_HTML.strip() + content[match.end():]
        print("--> Replaced existing pipeline simulator with expanded analytical walkthrough.")
    else:
        # Target insertion point: right after Section 1 diagram container
        needle = '<div class="diagram-container" id="svg-pipeline-architecture">'
        if needle in content:
            idx = content.find(needle)
            close_div = content.find('</div>', idx) + 6
            content = content[:close_div] + "\n\n" + PIPELINE_SIM_HTML.strip() + content[close_div:]
            print("--> Injected interactive pipeline simulator after architecture diagram.")
        else:
            sec2_needle = '<h2>2. Privilege Modes'
            idx = content.find(sec2_needle)
            if idx != -1:
                content = content[:idx] + PIPELINE_SIM_HTML.strip() + "\n\n      " + content[idx:]
                print("--> Injected interactive pipeline simulator before Section 2.")
            else:
                print("--> Error: could not locate insertion point.")
                return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand analytical narrative panes for instruction throughput simulator\n\n"
            "Add granular micro-architectural mechanics and design rationales across\n"
            "all pipeline, superscalar, and multicore steps in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for instruction throughput simulator!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_pipeline_walkthrough()
