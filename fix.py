#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject Interactive Dining Philosophers Stepper into Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "04-classic-synchronization-real-world-defenses.html"
)

DINING_STEPPER_HTML = r"""      <!-- ================================================================= -->
      <!-- INTERACTIVE PEDAGOGICAL AID: DINING PHILOSOPHERS STEPPER          -->
      <!-- ================================================================= -->
      <div class="aid-wrapper" style="background: #ffffff; border: 1px solid var(--border); border-radius: 10px; padding: 24px; margin: 28px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
        <div class="aid-header" style="font-weight: 700; font-size: 1.05rem; color: var(--primary); margin-bottom: 4px;">Interactive Walkthrough: Dining Philosophers Contention &amp; Asymmetry</div>
        <div class="aid-subtitle" style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 16px;">Trace step-by-step how simultaneous left-chopstick acquisition precipitates deadlock, and how asymmetric ordering restores liveness.</div>

        <div class="aid-grid" style="display: grid; grid-template-columns: 280px 1fr; gap: 20px; align-items: start;">
          <div class="controls-panel" style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
            <div class="preview-box" id="dp-preview-text" style="background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-size: 0.86rem; color: var(--text); margin-bottom: 14px; line-height: 1.5; height: 150px; max-height: 150px; display: flex; flex-direction: column; justify-content: center; overflow-y: auto;">
              <strong>Step 1: Quiescent State.</strong> All five philosophers are in the THINKING state. All five chopsticks ($C_0 \dots C_4$) lie free on the table.
            </div>

            <div class="stepper-btns" style="display: flex; gap: 8px; margin-bottom: 14px;">
              <button class="step-btn" id="dp-prev-btn" onclick="changeDpStep(-1)" disabled style="flex: 1; background: var(--primary); color: #ffffff; border: none; padding: 8px 12px; font-size: 0.8rem; font-weight: 600; border-radius: 4px; cursor: pointer;">&larr; Prev</button>
              <button class="step-btn" id="dp-next-btn" onclick="changeDpStep(1)" style="flex: 1; background: var(--primary); color: #ffffff; border: none; padding: 8px 12px; font-size: 0.8rem; font-weight: 600; border-radius: 4px; cursor: pointer;">Next &rarr;</button>
              <button class="step-btn" onclick="resetDpStepper()" style="background:#64748b; color: #ffffff; border: none; padding: 8px 12px; font-size: 0.8rem; font-weight: 600; border-radius: 4px; cursor: pointer;">Reset</button>
            </div>

            <div class="telemetry-bar" id="dp-telemetry-bar" style="background: #0f172a; color: #e2e8f0; font-family: var(--font-mono); font-size: 0.75rem; padding: 10px 12px; border-radius: 6px; margin-bottom: 14px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px 12px;">
              <div><strong>Phase:</strong> <span id="dp-tel-phase" style="color: #38bdf8;">1/4</span></div>
              <div><strong>Eating:</strong> <span id="dp-tel-eating">0 / 5</span></div>
              <div><strong>Chopsticks:</strong> <span id="dp-tel-chop">0 / 5 Held</span></div>
              <div><strong>State:</strong> <span id="dp-tel-state" style="color: #4ade80; font-weight: 700;">Quiescent</span></div>
            </div>

            <div class="toggle-bar" style="display: flex; gap: 8px; padding-top: 10px; border-top: 1px solid var(--border);">
              <span style="font-size: 0.72rem; font-weight: 700; align-self: center; color: var(--text-muted);">ORDER:</span>
              <button class="toggle-btn active" id="dp-btn-sym" onclick="setDpMode('sym')" style="background: #e0f2fe; color: var(--accent); border: 1px solid #bae6fd; padding: 4px 8px; font-size: 0.72rem; border-radius: 4px; cursor: pointer; font-weight: 600;">Symmetric</button>
              <button class="toggle-btn" id="dp-btn-asym" onclick="setDpMode('asym')" style="background: #f1f5f9; border: 1px solid var(--border); padding: 4px 8px; font-size: 0.72rem; border-radius: 4px; cursor: pointer; font-weight: 600; color: var(--text-muted);">Asymmetric</button>
            </div>
          </div>

          <div class="visual-canvas" style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 250px;">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 6px; color: var(--primary);">Synchronized Visual Canvas &mdash; Dining Table Topology</div>

            <!-- Circular Table SVG Canvas -->
            <svg viewBox="0 0 300 240" style="width: 100%; height: 100%; min-height: 200px; background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 6px;">
              <!-- Central Table -->
              <circle cx="150" cy="120" r="65" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" />
              <text x="150" y="124" fill="#94a3b8" font-size="11" font-weight="700" text-anchor="middle">Table</text>

              <!-- Chopstick Rectangles (Radial between philosophers) -->
              <!-- C0 (between P0 and P1) -->
              <rect id="dp-c0" x="145" y="60" width="10" height="24" rx="2" fill="#d97706" transform="rotate(36 150 72)" />
              <text x="168" y="74" fill="#b45309" font-size="8" font-weight="700">C0</text>

              <!-- C1 (between P1 and P2) -->
              <rect id="dp-c1" x="180" y="130" width="10" height="24" rx="2" fill="#d97706" transform="rotate(108 185 142)" />
              <text x="200" y="152" fill="#b45309" font-size="8" font-weight="700">C1</text>

              <!-- C2 (between P2 and P3) -->
              <rect id="dp-c2" x="125" y="170" width="10" height="24" rx="2" fill="#d97706" transform="rotate(180 130 182)" />
              <text x="135" y="198" fill="#b45309" font-size="8" font-weight="700">C2</text>

              <!-- C3 (between P3 and P4) -->
              <rect id="dp-c3" x="90" y="130" width="10" height="24" rx="2" fill="#d97706" transform="rotate(-108 95 142)" />
              <text x="75" y="152" fill="#b45309" font-size="8" font-weight="700">C3</text>

              <!-- C4 (between P4 and P0) -->
              <rect id="dp-c4" x="125" y="60" width="10" height="24" rx="2" fill="#d97706" transform="rotate(-36 130 72)" />
              <text x="110" y="74" fill="#b45309" font-size="8" font-weight="700">C4</text>

              <!-- Philosopher Nodes -->
              <!-- P0 (Top Center) -->
              <circle id="dp-p0" cx="150" cy="25" r="16" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="150" y="29" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P0</text>

              <!-- P1 (Top Right) -->
              <circle id="dp-p1" cx="245" cy="85" r="16" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="245" y="89" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P1</text>

              <!-- P2 (Bottom Right) -->
              <circle id="dp-p2" cx="210" cy="195" r="16" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="210" y="199" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P2</text>

              <!-- P3 (Bottom Left) -->
              <circle id="dp-p3" cx="90" cy="195" r="16" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="90" y="199" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P3</text>

              <!-- P4 (Top Left) -->
              <circle id="dp-p4" cx="55" cy="85" r="16" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="55" y="89" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P4</text>
            </svg>

            <div style="font-size: 0.8rem; color: var(--text-muted); text-align: center; margin-top: 8px;" id="dp-canvas-banner">
              Simulation Status: <strong>Ready to step forward</strong>
            </div>
          </div>
        </div>

        <div class="panes-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 16px;">
          <div class="pane-box" style="background: #f8fafc; border: 1px solid var(--border); border-left: 3px solid var(--success); border-radius: 6px; padding: 12px 14px; font-size: 0.82rem;">
            <div class="pane-title" style="color: var(--success); font-weight: 700; margin-bottom: 6px; text-transform: uppercase;">&#128269; What Is Happening</div>
            <div id="dp-pane-what" style="color: var(--text);">All philosophers are initialized in THINKING state. No semaphores or mutexes are locked.</div>
          </div>
          <div class="pane-box" style="background: #f8fafc; border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 6px; padding: 12px 14px; font-size: 0.82rem;">
            <div class="pane-title" style="color: var(--accent); font-weight: 700; margin-bottom: 6px; text-transform: uppercase;">&#9881; Why The System Does This</div>
            <div id="dp-pane-why" style="color: var(--text);">Independent concurrent threads start in uncoupled states before contending for shared physical hardware.</div>
          </div>
        </div>
      </div>
"""

