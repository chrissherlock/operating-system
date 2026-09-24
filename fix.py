#!/usr/bin/env python3
# =====================================================================
# fix.py: Apply syntax highlighting to code snippets in Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "04-classic-synchronization-real-world-defenses.html"
)

NAIVE_OLD = r"""      <pre><code>// Naive Philosopher Routine (Deadlock Prone)
void philosopher(int i) {
    while (true) {
        think();
        wait(chopstick[i]);                 // Grab left chopstick
        wait(chopstick[(i + 1) % 5]);       // Grab right chopstick
        eat();
        signal(chopstick[i]);              // Release left chopstick
        signal(chopstick[(i + 1) % 5]);     // Release right chopstick
    }
}</code></pre>"""

NAIVE_NEW = r"""      <!-- Syntax Highlighted Code Box: Naive Implementation -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.85rem; overflow-x: auto; margin: 16px 0; border: 1px solid var(--border);">
        <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
          c &bull; naive_philosopher.c
        </div>
        <pre style="margin: 0; line-height: 1.5;"><span style="color: #94a3b8;">// Naive Philosopher Routine (Deadlock Prone)</span>
<span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">philosopher</span>(<span style="color: #6ee7b7;">int</span> i) {
    <span style="color: #c084fc;">while</span> (<span style="color: #fbbf24;">true</span>) {
        <span style="color: #60a5fa;">think</span>();
        <span style="color: #60a5fa;">wait</span>(chopstick[i]);                 <span style="color: #94a3b8;">// Grab left chopstick</span>
        <span style="color: #60a5fa;">wait</span>(chopstick[(i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>]);       <span style="color: #94a3b8;">// Grab right chopstick</span>
        <span style="color: #60a5fa;">eat</span>();
        <span style="color: #60a5fa;">signal</span>(chopstick[i]);              <span style="color: #94a3b8;">// Release left chopstick</span>
        <span style="color: #60a5fa;">signal</span>(chopstick[(i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>]);     <span style="color: #94a3b8;">// Release right chopstick</span>
    }
}</pre>
      </div>"""

LIVELOCK_OLD = r"""      <pre><code>// Livelock Hazard
void philosopher_trylock(int i) {
    while (true) {
        think();
        acquire(chopstick[i]);
        if (!try_acquire(chopstick[(i + 1) % 5])) {
            release(chopstick[i]);          // Back off to prevent deadlock
            continue;                       // Retry from the start
        }
        eat();
        release(chopstick[i]);
        release(chopstick[(i + 1) % 5]);
    }
}</code></pre>"""

LIVELOCK_NEW = r"""      <!-- Syntax Highlighted Code Box: Livelock Hazard -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.85rem; overflow-x: auto; margin: 16px 0; border: 1px solid var(--border);">
        <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
          c &bull; livelock_hazard.c
        </div>
        <pre style="margin: 0; line-height: 1.5;"><span style="color: #94a3b8;">// Livelock Hazard (Polite-Retreat Oscillation)</span>
<span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">philosopher_trylock</span>(<span style="color: #6ee7b7;">int</span> i) {
    <span style="color: #c084fc;">while</span> (<span style="color: #fbbf24;">true</span>) {
        <span style="color: #60a5fa;">think</span>();
        <span style="color: #60a5fa;">acquire</span>(chopstick[i]);
        <span style="color: #c084fc;">if</span> (!<span style="color: #60a5fa;">try_acquire</span>(chopstick[(i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>])) {
            <span style="color: #60a5fa;">release</span>(chopstick[i]);          <span style="color: #94a3b8;">// Back off to prevent deadlock</span>
            <span style="color: #c084fc;">continue</span>;                       <span style="color: #94a3b8;">// Retry from the start</span>
        }
        <span style="color: #60a5fa;">eat</span>();
        <span style="color: #60a5fa;">release</span>(chopstick[i]);
        <span style="color: #60a5fa;">release</span>(chopstick[(i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>]);
    }
}</pre>
      </div>"""

def apply_syntax_highlighting():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if NAIVE_OLD in content:
        content = content.replace(NAIVE_OLD, NAIVE_NEW)
    else:
        print("Warning: NAIVE_OLD pattern not matched directly.")

    if LIVELOCK_OLD in content:
        content = content.replace(LIVELOCK_OLD, LIVELOCK_NEW)
    else:
        print("Warning: LIVELOCK_OLD pattern not matched directly.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully applied syntax highlighting to {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if apply_syntax_highlighting():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Apply syntax highlighting to C code blocks in Module 04 Section 1\n\n"
                "Upgrade naive philosopher and livelock code snippets with full syntax\n"
                "highlighting spans and dark header boxes matching curriculum design."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
