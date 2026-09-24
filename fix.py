#!/usr/bin/env python3
# =====================================================================
# fix.py: Implement all four interactive pedagogical aids in Week 4
# =====================================================================
import os
import subprocess

MOD02_PATH = os.path.join("week04-concurrency-and-mutual-exclusion", "02-hardware-primitives-spinlocks.html")
MOD03_PATH = os.path.join("week04-concurrency-and-mutual-exclusion", "03-semaphores-mutexes-monitors.html")
MOD04_PATH = os.path.join("week04-concurrency-and-mutual-exclusion", "04-classical-synchronization.html")

# =====================================================================
# 1. PETERSON ARBITRATION & REORDERING STEPPER (Module 02, Section 2)
# =====================================================================
PETERSON_STEPPER_HTML = r"""
    <!-- Interactive Aid: Peterson Arbitration & Store-Buffer Reordering -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Peterson's Algorithm &amp; Store-Buffer Reordering</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="p-dim-sc" onclick="setPetersonDim('sc')">Sequential Consistency</button>
          <button class="dim-btn" id="p-dim-ooo" onclick="setPetersonDim('ooo')">Store-Buffer Reorder (Bug)</button>
          <button class="dim-btn" id="p-dim-fence" onclick="setPetersonDim('fence')">Memory Fence (Protected)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Arbitration Arc</span>
        <span id="p-scenario-text">Core 0 (P0) and Core 1 (P1) simultaneously execute Peterson's protocol. Under Sequential Consistency, the polite assignment to turn breaks the tie deterministically.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Timeline Clock</span>
          <span class="telemetry-val highlight" id="p-telem-time">T = 0 ns</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">P0 State &amp; Flag</span>
          <span class="telemetry-val" id="p-telem-p0">flag[0] = false</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">P1 State &amp; Flag</span>
          <span class="telemetry-val" id="p-telem-p1">flag[1] = false</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Shared Memory 'turn'</span>
          <span class="telemetry-val highlight" id="p-telem-turn">turn = 0</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Critical Section State</span>
          <span class="telemetry-val highlight" id="p-telem-status">Empty (Safe)</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="hw-canvas" viewBox="0 0 760 250">
          <defs>
            <marker id="p-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
            </marker>
            <marker id="p-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
            </marker>
            <marker id="p-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
            </marker>
          </defs>

          <!-- Core 0 Block -->
          <g transform="translate(20, 20)">
            <rect width="210" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="10.5" font-weight="700" fill="#0284c7">CPU CORE 0 (P0)</text>

            <rect id="p-rect-c0-stage" x="12" y="36" width="186" height="42" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
            <text id="p-txt-c0-stage" x="105" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="#0369a1">STAGE: IDLE</text>

            <rect x="12" y="86" width="186" height="48" rx="4" fill="#0f172a"/>
            <text x="20" y="104" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#94a3b8">CURRENT INSTRUCTION:</text>
            <text id="p-txt-c0-instr" x="20" y="122" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#38bdf8">enter_region(0)</text>

            <!-- Store Buffer Box -->
            <rect id="p-rect-c0-sbuf" x="12" y="142" width="186" height="56" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
            <text x="20" y="158" font-size="8" font-weight="700" fill="#475569">STORE BUFFER (FIFO):</text>
            <text id="p-txt-c0-sbuf" x="20" y="174" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">[Buffer Empty: Drained]</text>
            <text id="p-txt-c0-sbuf-status" x="20" y="188" font-size="7.5" fill="#94a3b8">Writes commit immediately</text>
          </g>

          <!-- Middle: Shared Physical Memory & Interconnect -->
          <g transform="translate(250, 20)">
            <rect width="260" height="210" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
            <text x="130" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0f172a">SHARED DRAM CELLS</text>

            <!-- Intent Array Box -->
            <rect x="14" y="38" width="232" height="48" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
            <text x="22" y="54" font-size="8" font-weight="700" fill="#0369a1">SHARED ARRAY: flag[2]</text>
            <text id="p-txt-mem-flags" x="130" y="74" text-anchor="middle" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#0f172a">flag[0]=F &nbsp;|&nbsp; flag[1]=F</text>

            <!-- Turn Scalar Box -->
            <rect x="14" y="94" width="232" height="52" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="22" y="112" font-size="8" font-weight="700" fill="#475569">TIE-BREAKER SCALAR: turn</text>
            <text id="p-txt-mem-turn" x="130" y="134" text-anchor="middle" font-family="var(--font-mono)" font-size="16" font-weight="700" fill="#0284c7">turn = 0</text>

            <!-- Critical Region Occupancy Status -->
            <rect id="p-rect-cs-badge" x="14" y="154" width="232" height="44" rx="4" fill="#dcfce7" stroke="#16a34a"/>
            <text id="p-txt-cs-badge" x="130" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">&#10003; CRITICAL REGION: VACANT</text>
          </g>

          <!-- Core 1 Block -->
          <g transform="translate(530, 20)">
            <rect width="210" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="10.5" font-weight="700" fill="#d97706">CPU CORE 1 (P1)</text>

            <rect id="p-rect-c1-stage" x="12" y="36" width="186" height="42" rx="4" fill="#fef3c7" stroke="#d97706"/>
            <text id="p-txt-c1-stage" x="105" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="#92400e">STAGE: IDLE</text>

            <rect x="12" y="86" width="186" height="48" rx="4" fill="#0f172a"/>
            <text x="20" y="104" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#94a3b8">CURRENT INSTRUCTION:</text>
            <text id="p-txt-c1-instr" x="20" y="122" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#38bdf8">enter_region(1)</text>

            <!-- Store Buffer Box -->
            <rect id="p-rect-c1-sbuf" x="12" y="142" width="186" height="56" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
            <text x="20" y="158" font-size="8" font-weight="700" fill="#475569">STORE BUFFER (FIFO):</text>
            <text id="p-txt-c1-sbuf" x="20" y="174" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">[Buffer Empty: Drained]</text>
            <text id="p-txt-c1-sbuf-status" x="20" y="188" font-size="7.5" fill="#94a3b8">Writes commit immediately</text>
          </g>
        </svg>
      </div>

      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="p-btn-prev" onclick="stepPeterson(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="p-btn-next" onclick="stepPeterson(1)">Next Step &rarr;</button>
          <button class="btn-step" id="p-btn-reset" onclick="resetPeterson()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="p-txt-narrative">Initial State: Both processes are in their remainder sections. Both flags are false. Critical region is completely empty.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="p-txt-what">Both processes are idle. Memory holds flags=false, turn=0.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="p-txt-why">Baseline state before concurrent contention begins.</p>
        </div>
      </div>
    </div>
"""

