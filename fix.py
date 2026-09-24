#!/usr/bin/env python3
# =====================================================================
# fix.py: Add Counting Semaphore and Hoare/Mesa Steppers to Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "03-semaphores-mutexes-monitors.html"
)

# =====================================================================
# HTML & SVG FOR AID 1: COUNTING SEMAPHORE RING STEPPER (Section 2)
# =====================================================================
SEMAPHORE_RING_AID = r"""
    <!-- Interactive Aid: Bounded-Buffer Counting Semaphore Pipeline -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Counting Semaphore Bounded-Buffer Pipeline (N = 3)</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="sr-dim-pipe" onclick="setSemRingDim('pipe')">Balanced Pipeline</button>
          <button class="dim-btn" id="sr-dim-sat" onclick="setSemRingDim('sat')">Buffer Saturation (Producer Blocks)</button>
          <button class="dim-btn" id="sr-dim-empty" onclick="setSemRingDim('empty')">Buffer Starvation (Consumer Blocks)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Resource Model</span>
        <span id="sr-scenario-text">Producer and Consumer coordinate over a 3-slot circular buffer using counting semaphores 'empty' (init 3) and 'full' (init 0), guarded by binary semaphore 'mutex' (init 1).</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Timeline Clock</span>
          <span class="telemetry-val highlight" id="sr-telem-time">T = 0 ms</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Active Thread</span>
          <span class="telemetry-val" id="sr-telem-thread">Producer</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">empty Permit Count</span>
          <span class="telemetry-val highlight" id="sr-telem-empty">empty = 3</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">full Item Count</span>
          <span class="telemetry-val" id="sr-telem-full">full = 0</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">mutex Gatekeeper</span>
          <span class="telemetry-val highlight" id="sr-telem-mutex">mutex = 1 (FREE)</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="hw-canvas" viewBox="0 0 760 250">
          <defs>
            <marker id="sr-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
            </marker>
            <marker id="sr-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
            </marker>
          </defs>

          <!-- Left: Producer Context -->
          <g transform="translate(20, 20)">
            <rect width="200" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="10" font-weight="700" fill="#0284c7">PRODUCER THREAD</text>

            <rect id="sr-rect-p-state" x="12" y="36" width="176" height="42" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
            <text id="sr-txt-p-state" x="100" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">STATE: READY</text>

            <rect x="12" y="86" width="176" height="50" rx="4" fill="#0f172a"/>
            <text x="20" y="104" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#94a3b8">NEXT ACTION:</text>
            <text id="sr-txt-p-action" x="20" y="122" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#38bdf8">down(&amp;empty)</text>

            <rect x="12" y="144" width="176" height="56" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="162" font-size="7.5" font-weight="700" fill="#475569">WAIT QUEUE STATUS:</text>
            <text id="sr-txt-p-queue" x="20" y="180" font-family="var(--font-mono)" font-size="8" fill="#64748b">Runnable (Ready)</text>
          </g>

          <!-- Middle: 3-Slot Circular Buffer & Semaphores -->
          <g transform="translate(240, 20)">
            <rect width="280" height="210" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
            <text x="140" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0f172a">BUFFER RING (N = 3) &amp; SEMAPHORES</text>

            <!-- Buffer Slots -->
            <g transform="translate(15, 38)">
              <!-- Slot 0 -->
              <rect id="sr-rect-slot-0" x="0" y="0" width="76" height="46" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
              <text x="38" y="18" text-anchor="middle" font-size="7.5" font-weight="700" fill="#64748b">Slot 0</text>
              <text id="sr-txt-slot-0" x="38" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#94a3b8">[Empty]</text>

              <!-- Slot 1 -->
              <rect id="sr-rect-slot-1" x="87" y="0" width="76" height="46" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
              <text x="125" y="18" text-anchor="middle" font-size="7.5" font-weight="700" fill="#64748b">Slot 1</text>
              <text id="sr-txt-slot-1" x="125" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#94a3b8">[Empty]</text>

              <!-- Slot 2 -->
              <rect id="sr-rect-slot-2" x="174" y="0" width="76" height="46" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
              <text x="212" y="18" text-anchor="middle" font-size="7.5" font-weight="700" fill="#64748b">Slot 2</text>
              <text id="sr-txt-slot-2" x="212" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#94a3b8">[Empty]</text>
            </g>

            <!-- Semaphore Readout Box -->
            <rect id="sr-rect-sem-panel" x="15" y="96" width="250" height="98" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="25" y="114" font-size="8.5" font-weight="700" fill="#475569">SEMAPHORE REGISTRY:</text>

            <text id="sr-txt-sem-empty" x="25" y="136" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#0284c7">empty: 3 (Available Slots)</text>
            <text id="sr-txt-sem-full" x="25" y="154" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#059669">full : 0 (Available Items)</text>
            <text id="sr-txt-sem-mutex" x="25" y="172" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#475569">mutex: 1 (Buffer Lock Free)</text>

            <text id="sr-txt-sem-queue" x="140" y="186" text-anchor="middle" font-size="7.5" font-weight="700" fill="#059669">&#10003; ALL THREADS RUNNABLE</text>
          </g>

          <!-- Right: Consumer Context -->
          <g transform="translate(540, 20)">
            <rect width="200" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="10" font-weight="700" fill="#d97706">CONSUMER THREAD</text>

            <rect id="sr-rect-c-state" x="12" y="36" width="176" height="42" rx="4" fill="#fef3c7" stroke="#d97706"/>
            <text id="sr-txt-c-state" x="100" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="#92400e">STATE: READY</text>

            <rect x="12" y="86" width="176" height="50" rx="4" fill="#0f172a"/>
            <text x="20" y="104" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#94a3b8">NEXT ACTION:</text>
            <text id="sr-txt-c-action" x="20" y="122" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#38bdf8">down(&amp;full)</text>

            <rect x="12" y="144" width="176" height="56" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="162" font-size="7.5" font-weight="700" fill="#475569">WAIT QUEUE STATUS:</text>
            <text id="sr-txt-c-queue" x="20" y="180" font-family="var(--font-mono)" font-size="8" fill="#64748b">Runnable (Ready)</text>
          </g>
        </svg>
      </div>

      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="sr-btn-prev" onclick="stepSemRing(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="sr-btn-next" onclick="stepSemRing(1)">Next Step &rarr;</button>
          <button class="btn-step" id="sr-btn-reset" onclick="resetSemRing()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="sr-txt-narrative">Initial State: Buffer is completely empty (N=3). empty=3, full=0, mutex=1. Both threads are ready.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="sr-txt-what">Counting semaphores are initialized to buffer capacity (empty=3) and available items (full=0).</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="sr-txt-why">Permit counting decouples producer and consumer burst rates up to the queue capacity.</p>
        </div>
      </div>
    </div>
"""

