#!/usr/bin/env python3
# =====================================================================
# fix.py: Add interactive lock-inversion stepper to Module 02 Section 1
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

INTERACTIVE_STEPPER_HTML = r"""      <!-- ================================================================= -->
      <!-- INTERACTIVE STEPPER: LOCK INVERSION & RUNTIME ARREST               -->
      <!-- ================================================================= -->
      <div class="aid-wrapper">
        <div class="aid-header">Interactive Walkthrough: Two-Thread Lock Inversion Deadlock</div>
        <div class="aid-subtitle">Trace step-by-step how conflicting acquisition orders interleave over time, driving concurrent threads into an unrecoverable sleep state.</div>

        <div class="aid-grid">
          <div class="controls-panel">
            <div class="preview-box" id="lock-preview-text">
              <strong>Step 1: Thread 1 Runs.</strong> Thread 1 executes <code>pthread_mutex_lock(&amp;lock_A)</code>. Lock A is unowned, so Thread 1 claims it immediately and proceeds.
            </div>

            <div class="stepper-btns">
              <button class="step-btn" id="lock-prev-btn" onclick="changeLockStep(-1)" disabled>&larr; Prev</button>
              <button class="step-btn" id="lock-next-btn" onclick="changeLockStep(1)">Next &rarr;</button>
              <button class="step-btn" onclick="resetLockStepper()" style="background:#64748b;">Reset</button>
            </div>

            <div class="telemetry-bar" id="lock-telemetry-bar" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px 12px; font-family: var(--font-mono); font-size: 0.75rem; background: #0f172a; color: #e2e8f0; padding: 10px 12px; border-radius: 6px;">
              <div><strong>Phase:</strong> <span id="lock-tel-phase" style="color: #38bdf8;">1/4</span></div>
              <div><strong>Active:</strong> <span id="lock-tel-active">Thread 1</span></div>
              <div><strong>Held:</strong> <span id="lock-tel-held">Lock A (T1)</span></div>
              <div><strong>State:</strong> <span id="lock-tel-state" style="color: #4ade80; font-weight: 700;">Running</span></div>
            </div>

            <div class="toggle-bar">
              <span style="font-size: 0.72rem; font-weight: 700; align-self: center; color: var(--text-muted);">ORDER:</span>
              <button class="toggle-btn active" id="lock-btn-inversion" onclick="setLockMode('inversion')">Inverted (Deadlock)</button>
              <button class="toggle-btn" id="lock-btn-ordered" onclick="setLockMode('ordered')">Ordered (Safe)</button>
            </div>
          </div>

          <div class="visual-canvas" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; background: #ffffff; border: 1px solid var(--border);">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 6px; color: var(--primary); text-align: left;">Synchronized Visual Canvas &mdash; Thread &amp; Mutex Topology</div>

            <svg viewBox="0 0 320 180" style="width: 100%; height: 100%; min-height: 190px; background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 8px;">
              <defs>
                <marker id="lock-arrow-alloc" viewBox="0 0 10 10" refX="20" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#0284c7"/>
                </marker>
                <marker id="lock-arrow-wait" viewBox="0 0 10 10" refX="20" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#d97706"/>
                </marker>
                <marker id="lock-arrow-dead" viewBox="0 0 10 10" refX="20" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#dc2626"/>
                </marker>
              </defs>

              <!-- Thread 1 (Left) -->
              <circle id="svg-t1-circle" cx="60" cy="50" r="22" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="60" y="47" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">Thread 1</text>
              <text id="svg-t1-state" x="60" y="60" fill="#0284c7" font-size="7.5" font-family="monospace" text-anchor="middle">RUNNING</text>

              <!-- Thread 2 (Right) -->
              <circle id="svg-t2-circle" cx="260" cy="50" r="22" fill="#ffffff" stroke="#64748b" stroke-width="2.5" />
              <text x="260" y="47" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">Thread 2</text>
              <text id="svg-t2-state" x="260" y="60" fill="#64748b" font-size="7.5" font-family="monospace" text-anchor="middle">READY</text>

              <!-- Mutex Lock A (Center Left) -->
              <rect id="svg-la-box" x="90" y="110" width="45" height="40" rx="4" fill="#ffffff" stroke="#16a34a" stroke-width="2" />
              <text x="112" y="126" fill="#15803d" font-size="8" font-weight="bold" text-anchor="middle">Lock A</text>
              <text id="svg-la-status" x="112" y="141" fill="#16a34a" font-size="7" font-family="monospace" text-anchor="middle">FREE</text>

              <!-- Mutex Lock B (Center Right) -->
              <rect id="svg-lb-box" x="185" y="110" width="45" height="40" rx="4" fill="#ffffff" stroke="#16a34a" stroke-width="2" />
              <text x="207" y="126" fill="#15803d" font-size="8" font-weight="bold" text-anchor="middle">Lock B</text>
              <text id="svg-lb-status" x="207" y="141" fill="#16a34a" font-size="7" font-family="monospace" text-anchor="middle">FREE</text>

              <!-- Dynamic Interactive Connector Lines -->
              <line id="svg-line-t1-la" x1="60" y1="72" x2="95" y2="110" stroke="#cbd5e1" stroke-width="2" />
              <line id="svg-line-t2-lb" x1="260" y1="72" x2="225" y2="110" stroke="#cbd5e1" stroke-width="2" />
              <line id="svg-line-t2-la" x1="240" y1="62" x2="135" y2="120" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="3,3" />
              <line id="svg-line-t1-lb" x1="80" y1="62" x2="185" y2="120" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="3,3" />
            </svg>

            <div style="font-size: 0.8rem; color: var(--text-muted); text-align: center; margin-top: 6px;" id="lock-canvas-banner">
              Runtime State: <strong>Thread 1 holds Lock A</strong>
            </div>
          </div>
        </div>

        <div class="panes-grid">
          <div class="pane-box" style="border-left: 3px solid var(--success);">
            <div class="pane-title" style="color: var(--success);">&#128269; What Is Happening</div>
            <div id="lock-pane-what" style="color: var(--text);">Thread 1 executes atomic compare-and-swap, acquiring Lock A without contention.</div>
          </div>
          <div class="pane-box" style="border-left: 3px solid var(--accent);">
            <div class="pane-title" style="color: var(--accent);">&#9881; Why The System Does This</div>
            <div id="lock-pane-why" style="color: var(--text);">Locks grant mutual exclusion; Thread 1 must hold Lock A before touching Account A to prevent data races.</div>
          </div>
        </div>
      </div>
"""

