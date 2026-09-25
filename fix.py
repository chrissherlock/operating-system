#!/usr/bin/env python3
# =====================================================================
# fix.py: Add interactive Coffman Conditions walkthrough to Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

COFFMAN_STEPPER_HTML = r"""      <!-- ================================================================= -->
      <!-- INTERACTIVE STEPPER: THE FOUR COFFMAN CONDITIONS CONJUNCTION       -->
      <!-- ================================================================= -->
      <div class="aid-wrapper">
        <div class="aid-header">Interactive Walkthrough: The Four Coffman Conditions in Action</div>
        <div class="aid-subtitle">Explore how all four conditions must combine simultaneously to trigger a deadlock, and see how breaking any single condition restores liveness.</div>

        <div class="aid-grid">
          <div class="controls-panel">
            <div class="preview-box" id="coff-preview-text">
              <strong>Step 1: Mutual Exclusion (C1 Active).</strong> Resource R1 cannot be shared. Process P1 claims exclusive ownership of R1, forcing any other requester to wait.
            </div>

            <div class="stepper-btns">
              <button class="step-btn" id="coff-prev-btn" onclick="changeCoffStep(-1)" disabled>&larr; Prev</button>
              <button class="step-btn" id="coff-next-btn" onclick="changeCoffStep(1)">Next &rarr;</button>
              <button class="step-btn" onclick="resetCoffStepper()" style="background:#64748b;">Reset</button>
            </div>

            <div class="telemetry-bar" id="coff-telemetry-bar" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px 12px; font-family: var(--font-mono); font-size: 0.75rem; background: #0f172a; color: #e2e8f0; padding: 10px 12px; border-radius: 6px;">
              <div><strong>Condition:</strong> <span id="coff-tel-cond" style="color: #38bdf8;">C1 (Mutex)</span></div>
              <div><strong>Preemption:</strong> <span id="coff-tel-preempt">Allowed</span></div>
              <div><strong>Wait Chain:</strong> <span id="coff-tel-chain">Linear</span></div>
              <div><strong>Deadlock:</strong> <span id="coff-tel-status" style="color: #4ade80; font-weight: 700;">FALSE</span></div>
            </div>

            <div class="toggle-bar">
              <span style="font-size: 0.72rem; font-weight: 700; align-self: center; color: var(--text-muted);">DEFENSE:</span>
              <button class="toggle-btn active" id="coff-btn-build" onclick="setCoffMode('build')">Accumulate (1 &rarr; 4)</button>
              <button class="toggle-btn" id="coff-btn-break" onclick="setCoffMode('break')">Break One (Liveness)</button>
            </div>
          </div>

          <div class="visual-canvas" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; background: #ffffff; border: 1px solid var(--border);">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 6px; color: var(--primary); text-align: left;">Synchronized Visual Canvas &mdash; Coffman Condition Gate</div>

            <!-- Visual Condition Status Dashboard -->
            <svg viewBox="0 0 320 180" style="width: 100%; height: 100%; min-height: 190px; background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 8px;">
              <!-- Condition Badges -->
              <!-- C1: Mutual Exclusion -->
              <rect id="svg-c1-box" x="15" y="20" width="135" height="34" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5" />
              <text x="25" y="36" fill="#15803d" font-size="8.5" font-weight="bold">C1: Mutual Exclusion</text>
              <text id="svg-c1-val" x="25" y="47" fill="#166534" font-size="7" font-family="monospace">ACTIVE (Exclusive)</text>

              <!-- C2: Hold and Wait -->
              <rect id="svg-c2-box" x="170" y="20" width="135" height="34" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="180" y="36" fill="#64748b" font-size="8.5" font-weight="bold">C2: Hold &amp; Wait</text>
              <text id="svg-c2-val" x="180" y="47" fill="#94a3b8" font-size="7" font-family="monospace">INACTIVE</text>

              <!-- C3: No Preemption -->
              <rect id="svg-c3-box" x="15" y="65" width="135" height="34" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="25" y="81" fill="#64748b" font-size="8.5" font-weight="bold">C3: No Preemption</text>
              <text id="svg-c3-val" x="25" y="92" fill="#94a3b8" font-size="7" font-family="monospace">INACTIVE (Revocable)</text>

              <!-- C4: Circular Wait -->
              <rect id="svg-c4-box" x="170" y="65" width="135" height="34" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="180" y="81" fill="#64748b" font-size="8.5" font-weight="bold">C4: Circular Wait</text>
              <text id="svg-c4-val" x="180" y="92" fill="#94a3b8" font-size="7" font-family="monospace">INACTIVE (Acyclic)</text>

              <!-- Conjunction Logic Bar -->
              <rect id="svg-eval-bar" x="15" y="115" width="290" height="45" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" />
              <text x="160" y="132" fill="#15803d" font-size="9" font-weight="bold" text-anchor="middle">CONJUNCTION EVALUATION</text>
              <text id="svg-eval-eq" x="160" y="148" fill="#166534" font-size="8" font-family="monospace" text-anchor="middle">C1 &and; &not;C2 &and; &not;C3 &and; &not;C4 = NO DEADLOCK</text>
            </svg>

            <div style="font-size: 0.8rem; color: var(--text-muted); text-align: center; margin-top: 6px;" id="coff-canvas-banner">
              Conjunction Status: <strong>System Safe (Only 1 condition active)</strong>
            </div>
          </div>
        </div>

        <div class="panes-grid">
          <div class="pane-box" style="border-left: 3px solid var(--success);">
            <div class="pane-title" style="color: var(--success);">&#128269; What Is Happening</div>
            <div id="coff-pane-what" style="color: var(--text);">Process P1 acquires exclusive access to resource R1. R1 cannot be shared simultaneously.</div>
          </div>
          <div class="pane-box" style="border-left: 3px solid var(--accent);">
            <div class="pane-title" style="color: var(--accent);">&#9881; Why The System Does This</div>
            <div id="coff-pane-why" style="color: var(--text);">Physical hardware (such as write heads or tape drives) produces corrupted data if accessed concurrently without mutual exclusion.</div>
          </div>
        </div>
      </div>
"""