# =====================================================================
# 2. MESI CACHELINE BOUNCING SIMULATOR (Module 02, Section 4)
# =====================================================================
MESI_BOUNCING_STEPPER_HTML = r"""
    <!-- Interactive Aid: MESI Cacheline Bouncing & TTAS Simulator -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: MESI Cacheline Bouncing &amp; TTAS Optimization</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="m-dim-naive" onclick="setMesiDim('naive')">Naive Spinlock (Bounce Storm)</button>
          <button class="dim-btn" id="m-dim-ttas" onclick="setMesiDim('ttas')">TTAS (Shared Cache Hit)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Hardware Topology</span>
        <span id="m-scenario-text">Core 0 holds spinlock [0x80001000]. Core 1 and Core 2 compete to acquire it. Under naive TSL, every spin issues an atomic write, causing continuous cacheline invalidations and bus saturation.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Timeline Clock</span>
          <span class="telemetry-val highlight" id="m-telem-time">T = 0 ns</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Core 0 Cache State</span>
          <span class="telemetry-val" id="m-telem-c0">Modified (M)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Core 1 Cache State</span>
          <span class="telemetry-val" id="m-telem-c1">Invalid (I)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Bus Traffic Saturation</span>
          <span class="telemetry-val highlight" id="m-telem-bus">0 MB/s (Idle)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Interconnect State</span>
          <span class="telemetry-val highlight" id="m-telem-status">Nominal</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="hw-canvas" viewBox="0 0 760 250">
          <defs>
            <marker id="m-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
            </marker>
            <marker id="m-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
            </marker>
          </defs>

          <!-- Core 0 (Lock Holder) -->
          <g transform="translate(15, 20)">
            <rect width="165" height="210" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="12" y="24" font-size="9.5" font-weight="700" fill="#059669">CORE 0 [Lock Holder]</text>

            <rect x="10" y="36" width="145" height="42" rx="3" fill="#dcfce7" stroke="#16a34a"/>
            <text x="18" y="52" font-size="8" font-weight="700" fill="#166534">CRITICAL SECTION</text>
            <text x="18" y="68" font-family="var(--font-mono)" font-size="8" fill="#14532d">balance += 100;</text>

            <rect id="m-rect-c0-cache" x="10" y="86" width="145" height="52" rx="3" fill="#dcfce7" stroke="#16a34a"/>
            <text x="18" y="102" font-size="8" font-weight="700" fill="#166534">L1 CACHE (MESI):</text>
            <text id="m-txt-c0-mesi" x="18" y="122" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="#166534">MODIFIED [M]</text>

            <rect x="10" y="146" width="145" height="52" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="18" y="162" font-size="7.5" font-weight="700" fill="#475569">BUS ACTIVITY:</text>
            <text id="m-txt-c0-bus" x="18" y="180" font-size="7.5" fill="#64748b">Holds line exclusively</text>
          </g>

          <!-- Central Interconnect Bus -->
          <g transform="translate(195, 20)">
            <rect width="365" height="210" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
            <text x="182" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#0f172a">SHARED INTERCONNECT BUS (RING / MESH)</text>

            <!-- Bus Telemetry Box -->
            <rect id="m-rect-bus-box" x="15" y="38" width="335" height="68" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
            <text id="m-txt-bus-title" x="182" y="56" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0284c7">INTERCONNECT STATUS: QUIET</text>
            <text id="m-txt-bus-desc" x="182" y="74" text-anchor="middle" font-size="8" fill="#64748b">No invalidation storm active</text>
            <text id="m-txt-bus-metric" x="182" y="92" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#059669">Bandwidth: 0 GB/s (Clean)</text>

            <!-- Invalidation Storm Vectors -->
            <g id="m-grp-storm-arrows" style="display: none;">
              <line x1="30" y1="130" x2="335" y2="130" stroke="#dc2626" stroke-width="3" stroke-dasharray="4 3"/>
              <text x="182" y="122" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#dc2626">&harr; RFO INVALIDATION BROADCASTS &harr;</text>
            </g>

            <rect x="25" y="148" width="315" height="50" rx="3" fill="#f0f9ff" stroke="#bae6fd"/>
            <text x="35" y="166" font-size="8" font-weight="700" fill="#0369a1">PHYSICAL MEMORY LINE: [0x80001000]</text>
            <text id="m-txt-mem-lock" x="35" y="184" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#0284c7">Value: 1 (LOCKED BY CORE 0)</text>
          </g>

          <!-- Core 1 & 2 (Spinners) -->
          <g transform="translate(575, 20)">
            <rect width="170" height="210" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="12" y="24" font-size="9.5" font-weight="700" fill="#d97706">CORE 1 [Spinner]</text>

            <rect x="10" y="36" width="150" height="42" rx="3" fill="#fef3c7" stroke="#d97706"/>
            <text x="18" y="52" font-size="8" font-weight="700" fill="#92400e">SPINNING CODE:</text>
            <text id="m-txt-c1-code" x="18" y="68" font-family="var(--font-mono)" font-size="8" fill="#b45309">while (xchg(&amp;lock, 1))</text>

            <rect id="m-rect-c1-cache" x="10" y="86" width="150" height="52" rx="3" fill="#fee2e2" stroke="#dc2626"/>
            <text x="18" y="102" font-size="8" font-weight="700" fill="#991b1b">L1 CACHE (MESI):</text>
            <text id="m-txt-c1-mesi" x="18" y="122" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="#dc2626">INVALID [I]</text>

            <rect x="10" y="146" width="150" height="52" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="18" y="162" font-size="7.5" font-weight="700" fill="#475569">MICRO-OP STATE:</text>
            <text id="m-txt-c1-state" x="18" y="180" font-size="7.5" fill="#64748b">Cache line invalidated</text>
          </g>
        </svg>
      </div>

      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="m-btn-prev" onclick="stepMesi(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="m-btn-next" onclick="stepMesi(1)">Next Step &rarr;</button>
          <button class="btn-step" id="m-btn-reset" onclick="resetMesi()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="m-txt-narrative">Core 0 holds the spinlock in its L1 cache with MESI state Modified (M). Core 1 is waiting for the lock.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="m-txt-what">Core 0 holds the lock line exclusively. Core 1 prepares to test the spinlock.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="m-txt-why">Baseline state showing how MESI coherency establishes single-core exclusivity.</p>
        </div>
      </div>
    </div>
"""

