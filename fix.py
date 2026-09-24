#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct arrows, marker orientation, and alignment in Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "02-batch-scheduling.html")

def adjust_gantt_arrows_and_lines():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix SVG defs inside 02-batch-scheduling.html
    # Replace the defs block to ensure standard horizontal right-pointing markers
    old_defs_start = '<defs>'
    old_defs_end = '</defs>'

    canvas_pos = content.find('<svg class="gantt-canvas"')
    defs_start = content.find(old_defs_start, canvas_pos)
    defs_end = content.find(old_defs_end, defs_start) + len(old_defs_end)

    clean_defs = r"""<defs>
            <pattern id="wait-stripe" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <line x1="0" y1="0" x2="0" y2="8" stroke="#fcd34d" stroke-width="4" />
              <line x1="4" y1="0" x2="4" y2="8" stroke="#fef3c7" stroke-width="4" />
            </pattern>
            <!-- Standard horizontal right-pointing markers (orient="auto" handles vertical lines perfectly) -->
            <marker id="arr-arrival-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#d97706" />
            </marker>
            <marker id="arr-arrival-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
            </marker>
            <marker id="arr-arrival-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
            </marker>
          </defs>"""

    content = content[:defs_start] + clean_defs + content[defs_end:]

    # 2. Update JavaScript step renderers to use the corrected markers and exact coordinates
    new_script = r"""  <script>
    const batchSteps = {
      fcfs: [
        {
          time: "T = 0 ms",
          active: "Process A (Burst: 24 ms)",
          queue: "Empty (No arrivals)",
          wait: "0.0 ms (A running)",
          showQueueB: false,
          showQueueC: false,
          showQueueA: false,
          cpuBars: `
            <!-- T=0 to T=2 is 30px (x=15 to 45) -->
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="30" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">A</text>
          `,
          waitBars: `
            <text x="25" y="152" font-size="9" fill="#94a3b8">Ready queue empty (No waiting tasks)</text>
          `,
          narrative: "Process A arrives at T=0 with a 24ms burst requirement. The CPU starts executing Process A. The Ready queue is currently empty.",
          what: "Process A enters the CPU core at T=0. Because no other jobs exist, Process A is granted immediate execution.",
          why: "The operating system maximizes hardware utilization by never letting an execution core sit idle when runnable work is present."
        },
        {
          time: "T = 2 ms",
          active: "Process A (Running: 22ms left)",
          queue: "Proc B (Arrived T=2 | Trapped)",
          wait: "Proc B accumulating wait!",
          showQueueB: true,
          showQueueC: false,
          showQueueA: false,
          bTimer: "Wait: 0ms (Just arrived)",
          cpuBars: `
            <!-- Process A active from T=0 past T=2 (30px = 2ms) -->
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="30" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">A</text>
            <path d="M 45 76 L 75 76" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="2 2"/>
            <text x="82" y="80" font-size="9" font-weight="600" fill="#dc2626">A continues running...</text>
          `,
          waitBars: `
            <!-- Process B Arrival Arrow at exact T=2 mark (x=45) pointing directly down into wait box -->
            <line x1="45" y1="102" x2="45" y2="126" stroke="#d97706" stroke-width="2" marker-end="url(#arr-arrival-amber)"/>
            <text x="45" y="98" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#d97706">B Arrives</text>

            <!-- Process B wait bar starting at T=2 (x=45) -->
            <rect x="45" y="132" width="60" height="34" rx="3" fill="url(#wait-stripe)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="75" y="153" text-anchor="middle" font-size="8.5" font-weight="700" fill="#b45309">B Trapped</text>
          `,
          narrative: "Process B (burst: 3ms) arrives at T=2. Notice the downward arrival arrow at T=2: under non-preemptive FCFS, Process A cannot be interrupted. Process B is trapped in the Ready queue.",
          what: "Process B enters the Ready queue at T=2. Even though Process B requires only 3ms of computation, it cannot preempt Process A and begins accumulating waiting time.",
          why: "Non-preemptive FCFS adheres strictly to FIFO arrival order without inspecting burst length; running tasks own the processor until voluntary yield or termination."
        },
        {
          time: "T = 4 ms",
          active: "Process A (Running: 20ms left)",
          queue: "Proc B &amp; Proc C (Trapped)",
          wait: "B waited 2ms, C arrived",
          showQueueB: true,
          showQueueC: true,
          showQueueA: false,
          bTimer: "Wait: 2ms in queue",
          cTimer: "Wait: 0ms (Just arrived)",
          cpuBars: `
            <!-- Process A active from T=0 past T=4 (x=15 to 75 = 60px) -->
            <rect x="15" y="55" width="60" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="45" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">A (Locked)</text>
            <path d="M 75 76 L 110 76" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="2 2"/>
            <text x="118" y="80" font-size="9" font-weight="600" fill="#dc2626">A runs to T=24...</text>
          `,
          waitBars: `
            <!-- Process B Arrival at T=2 (x=45) -->
            <line x1="45" y1="102" x2="45" y2="126" stroke="#d97706" stroke-width="1.5" marker-end="url(#arr-arrival-amber)"/>
            <text x="45" y="98" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#d97706">B (T=2)</text>
            <rect x="45" y="132" width="60" height="34" rx="3" fill="url(#wait-stripe)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="75" y="153" text-anchor="middle" font-size="8.5" font-weight="700" fill="#b45309">B Waiting</text>

            <!-- Process C Arrival at T=4 (x=75) -->
            <line x1="75" y1="102" x2="75" y2="126" stroke="#0284c7" stroke-width="2" marker-end="url(#arr-arrival-blue)"/>
            <text x="75" y="98" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#0284c7">C Arrives</text>
            <rect x="110" y="132" width="60" height="34" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
            <text x="140" y="153" text-anchor="middle" font-size="8" font-weight="700" fill="#0369a1">C Queued</text>
          `,
          narrative: "Process C (burst: 3ms) arrives at T=4. Both Process B and Process C are now stalled in the Ready queue behind Process A. This is the Convoy Effect.",
          what: "Two fast tasks (B and C) are trapped. Meanwhile, disk and network controllers sit completely idle waiting for B and C to run.",
          why: "FCFS ignores task size, severely damaging average turnaround time and degrading peripheral device utilization."
        },
        {
          time: "T = 24 ms",
          active: "Process B (Finally Dispatched)",
          queue: "Proc C (Waited 20ms!)",
          wait: "B waited 22ms for 3ms job",
          showQueueB: false,
          showQueueC: true,
          showQueueA: false,
          cTimer: "Wait: 20ms in queue",
          cpuBars: `
            <!-- Process A finished at T=24 (x=375) -->
            <rect x="15" y="55" width="360" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="195" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">Process A Finished (0-24ms)</text>
            <!-- Process B running from T=24 to 27 (x=375 to 420) -->
            <rect x="375" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="2"/>
            <text x="397" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B</text>
          `,
          waitBars: `
            <rect x="45" y="132" width="330" height="34" rx="3" fill="url(#wait-stripe)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="210" y="153" text-anchor="middle" font-size="8.5" font-weight="700" fill="#b45309">Proc B Total Queue Wait: 22 ms (T=2 to T=24)</text>
          `,
          narrative: "Process A finally completes at T=24. Process B is dispatched after an agonizing 22ms wait for a 3ms task. Process C has already waited 20ms and continues waiting.",
          what: "Process A terminates. The dispatcher switches to Process B. Process B's slowdown ratio is W = 25 / 3 = 8.3x.",
          why: "FCFS guarantees no starvation, but inflicts enormous queue delays on short tasks trapped behind large jobs."
        },
        {
          time: "T = 30 ms",
          active: "All Workloads Finished",
          queue: "Empty",
          wait: "Avg Turnaround: 25.0 ms",
          showQueueB: false,
          showQueueC: false,
          showQueueA: false,
          cpuBars: `
            <rect x="15" y="55" width="360" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="195" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">Process A (0-24ms)</text>
            <rect x="375" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="1.5"/>
            <text x="397" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B</text>
            <rect x="420" y="55" width="45" height="42" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="2"/>
            <text x="442" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#0369a1">C</text>
          `,
          waitBars: `
            <text x="25" y="152" font-size="9" font-weight="700" fill="#475569">Total Waits: A = 0ms | B = 22ms | C = 23ms (Average Wait: 15.0ms)</text>
          `,
          narrative: "All jobs finish by T=30. Average Turnaround Time = (24 + 25 + 26) / 3 = 25.0 ms. Average Waiting Time = (0 + 22 + 23) / 3 = 15.0 ms.",
          what: "Batch completes. Notice how the convoy effect created an asymmetric waiting distribution.",
          why: "Observing this structural flaw explains why operating systems developed preemptive Shortest Remaining Time Next."
        }
      ],
      srtn: [
        {
          time: "T = 0 ms",
          active: "Process A (Burst: 24 ms)",
          queue: "Empty",
          wait: "0.0 ms (A running)",
          showQueueB: false,
          showQueueC: false,
          showQueueA: false,
          cpuBars: `
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="30" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">A</text>
          `,
          waitBars: `
            <text x="25" y="152" font-size="9" fill="#94a3b8">Ready queue empty</text>
          `,
          narrative: "Process A arrives at T=0 with a 24ms burst requirement. The CPU starts executing Process A. Remaining time: 24ms.",
          what: "Process A runs on the core. No other tasks exist in the system.",
          why: "The CPU immediately services available tasks to eliminate idle execution cycles."
        },
        {
          time: "T = 2 ms",
          active: "Process B PREEMPTS Process A!",
          queue: "Proc A (Preempted: 22ms)",
          wait: "0.0 ms (B runs immediately!)",
          showQueueB: false,
          showQueueC: false,
          showQueueA: true,
          cpuBars: `
            <!-- Process A ran 0 to 2ms (x=15 to 45) -->
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="30" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">A</text>
            <!-- Process B preempts and runs at T=2 (x=45 to 90) -->
            <rect x="45" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="2.5"/>
            <text x="67" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B (Run)</text>
          `,
          waitBars: `
            <!-- Process B Arrival Arrow at T=2 (x=45) pointing down to B's start -->
            <line x1="45" y1="102" x2="45" y2="126" stroke="#059669" stroke-width="2" marker-end="url(#arr-arrival-green)"/>
            <text x="45" y="98" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#059669">B Arrives</text>
            <!-- Preempted A waiting in Ready queue -->
            <rect x="45" y="132" width="160" height="34" rx="3" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3 3"/>
            <text x="125" y="153" text-anchor="middle" font-size="8.5" font-weight="700" fill="#dc2626">Proc A Preempted (22ms left)</text>
          `,
          narrative: "Process B (3ms) arrives at T=2. SRTN compares B's requirement (3ms) against A's remaining time (22ms). Since 3ms &lt; 22ms, Process A is PREEMPTED immediately! Process B runs with ZERO wait time.",
          what: "The kernel forcibly suspends Process A, saves its registers to its trap frame, moves A to the Ready queue, and dispatches Process B.",
          why: "SRTN prioritizes jobs with the shortest remaining execution requirement, eliminating the convoy effect."
        },
        {
          time: "T = 4 ms",
          active: "Process B (1ms left)",
          queue: "Proc C (3ms), Proc A (22ms)",
          wait: "C queued; B finishing",
          showQueueB: false,
          showQueueC: true,
          showQueueA: true,
          cTimer: "Wait: 0ms (3ms burst)",
          cpuBars: `
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="30" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">A</text>
            <rect x="45" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="2"/>
            <text x="67" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B</text>
          `,
          waitBars: `
            <!-- Process C Arrival Arrow at T=4 (x=75) -->
            <line x1="75" y1="102" x2="75" y2="126" stroke="#0284c7" stroke-width="2" marker-end="url(#arr-arrival-blue)"/>
            <text x="75" y="98" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#0284c7">C Arrives</text>
            <rect x="95" y="132" width="65" height="34" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
            <text x="127" y="153" text-anchor="middle" font-size="8" font-weight="700" fill="#0369a1">C Queued</text>
          `,
          narrative: "Process C (3ms) arrives at T=4. The scheduler compares C (3ms) with running B (1ms remaining). 1ms &lt; 3ms, so Process B continues uninterrupted.",
          what: "Process B retains the core. Process C is placed ahead of Process A in the Ready queue because 3ms &lt; 22ms.",
          why: "The currently executing task has shorter remaining time than the new arrival, so preemption is unnecessary."
        },
        {
          time: "T = 5 ms",
          active: "Process C (Dispatched)",
          queue: "Proc A (22ms remaining)",
          wait: "C waited only 1ms!",
          showQueueB: false,
          showQueueC: false,
          showQueueA: true,
          cpuBars: `
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="30" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">A</text>
            <rect x="45" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="1.5"/>
            <text x="67" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B</text>
            <rect x="90" y="55" width="45" height="42" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="2"/>
            <text x="112" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#0369a1">C</text>
          `,
          waitBars: `
            <text x="25" y="152" font-size="8.5" font-weight="600" fill="#059669">Proc B finished at T=5 (Turnaround = 3ms, W = 1.0x)</text>
          `,
          narrative: "Process B completes at T=5. Process C (3ms) is selected over Process A (22ms). Process C executes from T=5 to T=8.",
          what: "Process B finishes with a turnaround time of 5 - 2 = 3ms (optimal!). Process C starts running after waiting only 1ms.",
          why: "SRTN clears short tasks out of the system rapidly, freeing up memory and allowing short jobs to start I/O operations."
        },
        {
          time: "T = 30 ms",
          active: "All Workloads Finished",
          queue: "Empty",
          wait: "Avg Turnaround: 12.33 ms!",
          showQueueB: false,
          showQueueC: false,
          showQueueA: false,
          cpuBars: `
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="30" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">A</text>
            <rect x="45" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="1.5"/>
            <text x="67" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B</text>
            <rect x="90" y="55" width="45" height="42" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5"/>
            <text x="112" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#0369a1">C</text>
            <rect x="135" y="55" width="330" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="300" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">Process A Resumed &amp; Finished (8-30ms)</text>
          `,
          waitBars: `
            <text x="25" y="152" font-size="8.5" font-weight="700" fill="#059669">Turnaround: A = 30ms | B = 3ms | C = 4ms (Average: 12.33 ms)</text>
          `,
          narrative: "Process C completes at T=8. Process A resumes and finishes at T=30. Average Turnaround = (30 + 3 + 4) / 3 = 12.33 ms (vs. 25.0 ms under FCFS).",
          what: "Workload finishes. Average waiting time dropped from 15.0 ms under FCFS to only 2.33 ms under SRTN.",
          why: "Preemptive SRTN prevents short tasks from being penalized by long jobs, maximizing batch throughput."
        }
      ]
    };

    let activeBatchDim = "fcfs";
    let activeBatchStep = 0;

    function renderBatchStepper() {
      const steps = batchSteps[activeBatchDim];
      const step = steps[activeBatchStep];

      // Update Live Telemetry
      document.getElementById("b-telem-time").textContent = step.time;
      document.getElementById("b-telem-active").textContent = step.active;
      document.getElementById("b-telem-queue").textContent = step.queue;
      document.getElementById("b-telem-wait").textContent = step.wait;

      // Update Queue Cards
      const cardB = document.getElementById("card-queue-b");
      const cardC = document.getElementById("card-queue-c");
      const cardA = document.getElementById("card-queue-a");
      const queueEmpty = document.getElementById("txt-queue-empty");

      cardB.style.display = step.showQueueB ? "block" : "none";
      cardC.style.display = step.showQueueC ? "block" : "none";
      cardA.style.display = step.showQueueA ? "block" : "none";

      if (step.bTimer && document.getElementById("txt-queue-b-timer")) {
        document.getElementById("txt-queue-b-timer").textContent = step.bTimer;
      }
      if (step.cTimer && document.getElementById("txt-queue-c-timer")) {
        document.getElementById("txt-queue-c-timer").textContent = step.cTimer;
      }

      queueEmpty.style.display = (!step.showQueueB && !step.showQueueC && !step.showQueueA) ? "block" : "none";

      // Update Gantt Tracks
      document.getElementById("gantt-cpu-bars").innerHTML = step.cpuBars;
      document.getElementById("gantt-wait-bars").innerHTML = step.waitBars;

      // Update Narrative Panel
      document.getElementById("b-txt-narrative").innerHTML = step.narrative;
      document.getElementById("b-btn-prev").disabled = (activeBatchStep === 0);
      document.getElementById("b-btn-next").disabled = (activeBatchStep === steps.length - 1);

      // Update Analytical Panes
      document.getElementById("b-txt-what").innerHTML = step.what;
      document.getElementById("b-txt-why").innerHTML = step.why;
    }

    function stepBatch(delta) {
      const steps = batchSteps[activeBatchDim];
      activeBatchStep = Math.max(0, Math.min(steps.length - 1, activeBatchStep + delta));
      renderBatchStepper();
    }

    function resetBatch() {
      activeBatchStep = 0;
      renderBatchStepper();
    }

    function setBatchDim(dim) {
      activeBatchDim = dim;
      activeBatchStep = 0;
      document.getElementById("dim-fcfs").classList.toggle("active", dim === "fcfs");
      document.getElementById("dim-srtn").classList.toggle("active", dim === "srtn");

      const scenarioText = dim === "fcfs"
        ? "Process A (24 ms burst) arrives at T=0. Process B (3 ms burst) arrives at T=2. Process C (3 ms burst) arrives at T=4. Observing how non-preemptive FCFS locks the CPU and traps incoming tasks in the Ready queue."
        : "Process A (24 ms burst) arrives at T=0. Process B (3 ms burst) arrives at T=2. Process C (3 ms burst) arrives at T=4. Observing how preemptive SRTN immediately interrupts Process A to achieve optimal turnaround times.";
      document.getElementById("batch-scenario-text").innerHTML = scenarioText;

      renderBatchStepper();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderBatchStepper();
    });
  </script>"""

    script_start = content.find("<script>")
    script_end = content.find("</script>") + 9
    if script_start != -1 and script_end != -1:
        content = content[:script_start] + new_script.strip() + content[script_end:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully aligned arrows and timeline ticks in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix arrival arrows and timeline alignment in Module 02 Gantt stepper\n\n"
            "Standardize marker definitions to horizontal base vectors with\n"
            "orient=\"auto\" and align arrival arrows directly with timeline ticks."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    adjust_gantt_arrows_and_lines()
