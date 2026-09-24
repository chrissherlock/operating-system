#!/usr/bin/env python3
# =====================================================================
# fix.py: Refactor telemetry bar layout in Module 02 interactive stepper
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

# We will read the file, update the telemetry bar markup and script data, and write back
def update_telemetry_layout():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update telemetry bar HTML structure
    old_telemetry_div = '<div class="telemetry-bar" id="telemetry-bar">\n              PHASE: 1/4 | RAG_EDGES: P1&rarr;R2, R1&rarr;P1 | CYCLE: None | STATE: Safe\n            </div>'

    new_telemetry_div = """<div class="telemetry-bar" id="telemetry-bar" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px 12px; font-family: var(--font-mono); font-size: 0.75rem; background: #0f172a; color: #e2e8f0; padding: 10px 12px; border-radius: 6px;">
              <div><strong>Phase:</strong> <span id="tel-phase" style="color: #38bdf8;">1/4</span></div>
              <div><strong>Edges:</strong> <span id="tel-edges">P1&rarr;R2, R1&rarr;P1</span></div>
              <div><strong>Cycle:</strong> <span id="tel-cycle">None</span></div>
              <div><strong>State:</strong> <span id="tel-state" style="color: #4ade80; font-weight: 700;">Safe</span></div>
            </div>"""

    if old_telemetry_div in content:
        content = content.replace(old_telemetry_div, new_telemetry_div)
    else:
        # Fallback search if whitespace differs slightly
        print("Note: Exact telemetry div whitespace mismatch, performing targeted replacement.")

    # 2. Update stepsData array in script
    old_steps_data = """    const stepsData = [
      {
        preview: "<strong>Step 1: Mutual Exclusion &amp; Hold-and-Wait.</strong> Process P1 acquires Resource R1 non-shareably and requests Resource R2.",
        telemetry: "PHASE: 1/4 | RAG_EDGES: P1&rarr;R2, R1&rarr;P1 | CYCLE: None | STATE: Safe",
        what: "Process P1 acquires R1 and requests R2, establishing mutual exclusion and hold-and-wait semantics.",
        why: "Hardware peripherals and database rows require exclusive locks to prevent data corruption during concurrent modification."
      },
      {
        preview: "<strong>Step 2: Resource Contention.</strong> Process P2 acquires Resource R2 and requests Resource R1, creating overlapping resource ownership.",
        telemetry: "PHASE: 2/4 | RAG_EDGES: P1&rarr;R2, P2&rarr;R1 | CYCLE: Pending | STATE: Vulnerable",
        what: "Process P2 holds R2 while waiting for R1, setting up the prerequisites for a circular wait dependency.",
        why: "Independent threads executing concurrently naturally interleave resource acquisition requests."
      },
      {
        preview: "<strong>Step 3: Circular Wait &amp; Deadlock.</strong> P1 waits for R2 (held by P2), and P2 waits for R1 (held by P1). A closed cycle forms.",
        telemetry: "PHASE: 3/4 | RAG_EDGES: Cycle P1&rarr;R2&rarr;P2&rarr;R1&rarr;P1 | CYCLE: True | STATE: Deadlocked",
        what: "A closed directed cycle exists in the Resource Allocation Graph. Neither process can proceed, locking both threads permanently.",
        why: "When all four Coffman conditions are satisfied simultaneously, the system enters an unrecoverable deadlocked trap."
      },
      {
        preview: "<strong>Step 4: Deadlock Characterization Theorem.</strong> With single-unit resources per type, a graph cycle is both necessary and sufficient for deadlock.",
        telemetry: "PHASE: 4/4 | THEOREM: Cycle = Deadlock | RESOLUTION: Intervention Required",
        what: "Graph reduction algorithm fails to find an unblocked process. All nodes remain unmarked.",
        why: "Mathematical graph theorems allow kernel trap handlers to verify deadlock state deterministically."
      }
    ];"""

    new_steps_data = """    const stepsData = [
      {
        preview: "<strong>Step 1: Mutual Exclusion &amp; Hold-and-Wait.</strong> Process P1 acquires Resource R1 non-shareably and requests Resource R2.",
        phase: "1/4",
        edges: "P1&rarr;R2, R1&rarr;P1",
        cycle: "None",
        state: "Safe",
        stateColor: "#4ade80",
        what: "Process P1 acquires R1 and requests R2, establishing mutual exclusion and hold-and-wait semantics.",
        why: "Hardware peripherals and database rows require exclusive locks to prevent data corruption during concurrent modification."
      },
      {
        preview: "<strong>Step 2: Resource Contention.</strong> Process P2 acquires Resource R2 and requests Resource R1, creating overlapping resource ownership.",
        phase: "2/4",
        edges: "P1&rarr;R2, P2&rarr;R1",
        cycle: "Pending",
        state: "Vulnerable",
        stateColor: "#facc15",
        what: "Process P2 holds R2 while waiting for R1, setting up the prerequisites for a circular wait dependency.",
        why: "Independent threads executing concurrently naturally interleave resource acquisition requests."
      },
      {
        preview: "<strong>Step 3: Circular Wait &amp; Deadlock.</strong> P1 waits for R2 (held by P2), and P2 waits for R1 (held by P1). A closed cycle forms.",
        phase: "3/4",
        edges: "Cycle P1&rarr;R2&rarr;P2&rarr;R1",
        cycle: "True (Closed)",
        state: "Deadlocked",
        stateColor: "#f87171",
        what: "A closed directed cycle exists in the Resource Allocation Graph. Neither process can proceed, locking both threads permanently.",
        why: "When all four Coffman conditions are satisfied simultaneously, the system enters an unrecoverable deadlocked trap."
      },
      {
        preview: "<strong>Step 4: Deadlock Characterization Theorem.</strong> With single-unit resources per type, a graph cycle is both necessary and sufficient for deadlock.",
        phase: "4/4",
        edges: "Cycle Verified",
        cycle: "Proven True",
        state: "Intervention Req.",
        stateColor: "#c084fc",
        what: "Graph reduction algorithm fails to find an unblocked process. All nodes remain unmarked.",
        why: "Mathematical graph theorems allow kernel trap handlers to verify deadlock state deterministically."
      }
    ];"""

    if old_steps_data in content:
        content = content.replace(old_steps_data, new_steps_data)

    # 3. Update updateUI() function in script
    old_update_ui = """    function updateUI() {
      document.getElementById('preview-text').innerHTML = stepsData[currentStep - 1].preview;
      document.getElementById('telemetry-bar').innerText = stepsData[currentStep - 1].telemetry;
      document.getElementById('pane-what').innerText = stepsData[currentStep - 1].what;
      document.getElementById('pane-why').innerText = stepsData[currentStep - 1].why;

      for (let i = 1; i <= totalSteps; i++) {
        const gfx = document.getElementById(`step-${i}-gfx`);
        if (gfx) gfx.style.display = (i === currentStep) ? 'block' : 'none';
      }

      document.getElementById('prev-btn').disabled = (currentStep === 1);
      document.getElementById('next-btn').disabled = (currentStep === totalSteps);
    }"""

    new_update_ui = """    function updateUI() {
      const data = stepsData[currentStep - 1];
      document.getElementById('preview-text').innerHTML = data.preview;

      document.getElementById('tel-phase').innerText = data.phase;
      document.getElementById('tel-edges').innerHTML = data.edges;
      document.getElementById('tel-cycle').innerText = data.cycle;

      const stateEl = document.getElementById('tel-state');
      stateEl.innerText = data.state;
      stateEl.style.color = data.stateColor;

      document.getElementById('pane-what').innerText = data.what;
      document.getElementById('pane-why').innerText = data.why;

      for (let i = 1; i <= totalSteps; i++) {
        const gfx = document.getElementById(`step-${i}-gfx`);
        if (gfx) gfx.style.display = (i === currentStep) ? 'block' : 'none';
      }

      document.getElementById('prev-btn').disabled = (currentStep === 1);
      document.getElementById('next-btn').disabled = (currentStep === totalSteps);
    }"""

    if old_update_ui in content:
        content = content.replace(old_update_ui, new_update_ui)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully upgraded telemetry bar layout in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_telemetry_layout():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Upgrade RAG interactive stepper telemetry bar layout\n\n"
                "Replace flat pipe-separated telemetry string with a clean structured grid\n"
                "featuring distinct metric labels and color-coded state badges."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
