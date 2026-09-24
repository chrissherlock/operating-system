#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 4 of 01-scheduling-introduction.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "01-scheduling-introduction.html")

def build_expanded_section_four():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_section_four = r"""    <h3>4. Conflicting Optimization Goals &amp; Metrics</h3>
    <p>
      An operating system scheduler operates in an environment of inherent physical constraints and mutually incompatible performance objectives. No single scheduling algorithm can simultaneously maximize raw hardware throughput, eliminate user latency, guarantee absolute fairness, and maintain zero scheduling overhead. Designing or selecting a scheduler requires understanding the formal mathematical metrics that quantify performance and the trade-offs that govern their optimization.
    </p>

    <h4>1. Formal Mathematical Scheduling Metrics</h4>
    <p>
      To evaluate and compare scheduling algorithms rigorously, operating system architects define precise timing invariants across the lifecycle of a process:
    </p>

    <ul>
      <li>
        <strong>Turnaround Time (<i>T</i><sub>turnaround</sub>):</strong>
        The total elapsed wall-clock duration from the instant a job is submitted or arrives in the Ready queue (<i>T</i><sub>arrival</sub>) to the exact instant it finishes execution (<i>T</i><sub>completion</sub>):
        <pre><code><i>T</i><sub>turnaround</sub> = <i>T</i><sub>completion</sub> &minus; <i>T</i><sub>arrival</sub></code></pre>
        Turnaround time represents the user's total elapsed waiting experience in batch environments. It comprises four distinct sub-components:
        <pre><code><i>T</i><sub>turnaround</sub> = <i>T</i><sub>exec</sub> + <i>T</i><sub>wait</sub> + <i>T</i><sub>io</sub> + <i>T</i><sub>dispatch</sub></code></pre>
        where <i>T</i><sub>exec</sub> is total CPU burst time, <i>T</i><sub>wait</sub> is cumulative time spent in the Ready queue, <i>T</i><sub>io</sub> is time spent blocked on peripheral devices, and <i>T</i><sub>dispatch</sub> is cumulative context-switch latency.
      </li>
      <li>
        <strong>Normalized Turnaround Time / Penalty Ratio (<i>W</i>):</strong>
        Absolute turnaround time is often deceptive because a 10-second turnaround is catastrophic for a job requiring only 1 millisecond of computation, but stellar for a batch simulation requiring 9 seconds. The normalized turnaround time (also called the <strong>slowdown</strong> or <strong>penalty ratio</strong>) measures the relative delay imposed by the operating system:
        <pre><code><i>W</i> = <i>T</i><sub>turnaround</sub> / <i>T</i><sub>exec</sub></code></pre>
        The minimum possible value is 1.0 (indicating the process ran with zero queue delays or context switches). Higher values indicate severe queuing congestion or scheduler starvation.
      </li>
      <li>
        <strong>Waiting Time (<i>T</i><sub>wait</sub>):</strong>
        The cumulative duration a process spends in the Ready queue waiting to be granted a CPU core. Unlike turnaround time, waiting time explicitly discounts time spent actively executing instructions or waiting for hardware I/O completion:
        <pre><code><i>T</i><sub>wait</sub> = <i>T</i><sub>turnaround</sub> &minus; <i>T</i><sub>exec</sub> &minus; <i>T</i><sub>io</sub></code></pre>
        In purely compute-bound workloads with zero I/O, this simplifies directly to:
        <pre><code><i>T</i><sub>wait</sub> = <i>T</i><sub>turnaround</sub> &minus; <i>T</i><sub>exec</sub></code></pre>
        A scheduler has no control over how long a program must calculate (<i>T</i><sub>exec</sub>) or how long a disk takes to spin (<i>T</i><sub>io</sub>); its sole mathematical objective when optimizing turnaround time is minimizing <i>T</i><sub>wait</sub>.
      </li>
      <li>
        <strong>Response Time (<i>T</i><sub>response</sub>):</strong>
        In interactive systems, the user does not wait for an entire program to complete before assessing responsiveness. <strong>Response time</strong> is the duration between a process entering the Ready queue (e.g., when a key is pressed or a packet arrives) and its very first dispatch onto a CPU core:
        <pre><code><i>T</i><sub>response</sub> = <i>T</i><sub>first_dispatch</sub> &minus; <i>T</i><sub>arrival</sub></code></pre>
        While turnaround time governs background batch efficiency, response time dictates the perceptible latency and tactile fluidity of user interfaces.
      </li>
      <li>
        <strong>System Throughput (<i>X</i>):</strong>
        The number of complete processes or tasks executed per unit time (e.g., jobs per second):
        <pre><code><i>X</i> = <i>N</i> / &Delta;<i>t</i></code></pre>
        Throughput depends heavily on average job length and context-switch frequency. If a scheduler spends too much time executing context switches, useful computational throughput drops.
      </li>
      <li>
        <strong>CPU Utilization (<i>U</i>):</strong>
        The fraction of total time the physical CPU execution units spend executing non-idle user instructions or productive kernel system calls:
        <pre><code><i>U</i> = (<i>T</i><sub>busy</sub> / <i>T</i><sub>total</sub>) &times; 100%</code></pre>
        In multi-programmed systems, CPU utilization increases with the degree of multiprogramming <i>n</i>. If the probability that any single process is waiting for I/O is <i>p</i>, the probability that all <i>n</i> processes are simultaneously idle is <i>p</i><sup><i>n</i></sup>, yielding theoretical processor utilization of:
        <pre><code><i>U</i> = 1 &minus; <i>p</i><sup><i>n</i></sup></code></pre>
      </li>
      <li>
        <strong>Fairness &amp; Predictability (Variance &amp; Jitter):</strong>
        A scheduler must guarantee comparable treatment for comparable workloads. Beyond average response time, interactive and real-time systems require minimal <strong>variance</strong> (&sigma;<sup>2</sup>). A system where response time fluctuates unpredictably between 10 ms and 2,000 ms feels broken to a human user and violates strict deadlines in a real-time system, even if the statistical average is acceptable.
      </li>
    </ul>

    <!-- Structural SVG Diagram: Timeline of Metric Intervals -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.3: Anatomical Process Lifecycle Timeline &amp; Metric Intervals</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Visualizing how Arrival, Ready Wait, Execution Bursts, I/O Blocks, and Completion map to Response, Wait, and Turnaround metrics.</div>

      <svg viewBox="0 0 820 280" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="tm-arr-left" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 8 2 L 2 5 L 8 8 z" fill="#0284c7" />
          </marker>
          <marker id="tm-arr-right" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 2 2 L 8 5 L 2 8 z" fill="#0284c7" />
          </marker>
          <marker id="tm-arr-purple-l" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 8 2 L 2 5 L 8 8 z" fill="#7c3aed" />
          </marker>
          <marker id="tm-arr-purple-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 2 2 L 8 5 L 2 8 z" fill="#7c3aed" />
          </marker>
          <marker id="tm-arr-dark-l" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 8 2 L 2 5 L 8 8 z" fill="#0f172a" />
          </marker>
          <marker id="tm-arr-dark-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 2 2 L 8 5 L 2 8 z" fill="#0f172a" />
          </marker>
        </defs>

        <!-- Base Time Axis -->
        <line x1="40" y1="120" x2="780" y2="120" stroke="#cbd5e1" stroke-width="2" />

        <!-- Execution Blocks along the timeline -->
        <!-- 1. Ready Queue Wait: x=60 to 180 (Width=120) -->
        <rect x="60" y="90" width="120" height="45" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3" />
        <text x="120" y="112" text-anchor="middle" font-size="10" font-weight="600" fill="#64748b">Ready Queue</text>
        <text x="120" y="125" text-anchor="middle" font-size="8.5" fill="#94a3b8">Wait (T_wait 1)</text>

        <!-- 2. First CPU Burst: x=180 to 320 (Width=140) -->
        <rect x="180" y="85" width="140" height="55" rx="4" fill="#f0fdf4" stroke="#059669" stroke-width="2" />
        <text x="250" y="110" text-anchor="middle" font-size="10.5" font-weight="700" fill="#166534">CPU Burst 1</text>
        <text x="250" y="126" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#15803d">Running</text>

        <!-- 3. I/O Block: x=320 to 460 (Width=140) -->
        <rect x="320" y="90" width="140" height="45" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" />
        <text x="390" y="112" text-anchor="middle" font-size="10" font-weight="600" fill="#b45309">Blocked (I/O Wait)</text>
        <text x="390" y="125" text-anchor="middle" font-size="8.5" fill="#d97706">Disk Read / NIC</text>

        <!-- 4. Ready Queue Wait 2: x=460 to 540 (Width=80) -->
        <rect x="460" y="90" width="80" height="45" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3" />
        <text x="500" y="112" text-anchor="middle" font-size="9.5" font-weight="600" fill="#64748b">Ready</text>
        <text x="500" y="125" text-anchor="middle" font-size="8" fill="#94a3b8">(T_wait 2)</text>

        <!-- 5. Second CPU Burst: x=540 to 720 (Width=180) -->
        <rect x="540" y="85" width="180" height="55" rx="4" fill="#f0fdf4" stroke="#059669" stroke-width="2" />
        <text x="630" y="110" text-anchor="middle" font-size="10.5" font-weight="700" fill="#166534">CPU Burst 2</text>
        <text x="630" y="126" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#15803d">Terminates / exit()</text>

        <!-- Vertical Milestone Guidelines -->
        <!-- T_arrival at x=60 -->
        <line x1="60" y1="35" x2="60" y2="175" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="2 2" />
        <text x="60" y="28" text-anchor="middle" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#0284c7">T_arrival</text>

        <!-- T_first_dispatch at x=180 -->
        <line x1="180" y1="35" x2="180" y2="175" stroke="#7c3aed" stroke-width="1.5" stroke-dasharray="2 2" />
        <text x="180" y="28" text-anchor="middle" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#7c3aed">T_first_dispatch</text>

        <!-- T_completion at x=720 -->
        <line x1="720" y1="35" x2="720" y2="245" stroke="#0f172a" stroke-width="1.5" stroke-dasharray="2 2" />
        <text x="720" y="28" text-anchor="middle" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#0f172a">T_completion</text>

        <!-- Dimension Interval 1: Response Time (T_arrival to T_first_dispatch) -->
        <line x1="64" y1="52" x2="176" y2="52" stroke="#7c3aed" stroke-width="2" marker-start="url(#tm-arr-purple-l)" marker-end="url(#tm-arr-purple-r)" />
        <text x="120" y="47" text-anchor="middle" font-family="var(--font-mono)" font-size="9.5" font-weight="700" fill="#7c3aed">T_response</text>

        <!-- Dimension Interval 2: Cumulative Waiting Time (Wait 1 + Wait 2) -->
        <line x1="64" y1="165" x2="176" y2="165" stroke="#0284c7" stroke-width="1.5" marker-start="url(#tm-arr-left)" marker-end="url(#tm-arr-right)" />
        <text x="120" y="180" text-anchor="middle" font-size="9" font-weight="600" fill="#0284c7">T_wait (1)</text>

        <line x1="464" y1="165" x2="536" y2="165" stroke="#0284c7" stroke-width="1.5" marker-start="url(#tm-arr-left)" marker-end="url(#tm-arr-right)" />
        <text x="500" y="180" text-anchor="middle" font-size="9" font-weight="600" fill="#0284c7">T_wait (2)</text>

        <text x="310" y="180" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#0284c7">Total T_wait = Wait(1) + Wait(2)</text>

        <!-- Dimension Interval 3: Turnaround Time (T_arrival to T_completion) -->
        <line x1="64" y1="225" x2="716" y2="225" stroke="#0f172a" stroke-width="2.5" marker-start="url(#tm-arr-dark-l)" marker-end="url(#tm-arr-dark-r)" />
        <text x="390" y="218" text-anchor="middle" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="#0f172a">T_turnaround = T_completion &minus; T_arrival (Total Elapsed Duration)</text>
      </svg>
    </div>

    <h4>2. Fundamental Architectural Dilemmas &amp; Trade-Offs</h4>
    <p>
      Optimizing an operating system scheduler is an exercise in managing engineering tensions along Pareto optimal frontiers:
    </p>

    <h5>A. Turnaround Time vs. Response Time</h5>
    <p>
      Algorithms that mathematically optimize average turnaround time (such as <strong>Shortest Job First / Shortest Remaining Time Next</strong>) do so by letting short jobs run to completion while ignoring long jobs. However, if an interactive process arrives while a compute job is underway, non-preemptive turnaround optimizers force the interactive task to wait, severely degrading response time.
    </p>
    <p>
      Conversely, algorithms designed to minimize response time (such as <strong>Round-Robin with tiny time slices</strong>) frequently interrupt long jobs to service incoming interactive events. Because every context switch incurs dispatch latency and invalidates CPU cache hierarchies, the total turnaround time for all jobs degrades.
    </p>

    <h5>B. System Throughput vs. Latency (The Quantum Sizing Dilemma)</h5>
    <p>
      Consider a system where every context switch requires dispatch latency &delta;. If the scheduler assigns a time quantum of length <i>q</i>, the fraction of CPU time wasted purely on dispatch overhead (&alpha;) is:
    </p>
    <pre><code>&alpha; = &delta; / (<i>q</i> + &delta;)</code></pre>
    <ul>
      <li><strong>Maximizing Throughput (Large <i>q</i>, e.g., <i>q</i> = 200 ms, &delta; = 1 ms):</strong> Overhead &alpha; &approx; 0.5%. Almost 99.5% of CPU cycles perform useful application computation. However, interactive response latency degrades to hundreds of milliseconds, causing unacceptable UI stutter.</li>
      <li><strong>Minimizing Latency (Small <i>q</i>, e.g., <i>q</i> = 4 ms, &delta; = 1 ms):</strong> Response time drops to near-imperceptible levels, but overhead &alpha; surges to 20%. One-fifth of the entire processor's silicon capacity is lost to context switches, MMU reloading, and cache thrashing.</li>
    </ul>

    <h5>C. Fairness vs. Prioritization &amp; Starvation</h5>
    <p>
      Strict fairness implies that every ready task receives an equal share of CPU cycles (e.g., pure Round-Robin or Generalized Processor Sharing). However, operating systems must enforce real-world urgency:
    </p>
    <ul>
      <li>A background disk-indexing service should not receive the same execution priority as the interactive display server rendering user keystrokes at 120 frames per second.</li>
      <li>However, introducing strict priority hierarchies immediately creates the risk of <strong>starvation</strong>: low-priority tasks may sit in the Ready queue indefinitely if higher-priority tasks arrive continuously. Schedulers must compromise strict prioritization through dynamic mechanisms such as <strong>aging</strong>.</li>
    </ul>

    <h4>3. Operational Environments &amp; Optimization Target Matrix</h4>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 22%;">Operational Arena</th>
            <th style="padding: 10px 14px; width: 38%;">Primary Optimization Targets</th>
            <th style="padding: 10px 14px; width: 40%;">Secondary Constraints &amp; Tolerated Trade-offs</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #0f172a;">All Operating Systems</td>
            <td style="padding: 10px 14px;">
              &bull; <strong>Fairness:</strong> Comparable processes receive comparable service.<br>
              &bull; <strong>Policy Enforcement:</strong> Stated allocation rules are upheld.<br>
              &bull; <strong>Starvation Freedom:</strong> No runnable task waits indefinitely.
            </td>
            <td style="padding: 10px 14px; color: var(--text-muted);">
              Must minimize scheduling algorithmic complexity (<i>O</i>(1) or <i>O</i>(log <i>N</i>) runqueue operations).
            </td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #0369a1;">Batch Processing Systems<br><span style="font-size: 0.78rem; font-weight: 400; color: #64748b;">(HPC, Scientific Compute, Compilers)</span></td>
            <td style="padding: 10px 14px;">
              &bull; <strong>Throughput:</strong> Maximize jobs completed per hour.<br>
              &bull; <strong>Turnaround Time:</strong> Minimize time from submission to output.<br>
              &bull; <strong>CPU Utilization:</strong> Keep execution units 100% busy.
            </td>
            <td style="padding: 10px 14px; color: var(--text-muted);">
              Response time is completely irrelevant; long preemption delays are encouraged to minimize cache churn and context switch overhead.
            </td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #0284c7;">Interactive &amp; Desktop Systems<br><span style="font-size: 0.78rem; font-weight: 400; color: #64748b;">(Workstations, Laptops, Mobile OS)</span></td>
            <td style="padding: 10px 14px;">
              &bull; <strong>Response Time:</strong> Fast feedback to user events (&lt;16&ndash;50 ms).<br>
              &bull; <strong>Proportionality:</strong> Simple tasks respond immediately.<br>
              &bull; <strong>Low Variance:</strong> Smooth UI frame rates without stutter.
            </td>
            <td style="padding: 10px 14px; color: var(--text-muted);">
              Tolerates 2%&ndash;5% throughput loss and lower average turnaround time to support continuous preemption and time slicing.
            </td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #059669;">Real-Time Embedded Systems<br><span style="font-size: 0.78rem; font-weight: 400; color: #64748b;">(Avionics, Robotics, Automotive ABS)</span></td>
            <td style="padding: 10px 14px;">
              &bull; <strong>Meeting Deadlines:</strong> Hard timing constraints must never fail.<br>
              &bull; <strong>Predictability (Zero Jitter):</strong> Deterministic worst-case execution time (WCET).
            </td>
            <td style="padding: 10px 14px; color: var(--text-muted);">
              Average throughput and hardware utilization are deliberately sacrificed; systems are intentionally over-provisioned to guarantee timing margins.
            </td>
          </tr>
        </tbody>
      </table>
    </div>"""

    # Replace Section 4 cleanly
    start_tag = "<h3>4. Conflicting Optimization Goals &amp; Metrics</h3>"
    end_tag = '<nav class="nav-bar" style="margin-top: 36px;'

    start_pos = content.find(start_tag)
    end_pos = content.find(end_tag)

    if start_pos == -1 or end_pos == -1:
        print("Error: Could not locate Section 4 tags in target file.")
        return False

    updated_content = content[:start_pos] + new_section_four + "\n\n    " + content[end_pos:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 4 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 4 in 01-scheduling-introduction.html with metric formulas\n\n"
            "Detail turnaround, slowdown ratio, wait, response, throughput overhead,\n"
            "variance/jitter, trade-off Pareto frontiers, and add an SVG timeline."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if build_expanded_section_four():
        run_git_sync()
