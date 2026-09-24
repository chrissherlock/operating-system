#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand and syntax highlight Section 1 in Module 04
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

EXPANDED_SECTION_ONE = r"""    <h3>1. The Bounded-Buffer (Producer-Consumer) Problem</h3>
    <p>
      The <strong>Bounded-Buffer Problem</strong> (originally formulated by Edsger W. Dijkstra) is the definitive architectural archetype for asynchronous decoupled systems.
    </p>
    <p>
      In modern computing, execution threads rarely operate in lockstep. A network card receives ethernet frames at gigabit line rate, an operating system audio server generates PCM audio buffers, and a database storage engine writes transaction log entries asynchronously to NVMe storage. In each scenario, an execution thread producing data must coordinate with an independent execution thread consuming data through a fixed-size storage buffer in memory.
    </p>

    <h4>Formal Problem Specification &amp; System Invariants</h4>
    <p>
      The architecture consists of one or more <strong>producers</strong> and one or more <strong>consumers</strong> sharing a circular ring buffer partitioned into <i>N</i> discrete slots:
    </p>
    <ul>
      <li><strong>Producer Obligation:</strong> Generates data items and deposits them into the buffer. A producer must be <em>blocked</em> from inserting when the buffer is full (<code>count == N</code>).</li>
      <li><strong>Consumer Obligation:</strong> Extracts data items from the buffer and consumes them. A consumer must be <em>blocked</em> from extracting when the buffer is empty (<code>count == 0</code>).</li>
      <li><strong>Mutual Exclusion Invariant:</strong> The physical slots, head/tail pointers, and metadata must never be modified by more than one thread concurrently.</li>
    </ul>

    <!-- Structural Diagram: Circular Ring Buffer Architecture -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.1: Circular Ring Buffer &amp; Tri-Semaphore Architecture</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How counting semaphores track vacant and populated slots while a binary semaphore serializes ring pointer updates.</div>

      <svg viewBox="0 0 760 250" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="bb-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="bb-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="bb-arr-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#d97706" />
          </marker>
        </defs>

        <!-- Circular Buffer Layout (Center) -->
        <g transform="translate(20, 20)">
          <rect width="450" height="210" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="20" y="26" font-size="10.5" font-weight="700" fill="#0284c7">CIRCULAR BUFFER RING (Capacity N = 5)</text>

          <!-- Slots 0..4 -->
          <g transform="translate(20, 45)">
            <!-- Slot 0: Full -->
            <rect x="0" y="0" width="76" height="60" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="38" y="22" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">SLOT 0</text>
            <text x="38" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" fill="#dc2626">[Item 0]</text>
            <text x="38" y="52" text-anchor="middle" font-size="7" fill="#7f1d1d">FULL</text>

            <!-- Slot 1: Full -->
            <rect x="83" y="0" width="76" height="60" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="121" y="22" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">SLOT 1</text>
            <text x="121" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" fill="#dc2626">[Item 1]</text>
            <text x="121" y="52" text-anchor="middle" font-size="7" fill="#7f1d1d">FULL</text>

            <!-- Slot 2: Full -->
            <rect x="166" y="0" width="76" height="60" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="204" y="22" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">SLOT 2</text>
            <text x="204" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" fill="#dc2626">[Item 2]</text>
            <text x="204" y="52" text-anchor="middle" font-size="7" fill="#7f1d1d">FULL</text>

            <!-- Slot 3: Empty -->
            <rect x="249" y="0" width="76" height="60" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
            <text x="287" y="22" text-anchor="middle" font-size="8" font-weight="700" fill="#64748b">SLOT 3</text>
            <text x="287" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#94a3b8">[Empty]</text>
            <text x="287" y="52" text-anchor="middle" font-size="7" fill="#64748b">VACANT</text>

            <!-- Slot 4: Empty -->
            <rect x="332" y="0" width="76" height="60" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
            <text x="370" y="22" text-anchor="middle" font-size="8" font-weight="700" fill="#64748b">SLOT 4</text>
            <text x="370" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#94a3b8">[Empty]</text>
            <text x="370" y="52" text-anchor="middle" font-size="7" fill="#64748b">VACANT</text>
          </g>

          <!-- Pointer Vectors -->
          <g transform="translate(20, 115)">
            <!-- Head Pointer (Producer Target) -->
            <rect x="235" y="10" width="105" height="34" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="287" y="25" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0369a1">head pointer = 3</text>
            <text x="287" y="37" text-anchor="middle" font-size="7" fill="#0284c7">&uarr; Next Producer Write</text>

            <!-- Tail Pointer (Consumer Target) -->
            <rect x="-10" y="10" width="98" height="34" rx="4" fill="#fef3c7" stroke="#d97706"/>
            <text x="39" y="25" text-anchor="middle" font-size="7.5" font-weight="700" fill="#92400e">tail pointer = 0</text>
            <text x="39" y="37" text-anchor="middle" font-size="7" fill="#b45309">&uarr; Next Consumer Read</text>
          </g>

          <!-- Conservation Equation Banner -->
          <rect x="20" y="165" width="408" height="32" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="224" y="185" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#0f172a">empty (2) + full (3) = N (5) [CONSERVED]</text>
        </g>

        <!-- Tri-Semaphore Registry (Right) -->
        <g transform="translate(485, 20)">
          <rect width="255" height="210" rx="8" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="16" y="24" font-size="10.5" font-weight="700" fill="#0f172a">TRI-SEMAPHORE STATE</text>

          <!-- Semaphore 1: empty -->
          <rect x="12" y="36" width="230" height="48" rx="4" fill="#f0f9ff" stroke="#0284c7"/>
          <text x="20" y="52" font-size="8" font-weight="700" fill="#0369a1">COUNTING: empty = 2</text>
          <text x="20" y="66" font-size="7.5" fill="#0284c7">Tracks vacant slots &bull; Producer down(&amp;empty)</text>
          <text x="20" y="77" font-size="7" fill="#64748b">Blocks producer when empty == 0</text>

          <!-- Semaphore 2: full -->
          <rect x="12" y="90" width="230" height="48" rx="4" fill="#fef2f2" stroke="#dc2626"/>
          <text x="20" y="106" font-size="8" font-weight="700" fill="#991b1b">COUNTING: full = 3</text>
          <text x="20" y="120" font-size="7.5" fill="#dc2626">Tracks populated slots &bull; Consumer down(&amp;full)</text>
          <text x="20" y="131" font-size="7" fill="#64748b">Blocks consumer when full == 0</text>

          <!-- Semaphore 3: mutex -->
          <rect x="12" y="144" width="230" height="52" rx="4" fill="#f0fdf4" stroke="#16a34a"/>
          <text x="20" y="160" font-size="8" font-weight="700" fill="#166534">BINARY: mutex = 1 (FREE)</text>
          <text x="20" y="174" font-size="7.5" fill="#15803d">Enforces exclusive critical section access</text>
          <text x="20" y="185" font-size="7" fill="#64748b">Guards ring pointers and buffer arrays</text>
        </g>
      </svg>
    </div>

    <h4>The Tri-Semaphore Architecture</h4>
    <p>
      To solve the bounded-buffer problem without busy waiting, Dijkstra established the canonical <strong>tri-semaphore architecture</strong>:
    </p>
    <div class="math-callout">
      <strong>Semaphore Initialization and Invariants:</strong>
      <pre><code><span class="syn-kw">semaphore_t</span> mutex; <span class="syn-cmt">/* Binary semaphore: initialized to 1 (Buffer locked = 0, free = 1) */</span>
<span class="syn-kw">semaphore_t</span> empty; <span class="syn-cmt">/* Counting semaphore: initialized to N (Vacant slots available) */</span>
<span class="syn-kw">semaphore_t</span> full;  <span class="syn-cmt">/* Counting semaphore: initialized to 0 (Populated items available) */</span></code></pre>
      <strong>The Fundamental Conservation Law:</strong>
      <br>
      At any instant in time, the sum of vacant slots and filled items must strictly equal the buffer capacity:
      <pre><code>empty + full = N</code></pre>
    </div>

    <h4>Complete POSIX C Implementation</h4>
    <p>
      Below is the complete, industrial-grade implementation using POSIX semaphores (<code>semaphore.h</code>):
    </p>

    <pre><code><span class="syn-cmt">/* Production Bounded-Buffer Implementation Using POSIX Semaphores */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;semaphore.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;pthread.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;stdbool.h&gt;</span>

<span class="syn-kw">#define</span> BUFFER_CAPACITY <span class="syn-num">8</span>

<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">int</span> data[BUFFER_CAPACITY];
    <span class="syn-kw">int</span> head;                  <span class="syn-cmt">/* Index for next insert: head = (head + 1) % N */</span>
    <span class="syn-kw">int</span> tail;                  <span class="syn-cmt">/* Index for next remove: tail = (tail + 1) % N */</span>
    <span class="syn-kw">sem_t</span> mutex;               <span class="syn-cmt">/* Binary semaphore guarding buffer pointers */</span>
    <span class="syn-kw">sem_t</span> empty;               <span class="syn-cmt">/* Counting semaphore tracking vacant slots */</span>
    <span class="syn-kw">sem_t</span> full;                <span class="syn-cmt">/* Counting semaphore tracking available items */</span>
} bounded_buffer_t;

<span class="syn-kw">void</span> buffer_init(bounded_buffer_t *b) {
    b-&gt;head = <span class="syn-num">0</span>;
    b-&gt;tail = <span class="syn-num">0</span>;
    <span class="syn-fn">sem_init</span>(&amp;b-&gt;mutex, <span class="syn-num">0</span>, <span class="syn-num">1</span>);               <span class="syn-cmt">/* Binary mutex: init 1 */</span>
    <span class="syn-fn">sem_init</span>(&amp;b-&gt;empty, <span class="syn-num">0</span>, BUFFER_CAPACITY); <span class="syn-cmt">/* Empty slots: init N */</span>
    <span class="syn-fn">sem_init</span>(&amp;b-&gt;full,  <span class="syn-num">0</span>, <span class="syn-num">0</span>);               <span class="syn-cmt">/* Full items: init 0 */</span>
}

<span class="syn-kw">void</span> buffer_produce(bounded_buffer_t *b, <span class="syn-kw">int</span> item) {
    <span class="syn-fn">sem_wait</span>(&amp;b-&gt;empty); <span class="syn-cmt">/* 1. Decrement empty slots (Blocks if buffer full!) */</span>
    <span class="syn-fn">sem_wait</span>(&amp;b-&gt;mutex); <span class="syn-cmt">/* 2. Acquire critical section lock */</span>

    <span class="syn-cmt">/* Critical Section: Insert item into circular ring */</span>
    b-&gt;data[b-&gt;head] = item;
    b-&gt;head = (b-&gt;head + <span class="syn-num">1</span>) % BUFFER_CAPACITY;

    <span class="syn-fn">sem_post</span>(&amp;b-&gt;mutex); <span class="syn-cmt">/* 3. Release critical section lock */</span>
    <span class="syn-fn">sem_post</span>(&amp;b-&gt;full);  <span class="syn-cmt">/* 4. Increment full items (Wakes waiting consumer) */</span>
}

<span class="syn-kw">int</span> buffer_consume(bounded_buffer_t *b) {
    <span class="syn-fn">sem_wait</span>(&amp;b-&gt;full);  <span class="syn-cmt">/* 1. Decrement full items (Blocks if buffer empty!) */</span>
    <span class="syn-fn">sem_wait</span>(&amp;b-&gt;mutex); <span class="syn-cmt">/* 2. Acquire critical section lock */</span>

    <span class="syn-cmt">/* Critical Section: Extract item from circular ring */</span>
    <span class="syn-kw">int</span> item = b-&gt;data[b-&gt;tail];
    b-&gt;tail = (b-&gt;tail + <span class="syn-num">1</span>) % BUFFER_CAPACITY;

    <span class="syn-fn">sem_post</span>(&amp;b-&gt;mutex); <span class="syn-cmt">/* 3. Release critical section lock */</span>
    <span class="syn-fn">sem_post</span>(&amp;b-&gt;empty); <span class="syn-cmt">/* 4. Increment empty slots (Wakes waiting producer) */</span>

    <span class="syn-kw">return</span> item;
}</code></pre>

    <h4>The Deadlock Inversion Trap &amp; Resource Allocation Graphs</h4>
    <p>
      In concurrent algorithm design, <strong>the order of lock acquisition dictates system liveness</strong>.
    </p>
    <p>
      Consider the catastrophic defect that occurs if an inexperienced developer swaps the order of the two wait calls in the producer routine:
    </p>

    <pre><code><span class="syn-cmt">/* FATAL: Inverted Lock Acquisition Ordering */</span>
<span class="syn-kw">void</span> flawed_producer(bounded_buffer_t *b, <span class="syn-kw">int</span> item) {
    <span class="syn-fn">sem_wait</span>(&amp;b-&gt;mutex); <span class="syn-cmt">/* STEP 1: Claim mutex FIRST (Catastrophic Error!) */</span>
    <span class="syn-fn">sem_wait</span>(&amp;b-&gt;empty); <span class="syn-cmt">/* STEP 2: Check empty slot availability */</span>

    b-&gt;data[b-&gt;head] = item;
    b-&gt;head = (b-&gt;head + <span class="syn-num">1</span>) % BUFFER_CAPACITY;

    <span class="syn-fn">sem_post</span>(&amp;b-&gt;mutex);
    <span class="syn-fn">sem_post</span>(&amp;b-&gt;full);
}</code></pre>

    <div class="math-callout">
      <strong>Anatomy of the Inversion Deadlock:</strong>
      <ol>
        <li>Suppose the buffer is full (<code>empty == 0</code>).</li>
        <li>The Producer executes <code>sem_wait(&amp;b-&gt;mutex)</code>. Because <code>mutex == 1</code>, the Producer acquires the lock (<code>mutex</code> drops to <code>0</code>).</li>
        <li>The Producer executes <code>sem_wait(&amp;b-&gt;empty)</code>. Because <code>empty == 0</code>, the Producer is suspended and moved to the <code>empty</code> wait queue. <strong>Crucially, the Producer is put to sleep while still holding the mutex!</strong></li>
        <li>The Consumer is scheduled. To free up a buffer slot, it must consume an item. It executes <code>sem_wait(&amp;b-&gt;full)</code> (which succeeds, as items exist).</li>
        <li>The Consumer then executes <code>sem_wait(&amp;b-&gt;mutex)</code>. Because the sleeping Producer holds <code>mutex</code>, <strong>the Consumer blocks immediately</strong>!</li>
      </ol>
      <strong>The Circular Wait Dependency (Deadlock):</strong>
      <br>
      The Producer holds <code>mutex</code> and is waiting for <code>empty</code> (which can only be produced by the Consumer).
      <br>
      The Consumer holds <code>full</code> and is waiting for <code>mutex</code> (which is held by the Producer).
      <pre><code>[Producer] &rarr; (holds mutex) &rarr; [blocks on empty] &larr; (produced by Consumer)
   &uarr;                                                      &darr;
   &plusmn;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash; [Consumer blocks on mutex] &larr;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&plusmn;</code></pre>
      Neither thread can ever make progress. The system is permanently locked.
    </div>

    <h4>The Win32 Windows Alternative</h4>
    <p>
      On Windows, the Bounded-Buffer problem can be implemented using native <strong>Win32 Kernel Semaphore Handles</strong>:
    </p>

    <pre><code><span class="syn-cmt">/* Windows Win32 Bounded-Buffer Implementation */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>

<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">int</span> data[BUFFER_CAPACITY];
    <span class="syn-kw">int</span> head, tail;
    HANDLE hMutex; <span class="syn-cmt">/* Mutex object or CRITICAL_SECTION */</span>
    HANDLE hEmpty; <span class="syn-cmt">/* Counting semaphore: init N, max N */</span>
    HANDLE hFull;  <span class="syn-cmt">/* Counting semaphore: init 0, max N */</span>
} win_bounded_buffer_t;

<span class="syn-kw">void</span> win_produce(win_bounded_buffer_t *b, <span class="syn-kw">int</span> item) {
    <span class="syn-fn">WaitForSingleObject</span>(b-&gt;hEmpty, INFINITE); <span class="syn-cmt">/* 1. Wait for vacant slot */</span>
    <span class="syn-fn">WaitForSingleObject</span>(b-&gt;hMutex, INFINITE); <span class="syn-cmt">/* 2. Acquire buffer lock */</span>

    b-&gt;data[b-&gt;head] = item;
    b-&gt;head = (b-&gt;head + <span class="syn-num">1</span>) % BUFFER_CAPACITY;

    <span class="syn-fn">ReleaseMutex</span>(b-&gt;hMutex);                  <span class="syn-cmt">/* 3. Release buffer lock */</span>
    <span class="syn-fn">ReleaseSemaphore</span>(b-&gt;hFull, <span class="syn-num">1</span>, NULL);      <span class="syn-cmt">/* 4. Signal populated item */</span>
}</code></pre>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate Section 1 boundaries
    start_marker = "<h3>1. The Bounded-Buffer (Producer-Consumer) Problem</h3>"
    end_marker = "<!-- Directed Narrative Stepper: Bounded Buffer Deadlock vs Correct -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_ONE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded and syntax-highlighted Section 1 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand and syntax-highlight Bounded-Buffer section in Module 04\n\n"
            "Add circular ring math invariants, tri-semaphore conservation formulas,\n"
            "deadlock RAG graph trace, POSIX vs. Win32 code, and an SVG architecture diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
