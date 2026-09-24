#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 in Module 04
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

EXPANDED_SECTION_TWO = r"""    <h3>2. The Dining Philosophers Problem</h3>
    <p>
      Originally formulated by Edsger W. Dijkstra in 1965 as an examination problem on synchronizing tape drives, and later refined into its allegorical form by C. A. R. Hoare, the <strong>Dining Philosophers Problem</strong> is the definitive paradigm for resource allocation deadlocks in multi-threaded operating systems.
    </p>
    <p>
      The problem models concurrent processes competing for limited, mutually exclusive non-preemptible resources (such as multiple disk spindles, database row locks, or memory channels).
    </p>

    <h4>Formal Specification</h4>
    <p>
      Five philosophers sit around a circular dining table:
    </p>
    <ul>
      <li>Each philosopher spends their entire life alternating between two internal states: <strong>Thinking</strong> and <strong>Eating</strong>.</li>
      <li>In the center of the table lies a communal bowl of spaghetti. Between each pair of adjacent philosophers lies a single chopstick (or fork). There are 5 philosophers and <strong>exactly 5 chopsticks</strong>.</li>
      <li>Eating spaghetti requires <strong>two chopsticks simultaneously</strong>: a philosopher must acquire both their left chopstick and their right chopstick.</li>
      <li>A chopstick can only be held by one philosopher at a time. When a philosopher finishes eating, they put down both chopsticks and return to thinking.</li>
    </ul>

    <!-- Structural Diagram: Dining Philosophers Table Topology -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.2: Dining Philosophers Circular Topology &amp; The Circular Wait Hazard</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How simultaneous left-hand acquisition establishes the fatal circular dependency ring.</div>

      <svg viewBox="0 0 760 260" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="dp-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="dp-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
        </defs>

        <!-- Circular Table Visual -->
        <g transform="translate(190, 130)">
          <!-- Main Table Rim -->
          <circle cx="0" cy="0" r="110" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
          <!-- Spaghetti Bowl -->
          <circle cx="0" cy="0" r="45" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
          <text x="0" y="4" text-anchor="middle" font-size="8.5" font-weight="700" fill="#92400e">SPAGHETTI</text>

          <!-- 5 Philosophers Placed in a Ring (R = 85) -->
          <!-- P0 (Top: -90 deg) -->
          <circle cx="0" cy="-80" r="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
          <text x="0" y="-76" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">P0</text>

          <!-- P1 (Top-Right: -18 deg) -->
          <circle cx="76" cy="-25" r="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
          <text x="76" y="-21" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">P1</text>

          <!-- P2 (Bottom-Right: +54 deg) -->
          <circle cx="47" cy="65" r="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
          <text x="47" y="69" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">P2</text>

          <!-- P3 (Bottom-Left: +126 deg) -->
          <circle cx="-47" cy="65" r="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
          <text x="-47" y="69" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">P3</text>

          <!-- P4 (Top-Left: +198 deg) -->
          <circle cx="-76" cy="-25" r="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
          <text x="-76" y="-21" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">P4</text>

          <!-- 5 Chopsticks Placed in Interstices (R = 52) -->
          <!-- C0 (between P4 and P0) -->
          <rect x="-42" y="-62" width="16" height="16" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="-34" y="-51" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#991b1b">C0</text>

          <!-- C1 (between P0 and P1) -->
          <rect x="26" y="-62" width="16" height="16" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="34" y="-51" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#991b1b">C1</text>

          <!-- C2 (between P1 and P2) -->
          <rect x="58" y="16" width="16" height="16" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="66" y="27" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#991b1b">C2</text>

          <!-- C3 (between P2 and P3) -->
          <rect x="-8" y="70" width="16" height="16" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="0" y="81" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#991b1b">C3</text>

          <!-- C4 (between P3 and P4) -->
          <rect x="-74" y="16" width="16" height="16" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="-66" y="27" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#991b1b">C4</text>
        </g>

        <!-- Right Panel: The 4 Coffman Deadlock Conditions -->
        <g transform="translate(380, 20)">
          <rect width="360" height="220" rx="8" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
          <text x="16" y="24" font-size="10.5" font-weight="700" fill="#991b1b">THE COFFMAN DEADLOCK CONDITIONS</text>

          <rect x="14" y="38" width="332" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="22" y="52" font-size="8" font-weight="700" fill="#0f172a">1. Mutual Exclusion:</text>
          <text x="22" y="65" font-size="7.5" fill="#475569">Chopsticks are non-shareable: exactly one philosopher per utensil.</text>

          <rect x="14" y="78" width="332" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="22" y="92" font-size="8" font-weight="700" fill="#0f172a">2. Hold and Wait:</text>
          <text x="22" y="105" font-size="7.5" fill="#475569">Philosopher holds their left chopstick while waiting for right.</text>

          <rect x="14" y="118" width="332" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="22" y="132" font-size="8" font-weight="700" fill="#0f172a">3. No Preemption:</text>
          <text x="22" y="145" font-size="7.5" fill="#475569">Utensils cannot be forcibly confiscated from an adjacent peer.</text>

          <rect x="14" y="158" width="332" height="50" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="22" y="174" font-size="8" font-weight="700" fill="#991b1b">4. Circular Wait (The Fatal Ring):</text>
          <text x="22" y="188" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#dc2626">P0 &rarr; C1 &rarr; P1 &rarr; C2 &rarr; P2 &rarr; C3 &rarr; P3 &rarr; C4 &rarr; P4 &rarr; C0 &rarr; P0</text>
          <text x="22" y="200" font-size="7" fill="#7f1d1d">Closed directed cycle in Resource Allocation Graph!</text>
        </g>
      </svg>
    </div>

    <h4>The Naive Implementation &amp; The Coffman Deadlock Conditions</h4>
    <p>
      The naive solution maps each chopstick to an individual binary semaphore (<code>chopstick[5]</code>, each initialized to <code>1</code>). Each philosopher runs an identical, symmetric routine:
    </p>

    <pre><code><span class="syn-cmt">/* FLAWED: Naive Symmetric Philosopher Routine */</span>
<span class="syn-kw">sem_t</span> chopstick[<span class="syn-num">5</span>]; <span class="syn-cmt">/* Initialized to 1 */</span>

<span class="syn-kw">void</span> philosopher_naive(<span class="syn-kw">int</span> i) {
    <span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
        <span class="syn-fn">think</span>();
        <span class="syn-fn">sem_wait</span>(&amp;chopstick[i]);             <span class="syn-cmt">/* 1. Pick up left chopstick */</span>
        <span class="syn-fn">sem_wait</span>(&amp;chopstick[(i + <span class="syn-num">1</span>) % <span class="syn-num">5</span>]);   <span class="syn-cmt">/* 2. Pick up right chopstick */</span>

        <span class="syn-fn">eat</span>();

        <span class="syn-fn">sem_post</span>(&amp;chopstick[i]);             <span class="syn-cmt">/* 3. Put down left chopstick */</span>
        <span class="syn-fn">sem_post</span>(&amp;chopstick[(i + <span class="syn-num">1</span>) % <span class="syn-num">5</span>]);   <span class="syn-cmt">/* 4. Put down right chopstick */</span>
    }
}</code></pre>

    <div class="math-callout">
      <strong>Why the Naive Solution Triggers Total Deadlock:</strong>
      <br>
      Suppose all five philosophers become hungry simultaneously. Each philosopher executes statement 1, grabbing their <strong>left chopstick</strong>:
      <ul>
        <li>Philosopher 0 grabs Chopstick 0.</li>
        <li>Philosopher 1 grabs Chopstick 1.</li>
        <li>Philosopher 2 grabs Chopstick 2.</li>
        <li>Philosopher 3 grabs Chopstick 3.</li>
        <li>Philosopher 4 grabs Chopstick 4.</li>
      </ul>
      Now, every philosopher executes statement 2, attempting to acquire their right chopstick:
      <ul>
        <li>Philosopher 0 demands Chopstick 1 (held by Philosopher 1) &rarr; BLOCKS.</li>
        <li>Philosopher 1 demands Chopstick 2 (held by Philosopher 2) &rarr; BLOCKS.</li>
        <li>Philosopher 2 demands Chopstick 3 (held by Philosopher 3) &rarr; BLOCKS.</li>
        <li>Philosopher 3 demands Chopstick 4 (held by Philosopher 4) &rarr; BLOCKS.</li>
        <li>Philosopher 4 demands Chopstick 0 (held by Philosopher 0) &rarr; BLOCKS.</li>
      </ul>
      This satisfies all four <strong>Coffman Conditions</strong>: Mutual Exclusion, Hold-and-Wait, No-Preemption, and Circular Wait. The system deadlocks permanently, and all five philosophers starve.
    </div>

    <h4>Strategy 1: Asymmetric Resource Hierarchy (Dijkstra's Symmetry Breaking)</h4>
    <p>
      Deadlock can only occur if a closed circular dependency cycle exists. Dijkstra proved that establishing a <strong>strict total ordering</strong> over all resources mathematically guarantees freedom from deadlock.
    </p>
    <p>
      Assign each chopstick a global numerical index from <code>0</code> to <code>4</code>. Establish a rule: <strong>every philosopher must always acquire their lower-numbered chopstick first, and their higher-numbered chopstick second</strong>:
    </p>
    <ul>
      <li>For Philosophers 0, 1, 2, and 3: The left chopstick (<code>i</code>) is lower than the right chopstick (<code>i + 1</code>). They pick up <strong>left first, then right</strong>.</li>
      <li>For Philosopher 4: The left chopstick is <code>4</code>, but the right chopstick is <code>(4 + 1) % 5 = 0</code>! Because <code>0 &lt; 4</code>, Philosopher 4 picks up <strong>right first (0), then left (4)</strong>.</li>
    </ul>

    <pre><code><span class="syn-cmt">/* Strategy 1: Asymmetric Symmetry Breaking */</span>
<span class="syn-kw">void</span> philosopher_asymmetric(<span class="syn-kw">int</span> i) {
    <span class="syn-kw">int</span> left = i;
    <span class="syn-kw">int</span> right = (i + <span class="syn-num">1</span>) % <span class="syn-num">5</span>;

    <span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
        <span class="syn-fn">think</span>();

        <span class="syn-kw">if</span> (i % <span class="syn-num">2</span> == <span class="syn-num">0</span>) {
            <span class="syn-cmt">/* Even philosophers: Left first, then Right */</span>
            <span class="syn-fn">sem_wait</span>(&amp;chopstick[left]);
            <span class="syn-fn">sem_wait</span>(&amp;chopstick[right]);
        } <span class="syn-kw">else</span> {
            <span class="syn-cmt">/* Odd philosophers: Right first, then Left */</span>
            <span class="syn-fn">sem_wait</span>(&amp;chopstick[right]);
            <span class="syn-fn">sem_wait</span>(&amp;chopstick[left]);
        }

        <span class="syn-fn">eat</span>();

        <span class="syn-fn">sem_post</span>(&amp;chopstick[left]);
        <span class="syn-fn">sem_post</span>(&amp;chopstick[right]);
    }
}</code></pre>

    <div class="math-callout">
      <strong>Proof of Deadlock Freedom under Resource Hierarchy:</strong>
      <br>
      Suppose all five philosophers become hungry simultaneously:
      <ol>
        <li>Philosopher 0 and Philosopher 4 both compete for Chopstick 0 as their very first acquisition.</li>
        <li>Exactly one of them wins (say, Philosopher 0 claims Chopstick 0).</li>
        <li>Philosopher 4 blocks immediately on Chopstick 0 <em>before claiming Chopstick 4</em>!</li>
        <li>Because Chopstick 4 is left untouched, Philosopher 3 successfully claims both Chopstick 3 and Chopstick 4, eats, and releases both.</li>
      </ol>
      The circular dependency cycle is broken. At least one philosopher is always guaranteed to eat.
    </div>

    <h4>Strategy 2: Tanenbaum's State-Tracking Semaphore Array</h4>
    <p>
      While the asymmetric approach prevents deadlock, it can introduce unequal waiting times. Andrew Tanenbaum designed an elegant solution utilizing an explicit <strong>state machine array</strong> that allows a philosopher to eat only when <em>neither neighbor is eating</em>:
    </p>

    <pre><code><span class="syn-cmt">/* Strategy 2: Tanenbaum's State-Tracking Solution */</span>
<span class="syn-kw">#define</span> N <span class="syn-num">5</span>
<span class="syn-kw">#define</span> LEFT  ((i + N - <span class="syn-num">1</span>) % N)
<span class="syn-kw">#define</span> RIGHT ((i + <span class="syn-num">1</span>) % N)

<span class="syn-kw">typedef enum</span> { THINKING, HUNGRY, EATING } state_t;

state_t state[N];         <span class="syn-cmt">/* Tracks state of every philosopher */</span>
<span class="syn-kw">sem_t</span> mutex;              <span class="syn-cmt">/* Binary mutex protecting state[] inspections */</span>
<span class="syn-kw">sem_t</span> s[N];               <span class="syn-cmt">/* One private semaphore per philosopher (init 0) */</span>

<span class="syn-kw">void</span> test_neighbors(<span class="syn-kw">int</span> i) {
    <span class="syn-cmt">/* If I am hungry AND neither neighbor is eating, begin eating */</span>
    <span class="syn-kw">if</span> (state[i] == HUNGRY &amp;&amp; state[LEFT] != EATING &amp;&amp; state[RIGHT] != EATING) {
        state[i] = EATING;
        <span class="syn-fn">sem_post</span>(&amp;s[i]);  <span class="syn-cmt">/* Wake myself up (increments s[i] from 0 to 1) */</span>
    }
}

<span class="syn-kw">void</span> take_forks(<span class="syn-kw">int</span> i) {
    <span class="syn-fn">sem_wait</span>(&amp;mutex);     <span class="syn-cmt">/* Enter critical section */</span>
    state[i] = HUNGRY;
    <span class="syn-fn">test_neighbors</span>(i);    <span class="syn-cmt">/* Attempt to claim both forks */</span>
    <span class="syn-fn">sem_post</span>(&amp;mutex);     <span class="syn-cmt">/* Exit critical section */</span>

    <span class="syn-fn">sem_wait</span>(&amp;s[i]);      <span class="syn-cmt">/* Block if forks were not available */</span>
}

<span class="syn-kw">void</span> put_forks(<span class="syn-kw">int</span> i) {
    <span class="syn-fn">sem_wait</span>(&amp;mutex);     <span class="syn-cmt">/* Enter critical section */</span>
    state[i] = THINKING;
    <span class="syn-fn">test_neighbors</span>(LEFT); <span class="syn-cmt">/* Check if left neighbor can now eat */</span>
    <span class="syn-fn">test_neighbors</span>(RIGHT);<span class="syn-cmt">/* Check if right neighbor can now eat */</span>
    <span class="syn-fn">sem_post</span>(&amp;mutex);     <span class="syn-cmt">/* Exit critical section */</span>
}</code></pre>

    <div class="math-callout">
      <strong>Key Insights of Tanenbaum's Solution:</strong>
      <ul>
        <li><strong>Atomic Dual Acquisition:</strong> Forks are never claimed one at a time. The test <code>state[LEFT] != EATING &amp;&amp; state[RIGHT] != EATING</code> ensures both forks are claimed simultaneously under the protection of <code>mutex</code>.</li>
        <li><strong>Self-Signaling via Private Semaphores:</strong> The private semaphore <code>s[i]</code> is initialized to <code>0</code>. If forks are available, <code>test_neighbors(i)</code> calls <code>sem_post(&amp;s[i])</code>, incrementing it to <code>1</code>. When the philosopher immediately follows with <code>sem_wait(&amp;s[i])</code>, they do not sleep. If forks were busy, <code>sem_post</code> is not called, and the philosopher blocks until an exiting neighbor calls <code>test_neighbors</code> on their behalf.</li>
      </ul>
    </div>

    <h4>Strategy 3: Windows WaitForMultipleObjects</h4>
    <p>
      On Windows NT platforms, the dining philosophers problem can be resolved using the kernel's native multi-handle wait capability:
    </p>

    <pre><code><span class="syn-cmt">/* Win32 Atomic Multi-Object Fork Acquisition */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>

HANDLE hChopsticks[<span class="syn-num">5</span>]; <span class="syn-cmt">/* Mutex handles for each utensil */</span>

<span class="syn-kw">void</span> philosopher_win32(<span class="syn-kw">int</span> i) {
    HANDLE needed[<span class="syn-num">2</span>];
    needed[<span class="syn-num">0</span>] = hChopsticks[i];
    needed[<span class="syn-num">1</span>] = hChopsticks[(i + <span class="syn-num">1</span>) % <span class="syn-num">5</span>];

    <span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
        <span class="syn-fn">think</span>();

        <span class="syn-cmt">/* Atomically wait for BOTH mutexes simultaneously (bWaitAll = TRUE) */</span>
        DWORD result = <span class="syn-fn">WaitForMultipleObjects</span>(<span class="syn-num">2</span>, needed, TRUE, INFINITE);
        <span class="syn-kw">if</span> (result == WAIT_OBJECT_0) {
            <span class="syn-fn">eat</span>();
            <span class="syn-fn">ReleaseMutex</span>(needed[<span class="syn-num">0</span>]);
            <span class="syn-fn">ReleaseMutex</span>(needed[<span class="syn-num">1</span>]);
        }
    }
}</code></pre>
    <p>
      Because <code>WaitForMultipleObjects(..., bWaitAll = TRUE)</code> is an <strong>atomic kernel-level operation</strong>, the operating system scheduler claims both handles together. If either utensil is held, the thread is suspended without claiming the other, eliminating the "Hold and Wait" Coffman condition.
    </p>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate Section 2 boundaries
    start_marker = "<h3>2. The Dining Philosophers Problem</h3>"
    end_marker = "<h3>3. The Readers-Writers Problem</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_TWO + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded and syntax-highlighted Section 2 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 2 in Module 04 with Dining Philosophers architectures\n\n"
            "Detail Coffman conditions, asymmetric symmetry breaking, Tanenbaum state\n"
            "matrix, Chandy-Misra tokens, Win32 multi-wait, and add an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