DP_SCRIPT_LOGIC = r"""
  <script>
    let dpStep = 1;
    const dpTotalSteps = 4;
    let dpMode = 'sym';

    const dpSymData = [
      {
        preview: "<strong>Step 1: Quiescent State.</strong> All five philosophers are in THINKING state. All five chopsticks ($C_0 \\dots C_4$) lie free on the table.",
        phase: "1/4", eating: "0 / 5", chop: "0 / 5 Held", state: "Quiescent", stateColor: "#4ade80",
        what: "All philosophers are initialized in THINKING state. No semaphores or mutexes are locked.",
        why: "Independent concurrent threads start in uncoupled states before contending for shared physical hardware.",
        banner: "Simulation Status: <strong>Quiescent (All Thinking)</strong>",
        activeNodes: [], eatingNodes: [], heldChopsticks: []
      },
      {
        preview: "<strong>Step 2: Simultaneous Left Acquisition.</strong> All philosophers become HUNGRY and invoke <code>wait(chopstick[i])</code> simultaneously. Each claims their left chopstick.",
        phase: "2/4", eating: "0 / 5", chop: "5 / 5 Held", state: "Hold-and-Wait", stateColor: "#d97706",
        what: "P0 takes C0, P1 takes C1, P2 takes C2, P3 takes C3, and P4 takes C4. Hold-and-wait is established system-wide.",
        why: "Without global admission control, threads greedily acquire the first available resource before verifying total path feasibility.",
        banner: "Hazard Active: <strong>Every philosopher holds 1 chopstick</strong>",
        activeNodes: ['dp-p0', 'dp-p1', 'dp-p2', 'dp-p3', 'dp-p4'], eatingNodes: [],
        heldChopsticks: ['dp-c0', 'dp-c1', 'dp-c2', 'dp-c3', 'dp-c4']
      },
      {
        preview: "<strong>Step 3: Right Chopstick Contention.</strong> Every philosopher invokes <code>wait(chopstick[(i+1)%5])</code>. Every right chopstick is already locked by their clockwise neighbor.",
        phase: "3/4", eating: "0 / 5", chop: "5 / 5 Contended", state: "Circular Wait", stateColor: "#dc2626",
        what: "P0 waits for C1 (held by P1); P1 waits for C2 (held by P2); ... P4 waits for C0 (held by P0). A directed cycle forms.",
        why: "Symmetric acquisition rules create symmetric lock contention, directly fulfilling Coffman's 4th condition.",
        banner: "Hazard Critical: <strong>5-Way Circular Wait Chain Formed</strong>",
        activeNodes: ['dp-p0', 'dp-p1', 'dp-p2', 'dp-p3', 'dp-p4'], eatingNodes: [],
        heldChopsticks: ['dp-c0', 'dp-c1', 'dp-c2', 'dp-c3', 'dp-c4']
      },
      {
        preview: "<strong>Step 4: Deadlock Collapse.</strong> All four Coffman conditions are satisfied simultaneously. No thread can proceed; zero forward progress is possible.",
        phase: "4/4", eating: "0 / 5", chop: "All Locked", state: "DEADLOCK", stateColor: "#dc2626",
        what: "System freezes permanently. Starvation is total. Thread queues remain blocked until operator intervention or timeout.",
        why: "Illustrates the catastrophic risk of unconstrained resource competition in concurrent operating systems.",
        banner: "System Halted: <strong>TOTAL DEADLOCK COLLAPSE</strong>",
        activeNodes: ['dp-p0', 'dp-p1', 'dp-p2', 'dp-p3', 'dp-p4'], eatingNodes: [],
        heldChopsticks: ['dp-c0', 'dp-c1', 'dp-c2', 'dp-c3', 'dp-c4']
      }
    ];

    const dpAsymData = [
      {
        preview: "<strong>Step 1: Quiescent State.</strong> All philosophers thinking. Odd/Even asymmetric pickup protocol activated (Even: Right first, Odd: Left first).",
        phase: "1/4", eating: "0 / 5", chop: "0 / 5 Held", state: "Asymmetric Init", stateColor: "#38bdf8",
        what: "Asymmetry breaks circular symmetry before execution starts by establishing distinct acquisition sequences.",
        why: "Havender's principle: imposing distinct ordering rules mathematically prohibits directed cycle formation.",
        banner: "Protocol: <strong>Asymmetric Ordering Active</strong>",
        activeNodes: [], eatingNodes: [], heldChopsticks: []
      },
      {
        preview: "<strong>Step 2: Contention on C0.</strong> P0 (even) reaches right for C4; P4 (odd) also reaches for C4. P0 wins C4; P4 is blocked BEFORE acquiring any chopstick.",
        phase: "2/4", eating: "0 / 5", chop: "3 / 5 Held", state: "Symmetry Broken", stateColor: "#38bdf8",
        what: "Because P4 is blocked without holding any resource, the Hold-and-Wait condition is broken across the ring.",
        why: "Forcing competitors to contest the same resource first prevents all agents from simultaneously grabbing one resource.",
        banner: "Progress: <strong>P4 blocked without holding resources</strong>",
        activeNodes: ['dp-p0', 'dp-p2'], eatingNodes: [],
        heldChopsticks: ['dp-c4', 'dp-c2']
      },
      {
        preview: "<strong>Step 3: Philosophers P0 &amp; P2 Eat Concurrently.</strong> P0 claims C0; P2 claims C1. Both hold two chopsticks and transition to EATING concurrently.",
        phase: "3/4", eating: "2 / 5", chop: "4 / 5 Active", state: "Active Eating", stateColor: "#16a34a",
        what: "P0 eats with (C4, C0) and P2 eats with (C2, C1). Maximum theoretical concurrency (floor(5/2) = 2) is achieved.",
        why: "The system reaches optimal scheduling capacity while remaining entirely deadlock-free.",
        banner: "Active Execution: <strong>P0 and P2 Eating Concurrently</strong>",
        activeNodes: [], eatingNodes: ['dp-p0', 'dp-p2'],
        heldChopsticks: ['dp-c4', 'dp-c0', 'dp-c2', 'dp-c1']
      },
      {
        preview: "<strong>Step 4: Resources Released &amp; Ring Cycles.</strong> P0 and P2 finish eating, releasing all 4 chopsticks. Waiting philosophers P1, P3, and P4 proceed fairly.",
        phase: "4/4", eating: "Alternating", chop: "Recycled", state: "Liveness Guaranteed", stateColor: "#16a34a",
        what: "P1 and P3 claim freed chopsticks and eat next. System maintains continuous forward progress without starvation.",
        why: "Asymmetry guarantees liveness and complete absence of circular dependencies indefinitely.",
        banner: "Protocol Success: <strong>Continuous Liveness &amp; Deadlock-Free</strong>",
        activeNodes: [], eatingNodes: ['dp-p1', 'dp-p3'],
        heldChopsticks: ['dp-c1', 'dp-c2', 'dp-c3']
      }
    ];

    function changeDpStep(dir) {
      dpStep += dir;
      if (dpStep < 1) dpStep = 1;
      if (dpStep > dpTotalSteps) dpStep = dpTotalSteps;
      updateDpUI();
    }

    function resetDpStepper() {
      dpStep = 1;
      updateDpUI();
    }

    function setDpMode(mode) {
      dpMode = mode;
      document.getElementById('dp-btn-sym').className = (mode === 'sym') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('dp-btn-asym').className = (mode === 'asym') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('dp-btn-sym').style.background = (mode === 'sym') ? '#e0f2fe' : '#f1f5f9';
      document.getElementById('dp-btn-asym').style.background = (mode === 'asym') ? '#e0f2fe' : '#f1f5f9';
      dpStep = 1;
      updateDpUI();
    }

    function updateDpUI() {
      const dataset = (dpMode === 'sym') ? dpSymData : dpAsymData;
      const data = dataset[dpStep - 1];

      document.getElementById('dp-preview-text').innerHTML = data.preview;
      document.getElementById('dp-tel-phase').innerText = data.phase;
      document.getElementById('dp-tel-eating').innerText = data.eating;
      document.getElementById('dp-tel-chop').innerText = data.chop;

      const stateEl = document.getElementById('dp-tel-state');
      stateEl.innerText = data.state;
      stateEl.style.color = data.stateColor;

      document.getElementById('dp-pane-what').innerHTML = data.what;
      document.getElementById('dp-pane-why').innerHTML = data.why;
      document.getElementById('dp-canvas-banner').innerHTML = data.banner;

      // Update SVG node styling
      ['dp-p0', 'dp-p1', 'dp-p2', 'dp-p3', 'dp-p4'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.setAttribute('fill', '#ffffff');
          el.setAttribute('stroke', '#0284c7');
        }
      });

      data.activeNodes.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.setAttribute('fill', (dpMode === 'sym' && dpStep >= 3) ? '#fee2e2' : '#fef3c7');
          el.setAttribute('stroke', (dpMode === 'sym' && dpStep >= 3) ? '#dc2626' : '#d97706');
        }
      });

      data.eatingNodes.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.setAttribute('fill', '#dcfce7');
          el.setAttribute('stroke', '#16a34a');
        }
      });

      // Update chopsticks styling
      ['dp-c0', 'dp-c1', 'dp-c2', 'dp-c3', 'dp-c4'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.setAttribute('fill', '#cbd5e1');
        }
      });

      data.heldChopsticks.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.setAttribute('fill', (dpMode === 'sym' && dpStep >= 3) ? '#dc2626' : '#d97706');
        }
      });

      document.getElementById('dp-prev-btn').disabled = (dpStep === 1);
      document.getElementById('dp-next-btn').disabled = (dpStep === dpTotalSteps);
    }
  </script>
"""

def inject_dining_stepper():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate injection site right after failure mode 1
    target_marker = "      <h4>3. Failure Mode 2: Livelock via Naive Preemption</h4>"
    if target_marker not in content:
        print("Error: Could not locate target marker in Module 04.")
        return False

    # Check if aid already exists
    if "Interactive Walkthrough: Dining Philosophers Contention &amp; Asymmetry" in content:
        print("Notice: Dining Philosophers stepper already exists in Module 04.")
        return True

    # Inject stepper before Failure Mode 2
    content = content.replace(target_marker, DINING_STEPPER_HTML + "\n" + target_marker)

    # Inject JavaScript logic before </body>
    if "let dpStep = 1;" not in content:
        content = content.replace("</body>", DP_SCRIPT_LOGIC + "\n</body>")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully injected Dining Philosophers Stepper into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if inject_dining_stepper():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Add interactive Dining Philosophers stepper widget to Module 04\n\n"
                "Implement circular table SVG visualization, live allocation telemetry,\n"
                "paired analytical panes, and symmetric vs asymmetric mode toggles."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
