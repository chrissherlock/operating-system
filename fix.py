#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 3 of 03-disk-hardware-scheduling.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "03-disk-hardware-scheduling.html"
)

EXPANDED_SECTION_THREE_PRE_AID = r"""    <h3>3. Disk Arm Scheduling Algorithms</h3>
    <p>
      In a multiprogramming operating system, dozens of processes issue concurrent reads and writes to storage. Because mechanical seek time and rotational delay dwarf electronic transfer speeds by over 500 to 1, the order in which pending disk requests are serviced directly dictates overall system throughput and interactive responsiveness.
    </p>
    <p>
      When an application issues a file read, the operating system block layer enqueues the request into a kernel dispatch queue. The <strong>Disk Arm Scheduler</strong> (or I/O elevator) reorders, merges, and dispatches pending requests to optimize physical head trajectory.
    </p>

    <!-- Structural Diagram: Trajectory Profiles across Schedulers -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.3: Trajectory Comparison Across Classical Disk Scheduling Policies</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Spatial head paths across cylinders 0 to 199 starting from cylinder 53 with pending queue [98, 183, 37, 122, 14, 124, 65, 67].</div>

      <svg viewBox="0 0 760 280" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="sched-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="sched-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Column 1: FCFS Thrashing -->
        <g transform="translate(15, 20)">
          <rect width="170" height="240" rx="6" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
          <text x="85" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">1. FCFS (FIFO)</text>
          <text x="85" y="38" text-anchor="middle" font-size="7" fill="#dc2626">Movement: 640 Cylinders</text>

          <!-- Graph axis: X is cylinder 0..199 (140px width), Y is sequence step down -->
          <g transform="translate(15, 50)">
            <line x1="0" y1="0" x2="140" y2="0" stroke="#cbd5e1" stroke-width="1"/>
            <text x="0" y="-4" font-size="6" font-family="var(--font-mono)" fill="#64748b">0</text>
            <text x="140" y="-4" text-anchor="end" font-size="6" font-family="var(--font-mono)" fill="#64748b">199</text>

            <!-- Path: 53 -> 98 -> 183 -> 37 -> 122 -> 14 -> 124 -> 65 -> 67 -->
            <polyline points="37,0 69,18 129,36 26,54 86,72 10,90 87,108 46,126 47,144"
                      fill="none" stroke="#dc2626" stroke-width="1.5" stroke-linejoin="round"/>
            <circle cx="37" cy="0" r="3" fill="#0f172a"/>
            <circle cx="47" cy="144" r="3" fill="#dc2626"/>
          </g>
          <text x="85" y="218" text-anchor="middle" font-size="6.5" fill="#7f1d1d">Wild full-stroke thrashing</text>
          <text x="85" y="230" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">Slowest Throughput</text>
        </g>

        <!-- Column 2: SSTF Greedy -->
        <g transform="translate(195, 20)">
          <rect width="170" height="240" rx="6" fill="#f8fafc" stroke="#d97706" stroke-width="1.5"/>
          <text x="85" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#92400e">2. SSTF (GREEDY)</text>
          <text x="85" y="38" text-anchor="middle" font-size="7" fill="#b45309">Movement: 236 Cylinders</text>

          <g transform="translate(15, 50)">
            <line x1="0" y1="0" x2="140" y2="0" stroke="#cbd5e1" stroke-width="1"/>
            <text x="0" y="-4" font-size="6" font-family="var(--font-mono)" fill="#64748b">0</text>
            <text x="140" y="-4" text-anchor="end" font-size="6" font-family="var(--font-mono)" fill="#64748b">199</text>

            <!-- Path: 53 -> 65 -> 67 -> 37 -> 14 -> 98 -> 122 -> 124 -> 183 -->
            <polyline points="37,0 46,18 47,36 26,54 10,72 69,90 86,108 87,126 129,144"
                      fill="none" stroke="#d97706" stroke-width="1.5" stroke-linejoin="round"/>
            <circle cx="37" cy="0" r="3" fill="#0f172a"/>
            <circle cx="129" cy="144" r="3" fill="#d97706"/>
          </g>
          <text x="85" y="218" text-anchor="middle" font-size="6.5" fill="#92400e">Trapped in local cluster</text>
          <text x="85" y="230" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">Outer Starvation Hazard</text>
        </g>

        <!-- Column 3: SCAN Elevator -->
        <g transform="translate(375, 20)">
          <rect width="175" height="240" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="87" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#0369a1">3. SCAN (ELEVATOR)</text>
          <text x="87" y="38" text-anchor="middle" font-size="7" fill="#0284c7">Movement: 208 Cylinders</text>

          <g transform="translate(15, 50)">
            <line x1="0" y1="0" x2="140" y2="0" stroke="#cbd5e1" stroke-width="1"/>
            <text x="0" y="-4" font-size="6" font-family="var(--font-mono)" fill="#64748b">0</text>
            <text x="140" y="-4" text-anchor="end" font-size="6" font-family="var(--font-mono)" fill="#64748b">199</text>

            <!-- Path: 53 -> 65 -> 67 -> 98 -> 122 -> 124 -> 183 -> [199] -> 37 -> 14 -->
            <polyline points="37,0 46,16 47,32 69,48 86,64 87,80 129,96 140,112 26,128 10,144"
                      fill="none" stroke="#0284c7" stroke-width="1.5" stroke-linejoin="round"/>
            <circle cx="37" cy="0" r="3" fill="#0f172a"/>
            <circle cx="10" cy="144" r="3" fill="#0284c7"/>
          </g>
          <text x="87" y="218" text-anchor="middle" font-size="6.5" fill="#0369a1">Sweeps to edge; reverses</text>
          <text x="87" y="230" text-anchor="middle" font-size="6.5" font-weight="700" fill="#059669">Zero Starvation</text>
        </g>

        <!-- Column 4: C-LOOK Optimized -->
        <g transform="translate(560, 20)">
          <rect width="185" height="240" rx="6" fill="#f8fafc" stroke="#16a34a" stroke-width="2"/>
          <text x="92" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#166534">4. C-LOOK (CIRCULAR)</text>
          <text x="92" y="38" text-anchor="middle" font-size="7" fill="#166534">Movement: 322 Cylinders</text>

          <g transform="translate(15, 50)">
            <line x1="0" y1="0" x2="140" y2="0" stroke="#cbd5e1" stroke-width="1"/>
            <text x="0" y="-4" font-size="6" font-family="var(--font-mono)" fill="#64748b">0</text>
            <text x="140" y="-4" text-anchor="end" font-size="6" font-family="var(--font-mono)" fill="#64748b">199</text>

            <!-- Path: 53 -> 65 -> 67 -> 98 -> 122 -> 124 -> 183 -> [Jump to 14] -> 37 -->
            <polyline points="37,0 46,18 47,36 69,54 86,72 87,90 129,108 10,126 26,144"
                      fill="none" stroke="#16a34a" stroke-width="1.5" stroke-linejoin="round"/>
            <!-- Jump line dashed -->
            <line x1="129" y1="108" x2="10" y2="126" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3"/>
            <circle cx="37" cy="0" r="3" fill="#0f172a"/>
            <circle cx="26" cy="144" r="3" fill="#16a34a"/>
          </g>
          <text x="92" y="218" text-anchor="middle" font-size="6.5" fill="#166534">Bounded to active requests</text>
          <text x="92" y="230" text-anchor="middle" font-size="6.5" font-weight="700" fill="#166534">Uniform Wait Distribution</text>
        </g>
      </svg>
    </div>

    <h4>The Dual Mandate of the Disk Arm Scheduler</h4>
    <p>
      An effective disk scheduler must balance two fundamentally competing objectives:
    </p>
    <ol>
      <li>
        <strong>Throughput Maximization:</strong> Squeezing the maximum number of megabytes per second out of the physical platters. This requires minimizing aggregate seek distance and reducing the frequency of head turnaround reversals:
        <div class="math-callout" style="text-align: center;">
          Total Seek Cost = &sum;<sub><i>i</i>=1</sub><sup><i>K</i></sup> | Cylinder<sub><i>i</i></sub> - Cylinder<sub><i>i</i>-1</sub> |
        </div>
      </li>
      <li>
        <strong>Fairness &amp; Bounded Latency:</strong> Ensuring that no single I/O request starves in the queue indefinitely while the arm services requests closer to the active cylinder cluster.
      </li>
    </ol>

    <div class="math-callout">
      <strong>Request Merging: Optimization Before Scheduling:</strong>
      <br>
      Before any arm movement algorithm evaluates pending requests, the operating system block layer executes <strong>Request Merging</strong>:
      <ul>
        <li><strong>Back Merging:</strong> If a newly enqueued request addresses Sector 104, and an existing pending request addresses Sectors 100&ndash;103, the kernel merges them into a single contiguous request spanning Sectors 100&ndash;104.</li>
        <li><strong>Front Merging:</strong> Merging a new request directly ahead of an existing request on the identical track.</li>
      </ul>
      Merging eliminates physical seek operations entirely by converting multiple small random I/O operations into a single continuous streaming burst!
    </div>

    <h4>Detailed Algorithmic Analysis</h4>

    <h5>1. First-Come, First-Served (FCFS)</h5>
    <p>
      The baseline scheduling policy services requests strictly in the chronological order of their arrival into the queue:
    </p>
    <ul>
      <li><strong>Advantages:</strong> Completely fair; zero starvation; trivial <i>O</i>(1) FIFO queue implementation.</li>
      <li>
        <strong>The Defect &mdash; Wild Head Thrashing:</strong> FCFS pays zero attention to spatial locality. If Process A requests an inner cylinder (Cylinder 14) and Process B requests an outer cylinder (Cylinder 183), the arm thrashes back and forth across the entire platter width.
        <br>
        On our classical benchmark workload, FCFS generates <strong>640 cylinders of head movement</strong>, operating at less than one-third the throughput of an elevator scheduler.
      </li>
    </ul>

    <h5>2. Shortest Seek Time First (SSTF)</h5>
    <p>
      SSTF applies a greedy heuristic: among all pending requests in the queue, it selects the request that requires the <strong>minimum physical seek distance from the current head position</strong>:
    </p>
    <div class="math-callout" style="text-align: center;">
      Next Target = argmin<sub><i>r</i> &isin; <i>Q</i></sub> | Head<sub>current</sub> - Cylinder<sub><i>r</i></sub> |
    </div>
    <ul>
      <li><strong>Performance:</strong> Slashes head travel from 640 cylinders down to <strong>236 cylinders</strong>, dramatically increasing throughput under low-to-medium loads.</li>
      <li>
        <strong>The Fatal Flaw &mdash; Pathological Starvation:</strong>
        Because SSTF is greedy, it favors requests clustered near the current cylinder. If an application continuously generates requests around Cylinders 50&ndash;70, the head lingers in that cluster indefinitely.
        <br>
        A request pending on Cylinder 183 will <strong>starve forever</strong> as long as new requests arrive in the local neighborhood! For this reason, pure SSTF is never deployed in general-purpose production operating systems.
      </li>
    </ul>

    <h5>3. SCAN (The Elevator Algorithm)</h5>
    <p>
      To eliminate starvation while preserving spatial locality, the <strong>SCAN algorithm</strong> mimics a commercial building elevator:
    </p>
    <ul>
      <li>The arm maintains a directional vector (e.g. <em>Moving Outward toward Cylinder 199</em>).</li>
      <li>The head sweeps continuously in that direction, servicing all pending requests encountered along its path.</li>
      <li>When the arm reaches the extreme cylinder of the disk (Cylinder 199), the arm <strong>reverses direction</strong> and begins sweeping inward toward Cylinder 0, servicing requests in reverse.</li>
      <li><strong>Starvation Bound:</strong> A request is guaranteed to be serviced in <strong>at most two full sweeps</strong> of the platter radius, permanently eliminating starvation.</li>
      <li>
        <strong>The SCAN Defect &mdash; Non-Uniform Waiting Distribution:</strong>
        SCAN suffers from an asymmetric waiting time distribution. When the arm passes Cylinder 50 heading right, the area directly behind it (Cylinders 0&ndash;49) has just been cleared of requests.
        <br>
        A new request arriving at Cylinder 48 must wait for the arm to travel all the way to 199, reverse, and sweep back down to 48&mdash;a wait of nearly two full disk strokes! In contrast, requests ahead of the advancing arm experience negligible wait times.
      </li>
    </ul>

    <h5>4. C-SCAN (Circular SCAN)</h5>
    <p>
      C-SCAN corrects the non-uniform wait distribution of SCAN by restricting servicing to a <strong>single sweep direction</strong>:
    </p>
    <ul>
      <li>The arm sweeps in one direction only (e.g. from lowest cylinder toward highest cylinder), servicing requests along the way.</li>
      <li>Upon reaching the outer extreme (Cylinder 199), the arm <strong>immediately performs a high-speed return jump back to Cylinder 0 without servicing any requests on the return journey</strong>!</li>
      <li>Once reset to Cylinder 0, it resumes its forward sweep.</li>
      <li><strong>Mathematical Fairness:</strong> By treating the cylinders as a circular ring, C-SCAN provides a mathematically <strong>uniform average waiting time</strong> for all cylinders across the platter surface.</li>
    </ul>

    <h5>5. LOOK and C-LOOK (Industrial Optimizations)</h5>
    <p>
      Standard SCAN and C-SCAN waste significant mechanical travel by driving the arm all the way to the absolute physical edge of the disk (Cylinder 0 and Cylinder 199) even when no requests are pending at those extreme boundaries.
    </p>
    <p>
      <strong>LOOK</strong> and <strong>C-LOOK</strong> add a forward-inspection lookahead:
    </p>
    <ul>
      <li>The arm advances in its current direction only as far as the <strong>highest pending request in the queue</strong>.</li>
      <li>In our benchmark workload, the highest pending request is <strong>Cylinder 183</strong>. LOOK reverses immediately at 183; it never wastes mechanical motion traveling to the unused Cylinder 199.</li>
      <li>Similarly, C-LOOK executes its circular return jump immediately upon completing Cylinder 183, jumping directly to the lowest pending request (<strong>Cylinder 14</strong>) rather than Cylinder 0.</li>
      <li>C-LOOK is the universal gold standard for rotational mechanical arm scheduling in production systems.</li>
    </ul>

    <h4>Modern Operating System Scheduling Architectures</h4>
    <p>
      In modern Linux and Windows kernels, disk scheduling has moved beyond pure geometric heuristics to address quality-of-service and hardware-offloaded queues:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Deadline Scheduler -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">1. The Linux Deadline Scheduler</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Separates requests into multiple queues:
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Sorted Elevator Queue:</strong> Standard C-LOOK ordering to maximize throughput.</li>
            <li><strong>Read FIFO Queue:</strong> Hard expiration deadline of <strong>500 ms</strong>.</li>
            <li><strong>Write FIFO Queue:</strong> Relaxed expiration deadline of <strong>5000 ms (5 s)</strong>.</li>
          </ul>
          <em>Why Prioritize Reads?</em> Applications issuing reads typically block until data is returned. Writes are buffered asynchronously in the page cache. If a read request approaches its 500 ms deadline, the scheduler aborts elevator ordering and services the read immediately!
        </p>
      </div>

      <!-- NCQ Hardware Queuing -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">2. Native Command Queuing (NCQ)</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Modern SATA and SAS drives implement hardware-side scheduling:
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>The host OS dispatches up to <strong>32 commands simultaneously</strong> (or 256 in SCSI TCQ) into the drive controller's internal queue.</li>
            <li>The on-drive microprocessor knows the <em>exact real-time angular position</em> of the spinning platters (which the host OS cannot know due to PCIe bus latency).</li>
            <li>The drive controller executes <strong>Rotational Position Sorting (RPS)</strong>, dynamically choosing the request that minimizes the sum of seek time <em>plus</em> immediate rotational delay!</li>
          </ul>
        </p>
      </div>
    </div>"""

def update_section_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Disk Arm Scheduling Algorithms</h3>"
    end_marker = "<!-- Directed Narrative Stepper: Disk Arm Scheduling Arena -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 boundaries before the interactive stepper.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_THREE_PRE_AID + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 3 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 3 of Module 03 on Disk Arm Scheduling Algorithms\n\n"
            "Detail FCFS thrashing, SSTF starvation, SCAN vs C-SCAN uniform wait math,\n"
            "LOOK/C-LOOK optimizations, NCQ hardware queues, and add an SVG comparison."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_three():
        run_git_sync()