# =====================================================================
# HTML & SVG FOR AID 2: HOARE VS. MESA MONITOR STEPPER (Section 4)
# =====================================================================
MONITOR_MESA_HOARE_AID = r"""
    <!-- Interactive Aid: Hoare vs Mesa Monitor Signaling Stepper -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Hoare vs. Mesa Signaling &amp; The While-Loop Invariant</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="hm-dim-safe" onclick="setHmDim('safe')">Mesa (Safe: while Loop)</button>
          <button class="dim-btn" id="hm-dim-bug" onclick="setHmDim('bug')">Mesa (Bug: if Statement)</button>
          <button class="dim-btn" id="hm-dim-hoare" onclick="setHmDim('hoare')">Hoare (Signal-and-Wait)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Signaling Dilemma</span>
        <span id="hm-scenario-text">Consumer T1 sleeps on condition 'not_empty'. Producer T2 deposits an item and signals. Meanwhile, a newly arrived Consumer T3 attempts to remove an item.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Timeline Clock</span>
          <span class="telemetry-val highlight" id="hm-telem-time">T = 0 ms</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Active Inside Monitor</span>
          <span class="telemetry-val highlight" id="hm-telem-active">Thread 2 (Producer)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Buffer Item Count</span>
          <span class="telemetry-val" id="hm-telem-count">count = 1</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Signaler State</span>
          <span class="telemetry-val" id="hm-telem-signaler">T2 Signaling not_empty</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Safety State</span>
          <span class="telemetry-val highlight" id="hm-telem-status">Nominal</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="hw-canvas" viewBox="0 0 760 260">
          <defs>
            <marker id="hm-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
            </marker>
            <marker id="hm-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
            </marker>
          </defs>

          <!-- Left: Monitor Entry Queue -->
          <g transform="translate(20, 20)">
            <rect width="180" height="220" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="9.5" font-weight="700" fill="#0f172a">MONITOR ENTRY QUEUE</text>

            <rect id="hm-rect-q-t3" x="12" y="38" width="156" height="46" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="56" font-size="8" font-weight="700" fill="#334155">Thread 3 [Sneaky Consumer]</text>
            <text id="hm-txt-q-t3" x="20" y="72" font-size="7.5" fill="#64748b">Arrived at gate &rarr; Ready</text>

            <rect id="hm-rect-q-t1" x="12" y="94" width="156" height="46" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="112" font-size="8" font-weight="700" fill="#334155">Thread 1 [Awakened Consumer]</text>
            <text id="hm-txt-q-t1" x="20" y="128" font-size="7.5" fill="#64748b">Sleeping on cond queue</text>

            <text x="14" y="165" font-size="7.5" fill="#475569">&bull; Entry serialized by mutex</text>
            <text id="hm-txt-q-note" x="14" y="180" font-size="7.5" font-weight="700" fill="#0284c7">Mesa: Signaler retains lock</text>
          </g>

          <!-- Middle: Inside Monitor Chamber -->
          <g transform="translate(220, 20)">
            <rect width="300" height="220" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
            <text x="150" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0284c7">ACTIVE MONITOR CHAMBER (1 THREAD MAX)</text>

            <rect id="hm-rect-active" x="15" y="38" width="270" height="65" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
            <text id="hm-txt-active-title" x="25" y="56" font-size="9" font-weight="700" fill="#166534">ACTIVE: Thread 2 (Producer)</text>
            <text id="hm-txt-active-action" x="25" y="72" font-family="var(--font-mono)" font-size="8" fill="#14532d">insert_item(); signal(not_empty);</text>
            <text id="hm-txt-active-sub" x="25" y="88" font-size="7.5" fill="#15803d">Holds monitor lock until return</text>

            <rect id="hm-rect-buf" x="15" y="115" width="270" height="42" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
            <text x="25" y="132" font-size="8" font-weight="700" fill="#0369a1">SHARED BUFFER STATE:</text>
            <text id="hm-txt-buf-val" x="25" y="146" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#0284c7">count = 1 [Item X Present]</text>

            <rect id="hm-rect-crash" x="15" y="165" width="270" height="44" rx="4" fill="#dcfce7" stroke="#16a34a"/>
            <text id="hm-txt-crash" x="150" y="192" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">&#10003; SYSTEM INVARIANTS SOUND</text>
          </g>

          <!-- Right: Condition Variable Wait Queue -->
          <g transform="translate(540, 20)">
            <rect width="200" height="220" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="24" font-size="9.5" font-weight="700" fill="#0f172a">COND: not_empty</text>

            <rect id="hm-rect-cond-box" x="12" y="38" width="176" height="70" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="56" font-size="8" font-weight="700" fill="#475569">SLEEP QUEUE:</text>
            <text id="hm-txt-cond-queue" x="20" y="74" font-family="var(--font-mono)" font-size="8.5" fill="#dc2626">[Thread 1 Asleep]</text>
            <text id="hm-txt-cond-status" x="20" y="92" font-size="7.5" fill="#64748b">Woken on signal</text>

            <rect x="12" y="120" width="176" height="88" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="138" font-size="7.5" font-weight="700" fill="#475569">PREDICATE CODE IN T1:</text>
            <text id="hm-txt-pred-code" x="20" y="156" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#059669">while (count == 0)</text>
            <text x="20" y="170" font-family="var(--font-mono)" font-size="8" fill="#64748b">  wait(&amp;not_empty);</text>
            <text id="hm-txt-pred-verdict" x="20" y="192" font-size="7.5" font-weight="700" fill="#059669">&#10003; Safe against theft</text>
          </g>
        </svg>
      </div>

      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="hm-btn-prev" onclick="stepHm(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="hm-btn-next" onclick="stepHm(1)">Next Step &rarr;</button>
          <button class="btn-step" id="hm-btn-reset" onclick="resetHm()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="hm-txt-narrative">Initial State: Consumer T1 is asleep on 'not_empty'. Producer T2 deposits an item (count=1) and calls signal(not_empty).</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="hm-txt-what">Producer T2 finishes insertion and signals the condition variable.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="hm-txt-why">Under Mesa semantics, signaling transitions the waiter to READY without immediately yielding the CPU.</p>
        </div>
      </div>
    </div>
"""