# =====================================================================
# 3. LINUX FUTEX STEPPER (Module 03, Section 3)
# =====================================================================
FUTEX_STEPPER_HTML = r"""
    <!-- Interactive Aid: Linux Futex Fast-Path vs Slow-Path -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Linux Futex Fast-Path vs. Kernel Slow-Path</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="f-dim-fast" onclick="setFutexDim('fast')">Uncontended (Fast-Path)</button>
          <button class="dim-btn" id="f-dim-slow" onclick="setFutexDim('slow')">Contended (FUTEX_WAIT)</button>
          <button class="dim-btn" id="f-dim-wake" onclick="setFutexDim('wake')">Unlock (FUTEX_WAKE)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Execution Path</span>
        <span id="f-scenario-text">Thread A acquires an uncontended lock. It executes entirely in Ring 3 user space with a single atomic CAS instruction, incurring ZERO system calls.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Timeline Clock</span>
          <span class="telemetry-val highlight" id="f-telem-time">T = 0 ns</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Current Privilege Ring</span>
          <span class="telemetry-val" id="f-telem-ring">Ring 3 (User Space)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">User Futex Word (*uaddr)</span>
          <span class="telemetry-val highlight" id="f-telem-uaddr">0 (UNLOCKED)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">System Call Count</span>
          <span class="telemetry-val highlight" id="f-telem-syscalls">0 Syscalls</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Execution Latency</span>
          <span class="telemetry-val highlight" id="f-telem-lat">~5 ns (Fast Path)</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="hw-canvas" viewBox="0 0 760 250">
          <defs>
            <marker id="f-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
            </marker>
            <marker id="f-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
            </marker>
            <marker id="f-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
            </marker>
          </defs>

          <!-- Top Half: Ring 3 User Space -->
          <g transform="translate(20, 15)">
            <rect width="720" height="105" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
            <text x="16" y="22" font-size="10" font-weight="700" fill="#0284c7">RING 3: USER-SPACE VIRTUAL MEMORY (Fast-Path Domain)</text>

            <!-- Thread Context Box -->
            <rect id="f-rect-u-thread" x="14" y="34" width="220" height="60" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="24" y="52" font-size="8" font-weight="700" fill="#0369a1">ACTIVE THREAD: Thread A</text>
            <text id="f-txt-u-action" x="24" y="70" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#0f172a">atomic_cas(uaddr, 0, 1)</text>
            <text id="f-txt-u-ring-label" x="24" y="84" font-size="7.5" fill="#64748b">No kernel privilege required</text>

            <!-- Futex Word Box -->
            <rect id="f-rect-uaddr" x="250" y="34" width="220" height="60" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
            <text x="260" y="52" font-size="8" font-weight="700" fill="#475569">FUTEX WORD: uint32_t *uaddr</text>
            <text id="f-txt-uaddr-val" x="360" y="74" text-anchor="middle" font-family="var(--font-mono)" font-size="16" font-weight="700" fill="#059669">0 (FREE)</text>
            <text id="f-txt-uaddr-desc" x="360" y="87" text-anchor="middle" font-size="7.5" fill="#64748b">0=Free, 1=Held, 2=Waiters</text>

            <!-- Fast-Path Indicator Box -->
            <rect id="f-rect-fast-badge" x="485" y="34" width="220" height="60" rx="4" fill="#dcfce7" stroke="#16a34a"/>
            <text x="595" y="56" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">&#10003; FAST-PATH HIT: ~5 ns</text>
            <text id="f-txt-fast-desc" x="595" y="74" text-anchor="middle" font-size="7.5" fill="#166534">Atomic swap succeeds in user space</text>
            <text x="595" y="86" text-anchor="middle" font-size="7.5" font-weight="700" fill="#166534">ZERO KERNEL SYSTEM CALLS</text>
          </g>

          <!-- Divider: Ring Transition Boundary -->
          <line x1="20" y1="130" x2="740" y2="130" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 4"/>
          <text x="380" y="134" text-anchor="middle" font-size="7.5" font-weight="700" fill="#64748b">USER / KERNEL PRIVILEGE BOUNDARY (syscall / sysret)</text>

          <!-- Bottom Half: Ring 0 Kernel Space -->
          <g transform="translate(20, 145)">
            <rect width="720" height="90" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="16" y="20" font-size="10" font-weight="700" fill="#0f172a">RING 0: KERNEL SPACE (Slow-Path Domain &mdash; sys_futex)</text>

            <!-- Kernel Wait Queue Bucket -->
            <rect id="f-rect-k-queue" x="14" y="28" width="456" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="24" y="44" font-size="8" font-weight="700" fill="#475569">KERNEL HASH BUCKET WAIT QUEUE: futex_queues[hash(uaddr)]</text>
            <text id="f-txt-k-queue-items" x="24" y="64" font-family="var(--font-mono)" font-size="9" fill="#94a3b8">[Queue Empty: No Threads Sleeping]</text>

            <!-- Scheduler Action Box -->
            <rect id="f-rect-k-sched" x="485" y="28" width="220" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="495" y="44" font-size="8" font-weight="700" fill="#475569">OS SCHEDULER:</text>
            <text id="f-txt-k-sched" x="495" y="64" font-size="8.5" font-weight="600" fill="#64748b">No descheduling required</text>
          </g>
        </svg>
      </div>

      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="f-btn-prev" onclick="stepFutex(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="f-btn-next" onclick="stepFutex(1)">Next Step &rarr;</button>
          <button class="btn-step" id="f-btn-reset" onclick="resetFutex()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="f-txt-narrative">Futex variable is 0 (unlocked). Thread A issues an atomic CAS to claim the lock.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="f-txt-what">Thread A executes atomic cmpxchg(uaddr, 0, 1) entirely inside Ring 3 user memory.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="f-txt-why">Uncontended locks should execute in single-digit nanoseconds without paying the overhead of kernel traps.</p>
        </div>
      </div>
    </div>
"""

# =====================================================================
# 4. READERS-WRITERS FAIR QUEUEING STEPPER (Module 04, Section 3)
# =====================================================================
RW_STEPPER_HTML = r"""
    <!-- Interactive Aid: Readers-Writers Starvation vs Fair Turnstile -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Readers-Writers Starvation vs. Fair Turnstile</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="rw-dim-starve" onclick="setRwDim('starve')">Reader-Preference (Starvation)</button>
          <button class="dim-btn" id="rw-dim-fair" onclick="setRwDim('fair')">Fair Turnstile (Bounded)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Policy Simulation</span>
        <span id="rw-scenario-text">Reader R1 is currently reading the database. Writer W1 arrives to submit an update. Under Reader-Preference, continuous overlapping reader arrivals starve W1 permanently.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Timeline Clock</span>
          <span class="telemetry-val highlight" id="rw-telem-time">T = 0 ms</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Active Readers Inside</span>
          <span class="telemetry-val" id="rw-telem-rc">read_count = 1</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Writer Queue State</span>
          <span class="telemetry-val" id="rw-telem-writer">W1 Awaiting Entry</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Database Access Mode</span>
          <span class="telemetry-val highlight" id="rw-telem-db">SHARED_READ</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Fairness Metric</span>
          <span class="telemetry-val highlight" id="rw-telem-status">Nominal</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="hw-canvas" viewBox="0 0 760 250">
          <!-- Left: Turnstile Entry Gate -->
          <g transform="translate(20, 20)">
            <rect width="210" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="10.5" font-weight="700" fill="#0284c7">ENTRY TURNSTILE GATE</text>

            <rect id="rw-rect-gate" x="12" y="38" width="186" height="48" rx="4" fill="#dcfce7" stroke="#16a34a"/>
            <text id="rw-txt-gate-title" x="105" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">GATE STATUS: OPEN</text>
            <text id="rw-txt-gate-sub" x="105" y="74" text-anchor="middle" font-size="7.5" fill="#166534">Readers pass freely</text>

            <!-- Waiting Threads Queue -->
            <rect x="12" y="96" width="186" height="100" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="114" font-size="8" font-weight="700" fill="#475569">PENDING ARRIVAL QUEUE:</text>
            <text id="rw-txt-q-r2" x="20" y="134" font-family="var(--font-mono)" font-size="8.5" fill="#0284c7">Reader R2 (Arrived T=1)</text>
            <text id="rw-txt-q-w1" x="20" y="152" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#dc2626">Writer W1 (Blocked T=1)</text>
            <text id="rw-txt-q-r3" x="20" y="170" font-family="var(--font-mono)" font-size="8.5" fill="#0284c7">Reader R3 (Arrived T=2)</text>
          </g>

          <!-- Middle: Database Chamber -->
          <g transform="translate(250, 20)">
            <rect width="260" height="210" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
            <text x="130" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0f172a">SHARED DATABASE CHAMBER</text>

            <!-- Database Content Block -->
            <rect id="rw-rect-db-state" x="15" y="40" width="230" height="90" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
            <text id="rw-txt-db-mode" x="130" y="64" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0369a1">CURRENT MODE: SHARED READ</text>
            <text id="rw-txt-db-readers" x="130" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="14" font-weight="700" fill="#0284c7">Active: [R1]</text>
            <text id="rw-txt-db-count" x="130" y="112" text-anchor="middle" font-size="8" fill="#64748b">read_count = 1 | db_mutex HELD</text>

            <!-- Semaphore Readout -->
            <rect x="15" y="140" width="230" height="56" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="24" y="158" font-size="8" font-weight="700" fill="#475569">SYNCHRONIZATION STATE:</text>
            <text id="rw-txt-db-sem" x="24" y="176" font-family="var(--font-mono)" font-size="8.5" fill="#0f172a">db_mutex=0 (Held by Readers)</text>
          </g>

          <!-- Right: Writer Status & Starvation Telemetry -->
          <g transform="translate(530, 20)">
            <rect width="210" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="10.5" font-weight="700" fill="#dc2626">WRITER W1 STATUS</text>

            <rect id="rw-rect-w1-badge" x="12" y="38" width="186" height="60" rx="4" fill="#fee2e2" stroke="#dc2626"/>
            <text id="rw-txt-w1-status" x="105" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">WRITER STARVING!</text>
            <text id="rw-txt-w1-sub" x="105" y="78" text-anchor="middle" font-size="7.5" fill="#7f1d1d">Blocked on db_mutex</text>

            <rect x="12" y="108" width="186" height="88" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="126" font-size="8" font-weight="700" fill="#475569">FAIRNESS METRICS:</text>
            <text id="rw-txt-w-wait" x="20" y="146" font-family="var(--font-mono)" font-size="8.5" fill="#dc2626">Wait Time: 0 ms</text>
            <text id="rw-txt-bypass-count" x="20" y="164" font-size="8" fill="#64748b">Readers Bypassed: 0</text>
            <text id="rw-txt-fairness-tag" x="20" y="180" font-size="7.5" font-weight="700" fill="#dc2626">Starvation Risk: HIGH</text>
          </g>
        </svg>
      </div>

      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="rw-btn-prev" onclick="stepRw(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="rw-btn-next" onclick="stepRw(1)">Next Step &rarr;</button>
          <button class="btn-step" id="rw-btn-reset" onclick="resetRw()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="rw-txt-narrative">Initial State: Reader R1 is inside the database. Writer W1 and Reader R2 arrive simultaneously.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="rw-txt-what">Reader R1 holds db_mutex. Writer W1 and Reader R2 arrive at the gate.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="rw-txt-why">Baseline setup demonstrating how different scheduling policies arbitrate competing reader and writer queues.</p>
        </div>
      </div>
    </div>
"""