def integrate_interactive_stepper():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for insertion point right after two-thread lock inversion explanation
    search_anchor = "<p>\n        Both threads are now asleep waiting for each other. Neither thread will ever wake up on its own.\n      </p>"
    if search_anchor not in content:
        # Fallback search with looser whitespace
        search_anchor = "Both threads are now asleep waiting for each other. Neither thread will ever wake up on its own."
        if search_anchor not in content:
            print("Error: Could not locate Section 1 two-thread walkthrough anchor.")
            return False

    # Check if already inserted
    if "Interactive Walkthrough: Two-Thread Lock Inversion Deadlock" in content:
        print("Notice: Interactive stepper already exists in Module 02.")
        return True

    anchor_pos = content.find(search_anchor)
    insert_pos = content.find("</p>", anchor_pos) + len("</p>")

    updated_content = content[:insert_pos] + "\n\n" + INTERACTIVE_STEPPER_HTML + content[insert_pos:]

    # Add JavaScript driving logic to end of script section
    js_search = "function setTopology(topo) {"
    if js_search in updated_content and "let lockStep = 1;" not in updated_content:
        js_logic = r"""
    // --- Interactive Lock Inversion Stepper Logic ---
    let lockStep = 1;
    const lockTotalSteps = 4;
    let lockMode = 'inversion';

    const lockInversionData = [
      {
        preview: "<strong>Step 1: Thread 1 Claims Lock A.</strong> Thread 1 calls <code>pthread_mutex_lock(&amp;lock_A)</code>. Mutex A is unlocked, so Thread 1 acquires it and transitions to active ownership.",
        phase: "1/4", active: "Thread 1", held: "Lock A (T1)", state: "Running", stateColor: "#4ade80",
        what: "Thread 1 executes atomic test-and-set. Lock A ownership is granted to Thread 1.",
        why: "Mutual exclusion ensures Thread 1 can modify Account A without concurrent race hazards.",
        banner: "Step 1: <strong>Thread 1 holds Lock A (Running)</strong>",
        t1State: "HOLDING A", t1Color: "#0284c7", t2State: "READY", t2Color: "#64748b",
        laText: "OWNED (T1)", laStroke: "#0284c7", lbText: "FREE", lbStroke: "#16a34a",
        l1: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l2: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l3: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l4: { stroke: "#cbd5e1", width: "1.5", marker: "none" }
      },
      {
        preview: "<strong>Step 2: Preemption &amp; Thread 2 Claims Lock B.</strong> Scheduler interrupts Thread 1. Thread 2 dispatches and calls <code>pthread_mutex_lock(&amp;lock_B)</code>, acquiring Lock B.",
        phase: "2/4", active: "Thread 2", held: "Lock A, Lock B", state: "Contention", stateColor: "#facc15",
        what: "Thread 2 executes on CPU while Thread 1 is temporarily preempted. Thread 2 claims Lock B.",
        why: "In preemptive multitasking, threads can be switched out at any arbitrary assembly boundary.",
        banner: "Step 2: <strong>Thread 1 holds Lock A | Thread 2 holds Lock B</strong>",
        t1State: "PREEMPTED", t1Color: "#0284c7", t2State: "HOLDING B", t2Color: "#0284c7",
        laText: "OWNED (T1)", laStroke: "#0284c7", lbText: "OWNED (T2)", lbStroke: "#0284c7",
        l1: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l2: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l3: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l4: { stroke: "#cbd5e1", width: "1.5", marker: "none" }
      },
      {
        preview: "<strong>Step 3: Thread 2 Blocks on Lock A.</strong> Thread 2 calls <code>pthread_mutex_lock(&amp;lock_A)</code>. Because Lock A is held by Thread 1, Thread 2 is put to sleep (BLOCKED).",
        phase: "3/4", active: "Thread 2 (Blocked)", held: "Lock A, Lock B", state: "T2 Blocked", stateColor: "#facc15",
        what: "Thread 2 attempts to acquire Lock A, fails, and yields the CPU. OS marks Thread 2 BLOCKED.",
        why: "Mutual exclusion forbids multiple owners; waiting threads sleep to avoid burning CPU cycles.",
        banner: "Step 3: <strong>Thread 2 blocked waiting for Lock A (held by Thread 1)</strong>",
        t1State: "HOLDING A", t1Color: "#0284c7", t2State: "BLOCKED (A)", t2Color: "#d97706",
        laText: "OWNED (T1)", laStroke: "#0284c7", lbText: "OWNED (T2)", lbStroke: "#0284c7",
        l1: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l2: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l3: { stroke: "#d97706", width: "2.5", marker: "url(#lock-arrow-wait)" },
        l4: { stroke: "#cbd5e1", width: "1.5", marker: "none" }
      },
      {
        preview: "<strong>Step 4: Circular Wait &amp; System Deadlock!</strong> Thread 1 resumes and calls <code>pthread_mutex_lock(&amp;lock_B)</code>. Held by Thread 2! Thread 1 blocks. Both threads are permanently frozen.",
        phase: "4/4", active: "None (Deadlock)", held: "Circular Wait", state: "DEADLOCKED", stateColor: "#dc2626",
        what: "Thread 1 blocks on Lock B; Thread 2 blocks on Lock A. No thread can wake the other.",
        why: "Opposing lock acquisition order creates a closed circular dependency loop with zero escape.",
        banner: "DEADLOCK CONFIRMED: <strong>Thread 1 and Thread 2 are permanently frozen</strong>",
        t1State: "DEADLOCKED", t1Color: "#dc2626", t2State: "DEADLOCKED", t2Color: "#dc2626",
        laText: "LOCKED (T1)", laStroke: "#dc2626", lbText: "LOCKED (T2)", lbStroke: "#dc2626",
        l1: { stroke: "#dc2626", width: "2.5", marker: "url(#lock-arrow-dead)" },
        l2: { stroke: "#dc2626", width: "2.5", marker: "url(#lock-arrow-dead)" },
        l3: { stroke: "#dc2626", width: "2.5", marker: "url(#lock-arrow-dead)" },
        l4: { stroke: "#dc2626", width: "2.5", marker: "url(#lock-arrow-dead)" }
      }
    ];

    const lockOrderedData = [
      {
        preview: "<strong>Step 1: Consistent Lock Order.</strong> Both threads agree to acquire Lock A before Lock B ($A \\prec B$). Thread 1 claims Lock A first.",
        phase: "1/4", active: "Thread 1", held: "Lock A (T1)", state: "Running", stateColor: "#4ade80",
        what: "Thread 1 claims Lock A. Thread 2 cannot claim Lock B until it acquires Lock A.",
        why: "Global lock ordering prevents circular wait from ever forming.",
        banner: "Safe Order: <strong>Thread 1 claims Lock A first under global hierarchy</strong>",
        t1State: "HOLDING A", t1Color: "#0284c7", t2State: "READY", t2Color: "#64748b",
        laText: "OWNED (T1)", laStroke: "#0284c7", lbText: "FREE", lbStroke: "#16a34a",
        l1: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l2: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l3: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l4: { stroke: "#cbd5e1", width: "1.5", marker: "none" }
      },
      {
        preview: "<strong>Step 2: Thread 2 Attempts Lock A &amp; Blocks Early.</strong> Thread 2 dispatches and tries to acquire Lock A. It immediately sleeps without holding any other lock.",
        phase: "2/4", active: "Thread 2 (Sleep)", held: "Lock A (T1)", state: "Safe Wait", stateColor: "#38bdf8",
        what: "Thread 2 blocks on Lock A, but holds 0 locks. Hold-and-wait condition is broken!",
        why: "Because Thread 2 holds nothing, it cannot starve or block Thread 1.",
        banner: "Safe Order: <strong>Thread 2 waits on Lock A without holding Lock B</strong>",
        t1State: "HOLDING A", t1Color: "#0284c7", t2State: "BLOCKED (A)", t2Color: "#d97706",
        laText: "OWNED (T1)", laStroke: "#0284c7", lbText: "FREE", lbStroke: "#16a34a",
        l1: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l2: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l3: { stroke: "#d97706", width: "2.5", marker: "url(#lock-arrow-wait)" },
        l4: { stroke: "#cbd5e1", width: "1.5", marker: "none" }
      },
      {
        preview: "<strong>Step 3: Thread 1 Claims Lock B &amp; Finishes.</strong> Thread 1 claims Lock B without contention, modifies both accounts, and releases both locks.",
        phase: "3/4", active: "Thread 1", held: "Lock A &amp; B", state: "Completing", stateColor: "#4ade80",
        what: "Thread 1 completes its critical section and releases Lock B then Lock A.",
        why: "Uncontested execution guarantees forward progress and prevents deadlocks.",
        banner: "Safe Order: <strong>Thread 1 completes transaction and unlocks all mutexes</strong>",
        t1State: "FINISHING", t1Color: "#16a34a", t2State: "BLOCKED (A)", t2Color: "#d97706",
        laText: "OWNED (T1)", laStroke: "#0284c7", lbText: "OWNED (T1)", lbStroke: "#0284c7",
        l1: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" },
        l2: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l3: { stroke: "#d97706", width: "2.5", marker: "url(#lock-arrow-wait)" },
        l4: { stroke: "#0284c7", width: "2.5", marker: "url(#lock-arrow-alloc)" }
      },
      {
        preview: "<strong>Step 4: Thread 2 Wakes &amp; Completes.</strong> With Lock A freed, Thread 2 wakes up, acquires Lock A then Lock B, and completes successfully.",
        phase: "4/4", active: "Thread 2", held: "Released", state: "Completed", stateColor: "#16a34a",
        what: "Thread 2 executes cleanly. Both threads complete without deadlock.",
        why: "Global lock hierarchies guarantee mathematically that cycles cannot exist in the allocation graph.",
        banner: "Success: <strong>All transactions completed without deadlock</strong>",
        t1State: "TERMINATED", t1Color: "#64748b", t2State: "COMPLETED", t2Color: "#16a34a",
        laText: "FREE", laStroke: "#16a34a", lbText: "FREE", lbStroke: "#16a34a",
        l1: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l2: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l3: { stroke: "#cbd5e1", width: "1.5", marker: "none" },
        l4: { stroke: "#cbd5e1", width: "1.5", marker: "none" }
      }
    ];

    function changeLockStep(dir) {
      lockStep += dir;
      if (lockStep < 1) lockStep = 1;
      if (lockStep > lockTotalSteps) lockStep = lockTotalSteps;
      updateLockUI();
    }

    function resetLockStepper() {
      lockStep = 1;
      updateLockUI();
    }

    function setLockMode(mode) {
      lockMode = mode;
      document.getElementById('lock-btn-inversion').className = (mode === 'inversion') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('lock-btn-ordered').className = (mode === 'ordered') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('lock-btn-inversion').style.background = (mode === 'inversion') ? '#e0f2fe' : '#f1f5f9';
      document.getElementById('lock-btn-ordered').style.background = (mode === 'ordered') ? '#e0f2fe' : '#f1f5f9';
      lockStep = 1;
      updateLockUI();
    }

    function updateLockUI() {
      const dataset = (lockMode === 'inversion') ? lockInversionData : lockOrderedData;
      const data = dataset[lockStep - 1];

      document.getElementById('lock-preview-text').innerHTML = data.preview;
      document.getElementById('lock-tel-phase').innerText = data.phase;
      document.getElementById('lock-tel-active').innerText = data.active;
      document.getElementById('lock-tel-held').innerHTML = data.held;

      const stEl = document.getElementById('lock-tel-state');
      stEl.innerText = data.state;
      stEl.style.color = data.stateColor;

      document.getElementById('lock-pane-what').innerHTML = data.what;
      document.getElementById('lock-pane-why').innerHTML = data.why;
      document.getElementById('lock-canvas-banner').innerHTML = data.banner;

      // Update SVG visual nodes
      const t1Circle = document.getElementById('svg-t1-circle');
      const t1StateTxt = document.getElementById('svg-t1-state');
      t1Circle.setAttribute('stroke', data.t1Color);
      t1StateTxt.textContent = data.t1State;
      t1StateTxt.setAttribute('fill', data.t1Color);

      const t2Circle = document.getElementById('svg-t2-circle');
      const t2StateTxt = document.getElementById('svg-t2-state');
      t2Circle.setAttribute('stroke', data.t2Color);
      t2StateTxt.textContent = data.t2State;
      t2StateTxt.setAttribute('fill', data.t2Color);

      const laBox = document.getElementById('svg-la-box');
      const laStatusTxt = document.getElementById('svg-la-status');
      laBox.setAttribute('stroke', data.laStroke);
      laStatusTxt.textContent = data.laText;
      laStatusTxt.setAttribute('fill', data.laStroke);

      const lbBox = document.getElementById('svg-lb-box');
      const lbStatusTxt = document.getElementById('svg-lb-status');
      lbBox.setAttribute('stroke', data.lbStroke);
      lbStatusTxt.textContent = data.lbText;
      lbStatusTxt.setAttribute('fill', data.lbStroke);

      // Update Connector Lines
      const l1 = document.getElementById('svg-line-t1-la');
      const l2 = document.getElementById('svg-line-t2-lb');
      const l3 = document.getElementById('svg-line-t2-la');
      const l4 = document.getElementById('svg-line-t1-lb');

      l1.setAttribute('stroke', data.l1.stroke);
      l1.setAttribute('stroke-width', data.l1.width);
      l1.setAttribute('marker-end', data.l1.marker);

      l2.setAttribute('stroke', data.l2.stroke);
      l2.setAttribute('stroke-width', data.l2.width);
      l2.setAttribute('marker-end', data.l2.marker);

      l3.setAttribute('stroke', data.l3.stroke);
      l3.setAttribute('stroke-width', data.l3.width);
      l3.setAttribute('marker-end', data.l3.marker);

      l4.setAttribute('stroke', data.l4.stroke);
      l4.setAttribute('stroke-width', data.l4.width);
      l4.setAttribute('marker-end', data.l4.marker);

      document.getElementById('lock-prev-btn').disabled = (lockStep === 1);
      document.getElementById('lock-next-btn').disabled = (lockStep === lockTotalSteps);
    }
"""
        updated_content = updated_content.replace(js_search, js_logic + "\n    " + js_search)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully integrated lock-inversion stepper into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if integrate_interactive_stepper():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Add interactive lock inversion stepper to Week 6 Module 02\n\n"
                "Embed a directed narrative stepper visualizing two-thread mutex deadlock\n"
                "with state telemetry, synchronized canvas, and lock hierarchy toggles."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