def integrate_coffman_stepper():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for insertion point right after the Necessary vs Sufficient callout in Section 2
    search_anchor = '<div class="math-callout">\n        <strong>The Necessary vs. Sufficient Distinction:</strong>'
    if search_anchor not in content:
        # Fallback with flexible whitespace
        search_anchor = "The Necessary vs. Sufficient Distinction:"
        if search_anchor not in content:
            print("Error: Could not locate Section 2 callout anchor.")
            return False

    if "Interactive Walkthrough: The Four Coffman Conditions in Action" in content:
        print("Notice: Coffman stepper already exists in Module 02.")
        return True

    anchor_pos = content.find(search_anchor)
    insert_pos = content.find("</div>", anchor_pos) + len("</div>")

    updated_content = content[:insert_pos] + "\n\n" + COFFMAN_STEPPER_HTML + content[insert_pos:]

    # Add JavaScript driving logic to end of script section
    js_search = "function setTopology(topo) {"
    if js_search in updated_content and "let coffStep = 1;" not in updated_content:
        js_logic = r"""
    // --- Interactive Coffman Conditions Stepper Logic ---
    let coffStep = 1;
    const coffTotalSteps = 4;
    let coffMode = 'build';

    const coffBuildData = [
      {
        preview: "<strong>Step 1: Mutual Exclusion (C1).</strong> Resource R1 is non-shareable. P1 claims R1 exclusively. Other processes requesting R1 are blocked.",
        phase: "C1 Active", cond: "C1 (Mutex)", preempt: "Allowed", chain: "Linear", status: "SAFE", statusColor: "#4ade80",
        what: "P1 holds exclusive lock on R1. Mutual exclusion is satisfied.",
        why: "Exclusive access protects hardware devices and memory consistency from race conditions.",
        banner: "Conjunction: <strong>C1 active &mdash; System Safe (0 cycles)</strong>",
        c1: { fill: "#fef3c7", stroke: "#d97706", txt: "ACTIVE (Exclusive)", col: "#92400e" },
        c2: { fill: "#f8fafc", stroke: "#cbd5e1", txt: "INACTIVE", col: "#94a3b8" },
        c3: { fill: "#f8fafc", stroke: "#cbd5e1", txt: "INACTIVE (Revocable)", col: "#94a3b8" },
        c4: { fill: "#f8fafc", stroke: "#cbd5e1", txt: "INACTIVE (Acyclic)", col: "#94a3b8" },
        eval: { fill: "#f0fdf4", stroke: "#16a34a", col: "#15803d", eq: "C1 \u2227 \u00ACC2 \u2227 \u00ACC3 \u2227 \u00ACC4 \u2192 NO DEADLOCK" }
      },
      {
        preview: "<strong>Step 2: Hold and Wait (C2 Added).</strong> P1 holds R1 while requesting R2. Meanwhile, P2 holds R2 and requests R1. Processes hold existing assets while sleeping.",
        phase: "C1 + C2", cond: "C1 &and; C2", preempt: "Allowed", chain: "Pending", status: "VULNERABLE", statusColor: "#facc15",
        what: "Processes retain their allocated resources while suspended awaiting additional ones.",
        why: "Programs allocate resources incrementally over time rather than requesting all resources upfront.",
        banner: "Conjunction: <strong>C1 &and; C2 active &mdash; Vulnerable, but preemption can still break it</strong>",
        c1: { fill: "#fef3c7", stroke: "#d97706", txt: "ACTIVE (Exclusive)", col: "#92400e" },
        c2: { fill: "#fef3c7", stroke: "#d97706", txt: "ACTIVE (Hold & Wait)", col: "#92400e" },
        c3: { fill: "#f8fafc", stroke: "#cbd5e1", txt: "INACTIVE (Revocable)", col: "#94a3b8" },
        c4: { fill: "#f8fafc", stroke: "#cbd5e1", txt: "INACTIVE (Acyclic)", col: "#94a3b8" },
        eval: { fill: "#fffbeb", stroke: "#d97706", col: "#b45309", eq: "C1 \u2227 C2 \u2227 \u00ACC3 \u2227 \u00ACC4 \u2192 NO DEADLOCK" }
      },
      {
        preview: "<strong>Step 3: No Preemption (C3 Added).</strong> The OS cannot revoke held resources. Only the owning process may voluntarily unlock R1 or R2.",
        phase: "C1 + C2 + C3", cond: "C1 &and; C2 &and; C3", preempt: "FORBIDDEN", chain: "Locked", status: "HIGH RISK", statusColor: "#f97316",
        what: "Neither P1 nor P2 can be forcibly stripped of their allocations. Preemption is forbidden.",
        why: "Preempting arbitrary database locks or open file writes can leave critical structures corrupt.",
        banner: "Conjunction: <strong>C1 &and; C2 &and; C3 active &mdash; Three conditions locked in</strong>",
        c1: { fill: "#fef3c7", stroke: "#d97706", txt: "ACTIVE (Exclusive)", col: "#92400e" },
        c2: { fill: "#fef3c7", stroke: "#d97706", txt: "ACTIVE (Hold & Wait)", col: "#92400e" },
        c3: { fill: "#fef3c7", stroke: "#d97706", txt: "ACTIVE (No Preempt)", col: "#92400e" },
        c4: { fill: "#f8fafc", stroke: "#cbd5e1", txt: "INACTIVE (Acyclic)", col: "#94a3b8" },
        eval: { fill: "#fffbeb", stroke: "#f97316", col: "#c2410c", eq: "C1 \u2227 C2 \u2227 C3 \u2227 \u00ACC4 \u2192 NO DEADLOCK" }
      },
      {
        preview: "<strong>Step 4: Circular Wait (C4 Added &mdash; DEADLOCK).</strong> P1 waits for R2 (held by P2), and P2 waits for R1 (held by P1). All four conditions are satisfied!",
        phase: "ALL 4 ACTIVE", cond: "C1 &and; C2 &and; C3 &and; C4", preempt: "FORBIDDEN", chain: "CLOSED CYCLE", status: "DEADLOCKED", statusColor: "#dc2626",
        what: "A closed dependency ring forms: P1 &rarr; R2 &rarr; P2 &rarr; R1 &rarr; P1. Both threads freeze permanently.",
        why: "When all four necessary conditions coincide, deadlock is mathematically inevitable.",
        banner: "DEADLOCK TRIGGERED: <strong>All 4 conditions true &mdash; System permanently frozen</strong>",
        c1: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE (Exclusive)", col: "#991b1b" },
        c2: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE (Hold & Wait)", col: "#991b1b" },
        c3: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE (No Preempt)", col: "#991b1b" },
        c4: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE (Cycle)", col: "#991b1b" },
        eval: { fill: "#fee2e2", stroke: "#dc2626", col: "#b91c1c", eq: "C1 \u2227 C2 \u2227 C3 \u2227 C4 \u2192 DEADLOCK TRIGGERED!" }
      }
    ];

    const coffBreakData = [
      {
        preview: "<strong>Defense 1: Break Mutual Exclusion (Spooled Shared Access).</strong> Virtualize R1 via a daemon spooler. Multiple processes write to disk queues; deadlock cannot occur.",
        phase: "Break C1", cond: "&not;C1 (Shared)", preempt: "Forbidden", chain: "Closed", status: "RESOLVED", statusColor: "#16a34a",
        what: "Printer or socket is made sharable via daemon queues. Mutual exclusion is eliminated.",
        why: "Without exclusive locking, processes never block waiting for exclusive physical ownership.",
        banner: "Mitigation Verified: <strong>&not;C1 breaks deadlock &mdash; Spooler restores liveness</strong>",
        c1: { fill: "#dcfce7", stroke: "#16a34a", txt: "BROKEN (Spooled)", col: "#15803d" },
        c2: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c3: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c4: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        eval: { fill: "#f0fdf4", stroke: "#16a34a", col: "#15803d", eq: "\u00ACC1 \u2227 C2 \u2227 C3 \u2227 C4 \u2192 NO DEADLOCK (Broken C1)" }
      },
      {
        preview: "<strong>Defense 2: Break Hold &amp; Wait (All-or-Nothing Allocation).</strong> Require processes to request all needed resources at startup. If any resource is unavailable, hold nothing.",
        phase: "Break C2", cond: "&not;C2 (Atomic)", preempt: "Forbidden", chain: "None", status: "RESOLVED", statusColor: "#16a34a",
        what: "Process must release held assets before requesting new ones, or claim all resources in one atomic call.",
        why: "A thread that holds zero resources while waiting cannot block another thread.",
        banner: "Mitigation Verified: <strong>&not;C2 breaks deadlock &mdash; Conservative allocation</strong>",
        c1: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c2: { fill: "#dcfce7", stroke: "#16a34a", txt: "BROKEN (All-or-None)", col: "#15803d" },
        c3: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c4: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        eval: { fill: "#f0fdf4", stroke: "#16a34a", col: "#15803d", eq: "C1 \u2227 \u00ACC2 \u2227 C3 \u2227 C4 \u2192 NO DEADLOCK (Broken C2)" }
      },
      {
        preview: "<strong>Defense 3: Break No Preemption (Resource Revocation).</strong> If P1 requests a busy resource, the kernel forcibly revokes its existing allocations and restarts P1.",
        phase: "Break C3", cond: "&not;C3 (Preempt)", preempt: "FORCED", chain: "Broken", status: "RESOLVED", statusColor: "#16a34a",
        what: "Kernel preempts held locks from blocked processes, rolling them back to clean checkpoints.",
        why: "Forcible preemption breaks the permanent sleep invariant.",
        banner: "Mitigation Verified: <strong>&not;C3 breaks deadlock &mdash; Kernel preemption enabled</strong>",
        c1: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c2: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c3: { fill: "#dcfce7", stroke: "#16a34a", txt: "BROKEN (Preemption)", col: "#15803d" },
        c4: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        eval: { fill: "#f0fdf4", stroke: "#16a34a", col: "#15803d", eq: "C1 \u2227 C2 \u2227 \u00ACC3 \u2227 C4 \u2192 NO DEADLOCK (Broken C3)" }
      },
      {
        preview: "<strong>Defense 4: Break Circular Wait (Global Linear Ordering).</strong> Impose strict numerical ordering $F(R)$. Threads may only request resources in strictly ascending order.",
        phase: "Break C4", cond: "&not;C4 (Hierarchy)", preempt: "Forbidden", chain: "DAG Only", status: "RESOLVED", statusColor: "#16a34a",
        what: "Global hierarchy guarantees the resource allocation graph is a Directed Acyclic Graph (DAG).",
        why: "A cycle cannot exist in a graph where all edges point from lower to higher indices.",
        banner: "Mitigation Verified: <strong>&not;C4 breaks deadlock &mdash; Havender linear hierarchy</strong>",
        c1: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c2: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c3: { fill: "#fee2e2", stroke: "#dc2626", txt: "ACTIVE", col: "#991b1b" },
        c4: { fill: "#dcfce7", stroke: "#16a34a", txt: "BROKEN (Strict DAG)", col: "#15803d" },
        eval: { fill: "#f0fdf4", stroke: "#16a34a", col: "#15803d", eq: "C1 \u2227 C2 \u2227 C3 \u2227 \u00ACC4 \u2192 NO DEADLOCK (Broken C4)" }
      }
    ];

    function changeCoffStep(dir) {
      coffStep += dir;
      if (coffStep < 1) coffStep = 1;
      if (coffStep > coffTotalSteps) coffStep = coffTotalSteps;
      updateCoffUI();
    }

    function resetCoffStepper() {
      coffStep = 1;
      updateCoffUI();
    }

    function setCoffMode(mode) {
      coffMode = mode;
      document.getElementById('coff-btn-build').className = (mode === 'build') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('coff-btn-break').className = (mode === 'break') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('coff-btn-build').style.background = (mode === 'build') ? '#e0f2fe' : '#f1f5f9';
      document.getElementById('coff-btn-break').style.background = (mode === 'break') ? '#e0f2fe' : '#f1f5f9';
      coffStep = 1;
      updateCoffUI();
    }

    function updateCoffUI() {
      const dataset = (coffMode === 'build') ? coffBuildData : coffBreakData;
      const data = dataset[coffStep - 1];

      document.getElementById('coff-preview-text').innerHTML = data.preview;
      document.getElementById('coff-tel-cond').innerHTML = data.cond;
      document.getElementById('coff-tel-preempt').innerText = data.preempt;
      document.getElementById('coff-tel-chain').innerText = data.chain;

      const stEl = document.getElementById('coff-tel-status');
      stEl.innerText = data.status;
      stEl.style.color = data.statusColor;

      document.getElementById('coff-pane-what').innerText = data.what;
      document.getElementById('coff-pane-why').innerText = data.why;
      document.getElementById('coff-canvas-banner').innerHTML = data.banner;

      // Update C1 box
      const b1 = document.getElementById('svg-c1-box');
      const v1 = document.getElementById('svg-c1-val');
      b1.setAttribute('fill', data.c1.fill);
      b1.setAttribute('stroke', data.c1.stroke);
      v1.textContent = data.c1.txt;
      v1.setAttribute('fill', data.c1.col);

      // Update C2 box
      const b2 = document.getElementById('svg-c2-box');
      const v2 = document.getElementById('svg-c2-val');
      b2.setAttribute('fill', data.c2.fill);
      b2.setAttribute('stroke', data.c2.stroke);
      v2.textContent = data.c2.txt;
      v2.setAttribute('fill', data.c2.col);

      // Update C3 box
      const b3 = document.getElementById('svg-c3-box');
      const v3 = document.getElementById('svg-c3-val');
      b3.setAttribute('fill', data.c3.fill);
      b3.setAttribute('stroke', data.c3.stroke);
      v3.textContent = data.c3.txt;
      v3.setAttribute('fill', data.c3.col);

      // Update C4 box
      const b4 = document.getElementById('svg-c4-box');
      const v4 = document.getElementById('svg-c4-val');
      b4.setAttribute('fill', data.c4.fill);
      b4.setAttribute('stroke', data.c4.stroke);
      v4.textContent = data.c4.txt;
      v4.setAttribute('fill', data.c4.col);

      // Update evaluation bar
      const eb = document.getElementById('svg-eval-bar');
      const eq = document.getElementById('svg-eval-eq');
      eb.setAttribute('fill', data.eval.fill);
      eb.setAttribute('stroke', data.eval.stroke);
      eq.textContent = data.eval.eq;
      eq.setAttribute('fill', data.eval.col);

      document.getElementById('coff-prev-btn').disabled = (coffStep === 1);
      document.getElementById('coff-next-btn').disabled = (coffStep === coffTotalSteps);
    }
"""
        updated_content = updated_content.replace(js_search, js_logic + "\n    " + js_search)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully integrated Coffman stepper into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if integrate_coffman_stepper():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Add interactive Coffman conditions stepper to Week 6 Module 02\n\n"
                "Embed a directed narrative walkthrough evaluating the conjunction of all\n"
                "four Coffman conditions with live state telemetry and mitigation toggles."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