# =====================================================================
# JAVASCRIPT IMPLEMENTATIONS FOR NEW MODULE 03 STEPPERS
# =====================================================================
JS_MOD03_EXPANDED = r"""
  <script>
    // --- STEPPER 1: COUNTING SEMAPHORE RING PIPELINE ---
    const semRingSteps = {
      pipe: [
        {
          time: "T = 0 ms", thread: "Producer", empty: "empty = 3", full: "full = 0", mutex: "mutex = 1 (FREE)",
          pState: "STATE: READY", pAction: "down(&empty)", pQueue: "Runnable (Ready)",
          cState: "STATE: READY", cAction: "down(&full)", cQueue: "Runnable (Ready)",
          s0: "[Empty]", s1: "[Empty]", s2: "[Empty]",
          s0Fill: "#f1f5f9", s1Fill: "#f1f5f9", s2Fill: "#f1f5f9",
          semEmpty: "empty: 3 (Available Slots)", semFull: "full : 0 (Available Items)", semMutex: "mutex: 1 (Free)",
          queueNote: "&#10003; ALL THREADS RUNNABLE", queueColor: "#059669",
          narrative: "Initial State: Buffer is empty (N=3). empty=3 permits, full=0 items. Producer runs first.",
          what: "Producer calls down(&empty), claims one vacant slot permit, and acquires mutex.",
          why: "Counting semaphores track resource slots without holding mutual exclusion."
        },
        {
          time: "T = 1 ms", thread: "Producer (Inserts)", empty: "empty = 2", full: "full = 1", mutex: "mutex = 1 (RELEASED)",
          pState: "INSERTED ITEM A", pAction: "up(&full)", pQueue: "Completed cycle",
          cState: "STATE: DISPATCHED", cAction: "down(&full)", cQueue: "Runnable",
          s0: "[Item A]", s1: "[Empty]", s2: "[Empty]",
          s0Fill: "#dcfce7", s1Fill: "#f1f5f9", s2Fill: "#f1f5f9",
          semEmpty: "empty: 2 (Slots Free)", semFull: "full : 1 (Item Ready)", semMutex: "mutex: 1 (Free)",
          queueNote: "&#10003; ITEM A AVAILABLE FOR DRAIN", queueColor: "#059669",
          narrative: "Producer deposits Item A, releases mutex, and calls up(&full). full increments 0 -> 1. Consumer is runnable!",
          what: "Item A is latched into Slot 0. full counter incremented to 1.",
          why: "up(&full) increments permit counter to inform consumers of new data."
        },
        {
          time: "T = 2 ms", thread: "Consumer (Removes)", empty: "empty = 3", full: "full = 0", mutex: "mutex = 1 (RELEASED)",
          pState: "STATE: READY", pAction: "down(&empty)", pQueue: "Ready",
          cState: "CONSUMED ITEM A", cAction: "up(&empty)", cQueue: "Cycle complete",
          s0: "[Empty]", s1: "[Empty]", s2: "[Empty]",
          s0Fill: "#f1f5f9", s1Fill: "#f1f5f9", s2Fill: "#f1f5f9",
          semEmpty: "empty: 3 (All Free)", semFull: "full : 0 (Drained)", semMutex: "mutex: 1 (Free)",
          queueNote: "&#10003; BALANCED PIPELINE STEADY-STATE", queueColor: "#059669",
          narrative: "Consumer calls down(&full), claims mutex, removes Item A, and calls up(&empty). empty increments 2 -> 3. Perfect balance!",
          what: "Item removed. Slot 0 recycled. Counter state returned to baseline.",
          why: "The pipe operates continuously without either thread blocking."
        }
      ],
      sat: [
        {
          time: "T = 0 ms", thread: "Producer (Burst)", empty: "empty = 0 (FULL!)", full: "full = 3", mutex: "mutex = 1",
          pState: "BURST COMPLETED", pAction: "down(&empty) [4th item]", pQueue: "Ready for 4th item",
          cState: "STATE: IDLE", cAction: "Asleep", cQueue: "Idle",
          s0: "[Item 1]", s1: "[Item 2]", s2: "[Item 3]",
          s0Fill: "#dcfce7", s1Fill: "#dcfce7", s2Fill: "#dcfce7",
          semEmpty: "empty: 0 (BUFFER SATURATED)", semFull: "full : 3 (Buffer Full)", semMutex: "mutex: 1 (Free)",
          queueNote: "BUFFER AT 100% CAPACITY", queueColor: "#d97706",
          narrative: "Producer bursts 3 items rapidly, filling Slots 0, 1, and 2. empty counter decrements to 0. Buffer is SATURATED.",
          what: "Producer fills all 3 available slots. empty reaches 0.",
          why: "Counting semaphore strictly bounds buffer capacity to prevent memory overflow."
        },
        {
          time: "T = 1 ms", thread: "Producer BLOCKS", empty: "empty = -1", full: "full = 3", mutex: "mutex = 1 (FREE)",
          pState: "BLOCKED (SLEEPING)", pAction: "Suspended on empty", pQueue: "ENQUEUED ON EMPTY WAIT LIST",
          cState: "STATE: DISPATCHED", cAction: "down(&full)", cQueue: "Runnable",
          s0: "[Item 1]", s1: "[Item 2]", s2: "[Item 3]",
          s0Fill: "#dcfce7", s1Fill: "#dcfce7", s2Fill: "#dcfce7",
          semEmpty: "empty: -1 (1 PRODUCER ASLEEP)", semFull: "full : 3 (Full)", semMutex: "mutex: 1 (FREE!)",
          queueNote: "&times; PRODUCER SUSPENDED SAFELY", queueColor: "#dc2626",
          narrative: "Producer attempts 4th insert. down(&empty) decrements 0 -> -1. PRODUCER SLEEPS SAFELY. Notice mutex is 1 (free) for Consumer!",
          what: "Producer is descheduled and appended to empty's wait queue.",
          why: "Testing empty before mutex avoids deadlock; Consumer can enter freely."
        },
        {
          time: "T = 2 ms", thread: "Consumer WAKES P", empty: "empty = 0", full: "full = 2", mutex: "mutex = 1",
          pState: "WAKING UP (READY)", pAction: "Will claim Slot 0", pQueue: "Dequeued from wait list",
          cState: "REMOVED ITEM 1", cAction: "up(&empty)", cQueue: "Drained 1 item",
          s0: "[Empty]", s1: "[Item 2]", s2: "[Item 3]",
          s0Fill: "#f1f5f9", s1Fill: "#dcfce7", s2Fill: "#dcfce7",
          semEmpty: "empty: 0 (P Woken)", semFull: "full : 2 (Items Remain)", semMutex: "mutex: 1 (Free)",
          queueNote: "&#10003; PRODUCER RESUMED CLEANLY", queueColor: "#059669",
          narrative: "Consumer removes Item 1 and calls up(&empty). Producer is popped from wait queue and moved to READY. Clean pipeline handoff!",
          what: "Consumer frees a slot and signals the sleeping Producer.",
          why: "up() increments the negative counter and transitions the sleeping PCB to TASK_RUNNING."
        }
      ],
      empty: [
        {
          time: "T = 0 ms", thread: "Consumer", empty: "empty = 3", full: "full = 0 (EMPTY!)", mutex: "mutex = 1",
          pState: "STATE: IDLE", pAction: "Idle", pQueue: "Idle",
          cState: "STATE: RUNNING", cAction: "down(&full)", cQueue: "About to block",
          s0: "[Empty]", s1: "[Empty]", s2: "[Empty]",
          s0Fill: "#f1f5f9", s1Fill: "#f1f5f9", s2Fill: "#f1f5f9",
          semEmpty: "empty: 3 (Empty Buffer)", semFull: "full : 0 (NO ITEMS)", semMutex: "mutex: 1 (Free)",
          queueNote: "BUFFER EMPTY: CONSUMER WILL BLOCK", queueColor: "#d97706",
          narrative: "Buffer is completely empty (full = 0). Consumer arrives and attempts to remove an item.",
          what: "Consumer calls down(&full) on counter value 0.",
          why: "Consumer cannot drain from an empty buffer."
        },
        {
          time: "T = 1 ms", thread: "Consumer BLOCKS", empty: "empty = 3", full: "full = -1", mutex: "mutex = 1",
          pState: "STATE: DISPATCHED", pAction: "produce_item()", pQueue: "Producer starts",
          cState: "BLOCKED (SLEEPING)", cAction: "Suspended on full", cQueue: "ENQUEUED ON FULL WAIT LIST",
          s0: "[Empty]", s1: "[Empty]", s2: "[Empty]",
          s0Fill: "#f1f5f9", s1Fill: "#f1f5f9", s2Fill: "#f1f5f9",
          semEmpty: "empty: 3 (Free)", semFull: "full : -1 (1 CONSUMER ASLEEP)", semMutex: "mutex: 1 (Free)",
          queueNote: "&times; CONSUMER SUSPENDED SAFELY", queueColor: "#dc2626",
          narrative: "down(&full) decrements 0 -> -1. Consumer is descheduled and enqueued on full's wait list. Zero CPU cycles wasted!",
          what: "Consumer is moved to BLOCKED state awaiting data.",
          why: "Sleeping frees CPU execution cores for productive work."
        },
        {
          time: "T = 2 ms", thread: "Producer WAKES C", empty: "empty = 2", full: "full = 0", mutex: "mutex = 1",
          pState: "INSERTED ITEM", pAction: "up(&full)", pQueue: "Cycle complete",
          cState: "WAKING UP (READY)", pAction: "Will drain Slot 0", cQueue: "Dequeued from wait list",
          s0: "[Item Alpha]", s1: "[Empty]", s2: "[Empty]",
          s0Fill: "#dcfce7", s1Fill: "#f1f5f9", s2Fill: "#f1f5f9",
          semEmpty: "empty: 2 (Slots Free)", semFull: "full : 0 (Item Delivered)", semMutex: "mutex: 1 (Free)",
          queueNote: "&#10003; CONSUMER WOKEN BY UP(&FULL)", queueColor: "#059669",
          narrative: "Producer deposits Item Alpha and calls up(&full). full increments -1 -> 0. Consumer is awakened immediately!",
          what: "Producer signals full. Consumer returns to READY runqueue.",
          why: "The semaphore acts as a synchronization rendezvous between asynchronous threads."
        }
      ]
    };

    let activeSemRingDim = "pipe";
    let activeSemRingStep = 0;

    function renderSemRing() {
      const steps = semRingSteps[activeSemRingDim];
      const step = steps[activeSemRingStep];

      document.getElementById("sr-telem-time").textContent = step.time;
      document.getElementById("sr-telem-thread").textContent = step.thread;
      document.getElementById("sr-telem-empty").textContent = step.empty;
      document.getElementById("sr-telem-full").textContent = step.full;
      document.getElementById("sr-telem-mutex").textContent = step.mutex;

      document.getElementById("sr-txt-p-state").textContent = step.pState;
      document.getElementById("sr-txt-p-action").textContent = step.pAction;
      document.getElementById("sr-txt-p-queue").textContent = step.pQueue;

      document.getElementById("sr-txt-c-state").textContent = step.cState;
      document.getElementById("sr-txt-c-action").textContent = step.cAction;
      document.getElementById("sr-txt-c-queue").textContent = step.cQueue;

      document.getElementById("sr-txt-slot-0").textContent = step.s0;
      document.getElementById("sr-txt-slot-1").textContent = step.s1;
      document.getElementById("sr-txt-slot-2").textContent = step.s2;
      document.getElementById("sr-rect-slot-0").setAttribute("fill", step.s0Fill);
      document.getElementById("sr-rect-slot-1").setAttribute("fill", step.s1Fill);
      document.getElementById("sr-rect-slot-2").setAttribute("fill", step.s2Fill);

      document.getElementById("sr-txt-sem-empty").textContent = step.semEmpty;
      document.getElementById("sr-txt-sem-full").textContent = step.semFull;
      document.getElementById("sr-txt-sem-mutex").textContent = step.semMutex;

      document.getElementById("sr-txt-sem-queue").innerHTML = step.queueNote;
      document.getElementById("sr-txt-sem-queue").setAttribute("fill", step.queueColor);

      document.getElementById("sr-txt-narrative").innerHTML = step.narrative;
      document.getElementById("sr-txt-what").innerHTML = step.what;
      document.getElementById("sr-txt-why").innerHTML = step.why;

      document.getElementById("sr-btn-prev").disabled = (activeSemRingStep === 0);
      document.getElementById("sr-btn-next").disabled = (activeSemRingStep === steps.length - 1);
    }

    function stepSemRing(delta) {
      const steps = semRingSteps[activeSemRingDim];
      activeSemRingStep = Math.max(0, Math.min(steps.length - 1, activeSemRingStep + delta));
      renderSemRing();
    }

    function resetSemRing() {
      activeSemRingStep = 0;
      renderSemRing();
    }

    function setSemRingDim(dim) {
      activeSemRingDim = dim;
      activeSemRingStep = 0;
      document.getElementById("sr-dim-pipe").classList.toggle("active", dim === "pipe");
      document.getElementById("sr-dim-sat").classList.toggle("active", dim === "sat");
      document.getElementById("sr-dim-empty").classList.toggle("active", dim === "empty");
      renderSemRing();
    }

    // --- STEPPER 2: HOARE VS. MESA MONITOR SIGNALING ---
    const hmSteps = {
      safe: [
        {
          time: "T = 0 ms", active: "Thread 2 (Producer)", count: "count = 1", signaler: "T2: signal(not_empty)", status: "Mesa (Safe while)",
          qT3: "Arrived at gate &rarr; Waiting", qT1: "Woken to Entry Queue",
          qNote: "Mesa: Signaler retains lock",
          activeTitle: "ACTIVE: Thread 2 (Producer)", activeAction: "insert_item(); signal();", activeSub: "Holds lock until return",
          bufVal: "count = 1 [Item X Present]",
          crashText: "&#10003; SYSTEM INVARIANTS SOUND", crashFill: "#dcfce7", crashStroke: "#16a34a", crashColor: "#166534",
          condQueue: "[Thread 1 Woken &rarr; Queue]", predCode: "while (count == 0)", predVerdict: "&#10003; Safe against theft",
          narrative: "Thread 2 finishes inserting Item X and signals not_empty. Under Mesa semantics, T2 retains the lock! T1 is moved to the monitor Entry Queue.",
          what: "T2 signals condition variable. T1 is awakened and moved to monitor entry queue.",
          why: "Mesa semantics avoid immediate context switches by letting the signaler finish its quantum."
        },
        {
          time: "T = 1 ms", active: "Thread 3 [THEFT!]", count: "count = 0 (STOLEN)", signaler: "T2 Exited Monitor", status: "Item Snatched by T3",
          qT3: "Inside Monitor (Snatched lock)", qT1: "Still waiting in queue",
          qNote: "T3 preempted awakened T1",
          activeTitle: "ACTIVE: Thread 3 [Sneaky Consumer]", activeAction: "remove_item(); /* Snatches X */", activeSub: "T3 claimed lock before T1!",
          bufVal: "count = 0 [EMPTY!]",
          crashText: "ITEM SNATCHED WHILE T1 WAITED", crashFill: "#fef3c7", crashStroke: "#d97706", crashColor: "#92400e",
          condQueue: "[Queue Empty]", predCode: "while (count == 0)", predVerdict: "&#10003; Guard will protect T1",
          narrative: "T2 exits. Before T1 can run, newly arrived Thread 3 grabs the monitor lock, removes Item X, and exits! The buffer is now EMPTY again!",
          what: "Thread 3 enters the monitor ahead of Thread 1 and drains the buffer.",
          why: "Under Mesa semantics, awakened threads must compete with incoming threads for the monitor lock."
        },
        {
          time: "T = 2 ms", active: "Thread 1 (Re-tests)", count: "count = 0", signaler: "None", status: "WHILE LOOP PROTECTS T1",
          qT3: "Exited Monitor", qT1: "Inside & Re-evaluating",
          qNote: "while loop loops back!",
          activeTitle: "ACTIVE: Thread 1 (Awakened)", activeAction: "while (count == 0) &rarr; TRUE!", activeSub: "Detects theft & sleeps safely!",
          bufVal: "count = 0 [STILL EMPTY]",
          crashText: "&#10003; WHILE LOOP AVERTED DISASTER!", crashFill: "#dcfce7", crashStroke: "#16a34a", crashColor: "#166534",
          condQueue: "[T1 Enqueued Back on Cond]", predCode: "while (count == 0)", predVerdict: "&#10003; SLEEPS SAFELY AGAIN",
          narrative: "Thread 1 acquires lock and re-evaluates: 'while (count == 0)' IS TRUE! T1 detects Item X was stolen, executes wait() again, and sleeps safely. Zero crash!",
          what: "Thread 1 loops back, discovers buffer is empty, and goes back to sleep.",
          why: "The while loop invariant is mandatory under Mesa semantics to protect against intervening thefts."
        }
      ],
      bug: [
        {
          time: "T = 0 ms", active: "Thread 2 (Producer)", count: "count = 1", signaler: "T2: signal(not_empty)", status: "Mesa (BUG: if check)",
          qT3: "Arrived at gate &rarr; Waiting", qT1: "Woken to Entry Queue",
          qNote: "BUGGY CODE: uses 'if'",
          activeTitle: "ACTIVE: Thread 2 (Producer)", activeAction: "insert_item(); signal();", activeSub: "Holds lock until return",
          bufVal: "count = 1 [Item X Present]",
          crashText: "FLAWED 'IF' STATEMENT ACTIVE", crashFill: "#fee2e2", crashStroke: "#dc2626", crashColor: "#991b1b",
          condQueue: "[Thread 1 Woken &rarr; Queue]", predCode: "if (count == 0) /* FATAL */", predVerdict: "&times; VULNERABLE TO THEFT",
          narrative: "FLAWED IMPLEMENTATION: Thread 1 was written using 'if (count == 0) wait()'. Thread 2 signals and finishes.",
          what: "Thread 1 uses an if statement instead of a while loop.",
          why: "Common programmer mistake assuming condition remains true after wakeup."
        },
        {
          time: "T = 1 ms", active: "Thread 3 [THEFT!]", count: "count = 0 (STOLEN)", signaler: "T2 Exited", status: "Item Snatched by T3",
          qT3: "Inside Monitor (Snatched lock)", qT1: "Still waiting in queue",
          qNote: "T3 claimed lock first",
          activeTitle: "ACTIVE: Thread 3 [Sneaky Consumer]", activeAction: "remove_item(); /* Snatches X */", activeSub: "Buffer drained to 0!",
          bufVal: "count = 0 [EMPTY!]",
          crashText: "ITEM SNATCHED: BUFFER EMPTY", crashFill: "#fee2e2", crashStroke: "#dc2626", crashColor: "#991b1b",
          condQueue: "[Queue Empty]", predCode: "if (count == 0) /* FATAL */", predVerdict: "&times; T1 WILL NOT RE-CHECK!",
          narrative: "Thread 3 snatches the lock, removes Item X, and exits. Buffer is empty (count = 0).",
          what: "Thread 3 leaves the buffer completely empty.",
          why: "Mesa semantics permit new callers to acquire the lock before waiters."
        },
        {
          time: "T = 2 ms", active: "Thread 1 (CRASHES)", count: "count = -1 (UNDERFLOW)", signaler: "None", status: "FATAL BUFFER CRASH!",
          qT3: "Exited", qT1: "Crashing on remove_item()",
          qNote: "No re-check performed!",
          activeTitle: "ACTIVE: Thread 1 [FATAL CRASH]", activeAction: "remove_item() on EMPTY BUFFER!", activeSub: "Underflow & Segfault!",
          bufVal: "count = -1 [CORRUPTED!]",
          crashText: "&times; CRITICAL BUG: SEGMENTATION FAULT!", crashFill: "#fee2e2", crashStroke: "#dc2626", crashColor: "#991b1b",
          condQueue: "[Queue Empty]", predCode: "if (count == 0) /* FATAL */", predVerdict: "&times; CRASHED: NO RE-TEST",
          narrative: "DISASTER: Thread 1 wakes up and DOES NOT RE-TEST condition! It assumes Item X is still there, calls remove_item() on an empty buffer, and crashes!",
          what: "Thread 1 drains from empty buffer, corrupting data structures.",
          why: "Because an if check was used, Thread 1 blindly assumed the predicate was still valid."
        }
      ],
      hoare: [
        {
          time: "T = 0 ms", active: "Thread 2 -> Thread 1", count: "count = 1", signaler: "T2: signal(not_empty)", status: "Hoare (Signal-and-Wait)",
          qT3: "Blocked at Gate", qT1: "RUNS INSTANTANEOUSLY",
          qNote: "T2 yields lock immediately!",
          activeTitle: "INSTANT HANDOFF: T2 &rarr; T1", activeAction: "T2 yields lock directly to T1", activeSub: "T3 strictly barred from entry",
          bufVal: "count = 1 [Item X Guaranteed]",
          crashText: "&#10003; HOARE SEMANTICS: PREDICATE TRUE", crashFill: "#dcfce7", crashStroke: "#16a34a", crashColor: "#166534",
          condQueue: "[Queue Empty: T1 Active]", predCode: "if (count == 0)", predVerdict: "&#10003; if is valid under Hoare",
          narrative: "Hoare Semantics: When Thread 2 calls signal(), it IMMEDIATELY yields the monitor lock and CPU to Thread 1. Thread 3 cannot sneak in!",
          what: "Signaler immediately yields lock directly to the awakened thread.",
          why: "Hoare guarantees the condition is strictly true when the awakened thread runs."
        },
        {
          time: "T = 1 ms", active: "Thread 1 (Consumes)", count: "count = 0", signaler: "T1 Finished", status: "Item Consumed Safely",
          qT3: "Now eligible to enter", qT1: "Exited Monitor",
          qNote: "Lock returns to T2 / T3",
          activeTitle: "ACTIVE: Thread 1 (Consumer)", activeAction: "remove_item(); /* Guaranteed X */", activeSub: "Consumed without re-test",
          bufVal: "count = 0 [Empty]",
          crashText: "&#10003; CLEAN HANDOFF (HIGH CONTEXT SWITCH COST)", crashFill: "#dcfce7", crashStroke: "#16a34a", crashColor: "#166534",
          condQueue: "[Queue Empty]", predCode: "if (count == 0)", predVerdict: "&#10003; Success",
          narrative: "Thread 1 consumes Item X with zero risk of theft. However, this required two immediate context switches, reducing multicore throughput.",
          what: "Thread 1 finishes cleanly without needing a while loop.",
          why: "Guaranteed predicate truth comes at the cost of high scheduling context switch overhead."
        }
      ]
    };

    let activeHmDim = "safe";
    let activeHmStep = 0;

    function renderHm() {
      const steps = hmSteps[activeHmDim];
      const step = steps[activeHmStep];

      document.getElementById("hm-telem-time").textContent = step.time;
      document.getElementById("hm-telem-active").textContent = step.active;
      document.getElementById("hm-telem-count").textContent = step.count;
      document.getElementById("hm-telem-signaler").textContent = step.signaler;
      document.getElementById("hm-telem-status").textContent = step.status;

      document.getElementById("hm-txt-q-t3").textContent = step.qT3;
      document.getElementById("hm-txt-q-t1").textContent = step.qT1;
      document.getElementById("hm-txt-q-note").textContent = step.qNote;

      document.getElementById("hm-txt-active-title").textContent = step.activeTitle;
      document.getElementById("hm-txt-active-action").textContent = step.activeAction;
      document.getElementById("hm-txt-active-sub").textContent = step.activeSub;

      document.getElementById("hm-txt-buf-val").textContent = step.bufVal;

      document.getElementById("hm-txt-crash").innerHTML = step.crashText;
      document.getElementById("hm-rect-crash").setAttribute("fill", step.crashFill);
      document.getElementById("hm-rect-crash").setAttribute("stroke", step.crashStroke);
      document.getElementById("hm-txt-crash").setAttribute("fill", step.crashColor);

      document.getElementById("hm-txt-cond-queue").textContent = step.condQueue;
      document.getElementById("hm-txt-pred-code").textContent = step.predCode;
      document.getElementById("hm-txt-pred-verdict").innerHTML = step.predVerdict;

      document.getElementById("hm-txt-narrative").innerHTML = step.narrative;
      document.getElementById("hm-txt-what").innerHTML = step.what;
      document.getElementById("hm-txt-why").innerHTML = step.why;

      document.getElementById("hm-btn-prev").disabled = (activeHmStep === 0);
      document.getElementById("hm-btn-next").disabled = (activeHmStep === steps.length - 1);
    }

    function stepHm(delta) {
      const steps = hmSteps[activeHmDim];
      activeHmStep = Math.max(0, Math.min(steps.length - 1, activeHmStep + delta));
      renderHm();
    }

    function resetHm() {
      activeHmStep = 0;
      renderHm();
    }

    function setHmDim(dim) {
      activeHmDim = dim;
      activeHmStep = 0;
      document.getElementById("hm-dim-safe").classList.toggle("active", dim === "safe");
      document.getElementById("hm-dim-bug").classList.toggle("active", dim === "bug");
      document.getElementById("hm-dim-hoare").classList.toggle("active", dim === "hoare");
      renderHm();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderSemRing();
      renderHm();
    });
  </script>
"""