# =====================================================================
# JAVASCRIPT CODE BLOCKS FOR STEPPERS
# =====================================================================
JS_MOD02_APPEND = r"""
  <script>
    // --- PETERSON STEPPER LOGIC ---
    const petersonSteps = {
      sc: [
        {
          time: "T = 0 ns", p0: "flag[0] = false", p1: "flag[1] = false", turn: "turn = 0", status: "Empty (Safe)",
          c0Stage: "STAGE: IDLE", c0Instr: "enter_region(0)", c0Sbuf: "[Buffer Empty]",
          c1Stage: "STAGE: IDLE", c1Instr: "enter_region(1)", c1Sbuf: "[Buffer Empty]",
          flags: "flag[0]=F | flag[1]=F", turnMem: "turn = 0",
          csBadge: "&#10003; CRITICAL REGION: VACANT", csFill: "#dcfce7", csStroke: "#16a34a", csColor: "#166534",
          narrative: "Initial state: Both processes are in remainder sections. Flags are false. Turn is 0.",
          what: "Sequential consistency assumes writes update memory immediately without store buffers.",
          why: "Baseline setup for theoretical two-process mutual exclusion."
        },
        {
          time: "T = 5 ns", p0: "flag[0] = true", p1: "flag[1] = true", turn: "turn = 1 (P0 yielded)", status: "Contention",
          c0Stage: "P0: INTENT SET", c0Instr: "turn = 1", c0Sbuf: "[Drained to RAM]",
          c1Stage: "P1: INTENT SET", c1Instr: "turn = 0", c1Sbuf: "[Drained to RAM]",
          flags: "flag[0]=T | flag[1]=T", turnMem: "turn = 1",
          csBadge: "ARBITRATION IN PROGRESS", csFill: "#fef3c7", csStroke: "#d97706", csColor: "#92400e",
          narrative: "Both declare intent. P0 sets flag[0]=true and turn=1. Memory immediately commits writes.",
          what: "P0 announces it wants to enter and politely offers turn=1 to P1.",
          why: "Peterson requires declaring intent before testing competitor."
        },
        {
          time: "T = 10 ns", p0: "P0 ENTERS CS", p1: "P1 SPINS", turn: "turn = 0 (FINAL)", status: "P0 Active in CS",
          c0Stage: "IN CRITICAL SECTION", c0Instr: "balance += 100", c0Sbuf: "[CS Active]",
          c1Stage: "SPINNING IN WHILE", c1Instr: "while (flag[0] && turn==0)", c1Sbuf: "[Blocked]",
          flags: "flag[0]=T | flag[1]=T", turnMem: "turn = 0 (P1 OVERWROTE)",
          csBadge: "&#10003; CS HELD BY P0 (P1 WAITING)", csFill: "#dcfce7", csStroke: "#16a34a", csColor: "#166534",
          narrative: "P1 executes turn=0 last, overwriting turn! P0 evaluates while condition: turn==1 is false! P0 enters CS. P1 spins safely.",
          what: "P1's write to turn overwrote P0's write. This broke the tie cleanly, granting entry to P0.",
          why: "Mutual exclusion is strictly preserved under Sequential Consistency."
        }
      ],
      ooo: [
        {
          time: "T = 0 ns", p0: "flag[0]=false", p1: "flag[1]=false", turn: "turn = 0", status: "Out-of-Order Silicon",
          c0Stage: "IDLE", c0Instr: "flag[0] = true", c0Sbuf: "[Empty]",
          c1Stage: "IDLE", c1Instr: "flag[1] = true", c1Sbuf: "[Empty]",
          flags: "flag[0]=F | flag[1]=F", turnMem: "turn = 0",
          csBadge: "REAL HARDWARE (OOO)", csFill: "#f8fafc", csStroke: "#cbd5e1", csColor: "#475569",
          narrative: "On modern out-of-order processors, CPU cores use private FIFO Store Buffers to hide write latencies.",
          what: "Stores are queued into store buffers before updating L1 cache.",
          why: "CPUs cannot stall execution waiting for memory bus write cycles."
        },
        {
          time: "T = 5 ns", p0: "Store Buffered!", p1: "Store Buffered!", turn: "turn = 0 in DRAM", status: "STORE-LOAD REORDER",
          c0Stage: "FLAG WRITE BUFFERED", c0Instr: "read flag[1] (Early)", c0Sbuf: "STORE: flag[0]=T (Uncommitted)",
          c1Stage: "FLAG WRITE BUFFERED", c1Instr: "read flag[0] (Early)", c1Sbuf: "STORE: flag[1]=T (Uncommitted)",
          flags: "flag[0]=F | flag[1]=F (STALE)", turnMem: "turn = 0",
          csBadge: "&times; STORE BUFFER NOT FLUSHED!", csFill: "#fee2e2", csStroke: "#dc2626", csColor: "#991b1b",
          narrative: "CRITICAL HARDWARE HAZARD: Both cores buffer their writes to flag[]. To optimize throughput, the CPU reorders subsequent LOADS ahead of pending STORES. Both cores read stale false flags from RAM!",
          what: "Both cores read their peer's flag as false because writes are still trapped inside private store buffers.",
          why: "Store-Load reordering is permitted on x86 and ARM to hide memory bus latency."
        },
        {
          time: "T = 10 ns", p0: "BOTH IN CS!", p1: "BOTH IN CS!", turn: "turn = ?", status: "SAFETY VIOLATION!",
          c0Stage: "ENTERS CS (BUG!)", c0Instr: "balance += 100", c0Sbuf: "[Buffered]",
          c1Stage: "ENTERS CS (BUG!)", c1Instr: "balance -= 50", c1Sbuf: "[Buffered]",
          flags: "flag[0]=T | flag[1]=T", turnMem: "turn = ?",
          csBadge: "&times; MUTUAL EXCLUSION COLLAPSED!", csFill: "#fee2e2", csStroke: "#dc2626", csColor: "#991b1b",
          narrative: "DISASTER: Because both cores read stale flags as false, both while loops evaluate to FALSE immediately! Both P0 and P1 enter the Critical Section simultaneously! Data is corrupted!",
          what: "Simultaneous execution inside critical section due to store-buffer latency.",
          why: "Peterson's algorithm fails completely on modern silicon without memory barriers."
        }
      ],
      fence: [
        {
          time: "T = 0 ns", p0: "flag[0]=false", p1: "flag[1]=false", turn: "turn = 0", status: "Memory Fence Active",
          c0Stage: "IDLE", c0Instr: "flag[0]=true; mfence;", c0Sbuf: "[Empty]",
          c1Stage: "IDLE", c1Instr: "flag[1]=true; mfence;", c1Sbuf: "[Empty]",
          flags: "flag[0]=F | flag[1]=F", turnMem: "turn = 0",
          csBadge: "&#10003; MFENCE PROTECTION ACTIVE", csFill: "#dcfce7", csStroke: "#16a34a", csColor: "#166534",
          narrative: "The compiler inserts architectural memory fences (mfence / dmb ish) to force store buffers to drain before loads can execute.",
          what: "Memory fences enforce strict sequential consistency across store buffers.",
          why: "Hardware is instructed not to reorder loads ahead of uncommitted stores."
        },
        {
          time: "T = 5 ns", p0: "FENCE DRAINING", p1: "FENCE DRAINING", turn: "turn = 1", status: "Draining Buffers",
          c0Stage: "PIPELINE STALLED ON FENCE", c0Instr: "mfence (Flushing)", c0Sbuf: "Flushing flag[0] -> RAM",
          c1Stage: "PIPELINE STALLED ON FENCE", c1Instr: "mfence (Flushing)", c1Sbuf: "Flushing flag[1] -> RAM",
          flags: "flag[0]=T | flag[1]=T", turnMem: "turn = 1",
          csBadge: "COMMITTING WRITES ACROSS BUS", csFill: "#fef3c7", csStroke: "#d97706", csColor: "#92400e",
          narrative: "The fence instruction stalls the processor core until all pending stores in the store buffer have been committed to physical cache.",
          what: "Store buffers are flushed. RAM receives true for both flags before any while loop executes.",
          why: "Eliminates the window where stale memory could be read by competing cores."
        },
        {
          time: "T = 10 ns", p0: "P0 IN CS", p1: "P1 SPINS", turn: "turn = 0", status: "Safe Synchronization",
          c0Stage: "IN CS (SAFE)", c0Instr: "balance += 100", c0Sbuf: "[Drained]",
          c1Stage: "SPINNING (SAFE)", c1Instr: "while loop", c1Sbuf: "[Drained]",
          flags: "flag[0]=T | flag[1]=T", turnMem: "turn = 0",
          csBadge: "&#10003; PERFECT MUTEX ENFORCED", csFill: "#dcfce7", csStroke: "#16a34a", csColor: "#166534",
          narrative: "Reads now observe the committed flags. P1's turn write breaks the tie safely. P0 enters; P1 spins. Correctness restored!",
          what: "Mutual exclusion operates with mathematically proven safety on modern hardware.",
          why: "Memory barriers bridge the gap between abstract algorithms and physical silicon."
        }
      ]
    };

    let activePetersonDim = "sc";
    let activePetersonStep = 0;

    function renderPeterson() {
      const steps = petersonSteps[activePetersonDim];
      const step = steps[activePetersonStep];

      document.getElementById("p-telem-time").textContent = step.time;
      document.getElementById("p-telem-p0").textContent = step.p0;
      document.getElementById("p-telem-p1").textContent = step.p1;
      document.getElementById("p-telem-turn").textContent = step.turn;
      document.getElementById("p-telem-status").textContent = step.status;

      document.getElementById("p-txt-c0-stage").textContent = step.c0Stage;
      document.getElementById("p-txt-c0-instr").textContent = step.c0Instr;
      document.getElementById("p-txt-c0-sbuf").textContent = step.c0Sbuf;

      document.getElementById("p-txt-c1-stage").textContent = step.c1Stage;
      document.getElementById("p-txt-c1-instr").textContent = step.c1Instr;
      document.getElementById("p-txt-c1-sbuf").textContent = step.c1Sbuf;

      document.getElementById("p-txt-mem-flags").textContent = step.flags;
      document.getElementById("p-txt-mem-turn").textContent = step.turnMem;

      document.getElementById("p-txt-cs-badge").innerHTML = step.csBadge;
      document.getElementById("p-rect-cs-badge").setAttribute("fill", step.csFill);
      document.getElementById("p-rect-cs-badge").setAttribute("stroke", step.csStroke);
      document.getElementById("p-txt-cs-badge").setAttribute("fill", step.csColor);

      document.getElementById("p-txt-narrative").innerHTML = step.narrative;
      document.getElementById("p-txt-what").innerHTML = step.what;
      document.getElementById("p-txt-why").innerHTML = step.why;

      document.getElementById("p-btn-prev").disabled = (activePetersonStep === 0);
      document.getElementById("p-btn-next").disabled = (activePetersonStep === steps.length - 1);
    }

    function stepPeterson(delta) {
      const steps = petersonSteps[activePetersonDim];
      activePetersonStep = Math.max(0, Math.min(steps.length - 1, activePetersonStep + delta));
      renderPeterson();
    }

    function resetPeterson() {
      activePetersonStep = 0;
      renderPeterson();
    }

    function setPetersonDim(dim) {
      activePetersonDim = dim;
      activePetersonStep = 0;
      document.getElementById("p-dim-sc").classList.toggle("active", dim === "sc");
      document.getElementById("p-dim-ooo").classList.toggle("active", dim === "ooo");
      document.getElementById("p-dim-fence").classList.toggle("active", dim === "fence");
      renderPeterson();
    }

    // --- MESI SIMULATOR LOGIC ---
    const mesiSteps = {
      naive: [
        {
          time: "T = 0 ns", c0: "Modified (M)", c1: "Invalid (I)", bus: "0 MB/s", status: "Core 0 Holds Lock",
          c0Mesi: "MODIFIED [M]", c1Mesi: "INVALID [I]",
          c1Code: "while (xchg(&lock, 1))", c1State: "Prepares atomic write",
          busTitle: "INTERCONNECT STATUS: QUIET", busDesc: "No invalidation storm active", busMetric: "Bandwidth: 0 GB/s",
          busStorm: false, memVal: "1 (LOCKED BY CORE 0)",
          narrative: "Core 0 holds the lock line exclusively in Modified (M) state. Core 1 prepares to enter spinlock.",
          what: "Core 0 holds lock line in L1 cache. Core 1 begins spin loop.",
          why: "Baseline single-core lock ownership."
        },
        {
          time: "T = 10 ns", c0: "Invalidated (I)!", c1: "Modified (M)", bus: "25.6 GB/s (STORM!)", status: "CACHELINE BOUNCE!",
          c0Mesi: "INVALID [I]", c1Mesi: "MODIFIED [M]",
          c1Code: "xchg(&lock, 1) -> 1", c1State: "Broadcasts RFO write!",
          busTitle: "INTERCONNECT STATUS: SATURATED!", busDesc: "Read-For-Ownership (RFO) storm active", busMetric: "Bandwidth: 25.6 GB/s (BUS SATURATED)",
          busStorm: true, memVal: "1 (LOCKED)",
          narrative: "Core 1 executes atomic xchg. This forces a write, broadcasting an Invalidate signal across the bus! Core 0's cache line is forcibly invalidated.",
          what: "Core 1 snatches exclusive ownership of the cache line just to write 1 and fail.",
          why: "Atomic instructions always require write ownership under MESI coherency."
        },
        {
          time: "T = 20 ns", c0: "Re-snatches (M)", c1: "Invalidated (I)!", bus: "32.0 GB/s (THRASHING)", status: "BUS CONGESTION",
          c0Mesi: "MODIFIED [M]", c1Mesi: "INVALID [I]",
          c1Code: "while (xchg(&lock, 1))", c1State: "Cacheline stolen back!",
          busTitle: "INTERCONNECT STATUS: THRASHING", busDesc: "Cache line bounces endlessly between cores", busMetric: "Bandwidth: 32.0 GB/s (OVERHEAT)",
          busStorm: true, memVal: "1 (LOCKED)",
          narrative: "Core 0 attempts to complete its critical section, requiring the cacheline back. The line bounces back and forth across the interconnect, killing bus throughput for all cores.",
          what: "Repeated atomic exchanges force continuous cache invalidations.",
          why: "Cacheline bouncing destroys scalability on multi-core sockets."
        }
      ],
      ttas: [
        {
          time: "T = 0 ns", c0: "Modified (M)", c1: "Shared (S)", bus: "0 MB/s", status: "Shared Cache Hits",
          c0Mesi: "MODIFIED [M]", c1Mesi: "SHARED [S]",
          c1Code: "while (lock == 1) pause;", c1State: "Spinning on local read",
          busTitle: "TTAS EFFICIENCY: ZERO BUS TRAFFIC", busDesc: "Spinners read locally from shared L1 cache", busMetric: "Bus Bandwidth: 0 GB/s (Silent)",
          busStorm: false, memVal: "1 (LOCKED)",
          narrative: "Under TTAS, Core 1 spins using standard READ instructions. Multiple cores hold the line in Shared (S) state without issuing bus writes.",
          what: "Core 1 spins in a local read-only loop. Bus traffic drops to zero.",
          why: "Reading a shared cache line does not invalidate peer caches."
        },
        {
          time: "T = 15 ns", c0: "Unlocks (Store 0)", c1: "Shared -> Excl", bus: "Single Invalidate", status: "Clean Handoff",
          c0Mesi: "INVALID [I]", c1Mesi: "EXCLUSIVE [E]",
          c1Code: "lock == 0 -> xchg succeeds!", c1State: "Claims freed lock",
          busTitle: "TTAS EFFICIENCY: CLEAN HANDOFF", busDesc: "Atomic write issued ONLY when lock is observed free", busMetric: "Bus Bandwidth: Normal (Clean)",
          busStorm: false, memVal: "0 -> 1 (HANDOFF TO C1)",
          narrative: "Core 0 stores 0 to unlock. Core 1 detects lock == 0 in its local cache, exits the read loop, and executes a single atomic xchg to claim the lock. Clean and scalable!",
          what: "Atomic write is executed exactly once upon lock release.",
          why: "TTAS eliminates O(N^2) invalidation storms across multi-core processors."
        }
      ]
    };

    let activeMesiDim = "naive";
    let activeMesiStep = 0;

    function renderMesi() {
      const steps = mesiSteps[activeMesiDim];
      const step = steps[activeMesiStep];

      document.getElementById("m-telem-time").textContent = step.time;
      document.getElementById("m-telem-c0").textContent = step.c0;
      document.getElementById("m-telem-c1").textContent = step.c1;
      document.getElementById("m-telem-bus").textContent = step.bus;
      document.getElementById("m-telem-status").textContent = step.status;

      document.getElementById("m-txt-c0-mesi").textContent = step.c0Mesi;
      document.getElementById("m-txt-c1-mesi").textContent = step.c1Mesi;
      document.getElementById("m-txt-c1-code").textContent = step.c1Code;
      document.getElementById("m-txt-c1-state").textContent = step.c1State;

      document.getElementById("m-txt-bus-title").textContent = step.busTitle;
      document.getElementById("m-txt-bus-desc").textContent = step.busDesc;
      document.getElementById("m-txt-bus-metric").textContent = step.busMetric;
      document.getElementById("m-grp-storm-arrows").style.display = step.busStorm ? "block" : "none";

      document.getElementById("m-txt-mem-lock").textContent = step.memVal;

      document.getElementById("m-txt-narrative").innerHTML = step.narrative;
      document.getElementById("m-txt-what").innerHTML = step.what;
      document.getElementById("m-txt-why").innerHTML = step.why;

      document.getElementById("m-btn-prev").disabled = (activeMesiStep === 0);
      document.getElementById("m-btn-next").disabled = (activeMesiStep === steps.length - 1);
    }

    function stepMesi(delta) {
      const steps = mesiSteps[activeMesiDim];
      activeMesiStep = Math.max(0, Math.min(steps.length - 1, activeMesiStep + delta));
      renderMesi();
    }

    function resetMesi() {
      activeMesiStep = 0;
      renderMesi();
    }

    function setMesiDim(dim) {
      activeMesiDim = dim;
      activeMesiStep = 0;
      document.getElementById("m-dim-naive").classList.toggle("active", dim === "naive");
      document.getElementById("m-dim-ttas").classList.toggle("active", dim === "ttas");
      renderMesi();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderPeterson();
      renderMesi();
    });
  </script>
"""

