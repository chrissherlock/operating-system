#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 5 in 02-batch-scheduling.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "02-batch-scheduling.html")

EXPANDED_SECTION_FIVE = r"""    <h3>5. Comprehensive Batch Scheduling Comparison</h3>
    <p>
      Selecting or designing a batch scheduling discipline requires evaluating trade-offs across four foundational axes: average turnaround latency, algorithmic complexity, runtime estimation feasibility, and starvation resistance.
    </p>

    <h4>1. Bridging the Gap: Highest Response Ratio Next (HRRN)</h4>
    <p>
      Non-preemptive Shortest Job First (SJF) minimizes average turnaround time, but leaves long compute jobs vulnerable to indefinite starvation if short jobs arrive continuously. Preemptive Shortest Remaining Time Next (SRTN) eliminates this arrival vulnerability, but requires hardware timer preemption and incurs continuous context-switching overhead.
    </p>
    <p>
      To resolve the starvation dilemma in strictly non-preemptive batch architectures without timer interrupts, Brinch Hansen developed <strong>Highest Response Ratio Next (HRRN)</strong>.
    </p>

    <div class="math-callout">
      <strong>The HRRN Priority Formula:</strong>
      <br>
      Whenever the CPU core becomes free, the scheduler calculates the <strong>Response Ratio (<i>R</i>)</strong> for every waiting process in the Ready queue and dispatches the task with the maximum ratio:
      <pre><code><i>R</i> = (<i>w</i> + <i>s</i>) / <i>s</i> = 1 + (<i>w</i> / <i>s</i>)</code></pre>
      where:
      <ul>
        <li><code><i>w</i></code> = Time spent waiting in the Ready queue so far.</li>
        <li><code><i>s</i></code> = Expected CPU service / burst time (estimated via &tau;).</li>
      </ul>
      <strong>Mechanisms of Built-In Aging:</strong>
      <ul>
        <li><em>Favors Short Jobs:</em> When a new task arrives (<code><i>w</i> = 0</code>), its ratio is <code><i>R</i> = 1.0</code>. As soon as it waits, a small expected burst <code><i>s</i></code> in the denominator causes <code><i>w</i> / <i>s</i></code> to grow rapidly, giving short jobs quick escalation.</li>
        <li><em>Prevents Starvation:</em> A massive compute job with large <code><i>s</i></code> starts with a sluggish ratio. However, as it sits in the queue, its waiting time <code><i>w</i></code> accumulates monotonically in the numerator. Eventually, <code><i>w</i></code> becomes large enough that the long job's ratio surpasses newly arrived short jobs, guaranteeing execution without preemption.</li>
      </ul>
    </div>

    <h4>2. Multi-Dimensional Batch Comparison Matrix</h4>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 18%;">Algorithm</th>
            <th style="padding: 10px 14px; width: 16%;">Selection Rule</th>
            <th style="padding: 10px 14px; width: 14%;">Preemption</th>
            <th style="padding: 10px 14px; width: 18%;">Turnaround Profile</th>
            <th style="padding: 10px 14px; width: 18%;">Starvation Risk</th>
            <th style="padding: 10px 14px; width: 16%;">Data Structure &amp; Cost</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #0284c7;">FCFS</td>
            <td style="padding: 10px 14px;"><code>MIN(Arrival)</code></td>
            <td style="padding: 10px 14px;">Non-Preemptive</td>
            <td style="padding: 10px 14px; color: #dc2626;">Poor (Degraded by Convoy Effect)</td>
            <td style="padding: 10px 14px; color: #059669;">Zero (Monotonic arrival order)</td>
            <td style="padding: 10px 14px;">FIFO Queue: <code><i>O</i>(1)</code> enqueue &amp; dequeue.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #059669;">SJF</td>
            <td style="padding: 10px 14px;"><code>MIN(Burst &tau;)</code></td>
            <td style="padding: 10px 14px;">Non-Preemptive</td>
            <td style="padding: 10px 14px; color: #059669;">Optimal for simultaneous arrivals</td>
            <td style="padding: 10px 14px; color: #dc2626;">High (Continuous short jobs starve long jobs)</td>
            <td style="padding: 10px 14px;">Min-Heap: <code><i>O</i>(log <i>n</i>)</code> insert/extract.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #7c3aed;">SRTN</td>
            <td style="padding: 10px 14px;"><code>MIN(Remaining &tau;)</code></td>
            <td style="padding: 10px 14px;">Preemptive</td>
            <td style="padding: 10px 14px; color: #059669;">Optimal across dynamic arrivals</td>
            <td style="padding: 10px 14px; color: #dc2626;">High (Long tasks can be repeatedly interrupted)</td>
            <td style="padding: 10px 14px;">Min-Heap: <code><i>O</i>(log <i>n</i>)</code> + context switch cost.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #d97706;">HRRN</td>
            <td style="padding: 10px 14px;"><code>MAX((<i>w</i>+<i>s</i>)/<i>s</i>)</code></td>
            <td style="padding: 10px 14px;">Non-Preemptive</td>
            <td style="padding: 10px 14px; color: #059669;">Near-Optimal (Balances short/long)</td>
            <td style="padding: 10px 14px; color: #059669;">Zero (Waiting time <i>w</i> guarantees aging)</td>
            <td style="padding: 10px 14px;">Linear scan: <code><i>O</i>(<i>n</i>)</code> per dispatch.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>3. Analytical Edge Cases &amp; Theorems</h4>
    <ul>
      <li>
        <strong>The Identical-Burst Degeneracy Theorem:</strong>
        If all processes in a workload require identical CPU burst durations (<i>s</i><sub>1</sub> = <i>s</i><sub>2</sub> = ... = <i>s</i><sub><i>n</i></sub> = <i>K</i>), then SJF, SRTN, and HRRN all collapse into standard First-Come First-Served (FCFS). Under this condition, preemption in SRTN provides zero mathematical benefit and serves only to waste CPU cycles in pointless context switching.
      </li>
      <li>
        <strong>The Starvation Threshold:</strong>
        Under SJF or SRTN, a long job requiring <i>S</i> seconds of CPU time will starve indefinitely if the arrival rate of short jobs &lambda;<sub>short</sub> and their mean service duration <i>E</i>[<i>S</i><sub>short</sub>] satisfy:
        <pre><code>&rho;<sub>short</sub> = &lambda;<sub>short</sub> &times; <i>E</i>[<i>S</i><sub>short</sub>] &ge; 1.0</code></pre>
        When the utilization generated solely by short tasks equals or exceeds 100% of CPU capacity, the ready queue never clears of short tasks, driving the waiting time of the long job to infinity:
        <pre><code><i>T</i><sub>wait</sub>(Long Job) &rarr; &infin;</code></pre>
      </li>
    </ul>

    <h4>4. Production Batch Systems &amp; HPC Scheduling</h4>
    <p>
      In modern High-Performance Computing (HPC) clusters and supercomputer workload managers (such as <strong>SLURM</strong>, <strong>PBS Pro</strong>, or <strong>HTCondor</strong>), CPU cores are scheduled across thousands of nodes executing multi-day scientific simulations.
    </p>
    <p>
      Because general-purpose exponential smoothing (&tau;) cannot reliably predict whether a climate model will run for 10 minutes or 48 hours, production HPC systems bypass estimation entirely:
    </p>
    <ul>
      <li><strong>Mandatory Wall-Clock Declarations:</strong> Users submit jobs with an explicit declared execution ceiling (<code>#SBATCH --time=04:00:00</code>). If the job exceeds this duration, the kernel immediately terminates it via <code>SIGKILL</code>.</li>
      <li><strong>Reservation Scheduling &amp; Backfilling:</strong>
        To prevent the convoy effect without killing long compute jobs, modern batch systems use <strong>Backfilling</strong>:
        <br>
        1. A massive 512-core simulation is queued and assigned an upcoming start reservation at <i>T</i> = 14:00.
        <br>
        2. Rather than leaving cores idle while waiting for earlier jobs to drain, the scheduler scans the queue for short jobs that can start immediately and finish <em>before</em> the 14:00 reservation.
        <br>
        3. These short jobs are "backfilled" into the execution gaps, achieving 95%+ CPU utilization across the cluster while honoring the reservation of the primary batch job.
      </li>
    </ul>"""

def update_section_five():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Identify Section 5 boundaries
    start_str = "<h3>5. Comprehensive Batch Scheduling Comparison</h3>"
    end_str = '<nav class="nav-bar" style="margin-top: 36px;'

    start_idx = content.find(start_str)
    end_idx = content.find(end_str)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 5 boundaries in target file.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_FIVE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 5 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 5 of 02-batch-scheduling.html with HRRN and HPC backfilling\n\n"
            "Add Highest Response Ratio Next, 4-way comparison matrix, starvation\n"
            "threshold analysis, and production HPC scheduling mechanics with backfill."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_five():
        run_git_sync()