def integrate_new_steppers_in_module_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insert Semaphore Ring Stepper in Section 2 (before Section 3)
    sec3_marker = "<h3>3. Kernel Sleep Queues &amp; Linux Futexes</h3>"
    if "sr-dim-pipe" not in content and sec3_marker in content:
        idx = content.find(sec3_marker)
        content = content[:idx] + SEMAPHORE_RING_AID + "\n\n    " + content[idx:]

    # 2. Insert Hoare vs. Mesa Stepper in Section 4 (before bottom navbar)
    bot_nav_marker = '<nav class="nav-bar" style="margin-top: 36px;'
    if "hm-dim-safe" not in content and bot_nav_marker in content:
        idx = content.find(bot_nav_marker)
        content = content[:idx] + MONITOR_MESA_HOARE_AID + "\n\n    " + content[idx:]

    # 3. Append JavaScript
    body_end = "</body>"
    if "semRingSteps" not in content and body_end in content:
        idx = content.find(body_end)
        content = content[:idx] + JS_MOD03_EXPANDED + "\n" + content[idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully integrated both interactive aids into {TARGET_FILE}")

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add Counting Semaphore and Hoare vs. Mesa steppers to Module 03\n\n"
            "Implement the Producer-Consumer 3-slot ring buffer semaphore stepper\n"
            "and the Hoare vs. Mesa monitor while-loop invariant interactive aid."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    integrate_new_steppers_in_module_three()
    run_git_sync()