# =====================================================================
# JAVASCRIPT LOGIC FOR MODULE 03 (FUTEX)
# =====================================================================
JS_MOD03_APPEND = r"""
  <script>
    const futexSteps = {
      fast: [
        {
          time: "T = 0 ns", ring: "Ring 3 (User Space)", uaddr: "0 (UNLOCKED)", syscalls: "0 Syscalls", lat: "~5 ns (Fast Path)",
          action: "atomic_cas(uaddr, 0, 1)", uaddrVal: "0 (FREE)", uaddrColor: "#059669",
          fastDesc: "Atomic CAS succeeds in user space",
          queueItems: "[Queue Empty: No Threads Sleeping]", sched: "No descheduling required",
          narrative: "Thread A attempts to acquire an uncontended mutex (*uaddr == 0).",
          what: "Thread A executes atomic cmpxchg in Ring 3 user space.",
          why: "Uncontended mutexes require zero kernel privileges."
        },
        {
          time: "T = 5 ns", ring: "Ring 3 (User Space)", uaddr: "1 (LOCKED BY THREAD A)", syscalls: "0 Syscalls", lat: "5 ns (COMPLETE)",
          action: "In Critical Section", uaddrVal: "1 (LOCKED)", uaddrColor: "#dc2626",
          fastDesc: "LOCK ACQUIRED WITH ZERO SYSCALLS!",
          queueItems: "[Queue Empty]", sched: "Thread A running in user space",
          narrative: "Atomic CAS succeeds! *uaddr is set from 0 to 1. Thread A enters its critical section immediately without entering the kernel!",
          what: "Thread A claims the lock in 5 nanoseconds.",
          why: "Eliminates kernel trap latency when no contention exists."
        }
      ],
      slow: [
        {
          time: "T = 0 ns", ring: "Ring 3 (User Space)", uaddr: "1 (HELD BY THREAD A)", syscalls: "0 Syscalls", lat: "Contention Detected",
          action: "atomic_cas(uaddr, 0, 1) -> FAILS", uaddrVal: "1 (LOCKED)", uaddrColor: "#dc2626",
          fastDesc: "Fast-path CAS failed: Lock already held",
          queueItems: "[Queue Empty]", sched: "Thread B must block",
          narrative: "Thread B attempts to acquire the lock, but finds *uaddr is already 1. Fast-path fails! Thread B must invoke the kernel slow-path.",
          what: "CAS returns failure. Thread B cannot enter critical section.",
          why: "Contended locks require operating system thread descheduling."
        },
        {
          time: "T = 150 ns", ring: "Ring 0 (Kernel Mode)", uaddr: "2 (WAITERS PRESENT)", syscalls: "1 (FUTEX_WAIT)", lat: "~200 ns (Syscall)",
          action: "sys_futex(uaddr, FUTEX_WAIT, 2)", uaddrVal: "2 (CONTENDED)", uaddrColor: "#dc2626",
          fastDesc: "DROPPED INTO KERNEL SLOW-PATH",
          queueItems: "futex_queues: [Thread B Enqueued & Blocked]", sched: "Thread B descheduled -> OS runs others",
          narrative: "Thread B sets *uaddr=2 and executes sys_futex(FUTEX_WAIT). The kernel verifies memory, puts Thread B on a wait queue, and context switches away.",
          what: "Kernel verifies *uaddr==2, suspends Thread B, and frees the CPU.",
          why: "Sleeping prevents Thread B from burning 100% CPU on spin loops."
        }
      ],
      wake: [
        {
          time: "T = 0 ns", ring: "Ring 3 -> Ring 0", uaddr: "2 (WAITERS PRESENT)", syscalls: "1 (FUTEX_WAKE)", lat: "~150 ns",
          action: "Thread A: sys_futex(FUTEX_WAKE, 1)", uaddrVal: "0 (RELEASED)", uaddrColor: "#059669",
          fastDesc: "Thread A releases lock & wakes waiter",
          queueItems: "futex_queues: [Thread B Waking Up]", sched: "Thread B moved to READY queue",
          narrative: "Thread A finishes its critical section. Seeing *uaddr was 2 (waiters present), it resets *uaddr=0 and issues sys_futex(FUTEX_WAKE, 1).",
          what: "Kernel wakes Thread B from hash queue and transitions it to READY.",
          why: "Guarantees prompt handoff without lost wakeup defects."
        }
      ]
    };

    let activeFutexDim = "fast";
    let activeFutexStep = 0;

    function renderFutex() {
      const steps = futexSteps[activeFutexDim];
      const step = steps[activeFutexStep];

      document.getElementById("f-telem-time").textContent = step.time;
      document.getElementById("f-telem-ring").textContent = step.ring;
      document.getElementById("f-telem-uaddr").textContent = step.uaddr;
      document.getElementById("f-telem-syscalls").textContent = step.syscalls;
      document.getElementById("f-telem-lat").textContent = step.lat;

      document.getElementById("f-txt-u-action").textContent = step.action;
      document.getElementById("f-txt-uaddr-val").textContent = step.uaddrVal;
      document.getElementById("f-txt-uaddr-val").setAttribute("fill", step.uaddrColor);
      document.getElementById("f-txt-fast-desc").textContent = step.fastDesc;

      document.getElementById("f-txt-k-queue-items").textContent = step.queueItems;
      document.getElementById("f-txt-k-sched").textContent = step.sched;

      document.getElementById("f-txt-narrative").innerHTML = step.narrative;
      document.getElementById("f-txt-what").innerHTML = step.what;
      document.getElementById("f-txt-why").innerHTML = step.why;

      document.getElementById("f-btn-prev").disabled = (activeFutexStep === 0);
      document.getElementById("f-btn-next").disabled = (activeFutexStep === steps.length - 1);
    }

    function stepFutex(delta) {
      const steps = futexSteps[activeFutexDim];
      activeFutexStep = Math.max(0, Math.min(steps.length - 1, activeFutexStep + delta));
      renderFutex();
    }

    function resetFutex() {
      activeFutexStep = 0;
      renderFutex();
    }

    function setFutexDim(dim) {
      activeFutexDim = dim;
      activeFutexStep = 0;
      document.getElementById("f-dim-fast").classList.toggle("active", dim === "fast");
      document.getElementById("f-dim-slow").classList.toggle("active", dim === "slow");
      document.getElementById("f-dim-wake").classList.toggle("active", dim === "wake");
      renderFutex();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderFutex();
    });
  </script>
"""

