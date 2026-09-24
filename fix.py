#!/usr/bin/env python3
# =====================================================================
# fix.py: Embed architectural NPTL diagrams into Section 3 of Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "04-thread-implementation.html")

def inject_section_three_diagrams():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # -----------------------------------------------------------------
    # Diagram 1: PID vs. TGID & Thread Group Topology
    # -----------------------------------------------------------------
    diagram_tgid = r"""
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.1: Linux Thread Group Hierarchy (PID vs. TGID Representation)</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Every thread is an independent task_struct, unified under a shared TGID matching the Group Leader's PID.</div>

      <svg viewBox="0 0 820 320" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="nptl-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
          <marker id="leader-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Outer Parent (bash shell) -->
        <g transform="translate(290, 15)">
          <rect width="240" height="50" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3"/>
          <text x="120" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="#334155">PARENT PROCESS (e.g. bash / PID 2000)</text>
          <text x="120" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">real_parent of all threads in this group</text>
        </g>

        <!-- Task 1: Thread Group Leader -->
        <g transform="translate(30, 105)">
          <rect width="230" height="195" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <rect width="230" height="28" rx="6" fill="#0284c7"/>
          <text x="115" y="19" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">task_struct (Group Leader)</text>

          <rect x="15" y="38" width="200" height="26" rx="3" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="25" y="55" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">pid  = 4010 (TID: 4010)</text>

          <rect x="15" y="70" width="200" height="26" rx="3" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="87" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">tgid = 4010 (POSIX PID)</text>

          <rect x="15" y="102" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="118" font-family="var(--font-mono)" font-size="9" fill="#334155">group_leader &rarr; points to self</text>

          <rect x="15" y="132" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="148" font-family="var(--font-mono)" font-size="9" fill="#334155">real_parent  &rarr; bash (2000)</text>

          <rect x="15" y="162" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="178" font-family="var(--font-mono)" font-size="9" fill="#334155">mm, files, sighand (Shared)</text>
        </g>

        <!-- Task 2: Sibling Thread 1 -->
        <g transform="translate(295, 105)">
          <rect width="230" height="195" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <rect width="230" height="28" rx="6" fill="#0284c7"/>
          <text x="115" y="19" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">task_struct (Sibling 1)</text>

          <rect x="15" y="38" width="200" height="26" rx="3" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="25" y="55" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">pid  = 4011 (TID: 4011)</text>

          <rect x="15" y="70" width="200" height="26" rx="3" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="87" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">tgid = 4010 (POSIX PID)</text>

          <rect x="15" y="102" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="118" font-family="var(--font-mono)" font-size="9" fill="#334155">group_leader &rarr; Task 4010</text>

          <rect x="15" y="132" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="148" font-family="var(--font-mono)" font-size="9" fill="#334155">real_parent  &rarr; bash (2000)</text>

          <rect x="15" y="162" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="178" font-family="var(--font-mono)" font-size="9" fill="#334155">mm, files, sighand (Shared)</text>
        </g>

        <!-- Task 3: Sibling Thread 2 -->
        <g transform="translate(560, 105)">
          <rect width="230" height="195" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <rect width="230" height="28" rx="6" fill="#0284c7"/>
          <text x="115" y="19" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">task_struct (Sibling 2)</text>

          <rect x="15" y="38" width="200" height="26" rx="3" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="25" y="55" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">pid  = 4012 (TID: 4012)</text>

          <rect x="15" y="70" width="200" height="26" rx="3" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="87" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">tgid = 4010 (POSIX PID)</text>

          <rect x="15" y="102" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="118" font-family="var(--font-mono)" font-size="9" fill="#334155">group_leader &rarr; Task 4010</text>

          <rect x="15" y="132" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="148" font-family="var(--font-mono)" font-size="9" fill="#334155">real_parent  &rarr; bash (2000)</text>

          <rect x="15" y="162" width="200" height="24" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="178" font-family="var(--font-mono)" font-size="9" fill="#334155">mm, files, sighand (Shared)</text>
        </g>

        <!-- real_parent Linkages to bash -->
        <path d="M 145 105 C 145 75, 290 50, 310 50" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#nptl-arr)"/>
        <path d="M 410 105 L 410 65" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#nptl-arr)"/>
        <path d="M 675 105 C 675 75, 530 50, 510 50" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#nptl-arr)"/>

        <!-- thread_group Circular Linkages Between Siblings -->
        <path d="M 260 215 L 295 215" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#nptl-arr)"/>
        <path d="M 295 230 L 260 230" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#nptl-arr)"/>

        <path d="M 525 215 L 560 215" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#nptl-arr)"/>
        <path d="M 560 230 L 525 230" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#nptl-arr)"/>

        <path d="M 790 220 C 815 220, 815 285, 410 285 C 15 285, 15 220, 30 220" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="4 2" marker-end="url(#nptl-arr)"/>
        <text x="410" y="298" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#0284c7">thread_group circular doubly-linked list</text>
      </svg>
    </div>
"""

    # -----------------------------------------------------------------
    # Diagram 2: Fast Userspace Mutex (futex) Fast/Slow Path
    # -----------------------------------------------------------------
    diagram_futex = r"""
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.2: Futex Dual-Path Locking Architecture (User-Space Atomics vs. Kernel Wait Queue)</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Uncontended locks operate entirely in user space via atomic instructions; contention transitions to a kernel sleep queue.</div>

      <svg viewBox="0 0 820 330" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="fx-fast" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
          </marker>
          <marker id="fx-slow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
          </marker>
          <marker id="fx-wake" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
        </defs>

        <!-- User Space vs Kernel Space Boundary -->
        <rect x="15" y="10" width="790" height="155" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 4"/>
        <text x="30" y="32" font-size="11" font-weight="700" fill="#475569">USER SPACE (Ring 3)</text>

        <rect x="15" y="180" width="790" height="140" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <text x="30" y="202" font-size="11" font-weight="700" fill="#0f172a">KERNEL SPACE (Ring 0) &mdash; Futex Subsystem</text>

        <!-- Thread A: Fast Path -->
        <g transform="translate(45, 50)">
          <rect width="210" height="95" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2"/>
          <text x="15" y="22" font-size="11" font-weight="700" fill="#059669">Thread A (Lock Holder)</text>
          <text x="15" y="38" font-size="9" fill="#64748b">1. Atomic compare-and-swap</text>
          <rect x="12" y="48" width="186" height="34" rx="3" fill="#f0fdf4" stroke="#86efac"/>
          <text x="20" y="68" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#166534">lock_val = 0 &rarr; 1 (Locked)</text>
        </g>

        <!-- Shared Memory Futex Variable -->
        <g transform="translate(315, 60)">
          <rect width="180" height="75" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="90" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="#0284c7">Shared Integer</text>
          <text x="90" y="40" text-anchor="middle" font-family="var(--font-mono)" font-size="10" fill="#334155">uint32_t val</text>
          <text x="90" y="58" text-anchor="middle" font-size="9" fill="#64748b">Resident in User Virtual RAM</text>
        </g>

        <!-- Thread B: Contention Path -->
        <g transform="translate(555, 50)">
          <rect width="220" height="95" rx="6" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
          <text x="15" y="22" font-size="11" font-weight="700" fill="#dc2626">Thread B (Contender)</text>
          <text x="15" y="38" font-size="9" fill="#64748b">2. CMPXCHG fails (already 1)</text>
          <rect x="12" y="48" width="196" height="34" rx="3" fill="#fef2f2" stroke="#fca5a5"/>
          <text x="20" y="68" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#b91c1c">FUTEX_WAIT Syscall Trap</text>
        </g>

        <!-- Fast Path Flow (No Syscall) -->
        <path d="M 255 97 L 315 97" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#fx-fast)"/>
        <text x="285" y="90" text-anchor="middle" font-size="8" font-weight="700" fill="#059669">FAST</text>

        <!-- Contention Slow Path (Syscall Downward) -->
        <path d="M 665 145 L 665 210" fill="none" stroke="#dc2626" stroke-width="2" marker-end="url(#fx-slow)"/>
        <text x="675" y="175" font-size="9" font-weight="600" fill="#dc2626">sys_futex(FUTEX_WAIT)</text>

        <!-- Kernel Wait Queue -->
        <g transform="translate(360, 210)">
          <rect width="400" height="95" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="20" y="25" font-size="11" font-weight="700" fill="#0f172a">Futex Hash Bucket Wait Queue</text>
          <text x="20" y="42" font-family="var(--font-mono)" font-size="9" fill="#64748b">Key: Physical Page Frame + Offset of &amp;val</text>
          <rect x="20" y="52" width="360" height="36" rx="4" fill="#fef3c7" stroke="#fcd34d"/>
          <text x="30" y="74" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#92400e">Thread B: TASK_INTERRUPTIBLE (Sleeping on Hash Bucket)</text>
        </g>

        <!-- Unlock & Wakeup Path -->
        <path d="M 150 145 C 150 255, 300 255, 360 255" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#fx-wake)"/>
        <text x="220" y="245" font-size="9" font-weight="600" fill="#0284c7">3. sys_futex(FUTEX_WAKE, 1)</text>
      </svg>
    </div>
"""

    # -----------------------------------------------------------------
    # Diagram 3: CLONE_CHILD_CLEARTID Thread Reaping Mechanism
    # -----------------------------------------------------------------
    diagram_cleartid = r"""
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.3: Kernel-Driven Thread Reaping via CLONE_CHILD_CLEARTID</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">How pthread_join() synchronizes without busy-polling by relying on atomic kernel teardown in do_exit().</div>

      <svg viewBox="0 0 820 300" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="ct-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
          <marker id="ct-act" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Step 1: Thread 1 Joins -->
        <g transform="translate(30, 40)">
          <rect width="220" height="230" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <rect width="220" height="28" rx="6" fill="#0284c7"/>
          <text x="110" y="19" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">Step 1: Joining Thread (T1)</text>

          <text x="15" y="48" font-size="10" font-weight="600" fill="#334155">Invokes pthread_join(tid2):</text>
          <rect x="15" y="58" width="190" height="48" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="25" y="76" font-family="var(--font-mono)" font-size="9" fill="#0369a1">Checks *ctid == tid2</text>
          <text x="25" y="94" font-family="var(--font-mono)" font-size="9" fill="#0369a1">Enters futex_wait(ctid)</text>

          <rect x="15" y="120" width="190" height="40" rx="4" fill="#fef3c7" stroke="#fcd34d"/>
          <text x="25" y="144" font-size="10" font-weight="600" fill="#92400e">Status: Sleeping in Kernel</text>

          <text x="15" y="185" font-size="9" fill="#64748b">Zero CPU cycles consumed;</text>
          <text x="15" y="200" font-size="9" fill="#64748b">No polling loop overhead.</text>
        </g>

        <!-- Step 2: Thread 2 Exits in Kernel -->
        <g transform="translate(300, 40)">
          <rect width="220" height="230" rx="6" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
          <rect width="220" height="28" rx="6" fill="#dc2626"/>
          <text x="110" y="19" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">Step 2: Exiting Thread (T2)</text>

          <text x="15" y="48" font-size="10" font-weight="600" fill="#334155">Calls pthread_exit():</text>
          <rect x="15" y="58" width="190" height="48" rx="4" fill="#fef2f2" stroke="#fca5a5"/>
          <text x="25" y="76" font-family="var(--font-mono)" font-size="9" fill="#b91c1c">sys_exit() Trap</text>
          <text x="25" y="94" font-family="var(--font-mono)" font-size="9" fill="#b91c1c">Enters kernel do_exit()</text>

          <rect x="15" y="120" width="190" height="40" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="25" y="144" font-size="10" font-weight="600" fill="#475569">Status: T2 Terminating</text>

          <text x="15" y="185" font-size="9" fill="#64748b">Kernel reads task_struct</text>
          <text x="15" y="200" font-size="9" fill="#64748b">CLONE_CHILD_CLEARTID flag</text>
        </g>

        <!-- Step 3: Kernel Atomic Action & Wakeup -->
        <g transform="translate(570, 40)">
          <rect width="220" height="230" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2"/>
          <rect width="220" height="28" rx="6" fill="#059669"/>
          <text x="110" y="19" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">Step 3: Kernel do_exit() Action</text>

          <rect x="15" y="45" width="190" height="52" rx="4" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="65" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">1. *ctid = 0</text>
          <text x="25" y="82" font-size="9" fill="#15803d">Zeroes memory location</text>

          <rect x="15" y="108" width="190" height="52" rx="4" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="128" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">2. futex_wake(ctid, 1)</text>
          <text x="25" y="145" font-size="9" fill="#15803d">Wakes Thread 1 from sleep</text>

          <text x="15" y="185" font-size="9" font-weight="600" fill="#059669">Thread 1 Awakens:</text>
          <text x="15" y="200" font-size="9" fill="#334155">Reads return status;</text>
          <text x="15" y="215" font-size="9" fill="#334155">Reclaims Thread 2's stack.</text>
        </g>

        <!-- Transition Arrows -->
        <path d="M 250 145 L 300 145" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#ct-arr)"/>
        <path d="M 520 145 L 570 145" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#ct-act)"/>
      </svg>
    </div>
"""

    # Inject Figure 3.1 after Section 3.2
    anchor_32 = "<h4>2. The Unified Task Abstraction: PID vs. TGID</h4>"
    if "Figure 3.1: Linux Thread Group Hierarchy" not in content:
        content = content.replace(anchor_32, anchor_32 + "\n" + diagram_tgid)

    # Inject Figure 3.2 after Section 3.4
    anchor_34 = "<h4>4. Fast Userspace Mutexes (futex)</h4>"
    if "Figure 3.2: Futex Dual-Path Locking Architecture" not in content:
        content = content.replace(anchor_34, anchor_34 + "\n" + diagram_futex)

    # Inject Figure 3.3 after Section 3.6
    anchor_36 = "<h4>6. Thread Teardown and Reaping: How pthread_join() Works</h4>"
    if "Figure 3.3: Kernel-Driven Thread Reaping" not in content:
        content = content.replace(anchor_36, anchor_36 + "\n" + diagram_cleartid)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully injected NPTL diagrams into Section 3 of {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add detailed NPTL diagrams to Section 3 of Module 04\n\n"
            "Embed SVG diagrams illustrating PID/TGID thread group topology, futex\n"
            "fast/slow path mechanics, and CLONE_CHILD_CLEARTID thread reaping."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_section_three_diagrams()
