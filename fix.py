#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand and syntax highlight Section 1 in Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "03-semaphores-mutexes-monitors.html"
)

# Syntax CSS rules to ensure colors render
SYNTAX_CSS = r"""    /* Syntax Highlighting */
    .syn-kw { color: #38bdf8; font-weight: 600; }
    .syn-fn { color: #60a5fa; font-weight: 600; }
    .syn-num { color: #f59e0b; }
    .syn-str { color: #34d399; }
    .syn-cmt { color: #64748b; font-style: italic; }"""

EXPANDED_SECTION_ONE = r"""    <h3>1. Sleep &amp; Wakeup: The Lost Wakeup Hazard</h3>
    <p>
      In Module 02, we explored how hardware atomic instructions enable spinlocks. While spinlocks provide rapid mutual exclusion for tiny, nanosecond critical sections on multiprocessor systems, they suffer from a fatal operational defect: <strong>busy waiting</strong>.
    </p>
    <p>
      A spinning thread burns 100% of its CPU time slice executing instructions that achieve zero computational work. If the thread holding the lock is descheduled, preempted, or waiting on a slow peripheral (such as an NVMe disk read, network packet, or user keystroke), all competing threads on other cores spin fruitlessly, driving system temperature and power consumption to maximum while stalling progress.
    </p>
    <p>
      To build scalable operating systems, software requires <strong>blocking primitives</strong>: mechanisms that allow a thread to release its CPU execution core voluntarily, enter a suspended state (<code>BLOCKED</code> or <code>WAITING</code>), and sleep until another execution thread notifies it that the desired event or resource has become available.
    </p>

    <h4>The Primitive Sleep and Wakeup Abstraction</h4>
    <p>
      The earliest blocking synchronization models relied on a pair of paired operating system primitives:
    </p>
    <ul>
      <li><code>sleep()</code>: An atomic system call that causes the invoking process to suspend execution. The kernel removes the process from the scheduler's <code>READY</code> runqueue, updates its state to <code>BLOCKED</code>, and context-switches to another runnable thread.</li>
      <li><code>wakeup(pid)</code>: A system call taking a target process identifier (PID) as an argument. The kernel locates the target process's Process Control Block (PCB) and transitions its state from <code>BLOCKED</code> back to <code>READY</code>, placing it back onto the scheduler's runqueue.</li>
    </ul>

    <h4>The Classical Bounded-Buffer Producer-Consumer Model</h4>
    <p>
      To evaluate <code>sleep()</code> and <code>wakeup()</code>, consider the canonical <strong>Producer-Consumer problem</strong> (also called the <em>Bounded-Buffer problem</em>). Two processes share a common fixed-size buffer of capacity <i>N</i>:
    </p>
    <ul>
      <li>The <strong>Producer</strong> generates data items and deposits them into the buffer.</li>
      <li>The <strong>Consumer</strong> extracts data items from the buffer and consumes them.</li>
      <li>A shared integer variable <code>count</code> tracks the number of items currently residing in the buffer (initialized to <code>0</code>).</li>
    </ul>

    <pre><code><span class="syn-cmt">/* FLAWED: Producer-Consumer Implementation Using Primitive Sleep and Wakeup */</span>
<span class="syn-kw">#define</span> N <span class="syn-num">100</span>                   <span class="syn-cmt">/* Number of slots in the shared buffer */</span>
<span class="syn-kw">volatile int</span> count = <span class="syn-num">0</span>;         <span class="syn-cmt">/* Number of data items currently in buffer */</span>

<span class="syn-kw">void</span> producer(<span class="syn-kw">void</span>) {
    <span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
        item_t item = <span class="syn-fn">produce_item</span>(); <span class="syn-cmt">/* Generate next data item */</span>

        <span class="syn-kw">if</span> (count == N) {
            <span class="syn-fn">sleep</span>();            <span class="syn-cmt">/* Buffer is full: producer sleeps */</span>
        }

        <span class="syn-fn">insert_item</span>(item);      <span class="syn-cmt">/* Deposit item into buffer */</span>
        count++;                <span class="syn-cmt">/* Increment item counter */</span>

        <span class="syn-kw">if</span> (count == <span class="syn-num">1</span>) {
            <span class="syn-fn">wakeup</span>(consumer_pid); <span class="syn-cmt">/* Was empty: wake up sleeping consumer */</span>
        }
    }
}

<span class="syn-kw">void</span> consumer(<span class="syn-kw">void</span>) {
    <span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
        <span class="syn-kw">if</span> (count == <span class="syn-num">0</span>) {
            <span class="syn-fn">sleep</span>();            <span class="syn-cmt">/* Buffer is empty: consumer sleeps */</span>
        }

        item_t item = <span class="syn-fn">remove_item</span>(); <span class="syn-cmt">/* Extract item from buffer */</span>
        count--;                <span class="syn-cmt">/* Decrement item counter */</span>

        <span class="syn-kw">if</span> (count == N - <span class="syn-num">1</span>) {
            <span class="syn-fn">wakeup</span>(producer_pid); <span class="syn-cmt">/* Was full: wake up sleeping producer */</span>
        }

        <span class="syn-fn">consume_item</span>(item);     <span class="syn-cmt">/* Process the data item */</span>
    }
}</code></pre>

    <h4>The Anatomy of the Lost Wakeup Defect</h4>
    <p>
      This intuitive code contains a fatal synchronization flaw known as the <strong>Lost Wakeup Problem</strong>. The defect arises because the high-level test of <code>count</code> and the execution of <code>sleep()</code> are <strong>not atomic</strong>.
    </p>

    <!-- Structural Diagram: The Lost Wakeup Race Window -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.1: The Lost Wakeup Race Window Execution Timeline</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How preemption between condition testing and the sleep() system call causes signals to vanish permanently.</div>

      <svg viewBox="0 0 760 220" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="lw-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="lw-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Time Axis -->
        <line x1="30" y1="30" x2="730" y2="30" stroke="#cbd5e1" stroke-width="2"/>
        <text x="730" y="24" font-size="8" font-family="var(--font-mono)" fill="#64748b">TIME &rarr;</text>

        <!-- Step 1: Consumer Checks -->
        <g transform="translate(40, 45)">
          <rect width="150" height="65" rx="5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
          <text x="12" y="20" font-size="8.5" font-weight="700" fill="#0369a1">1. CONSUMER CHECKS</text>
          <text x="12" y="36" font-family="var(--font-mono)" font-size="8" fill="#0f172a">if (count == 0) &rarr; TRUE</text>
          <text x="12" y="52" font-size="7.5" fill="#0369a1">Decides to sleep...</text>
        </g>

        <!-- Step 2: Context Switch (Preemption Window) -->
        <g transform="translate(210, 45)">
          <rect width="155" height="65" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
          <text x="12" y="20" font-size="8.5" font-weight="700" fill="#991b1b">2. PREEMPTION GAP</text>
          <text x="12" y="36" font-size="7.5" font-weight="700" fill="#dc2626">&times; TIMER INTERRUPT!</text>
          <text x="12" y="50" font-size="7" fill="#7f1d1d">Consumer paused BEFORE</text>
          <text x="12" y="60" font-size="7" fill="#7f1d1d">executing sleep()</text>
        </g>

        <!-- Step 3: Producer Wakes -->
        <g transform="translate(385, 45)">
          <rect width="165" height="65" rx="5" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
          <text x="12" y="20" font-size="8.5" font-weight="700" fill="#92400e">3. PRODUCER RUNS</text>
          <text x="12" y="34" font-family="var(--font-mono)" font-size="7.5" fill="#b45309">count++ &rarr; count = 1</text>
          <text x="12" y="48" font-family="var(--font-mono)" font-size="7.5" fill="#b45309">wakeup(consumer)</text>
          <text x="12" y="60" font-size="7" font-weight="700" fill="#dc2626">&times; SIGNAL DISCARDED!</text>
        </g>

        <!-- Step 4: Deadlock -->
        <g transform="translate(570, 45)">
          <rect width="150" height="65" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
          <text x="12" y="20" font-size="8.5" font-weight="700" fill="#991b1b">4. PERMANENT SLEEP</text>
          <text x="12" y="36" font-family="var(--font-mono)" font-size="7.5" fill="#7f1d1d">Consumer: sleep()</text>
          <text x="12" y="50" font-size="7" font-weight="700" fill="#dc2626">&bull; Consumer sleeps forever</text>
          <text x="12" y="60" font-size="7" font-weight="700" fill="#dc2626">&bull; Buffer fills &rarr; Deadlock</text>
        </g>

        <!-- Connecting Vectors -->
        <line x1="190" y1="77" x2="208" y2="77" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#lw-arr-blue)"/>
        <line x1="365" y1="77" x2="383" y2="77" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#lw-arr-blue)"/>
        <line x1="550" y1="77" x2="568" y2="77" stroke="#dc2626" stroke-width="1.5" marker-end="url(#lw-arr-red)"/>

        <!-- Kernel Reaction Annotation -->
        <rect x="40" y="130" width="680" height="65" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
        <text x="20" y="22" font-size="8" font-weight="700" fill="#475569" transform="translate(40, 130)">THE KERNEL-LEVEL MECHANISM OF FAILURE:</text>
        <text x="20" y="38" font-size="7.5" fill="#334155" transform="translate(40, 130)">When wakeup(consumer_pid) arrives at Step 3, the Consumer's PCB state in the kernel is still <tspan font-family="var(--font-mono)" font-weight="700" fill="#0284c7">TASK_RUNNING (READY)</tspan>, not <tspan font-family="var(--font-mono)" font-weight="700" fill="#dc2626">TASK_INTERRUPTIBLE (BLOCKED)</tspan>.</text>
        <text x="20" y="52" font-size="7.5" fill="#334155" transform="translate(40, 130)">Because primitive wakeup calls are stateless pulses (they do not increment a counter), the kernel shrugs and discards the signal. When the Consumer resumes, it blindly enters sleep state with zero pending wakeups.</text>
      </svg>
    </div>

    <h5>Step-by-Step Breakdown of the Race Interleaving:</h5>
    <ol>
      <li>
        <strong>Evaluation (Consumer):</strong> The buffer is currently empty (<code>count == 0</code>). The Consumer executes <code>if (count == 0)</code>. The condition evaluates to <code>true</code>. The Consumer prepares to execute <code>sleep()</code>.
      </li>
      <li>
        <strong>Preemptive Interruption:</strong> Immediately after the comparison but <em>before</em> the CPU can execute the system call trap instruction for <code>sleep()</code>, the local APIC hardware timer generates an interrupt. The OS kernel context-switches from the Consumer to the Producer.
      </li>
      <li>
        <strong>Production &amp; Signal (Producer):</strong> The Producer runs. It produces an item, inserts it into slot 0, and increments <code>count</code> from <code>0</code> to <code>1</code>.
      </li>
      <li>
        <strong>The Stateless Wakeup Call:</strong> The Producer tests <code>if (count == 1)</code>. Finding it <code>true</code>, the Producer calls <code>wakeup(consumer_pid)</code>.
      </li>
      <li>
        <strong>The Silent Signal Loss:</strong> Inside the kernel, the dispatcher looks up the Consumer's process entry. Because the Consumer was interrupted before calling <code>sleep()</code>, <strong>the Consumer is not sleeping</strong>&mdash;it is in the <code>READY</code> state on the runqueue! A primitive <code>wakeup</code> signal has no memory buffer; because the process is not in the <code>BLOCKED</code> state, <strong>the wakeup signal is discarded by the kernel and permanently lost</strong>.
      </li>
      <li>
        <strong>The Fatal Sleep (Consumer):</strong> The Consumer is rescheduled. Its program counter resumes exactly where it was paused: at the <code>sleep()</code> instruction. It executes <code>sleep()</code>, moving its PCB to the <code>BLOCKED</code> queue. The Consumer is now asleep, waiting for a wakeup signal that was already delivered and lost.
      </li>
      <li>
        <strong>Complete System Deadlock:</strong> The Producer continues executing cycles, generating items and incrementing <code>count</code>. Because the Consumer is asleep, no items are ever removed. Eventually, the buffer fills completely (<code>count == N</code>). The Producer tests <code>if (count == N)</code>, finds it <code>true</code>, and calls <code>sleep()</code>.
      </li>
    </ol>
    <p>
      <strong>Result: Total, unrecoverable deadlock.</strong> Both processes are permanently asleep, neither can run to wake the other, and no exception, crash log, or fault is raised by the operating system.
    </p>

    <h4>The Failed Wakeup-Waiting Bit Patch</h4>
    <p>
      An intuitive early attempt to patch this flaw was to equip each process control block with a <strong>wakeup waiting bit</strong>:
    </p>
    <ul>
      <li>When a <code>wakeup()</code> signal was sent to a process that was not yet asleep, the kernel set the target's wakeup waiting bit to <code>1</code>.</li>
      <li>When a process called <code>sleep()</code>, the kernel checked this bit. If the bit was <code>1</code>, the kernel cleared the bit to <code>0</code> and allowed the process to continue running without sleeping.</li>
    </ul>
    <div class="math-callout">
      <strong>Why the Wakeup Waiting Bit Fails:</strong>
      <br>
      While a 1-bit memory prevents signal loss for two single-threaded processes under a single missed wakeup, it <strong>collapses completely under multi-process concurrency</strong>:
      <ul>
        <li>If three producers attempt to wake a consumer while it is preempted, the wakeup waiting bit is set to <code>1</code> on the first wakeup, but cannot represent the second or third wakeup (it saturates at <code>1</code>).</li>
        <li>Subsequent signals are lost, re-introducing the identical deadlock when multiple items are deposited.</li>
      </ul>
      This realization forced computer scientists to recognize a fundamental truth: <strong>synchronization primitives cannot be stateless boolean flags; they must be atomic integer counters equipped with FIFO wait queues</strong>&mdash;the exact definition of Dijkstra's Semaphore.
    </div>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate Section 1 boundaries
    start_marker = "<h3>1. Sleep &amp; Wakeup: The Lost Wakeup Hazard</h3>"
    end_marker = "<!-- Directed Narrative Stepper: Lost Wakeup vs. Semaphore -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 03.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_ONE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 1 of Module 03 with lost wakeup mechanics and syntax\n\n"
            "Detail sleep/wakeup state transitions, the stateless pulse defect,\n"
            "the failed wakeup-waiting bit patch, and add an SVG timing race diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