# =====================================================================
# JAVASCRIPT LOGIC FOR MODULE 04 (READERS-WRITERS)
# =====================================================================
JS_MOD04_APPEND = r"""
  <script>
    const rwSteps = {
      starve: [
        {
          time: "T = 0 ms", rc: "read_count = 1", writer: "W1 Arrives (T=0)", db: "SHARED_READ", status: "Reader-Preference",
          gateTitle: "GATE STATUS: OPEN TO READERS", gateSub: "Readers bypass queued writers",
          dbReaders: "Active: [R1]", dbCount: "read_count = 1 | db_mutex Held",
          w1Status: "WRITER BLOCKED ON DB_MUTEX", w1Sub: "Cannot enter while read_count > 0",
          wWait: "Wait: 0 ms", bypass: "Readers Bypassed: 0",
          narrative: "Reader R1 holds db_mutex. Writer W1 arrives and blocks. Under Reader-Preference, gate remains wide open to newly arriving readers.",
          what: "R1 is reading. W1 blocks on db_mutex.",
          why: "Reader-preference allows concurrent readers at the expense of writers."
        },
        {
          time: "T = 1 ms", rc: "read_count = 2", writer: "W1 Starving!", db: "SHARED_READ", status: "R2 Bypasses Writer",
          gateTitle: "GATE STATUS: R2 JUMPS QUEUE!", gateSub: "R2 enters without touching db_mutex",
          dbReaders: "Active: [R1, R2]", dbCount: "read_count = 2 | db_mutex Held",
          w1Status: "W1 STARVING: BYPASSED BY R2", w1Sub: "Waiting in queue...",
          wWait: "Wait: 1 ms", bypass: "Readers Bypassed: 1 (R2)",
          narrative: "Reader R2 arrives! Because read_count > 0, R2 does not check db_mutex; it increments read_count to 2 and enters. W1 is BYPASSED!",
          what: "R2 enters while W1 waits. read_count rises to 2.",
          why: "First readers-writers policy prioritizes read concurrency."
        },
        {
          time: "T = 2 ms", rc: "read_count = 2", writer: "W1 STARVED INDEFINITELY", db: "SHARED_READ", status: "STARVATION PATHOLOGY",
          gateTitle: "GATE STATUS: R3 JUMPS QUEUE!", gateSub: "R1 exits, but R3 enters!",
          dbReaders: "Active: [R2, R3]", dbCount: "read_count = 2 | db_mutex Held",
          w1Status: "W1 STARVED INDEFINITELY!", w1Sub: "read_count NEVER DROPS TO 0!",
          wWait: "Wait: 2 ms (Unbounded)", bypass: "Readers Bypassed: 2 (R2, R3)",
          narrative: "R1 finishes and exits, but R3 arrives before R2 finishes! read_count NEVER reaches 0. Writer W1 is starved indefinitely!",
          what: "Continuous stream of overlapping readers prevents writer from ever entering.",
          why: "Violates Condition 4 (Bounded Waiting): W1 suffers indefinite starvation."
        }
      ],
      fair: [
        {
          time: "T = 0 ms", rc: "read_count = 1", writer: "W1 Arrives at Turnstile", db: "SHARED_READ", status: "Fair Turnstile Active",
          gateTitle: "GATE STATUS: W1 CLAIMS TURNSTILE", gateSub: "Gate locked against NEW readers!",
          dbReaders: "Active: [R1]", dbCount: "read_count = 1 | Turnstile Held",
          w1Status: "W1 HOLDS TURNSTILE", w1Sub: "Awaiting R1 to drain",
          wWait: "Wait: 0 ms", bypass: "Readers Bypassed: 0",
          narrative: "Fair Turnstile: When Writer W1 arrives, it acquires the entry turnstile gate. NEW READERS (R2, R3) ARE BLOCKED AT THE GATE!",
          what: "W1 locks the turnstile gate. Existing readers can finish, but new readers must queue behind W1.",
          why: "Prevents newly arriving readers from jumping ahead of waiting writers."
        },
        {
          time: "T = 1 ms", rc: "read_count = 0", writer: "W1 ENTERS DATABASE!", db: "WRITE_EXCLUSIVE", status: "BOUNDED LATENCY",
          gateTitle: "GATE: R2 & R3 QUEUED BEHIND W1", gateSub: "W1 active in database",
          dbReaders: "Active: [W1 EXCLUSIVE]", dbCount: "read_count = 0 | EXCLUSIVE WRITE",
          w1Status: "WRITING EXCLUSIVELY (SAFE)", w1Sub: "Writing database updates...",
          wWait: "Wait: 1 ms (BOUNDED)", bypass: "Readers Bypassed: 0 (Fair)",
          narrative: "R1 finishes and leaves. read_count drops to 0. W1 enters the database immediately! Zero starvation. Bounded wait time!",
          what: "W1 writes with guaranteed exclusive mutual exclusion.",
          why: "Fairness queuing guarantees bounded waiting for all threads."
        }
      ]
    };

    let activeRwDim = "starve";
    let activeRwStep = 0;

    function renderRw() {
      const steps = rwSteps[activeRwDim];
      const step = steps[activeRwStep];

      document.getElementById("rw-telem-time").textContent = step.time;
      document.getElementById("rw-telem-rc").textContent = step.rc;
      document.getElementById("rw-telem-writer").textContent = step.writer;
      document.getElementById("rw-telem-db").textContent = step.db;
      document.getElementById("rw-telem-status").textContent = step.status;

      document.getElementById("rw-txt-gate-title").textContent = step.gateTitle;
      document.getElementById("rw-txt-gate-sub").textContent = step.gateSub;

      document.getElementById("rw-txt-db-readers").textContent = step.dbReaders;
      document.getElementById("rw-txt-db-count").textContent = step.dbCount;

      document.getElementById("rw-txt-w1-status").textContent = step.w1Status;
      document.getElementById("rw-txt-w1-sub").textContent = step.w1Sub;
      document.getElementById("rw-txt-w-wait").textContent = step.wWait;
      document.getElementById("rw-txt-bypass-count").textContent = step.bypass;

      document.getElementById("rw-txt-narrative").innerHTML = step.narrative;
      document.getElementById("rw-txt-what").innerHTML = step.what;
      document.getElementById("rw-txt-why").innerHTML = step.why;

      document.getElementById("rw-btn-prev").disabled = (activeRwStep === 0);
      document.getElementById("rw-btn-next").disabled = (activeRwStep === steps.length - 1);
    }

    function stepRw(delta) {
      const steps = rwSteps[activeRwDim];
      activeRwStep = Math.max(0, Math.min(steps.length - 1, activeRwStep + delta));
      renderRw();
    }

    function resetRw() {
      activeRwStep = 0;
      renderRw();
    }

    function setRwDim(dim) {
      activeRwDim = dim;
      activeRwStep = 0;
      document.getElementById("rw-dim-starve").classList.toggle("active", dim === "starve");
      document.getElementById("rw-dim-fair").classList.toggle("active", dim === "fair");
      renderRw();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderRw();
    });
  </script>
"""

