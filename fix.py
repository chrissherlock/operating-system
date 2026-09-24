#!/usr/bin/env python3
# =====================================================================
# fix.py: Demystify and deeply expand Section 4 in Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "03-interactive-scheduling.html")

NEW_SECTION_FOUR = r"""    <h3>4. Proportional-Share &amp; Lottery Scheduling</h3>
    <p>
      Every scheduler examined so far (FCFS, SJF, SRTN, Round-Robin, and MLFQ) operates on a <strong>priority or latency premise</strong>: they evaluate process queue states to answer the immediate operational question: <em>"Which specific process should run next to optimize turnaround time or user responsiveness?"</em>
    </p>
    <p>
      <strong>Proportional-Share scheduling</strong> (also called <em>Fair-Share scheduling</em>) abandons this framing entirely. Instead of optimizing for completion deadlines or interface responsiveness, it treats CPU execution bandwidth as an <strong>economic resource</strong>. Its foundational question is:
    </p>
    <blockquote style="border-left: 4px solid var(--accent); padding: 8px 16px; margin: 16px 0; background: #f8fafc; color: #334155; font-style: italic;">
      "How can the operating system guarantee that over time, Process A receives exactly 75% of the processor's silicon capacity, while Process B receives exactly 25%?"
    </blockquote>

    <h4>1. Lottery Scheduling: The Randomized Raffle</h4>
    <p>
      Pioneered by Carl Waldspurger and William Weihl, <strong>Lottery Scheduling</strong> uses probabilistic randomness to achieve proportional resource division:
    </p>
    <ul>
      <li>Processes are assigned <strong>lottery tickets</strong> representing their share of system resources. If Process <i>A</i> holds 75 tickets and Process <i>B</i> holds 25 tickets, Process <i>A</i> owns 75% of the ticket pool.</li>
      <li>At each scheduling tick, the kernel generates a pseudo-random integer in the range <code>[0, Total_Tickets &minus; 1]</code>.</li>
      <li>Whichever process holds the winning ticket number is granted the CPU for the upcoming time quantum.</li>
    </ul>

    <h5>Kernel Implementation: The Linked-List Traversal</h5>
    <p>
      A common misconception is that the kernel maintains a massive array containing millions of ticket numbers. In real operating systems, ticket tracking requires minimal memory: the scheduler maintains a linked list of runnable tasks, where each task's PCB simply stores its single integer ticket allocation.
    </p>
    <pre><code><span class="syn-cmt">/* Kernel Lottery Selection Algorithm: O(N) Traversal */</span>
<span class="syn-kw">int</span> total_tickets = <span class="syn-num">100</span>;
<span class="syn-kw">int</span> winning_ticket = <span class="syn-fn">random_int</span>(<span class="syn-num">0</span>, total_tickets - <span class="syn-num">1</span>); <span class="syn-cmt">/* e.g., draws 82 */</span>
<span class="syn-kw">int</span> counter = <span class="syn-num">0</span>;
<span class="syn-kw">struct</span> task_struct *curr = ready_list_head;

<span class="syn-kw">while</span> (curr != <span class="syn-kw">NULL</span>) {
    counter += curr-&gt;tickets;
    <span class="syn-kw">if</span> (counter &gt; winning_ticket) {
        <span class="syn-cmt">/* Found the task owning the winning range! */</span>
        <span class="syn-fn">switch_to</span>(curr);
        <span class="syn-kw">break</span>;
    }
    curr = curr-&gt;next;
}</code></pre>

    <div class="math-callout">
      <strong>Tracing the Silicon Dispatch Logic:</strong>
      <br>
      Suppose <strong>Process A</strong> has 75 tickets and <strong>Process B</strong> has 25 tickets. Total tickets = 100.
      <br>
      The winning draw is <strong>82</strong>:
      <ul>
        <li><strong>Check Process A:</strong> <code>counter = 0 + 75 = 75</code>. Is <code>75 &gt; 82</code>? <strong>False</strong>. Advance to next task.</li>
        <li><strong>Check Process B:</strong> <code>counter = 75 + 25 = 100</code>. Is <code>100 &gt; 82</code>? <strong>True</strong>! Process B wins the draw and executes.</li>
      </ul>
      To maximize algorithmic efficiency, kernels sort the ready list in descending order of tickets (placing high-ticket tasks at the front), minimizing average traversal steps.
    </div>

    <h5>Ticket Mechanics in Practice</h5>
    <ul>
      <li><strong>Ticket Currency:</strong> A multi-user system allocates global ticket currencies. If User <i>Alice</i> is granted 100 global tickets, she can launch two tasks and allocate 500 local "Alice-tickets" to Task 1 and 500 to Task 2. The kernel automatically converts Alice's local currency to 50 global tickets each (a 5:1 exchange rate).</li>
      <li><strong>Ticket Transfer:</strong> A client process waiting for a synchronous Remote Procedure Call (RPC) or database query can temporarily lend its tickets to the database worker thread. This boosts the worker's probability of winning execution slices, speeding up completion on the client's behalf.</li>
      <li><strong>Ticket Inflation:</strong> Mutually trusting cooperating processes can dynamically inflate or deflate their ticket allocations without negotiating with a central arbiter.</li>
    </ul>

    <h4>2. The Problem with Pure Randomness: Scheduling Jitter</h4>
    <p>
      The fundamental flaw of lottery scheduling is <strong>short-term variance (jitter)</strong>.
    </p>
    <p>
      While the Law of Large Numbers guarantees that a 75/25 ticket split will converge to an exact 3:1 ratio over millions of cycles, randomness does not guarantee fairness over short time windows. Just as flipping a fair coin can produce four heads in a row, Process <i>B</i> (the 25% task) might randomly win five consecutive draws.
    </p>
    <p>
      If Process <i>A</i> is rendering a video stream or handling real-time audio playback, losing several lottery draws in a row introduces noticeable stutter and dropped audio frames.
    </p>

    <h4>3. Stride Scheduling: Deterministic Fair-Share</h4>
    <p>
      To preserve the exact proportional guarantees of lottery scheduling while completely eliminating random variance, Waldspurger designed <strong>Stride Scheduling</strong>.
    </p>

    <h5>The Race &amp; Odometer Metaphor</h5>
    <p>
      Think of Stride Scheduling as a race where runners take strides of different lengths:
    </p>
    <ol>
      <li>
        <strong>Pick a Large System Constant (<i>K</i>):</strong> For example, <code><i>K</i> = 10,000</code>.
      </li>
      <li>
        <strong>Calculate Each Process's Stride:</strong> The stride is inversely proportional to its ticket allocation:
        <pre><code>Stride<sub><i>i</i></sub> = <i>K</i> / Tickets<sub><i>i</i></sub></code></pre>
        For Process <i>A</i> (75 tickets): <code>Stride<sub><i>A</i></sub> = 10,000 / 75 &approx; <strong>133</strong></code>.
        <br>
        For Process <i>B</i> (25 tickets): <code>Stride<sub><i>B</i></sub> = 10,000 / 25 = <strong>400</strong></code>.
      </li>
      <li>
        <strong>Maintain an Execution Odometer (the <code>pass</code> value):</strong>
        Every process tracks its progress using a <code>pass</code> counter (initialized to <code>0</code>).
      </li>
      <li>
        <strong>The Dispatch Invariant:</strong>
        The scheduler <strong>always selects the process with the minimum <code>pass</code> value</strong>. After that process executes for one quantum, its pass counter advances by its stride:
        <pre><code>pass<sub><i>i</i></sub> += Stride<sub><i>i</i></sub></code></pre>
      </li>
    </ol>

    <h5>Deterministic Step-by-Step Execution Trace</h5>
    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 8px 12px; width: 10%;">Tick</th>
            <th style="padding: 8px 12px; width: 30%;">Pass Counters Prior to Dispatch</th>
            <th style="padding: 8px 12px; width: 25%;">Task Selected (MIN pass)</th>
            <th style="padding: 8px 12px; width: 35%;">Pass Counter Update</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; font-weight: 700;">0</td>
            <td style="padding: 8px 12px;">Pass(A) = 0, Pass(B) = 0</td>
            <td style="padding: 8px 12px; font-weight: 700; color: #0284c7;">Process A <span style="font-size: 0.78rem; font-weight: 400; color: #64748b;">(Tie-break)</span></td>
            <td style="padding: 8px 12px;">Pass(A) = 0 + 133 = <strong>133</strong></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; font-weight: 700;">1</td>
            <td style="padding: 8px 12px;">Pass(A) = 133, Pass(B) = <strong>0</strong></td>
            <td style="padding: 8px 12px; font-weight: 700; color: #d97706;">Process B</td>
            <td style="padding: 8px 12px;">Pass(B) = 0 + 400 = <strong>400</strong></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; font-weight: 700;">2</td>
            <td style="padding: 8px 12px;">Pass(A) = <strong>133</strong>, Pass(B) = 400</td>
            <td style="padding: 8px 12px; font-weight: 700; color: #0284c7;">Process A</td>
            <td style="padding: 8px 12px;">Pass(A) = 133 + 133 = <strong>266</strong></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; font-weight: 700;">3</td>
            <td style="padding: 8px 12px;">Pass(A) = <strong>266</strong>, Pass(B) = 400</td>
            <td style="padding: 8px 12px; font-weight: 700; color: #0284c7;">Process A</td>
            <td style="padding: 8px 12px;">Pass(A) = 266 + 133 = <strong>399</strong></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; font-weight: 700;">4</td>
            <td style="padding: 8px 12px;">Pass(A) = <strong>399</strong>, Pass(B) = 400</td>
            <td style="padding: 8px 12px; font-weight: 700; color: #0284c7;">Process A</td>
            <td style="padding: 8px 12px;">Pass(A) = 399 + 133 = <strong>532</strong></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; font-weight: 700;">5</td>
            <td style="padding: 8px 12px;">Pass(A) = 532, Pass(B) = <strong>400</strong></td>
            <td style="padding: 8px 12px; font-weight: 700; color: #d97706;">Process B</td>
            <td style="padding: 8px 12px;">Pass(B) = 400 + 400 = <strong>800</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>
      Notice the resulting execution order: <strong>A, B, A, A, A, B</strong>.
      Over these 6 intervals, Process <i>A</i> executes 4 times and Process <i>B</i> executes 2 times. As time proceeds, the ratio converges precisely to 3:1 (75% vs. 25%) with <strong>zero randomness, zero jitter, and deterministic predictability</strong>.
    </p>

    <!-- Structural Diagram: Lottery Traversal vs Stride Execution -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.2: Lottery List Traversal vs. Stride Progress Tracking</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Comparing the probabilistic ticket list traversal against the deterministic pass counter odometer.</div>

      <svg viewBox="0 0 760 210" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <!-- Left Panel: Lottery List Traversal -->
        <g transform="translate(15, 10)">
          <rect width="350" height="185" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="14" y="24" font-size="11" font-weight="700" fill="#0284c7">LOTTERY SCHEDULING (Random Draw: 82)</text>

          <!-- Total Ticket Span -->
          <rect x="15" y="42" width="240" height="24" rx="3" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="135" y="58" text-anchor="middle" font-size="9" font-weight="700" fill="#0369a1">Process A: Tickets 0 &ndash; 74 (75% Pool)</text>

          <rect x="255" y="42" width="80" height="24" rx="3" fill="#fef3c7" stroke="#d97706"/>
          <text x="295" y="58" text-anchor="middle" font-size="9" font-weight="700" fill="#b45309">B: 75&ndash;99</text>

          <!-- List Traversal Walk -->
          <rect x="15" y="85" width="150" height="42" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="22" y="102" font-size="9.5" font-weight="700" fill="#0f172a">Task A (75 tkts)</text>
          <text x="22" y="118" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">sum=75 &lt; 82 (Skip)</text>

          <line x1="165" y1="106" x2="195" y2="106" stroke="#64748b" stroke-width="1.5" marker-end="url(#m-arr-blue)"/>

          <rect x="195" y="85" width="140" height="42" rx="4" fill="#f0fdf4" stroke="#059669" stroke-width="2"/>
          <text x="202" y="102" font-size="9.5" font-weight="700" fill="#166534">Task B (25 tkts)</text>
          <text x="202" y="118" font-family="var(--font-mono)" font-size="8.5" fill="#059669">sum=100 &gt; 82 (WIN!)</text>

          <text x="15" y="155" font-size="8.5" fill="#475569">&bull; Non-deterministic; subject to random clustering.</text>
          <text x="15" y="170" font-size="8.5" fill="#475569">&bull; Memory-efficient O(N) linked list walk.</text>
        </g>

        <!-- Right Panel: Stride Progress Odometer -->
        <g transform="translate(395, 10)">
          <rect width="350" height="185" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="14" y="24" font-size="11" font-weight="700" fill="#059669">STRIDE SCHEDULING (Deterministic Pass Values)</text>

          <!-- Stride formulas -->
          <rect x="15" y="42" width="155" height="34" rx="3" fill="#ffffff" stroke="#0284c7"/>
          <text x="22" y="57" font-size="9" font-weight="700" fill="#0284c7">Task A (75 tickets)</text>
          <text x="22" y="70" font-family="var(--font-mono)" font-size="8.5" fill="#334155">Stride = 10,000/75 = 133</text>

          <rect x="180" y="42" width="155" height="34" rx="3" fill="#ffffff" stroke="#d97706"/>
          <text x="187" y="57" font-size="9" font-weight="700" fill="#d97706">Task B (25 tickets)</text>
          <text x="187" y="70" font-family="var(--font-mono)" font-size="8.5" fill="#334155">Stride = 10,000/25 = 400</text>

          <!-- Progress Bars -->
          <text x="15" y="102" font-size="9" font-weight="600" fill="#475569">Pass Progression:</text>
          <rect x="15" y="112" width="133" height="16" rx="2" fill="#0284c7"/>
          <text x="155" y="125" font-family="var(--font-mono)" font-size="8.5" fill="#0284c7">A: 133 &rarr; 266 &rarr; 399</text>

          <rect x="15" y="134" width="200" height="16" rx="2" fill="#d97706"/>
          <text x="222" y="147" font-family="var(--font-mono)" font-size="8.5" fill="#d97706">B: 400 &rarr; 800</text>

          <text x="15" y="172" font-size="8.5" fill="#166534">&bull; Always pick MIN(pass); zero random variance.</text>
        </g>
      </svg>
    </div>

    <h4>4. Modern Lineage: Linux CFS &amp; Container Fair-Share</h4>
    <p>
      Why do operating systems courses teach Stride and Lottery scheduling if general-purpose desktop operating systems do not roll dice?
    </p>
    <p>
      Because <strong>Stride Scheduling is the direct conceptual ancestor of modern cloud virtualization and container resource management</strong>:
    </p>
    <ul>
      <li><strong>Linux Completely Fair Scheduler (CFS):</strong> The default scheduler of the Linux kernel does not use MLFQ queues. Instead, it implements a continuous variant of Stride Scheduling.</li>
      <li><strong>Virtual Runtime (<code>vruntime</code>):</strong> In Linux CFS, each thread's odometer is called its <code>vruntime</code>. A thread with a standard <code>nice</code> level of 0 accumulates <code>vruntime</code> in lockstep with physical wall-clock time.</li>
      <li><strong>Weights Instead of Strides:</strong> If a thread has high priority (low <code>nice</code>), its weight is large, so its <code>vruntime</code> accumulates very slowly (equivalent to a tiny Stride). If a thread has low priority, its <code>vruntime</code> advances rapidly.</li>
      <li><strong>Red-Black Tree Dispatch:</strong> The Linux kernel stores all runnable tasks in a self-balancing <strong>Red-Black Tree</strong> sorted by <code>vruntime</code>. The scheduler pulls the leftmost node in <code><i>O</i>(log <i>N</i>)</code> time—always choosing the task that has received the least virtual execution time.</li>
      <li><strong>Docker &amp; Kubernetes CPU Shares:</strong> When configuring CPU resource allocations in container environments (e.g., <code>docker run --cpu-shares 1024</code> vs. <code>--cpu-shares 512</code>), the container runtime writes these values directly into the kernel's CFS <code>cgroup</code> weights, using the exact proportional-share mathematics first established by lottery and stride scheduling.</li>
    </ul>"""

def update_section_four():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<h3>4. Proportional-Share &amp; Lottery Scheduling</h3>"
    end_tag = '<nav class="nav-bar" style="margin-top: 36px;'

    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 4 tags in target file.")
        return False

    updated_content = content[:start_idx] + NEW_SECTION_FOUR + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 4 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Clarify proportional-share and stride scheduling in Module 03\n\n"
            "Replace abstract theory with raffle ticket traversal, step-by-step stride\n"
            "math trace, Linux CFS vruntime lineage, and a dual-panel SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_four():
        run_git_sync()
