#!/usr/bin/env python3
# =====================================================================
# fix.py: Add visual arrival markers & wait track to Module 02 stepper
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "02-batch-scheduling.html")

def update_stepper_visuals():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the SVG and JS steps in 02-batch-scheduling.html
    # We will enhance the SVG canvas and the JS step definitions
    old_canvas_start = '<svg class="gantt-canvas" viewBox="0 0 760 220">'
    old_canvas_end = '</svg>\n      </div>'

    new_canvas = r"""<svg class="gantt-canvas" viewBox="0 0 760 260">
          <defs>
            <pattern id="wait-stripe" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <line x1="0" y1="0" x2="0" y2="8" stroke="#fcd34d" stroke-width="4" />
              <line x1="4" y1="0" x2="4" y2="8" stroke="#fef3c7" stroke-width="4" />
            </pattern>
            <marker id="arr-arrival" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 2 0 L 5 8 L 8 0 z" fill="#d97706" />
            </marker>
          </defs>

          <!-- Ready Queue Status Box (Left) -->
          <g transform="translate(15, 15)">
            <rect width="215" height="230" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="14" y="24" font-size="11" font-weight="700" fill="#0f172a">READY QUEUE (WAITING)</text>

            <!-- Proc B Queue Card -->
            <g id="card-queue-b" style="display: none;">
              <rect x="12" y="36" width="190" height="52" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="2"/>
              <text x="20" y="54" font-size="10" font-weight="700" fill="#b45309">Proc B (Burst: 3ms)</text>
              <text x="20" y="68" font-family="var(--font-mono)" font-size="9" fill="#d97706">Arrived T=2 | WAITING</text>
              <text id="txt-queue-b-timer" x="20" y="80" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">Wait: 0ms accumulating</text>
            </g>

            <!-- Proc C Queue Card -->
            <g id="card-queue-c" style="display: none;">
              <rect x="12" y="96" width="190" height="52" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
              <text x="20" y="114" font-size="10" font-weight="700" fill="#0369a1">Proc C (Burst: 3ms)</text>
              <text x="20" y="128" font-family="var(--font-mono)" font-size="9" fill="#0284c7">Arrived T=4 | WAITING</text>
              <text id="txt-queue-c-timer" x="20" y="140" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">Wait: 0ms accumulating</text>
            </g>

            <!-- Proc A (Preempted Card for SRTN) -->
            <g id="card-queue-a" style="display: none;">
              <rect x="12" y="156" width="190" height="52" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="2" stroke-dasharray="3 3"/>
              <text x="20" y="174" font-size="10" font-weight="700" fill="#b91c1c">Proc A (Preempted!)</text>
              <text x="20" y="188" font-family="var(--font-mono)" font-size="9" fill="#dc2626">Rem: 22ms | Queued</text>
              <text x="20" y="200" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">Waiting for CPU core</text>
            </g>

            <text id="txt-queue-empty" x="14" y="60" font-family="var(--font-mono)" font-size="9.5" fill="#94a3b8">Queue Empty (No waiters)</text>
          </g>

          <!-- Gantt Timeline & Arrival Arena (Right) -->
          <g transform="translate(245, 15)">
            <rect width="500" height="230" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="15" y="24" font-size="11" font-weight="700" fill="#0f172a">CPU EXECUTION &amp; ARRIVAL TIMELINE</text>

            <!-- Track 1: Active CPU Core Execution -->
            <text x="15" y="48" font-size="9.5" font-weight="700" fill="#475569">CPU CORE 0 (Running):</text>
            <rect x="15" y="55" width="470" height="42" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
            <g id="gantt-cpu-bars"></g>

            <!-- Track 2: Arrival & Waiting Queue Track -->
            <text x="15" y="122" font-size="9.5" font-weight="700" fill="#d97706">READY QUEUE ARRIVALS &amp; DELAYS:</text>
            <rect x="15" y="128" width="470" height="42" rx="4" fill="#fffbeb" stroke="#fef3c7"/>
            <g id="gantt-wait-bars"></g>

            <!-- Timeline Time Axis -->
            <line x1="15" y1="195" x2="485" y2="195" stroke="#94a3b8" stroke-width="2"/>
            <!-- Tick marks: Scale factor = 15px per ms, 0=15, 2=45, 4=75, 8=135, 24=375, 30=465 -->
            <line x1="15" y1="195" x2="15" y2="203" stroke="#475569" stroke-width="1.5"/>
            <text x="15" y="216" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#475569">T=0</text>

            <line x1="45" y1="195" x2="45" y2="203" stroke="#d97706" stroke-width="1.5"/>
            <text x="45" y="216" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#d97706">T=2</text>

            <line x1="75" y1="195" x2="75" y2="203" stroke="#0284c7" stroke-width="1.5"/>
            <text x="75" y="216" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#0284c7">T=4</text>

            <line x1="135" y1="195" x2="135" y2="203" stroke="#475569" stroke-width="1.5"/>
            <text x="135" y="216" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#475569">T=8</text>

            <line x1="375" y1="195" x2="375" y2="203" stroke="#475569" stroke-width="1.5"/>
            <text x="375" y="216" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#475569">T=24</text>

            <line x1="465" y1="195" x2="465" y2="203" stroke="#475569" stroke-width="1.5"/>
            <text x="465" y="216" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#475569">T=30</text>
          </g>
        </svg>"""

    c_start = content.find(old_canvas_start)
    c_end = content.find(old_canvas_end)
    if c_start != -1 and c_end != -1:
        content = content[:c_start] + new_canvas + content[c_end + len(old_canvas_end) - 12:]

    # Now replace the script block with enriched steps reflecting the visual arrival and wait tracks
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
            <rect x="15" y="55" width="40" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="35" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">A (0-2ms)</text>
          `,
          waitBars: `
            <text x="25" y="152" font-size="9" fill="#94a3b8">No tasks in Ready queue</text>
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
            <rect x="15" y="55" width="70" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="50" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">A (Monopolizing Core 0)</text>
          `,
          waitBars: `
            <!-- Process B Arrival Marker at T=2 (x=45) -->
            <path d="M 45 110 L 45 128" stroke="#d97706" stroke-width="2" marker-end="url(#arr-arrival)"/>
            <text x="45" y="105" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#d97706">&darr; B Arrives (3ms)</text>

            <rect x="45" y="132" width="40" height="34" rx="3" fill="url(#wait-stripe)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="65" y="153" text-anchor="middle" font-size="9" font-weight="700" fill="#b45309">B Trapped</text>
          `,
          narrative: "Process B (burst: 3ms) arrives at T=2. Notice the arrival marker &amp; striped amber wait bar: under non-preemptive FCFS, Process A cannot be interrupted. Process B is trapped in the Ready queue.",
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
            <rect x="15" y="55" width="105" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="67" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">Process A (Convoy Lock)</text>
          `,
          waitBars: `
            <!-- Process B Arrival at T=2 -->
            <text x="45" y="105" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#d97706">B (T=2)</text>
            <rect x="45" y="132" width="70" height="34" rx="3" fill="url(#wait-stripe)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="80" y="153" text-anchor="middle" font-size="8.5" font-weight="700" fill="#b45309">B Waiting...</text>

            <!-- Process C Arrival at T=4 (x=75) -->
            <path d="M 75 110 L 75 128" stroke="#0284c7" stroke-width="2" marker-end="url(#arr-arrival)"/>
            <text x="75" y="105" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#0284c7">&darr; C Arrives</text>
            <rect x="75" y="136" width="40" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
            <text x="95" y="153" text-anchor="middle" font-size="8" font-weight="700" fill="#0369a1">C Queued</text>
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
            <rect x="15" y="55" width="360" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="195" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">Process A Finished (0-24ms)</text>
            <rect x="375" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="2"/>
            <text x="397" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B</text>
          `,
          waitBars: `
            <rect x="45" y="132" width="330" height="34" rx="3" fill="url(#wait-stripe)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="210" y="153" text-anchor="middle" font-size="9" font-weight="700" fill="#b45309">Proc B Total Queue Wait: 22 ms! (T=2 to T=24)</text>
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
            <text x="25" y="152" font-size="9.5" font-weight="700" fill="#475569">Total Wait Times: A = 0ms | B = 22ms | C = 23ms (Average Wait: 15.0ms)</text>
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
            <rect x="15" y="55" width="30" height="42" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="30" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">A</text>
            <rect x="45" y="55" width="45" height="42" rx="3" fill="#f0fdf4" stroke="#059669" stroke-width="2.5"/>
            <text x="67" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B (RUNNING)</text>
          `,
          waitBars: `
            <path d="M 45 110 L 45 128" stroke="#059669" stroke-width="2" marker-end="url(#arr-arrival)"/>
            <text x="45" y="105" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#059669">&darr; B Arrives (3ms &lt; 22ms rem)</text>
            <rect x="45" y="132" width="150" height="34" rx="3" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3 3"/>
            <text x="120" y="153" text-anchor="middle" font-size="8.5" font-weight="700" fill="#dc2626">Proc A Preempted to Ready Queue</text>
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
            <path d="M 75 110 L 75 128" stroke="#0284c7" stroke-width="2" marker-end="url(#arr-arrival)"/>
            <text x="75" y="105" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#0284c7">&darr; C Arrives (3ms)</text>
            <rect x="75" y="132" width="15" height="34" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
            <text x="82" y="153" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0369a1">C</text>
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
            <text x="67" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">B (Fin)</text>
            <rect x="90" y="55" width="45" height="42" rx="3" fill="#f0f9ff" stroke="#0284c7" stroke-width="2"/>
            <text x="112" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#0369a1">C</text>
          `,
          waitBars: `
            <text x="25" y="152" font-size="9" font-weight="600" fill="#059669">Proc B finished at T=5 (Turnaround = 3ms, W = 1.0x!)</text>
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
            <text x="25" y="152" font-size="9.5" font-weight="700" fill="#059669">Turnaround Times: A = 30ms | B = 3ms | C = 4ms (Average Turnaround: 12.33 ms &mdash; 50%+ faster!)</text>
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
  </script>
"""

    script_start = content.find("<script>")
    script_end = content.find("</script>") + 9
    if script_start != -1 and script_end != -1:
        content = content[:script_start] + new_script.strip() + content[script_end:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully enhanced Gantt canvas and arrival tracking in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add arrival markers and waiting track to Gantt stepper in Module 02\n\n"
            "Render explicit arrival markers, accumulating wait duration bars, and\n"
            "highlighted Ready queue cards at T=2 and T=4 for trapped processes."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_stepper_visuals()