# =====================================================================
# INTEGRATION ROUTINES
# =====================================================================

def update_module_two():
    with open(MOD02_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insert Peterson Stepper before Section 3
    sec3_marker = "<h3>3. Hardware-Assisted Atomic Instructions</h3>"
    if "p-dim-sc" not in content and sec3_marker in content:
        idx = content.find(sec3_marker)
        content = content[:idx] + PETERSON_STEPPER_HTML + "\n\n    " + content[idx:]

    # 2. Insert MESI Stepper before bottom navbar
    bot_nav_marker = '<nav class="nav-bar" style="margin-top: 36px;'
    if "m-dim-naive" not in content and bot_nav_marker in content:
        idx = content.find(bot_nav_marker)
        content = content[:idx] + MESI_BOUNCING_STEPPER_HTML + "\n\n    " + content[idx:]

    # 3. Append JavaScript
    body_end = "</body>"
    if "petersonSteps" not in content and body_end in content:
        idx = content.find(body_end)
        content = content[:idx] + JS_MOD02_APPEND + "\n" + content[idx:]

    with open(MOD02_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"--> Successfully integrated Steppers A & B into {MOD02_PATH}")

def update_module_three():
    with open(MOD03_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert Futex Stepper before Section 4
    sec4_marker = "<h3>4. Monitors &amp; Condition Variables</h3>"
    if "f-dim-fast" not in content and sec4_marker in content:
        idx = content.find(sec4_marker)
        content = content[:idx] + FUTEX_STEPPER_HTML + "\n\n    " + content[idx:]

    # Append JavaScript
    body_end = "</body>"
    if "futexSteps" not in content and body_end in content:
        idx = content.find(body_end)
        content = content[:idx] + JS_MOD03_APPEND + "\n" + content[idx:]

    with open(MOD03_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"--> Successfully integrated Stepper C into {MOD03_PATH}")

def update_module_four():
    with open(MOD04_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert Readers-Writers Stepper before bottom navbar
    bot_nav_marker = '<nav class="nav-bar" style="margin-top: 36px;'
    if "rw-dim-starve" not in content and bot_nav_marker in content:
        idx = content.find(bot_nav_marker)
        content = content[:idx] + RW_STEPPER_HTML + "\n\n    " + content[idx:]

    # Append JavaScript
    body_end = "</body>"
    if "rwSteps" not in content and body_end in content:
        idx = content.find(body_end)
        content = content[:idx] + JS_MOD04_APPEND + "\n" + content[idx:]

    with open(MOD04_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"--> Successfully integrated Stepper D into {MOD04_PATH}")

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", MOD02_PATH, MOD03_PATH, MOD04_PATH], check=True)
        commit_msg = (
            "Implement comprehensive interactive steppers across Modules 02, 03, 04\n\n"
            "Add Peterson store-buffer reordering aid and MESI bouncing simulator to\n"
            "Module 02, Linux futex user/kernel transition aid to Module 03, and\n"
            "Readers-Writers fair turnstile starvation simulator to Module 04."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_module_two()
    update_module_three()
    update_module_four()
    run_git_sync()
