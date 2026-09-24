#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 3 in Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "04-classical-synchronization.html"
)

# Syntax CSS rules to ensure colors render
SYNTAX_CSS = r"""    /* Syntax Highlighting */
    .syn-kw { color: #38bdf8; font-weight: 600; }
    .syn-fn { color: #60a5fa; font-weight: 600; }
    .syn-num { color: #f59e0b; }
    .syn-str { color: #34d399; }
    .syn-cmt { color: #64748b; font-style: italic; }"""

EXPANDED_SECTION_THREE = r"""    <h3>3. The Readers-Writers Problem</h3>
    <p>
      Formulated by P. J. Courtois, F. Heymans, and D. L. Parnas in 1971, the <strong>Readers-Writers Problem</strong> models concurrent access to a shared resource&mdash;such as an in-memory database table, an operating system routing table, or a file system directory cache&mdash;where competing threads have asymmetric access requirements:
    </p>
    <ul>
      <li><strong>Readers:</strong> Execute read-only queries. They inspect or extract data without mutating state. Multiple readers may access the shared dataset <em>simultaneously</em> without hazard.</li>
      <li><strong>Writers:</strong> Mutate, insert, or delete data. A writer must have <strong>strict exclusive access</strong>: when a writer is modifying the dataset, no other writer may write, and <strong>no reader may read</strong> (preventing torn reads, dirty reads, and memory corruption).</li>
    </ul>

    <h4>The Concurrency Matrix</h4>
    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: center;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 8px 12px; text-align: left;">Active Entity</th>
            <th style="padding: 8px 12px;">Second Reader Arrives</th>
            <th style="padding: 8px 12px;">Second Writer Arrives</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; text-align: left; font-weight: 700;">Reader Active</td>
            <td style="padding: 8px 12px; color: #059669; font-weight: 700;">&#10003; PERMITTED (Concurrent Reads)</td>
            <td style="padding: 8px 12px; color: #dc2626; font-weight: 700;">&times; BLOCKED (Writer Must Wait)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 8px 12px; text-align: left; font-weight: 700;">Writer Active</td>
            <td style="padding: 8px 12px; color: #dc2626; font-weight: 700;">&times; BLOCKED (Reader Must Wait)</td>
            <td style="padding: 8px 12px; color: #dc2626; font-weight: 700;">&times; BLOCKED (Exclusive Access Only)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Structural Diagram: Readers-Writers Arbitration Topology -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.3: Readers-Writers Database Access Modes and Fair Turnstile Queuing</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How an entry turnstile enforces FIFO queueing, preventing continuous reader arrivals from starving waiting writers.</div>

      <svg viewBox="0 0 760 250" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="rw-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="rw-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="rw-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Left: Incoming Threads / Turnstile Gate -->
        <g transform="translate(20, 20)">
          <rect width="210" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10" font-weight="700" fill="#0f172a">ENTRY TURNSTILE GATE</text>

          <rect x="12" y="38" width="186" height="45" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="105" y="56" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">sem_t turnstile (Init 1)</text>
          <text x="105" y="70" text-anchor="middle" font-size="7.5" fill="#166534">Enforces FIFO arrival order</text>

          <!-- Queue Nodes -->
          <rect x="12" y="94" width="186" height="102" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="20" y="112" font-size="8" font-weight="700" fill="#475569">THREAD ARRIVAL SEQUENCE:</text>

          <rect x="20" y="122" width="170" height="20" rx="3" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="105" y="136" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#0369a1">Reader R1 &rarr; In Chamber</text>

          <rect x="20" y="146" width="170" height="20" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="105" y="160" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#991b1b">Writer W1 &rarr; Queued at Gate</text>

          <rect x="20" y="170" width="170" height="20" rx="3" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="105" y="184" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#64748b">Reader R2 &rarr; Blocked Behind W1</text>
        </g>

        <!-- Connecting Vector -->
        <line x1="230" y1="125" x2="255" y2="125" stroke="#0284c7" stroke-width="2" marker-end="url(#rw-arr-blue)"/>

        <!-- Middle: Shared Database Chamber -->
        <g transform="translate(260, 20)">
          <rect width="260" height="210" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="130" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0284c7">SHARED DATABASE CHAMBER</text>

          <!-- Dual Mode Chamber -->
          <g transform="translate(15, 38)">
            <!-- Mode 1: Concurrent Readers -->
            <rect x="0" y="0" width="230" height="74" rx="5" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5"/>
            <text x="15" y="18" font-size="8.5" font-weight="700" fill="#0369a1">SHARED READ CONCURRENCY:</text>
            <rect x="15" y="28" width="58" height="32" rx="3" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="44" y="48" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#0284c7">Reader 1</text>

            <rect x="85" y="28" width="58" height="32" rx="3" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="114" y="48" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#0284c7">Reader 2</text>

            <rect x="155" y="28" width="58" height="32" rx="3" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="184" y="48" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#0284c7">Reader 3</text>
          </g>

          <g transform="translate(15, 122)">
            <!-- Mode 2: Exclusive Writer -->
            <rect x="0" y="0" width="230" height="74" rx="5" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="15" y="18" font-size="8.5" font-weight="700" fill="#991b1b">EXCLUSIVE WRITE MUTEX:</text>
            <rect x="15" y="28" width="200" height="32" rx="3" fill="#fee2e2" stroke="#dc2626"/>
            <text x="115" y="48" text-anchor="middle" font-size="8.5" font-weight="700" fill="#991b1b">WRITER (SOLE OCCUPANT)</text>
          </g>
        </g>

        <!-- Right: Synchronization Registry & Telemetry -->
        <g transform="translate(535, 20)">
          <rect width="205" height="210" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10" font-weight="700" fill="#0f172a">SYNCHRONIZATION STATE</text>

          <rect x="12" y="38" width="181" height="48" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="20" y="54" font-size="8" font-weight="700" fill="#475569">READER COUNTER:</text>
          <text x="20" y="72" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#0284c7">read_count = 1</text>

          <rect x="12" y="94" width="181" height="48" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="20" y="110" font-size="8" font-weight="700" fill="#475569">RESOURCE LOCK:</text>
          <text x="20" y="128" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#dc2626">db_mutex = 0 (HELD)</text>

          <rect x="12" y="150" width="181" height="48" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="20" y="168" font-size="8" font-weight="700" fill="#166534">FAIRNESS POLICY:</text>
          <text x="20" y="184" font-size="7.5" font-weight="700" fill="#166534">&#10003; Fair Turnstile Active</text>
        </g>
      </svg>
    </div>

    <h4>The Three Classical Variations</h4>
    <p>
      The core challenge in solving the Readers-Writers problem is not merely achieving mutual exclusion, but establishing an equitable <strong>priority policy</strong> between readers and writers.
    </p>

    <h5>1. First Readers-Writers (Reader-Preference)</h5>
    <p>
      In this classic implementation, readers are given priority over writers. If the database is currently open for reading, any newly arrived reader is permitted to enter immediately, regardless of whether a writer is waiting:
    </p>

    <pre><code><span class="syn-cmt">/* First Readers-Writers (Reader-Preference) */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;semaphore.h&gt;</span>

<span class="syn-kw">int</span> read_count = <span class="syn-num">0</span>;
<span class="syn-kw">sem_t</span> count_mutex; <span class="syn-cmt">/* Binary semaphore protecting read_count (init 1) */</span>
<span class="syn-kw">sem_t</span> db_mutex;    <span class="syn-cmt">/* Binary semaphore protecting database access (init 1) */</span>

<span class="syn-kw">void</span> reader(<span class="syn-kw">void</span>) {
    <span class="syn-fn">sem_wait</span>(&amp;count_mutex);
    read_count++;
    <span class="syn-kw">if</span> (read_count == <span class="syn-num">1</span>) {
        <span class="syn-fn">sem_wait</span>(&amp;db_mutex);   <span class="syn-cmt">/* First reader locks database against writers */</span>
    }
    <span class="syn-fn">sem_post</span>(&amp;count_mutex);

    <span class="syn-fn">read_database</span>();           <span class="syn-cmt">/* Reading is executed concurrently */</span>

    <span class="syn-fn">sem_wait</span>(&amp;count_mutex);
    read_count--;
    <span class="syn-kw">if</span> (read_count == <span class="syn-num">0</span>) {
        <span class="syn-fn">sem_post</span>(&amp;db_mutex);   <span class="syn-cmt">/* Last reader unlocks database for writers */</span>
    }
    <span class="syn-fn">sem_post</span>(&amp;count_mutex);
}

<span class="syn-kw">void</span> writer(<span class="syn-kw">void</span>) {
    <span class="syn-fn">sem_wait</span>(&amp;db_mutex);       <span class="syn-cmt">/* Exclusive lock: blocks all readers and writers */</span>
    <span class="syn-fn">write_database</span>();
    <span class="syn-fn">sem_post</span>(&amp;db_mutex);
}</code></pre>

    <div class="math-callout">
      <strong>The Pathological Defect: Indefinite Writer Starvation</strong>
      <br>
      Suppose Reader 1 enters and claims <code>db_mutex</code>. While Reader 1 is reading, a Writer arrives and blocks on <code>sem_wait(&amp;db_mutex)</code>.
      <br>
      An instant later, Reader 2 arrives. Because <code>read_count</code> is already <code>1</code>, Reader 2 increments <code>read_count</code> to <code>2</code> and enters without touching <code>db_mutex</code>.
      <br>
      Before Reader 2 finishes, Reader 3 arrives. Then Reader 4 arrives. As long as a continuous stream of overlapping readers arrives, <strong><code>read_count</code> never drops to 0</strong>.
      <br>
      <strong>Result:</strong> The writer waits indefinitely in the queue, suffering permanent <strong>starvation</strong> (violating Condition 4: Bounded Waiting).
    </div>

    <h5>2. Second Readers-Writers (Writer-Preference)</h5>
    <p>
      To prevent writer starvation and ensure database updates are not delayed by an endless stream of reads, Courtois et al. designed the <strong>Writer-Preference</strong> variant:
    </p>
    <ul>
      <li>When a writer announces its intent to write, newly arriving readers are <strong>prevented from entering</strong> the chamber, even if other readers are currently reading.</li>
      <li>Existing readers are allowed to complete their read operations and exit.</li>
      <li>As soon as the last active reader exits, the waiting writer claims the database immediately.</li>
      <li><em>Trade-off:</em> While writer starvation is eliminated, a continuous stream of write operations will now cause <strong>reader starvation</strong>.</li>
    </ul>

    <h5>3. Third Readers-Writers (Fair FIFO Turnstile / No Starvation)</h5>
    <p>
      To achieve genuine fairness where <em>neither</em> readers nor writers starve, the algorithm introduces an architectural <strong>Turnstile Semaphore</strong> (<code>turnstile</code>, initialized to <code>1</code>):
    </p>

    <pre><code><span class="syn-cmt">/* Third Readers-Writers (Fair Turnstile: Starvation-Free) */</span>
<span class="syn-kw">int</span> read_count = <span class="syn-num">0</span>;
<span class="syn-kw">sem_t</span> count_mutex; <span class="syn-cmt">/* Protects read_count (init 1) */</span>
<span class="syn-kw">sem_t</span> db_mutex;    <span class="syn-cmt">/* Exclusive access to database (init 1) */</span>
<span class="syn-kw">sem_t</span> turnstile;   <span class="syn-cmt">/* Fair entry turnstile gate (init 1) */</span>

<span class="syn-kw">void</span> fair_reader(<span class="syn-kw">void</span>) {
    <span class="syn-fn">sem_wait</span>(&amp;turnstile);      <span class="syn-cmt">/* 1. Pass through entry turnstile */</span>
    <span class="syn-fn">sem_wait</span>(&amp;count_mutex);
    read_count++;
    <span class="syn-kw">if</span> (read_count == <span class="syn-num">1</span>) {
        <span class="syn-fn">sem_wait</span>(&amp;db_mutex);   <span class="syn-cmt">/* First reader locks database */</span>
    }
    <span class="syn-fn">sem_post</span>(&amp;count_mutex);
    <span class="syn-fn">sem_post</span>(&amp;turnstile);      <span class="syn-cmt">/* 2. Release turnstile for next thread in queue */</span>

    <span class="syn-fn">read_database</span>();

    <span class="syn-fn">sem_wait</span>(&amp;count_mutex);
    read_count--;
    <span class="syn-kw">if</span> (read_count == <span class="syn-num">0</span>) {
        <span class="syn-fn">sem_post</span>(&amp;db_mutex);   <span class="syn-cmt">/* Last reader unlocks database */</span>
    }
    <span class="syn-fn">sem_post</span>(&amp;count_mutex);
}

<span class="syn-kw">void</span> fair_writer(<span class="syn-kw">void</span>) {
    <span class="syn-fn">sem_wait</span>(&amp;turnstile);      <span class="syn-cmt">/* 1. Claim turnstile gate: BLOCKS new readers */</span>
    <span class="syn-fn">sem_wait</span>(&amp;db_mutex);       <span class="syn-cmt">/* 2. Await active readers to drain; claim database */</span>

    <span class="syn-fn">write_database</span>();

    <span class="syn-fn">sem_post</span>(&amp;turnstile);      <span class="syn-cmt">/* 3. Release turnstile gate */</span>
    <span class="syn-fn">sem_post</span>(&amp;db_mutex);       <span class="syn-cmt">/* 4. Release database */</span>
}</code></pre>

    <div class="math-callout">
      <strong>Why the Turnstile Prevents Writer Starvation:</strong>
      <br>
      When a writer arrives:
      <ol>
        <li>The writer executes <code>sem_wait(&amp;turnstile)</code> and claims the turnstile gate.</li>
        <li>If newly arriving readers appear, they attempt to execute <code>sem_wait(&amp;turnstile)</code> and <strong>block immediately at the gate behind the writer</strong>!</li>
        <li>The readers currently inside the chamber complete their reads and exit. The last reader sets <code>read_count = 0</code> and executes <code>sem_post(&amp;db_mutex)</code>.</li>
        <li>The writer acquires <code>db_mutex</code>, writes to the database, and releases both locks.</li>
      </ol>
      Readers can no longer jump ahead of an already waiting writer. Both readers and writers experience <strong>strictly bounded waiting times</strong>.
    </div>

    <h4>Production Systems: POSIX pthread_rwlock_t</h4>
    <p>
      In POSIX C systems programming, developers rarely write raw semaphore turnstiles. Instead, the runtime provides native, highly optimized <strong>Read-Write Locks</strong> (<code>pthread_rwlock_t</code>):
    </p>

    <pre><code><span class="syn-cmt">/* Production POSIX Read-Write Lock Usage */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;pthread.h&gt;</span>

<span class="syn-kw">pthread_rwlock_t</span> rwlock = PTHREAD_RWLOCK_INITIALIZER;

<span class="syn-kw">void</span> posix_reader(<span class="syn-kw">void</span>) {
    <span class="syn-fn">pthread_rwlock_rdlock</span>(&amp;rwlock); <span class="syn-cmt">/* Shared lock: multiple readers */</span>
    <span class="syn-fn">read_database</span>();
    <span class="syn-fn">pthread_rwlock_unlock</span>(&amp;rwlock);
}

<span class="syn-kw">void</span> posix_writer(<span class="syn-kw">void</span>) {
    <span class="syn-fn">pthread_rwlock_wrlock</span>(&amp;rwlock); <span class="syn-cmt">/* Exclusive lock: single writer */</span>
    <span class="syn-fn">write_database</span>();
    <span class="syn-fn">pthread_rwlock_unlock</span>(&amp;rwlock);
}</code></pre>

    <p>
      Under the GNU C Library (glibc) on Linux, developers can configure the scheduling attribute via <code>pthread_rwlockattr_setkind_np</code>:
    </p>
    <ul>
      <li><code>PTHREAD_RWLOCK_PREFER_READER_NP</code>: Default behavior (Reader-preference). Fast for read-heavy workloads, but vulnerable to writer starvation.</li>
      <li><code>PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP</code>: Writer-preference. Prevents writer starvation by immediately blocking subsequent readers when a writer queues.</li>
    </ul>

    <h4>The Linux Kernel Revolution: Read-Copy-Update (RCU)</h4>
    <p>
      In modern multi-core operating system kernels, traditional reader-writer locks have a fatal performance flaw: <strong>cacheline bouncing</strong>. Every time a reader acquires <code>rwlock</code>, it must atomically increment an internal reader counter. This atomic write forces cacheline invalidations across all CPU cores, degrading memory bus throughput.
    </p>
    <p>
      To solve this, the Linux kernel relies heavily on <strong>Read-Copy-Update (RCU)</strong>:
    </p>
    <ul>
      <li><strong>Zero-Overhead Readers:</strong> Readers execute with <strong>zero atomic instructions, zero locks, and zero memory bus traffic</strong>. Readers simply enter a read-side critical section by disabling local preemption (<code>rcu_read_lock()</code>).</li>
      <li><strong>Copy-on-Write for Writers:</strong> When a writer mutates a data structure (such as a linked list node), it creates a private duplicate copy, modifies the copy, and atomically overwrites the shared pointer to point to the new node.</li>
      <li><strong>Grace Period Reclamation:</strong> Existing readers continue reading the old node safely. The old memory node is freed only after a <strong>Grace Period</strong> has elapsed&mdash;when every core in the system has undergone at least one voluntary context switch, proving that all concurrent readers have completed.</li>
    </ul>"""

def update_section_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate Section 3 boundaries
    start_marker = "<h3>3. The Readers-Writers Problem</h3>"
    end_marker = "<h4>Windows Readers-Writers &amp; Dispatcher Objects</h4>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_THREE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded and syntax-highlighted Section 3 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 3 of Module 04 with Readers-Writers policies and RCU\n\n"
            "Detail 1st/2nd/3rd variants, starvation proofs, POSIX pthread_rwlock_t,\n"
            "Win32 SRWLOCK, Linux kernel RCU architecture, and add an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_three():
        run_git_sync()
