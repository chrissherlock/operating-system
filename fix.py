#!/usr/bin/env python3
# =====================================================================
# fix.py: Append 5-state model and SVG diagram to 03-os-concepts.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

FIVE_STATE_SECTION = r"""
    <h4>Lifecycle Boundaries: The Classical Five-State Model</h4>
    <p>
      While the three-state model captures the dynamic scheduling loop on the CPU, production operating systems must also manage process inception, admission control, and resource reclamation upon exit. The <strong>Five-State Process Model</strong> extends the execution loop by adding formal entry and exit boundaries:
    </p>
    <ul>
      <li><strong>New (Created):</strong> The process is being instantiated (e.g., via <code>fork()</code> in POSIX, <code>CreateProcess()</code> in Windows, or an OS batch loader). The kernel has allocated the Process Control Block (PCB) and assigned a unique PID, but memory translation structures and page mappings are not yet admitted to the active scheduling queue.</li>
      <li><strong>Terminated (Exit / Zombie):</strong> The process has completed execution (via <code>exit()</code>, <code>ExitProcess()</code>, or a terminating signal like <code>SIGKILL</code>). The operating system reclaims its virtual address space, file descriptor tables, and allocated heap memory. However, the PCB remains in the system process table as a <em>zombie</em> until the parent process issues a synchronization call (such as <code>wait()</code> or <code>waitpid()</code>) to collect its exit status code.</li>
    </ul>

    <!-- Diagram 2b: Five-State Process Lifecycle -->
    <div style="display: flex; justify-content: center; margin: 28px 0;">
      <svg viewBox="0 0 860 320" width="100%" height="100%" style="max-width: 860px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="trans5-arrow-blue" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
          </marker>
          <marker id="trans5-arrow-slate" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#64748b" />
          </marker>
          <marker id="trans5-arrow-red" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#ef4444" />
          </marker>
          <marker id="trans5-arrow-green" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#059669" />
          </marker>
          <marker id="trans5-arrow-amber" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#d97706" />
          </marker>
          <filter id="node5-shadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08" />
          </filter>
        </defs>

        <!-- Title Header -->
        <text x="430" y="24" fill="#0f172a" font-size="13" font-weight="700" text-anchor="middle">CLASSICAL FIVE-STATE PROCESS LIFECYCLE MODEL</text>
        <text x="430" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Creation &rarr; Active Scheduling Core &rarr; Termination / Zombie Teardown</text>

        <!-- 1. NEW STATE (Far Left) -->
        <g transform="translate(90, 115)" filter="url(#node5-shadow)">
          <circle cx="0" cy="0" r="44" fill="#f8fafc" stroke="#94a3b8" stroke-width="2" />
          <text x="0" y="-4" fill="#334155" font-size="11.5" font-weight="700" text-anchor="middle">NEW</text>
          <text x="0" y="12" fill="#64748b" font-size="8" text-anchor="middle">fork / create</text>
        </g>

        <!-- Transition: New -> Ready (Admit) -->
        <path d="M 134,115 L 216,115" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#trans5-arrow-blue)" />
        <rect x="145" y="90" width="60" height="18" rx="3" fill="#ffffff" stroke="#bae6fd" />
        <text x="175" y="103" fill="#0369a1" font-size="8" font-weight="700" text-anchor="middle">Admit</text>

        <!-- 2. READY STATE -->
        <g transform="translate(265, 115)" filter="url(#node5-shadow)">
          <circle cx="0" cy="0" r="46" fill="#eff6ff" stroke="#0284c7" stroke-width="2" />
          <text x="0" y="-4" fill="#0369a1" font-size="11.5" font-weight="700" text-anchor="middle">READY</text>
          <text x="0" y="12" fill="#64748b" font-size="8" text-anchor="middle">In Run Queue</text>
        </g>

        <!-- 3. RUNNING STATE -->
        <g transform="translate(565, 115)" filter="url(#node5-shadow)">
          <circle cx="0" cy="0" r="46" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
          <text x="0" y="-4" fill="#065f46" font-size="11.5" font-weight="700" text-anchor="middle">RUNNING</text>
          <text x="0" y="12" fill="#047857" font-size="8" text-anchor="middle">On CPU Core</text>
        </g>

        <!-- Transition: Ready -> Running (Dispatch - Top Arc) -->
        <path d="M 307,95 C 380,60 450,60 523,95" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#trans5-arrow-blue)" />
        <rect x="360" y="54" width="110" height="18" rx="3" fill="#ffffff" stroke="#bae6fd" />
        <text x="415" y="67" fill="#0369a1" font-size="8" font-weight="700" text-anchor="middle">Scheduler Dispatch</text>

        <!-- Transition: Running -> Ready (Preempt - Bottom Return Arc) -->
        <path d="M 523,135 C 450,170 380,170 307,135" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#trans5-arrow-slate)" />
        <rect x="355" y="158" width="120" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1" />
        <text x="415" y="171" fill="#475569" font-size="8" font-weight="600" text-anchor="middle">Timer Preemption</text>

        <!-- 4. BLOCKED STATE (Bottom Center) -->
        <g transform="translate(415, 255)" filter="url(#node5-shadow)">
          <circle cx="0" cy="0" r="46" fill="#fef2f2" stroke="#ef4444" stroke-width="2" />
          <text x="0" y="-4" fill="#991b1b" font-size="11.5" font-weight="700" text-anchor="middle">BLOCKED</text>
          <text x="0" y="12" fill="#b91c1c" font-size="8" text-anchor="middle">I/O / Sleep</text>
        </g>

        <!-- Transition: Running -> Blocked (I/O Wait) -->
        <path d="M 545,155 C 520,205 480,240 463,250" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#trans5-arrow-red)" />
        <rect x="495" y="205" width="95" height="18" rx="3" fill="#ffffff" stroke="#fca5a5" />
        <text x="542" y="218" fill="#b91c1c" font-size="8" font-weight="700" text-anchor="middle">Block for Event</text>

        <!-- Transition: Blocked -> Ready (I/O Complete) -->
        <path d="M 367,250 C 350,240 310,205 285,155" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#trans5-arrow-green)" />
        <rect x="240" y="205" width="95" height="18" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="287" y="218" fill="#065f46" font-size="8" font-weight="700" text-anchor="middle">Event Occurred</text>

        <!-- Transition: Running -> Terminated (Exit) -->
        <path d="M 611,115 L 702,115" fill="none" stroke="#d97706" stroke-width="2" marker-end="url(#trans5-arrow-amber)" />
        <rect x="625" y="90" width="65" height="18" rx="3" fill="#ffffff" stroke="#fde68a" />
        <text x="657" y="103" fill="#92400e" font-size="8" font-weight="700" text-anchor="middle">Exit / Kill</text>

        <!-- 5. TERMINATED STATE (Far Right) -->
        <g transform="translate(750, 115)" filter="url(#node5-shadow)">
          <circle cx="0" cy="0" r="44" fill="#fffbeb" stroke="#d97706" stroke-width="2" />
          <text x="0" y="-4" fill="#92400e" font-size="10.5" font-weight="700" text-anchor="middle">TERMINATED</text>
          <text x="0" y="12" fill="#78350f" font-size="8" text-anchor="middle">Zombie / Exit</text>
        </g>
      </svg>
    </div>

    <h4>Virtual Memory Realities: The Seven-State Model</h4>
    <p>
      When physical RAM becomes heavily overcommitted, real-world operating systems employ a <strong>Seven-State Model</strong> by swapping entire process images out to secondary backing stores (swap partitions or paging files). This introduces two suspended states:
    </p>
    <ul>
      <li><strong>Ready / Suspended:</strong> The process is capable of running immediately once loaded into memory, but currently resides in secondary storage.</li>
      <li><strong>Blocked / Suspended:</strong> The process is both waiting for an external event (e.g., I/O) and has had its address space paged out to disk to free physical DRAM frames.</li>
    </ul>
"""

def append_five_state_model():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the anchor point right after the 3-state diagram and before Section 2
    # The 3-state diagram closes with </svg>\n    </div>
    # Section 2 starts with <h3>2. Address Spaces
    sec2_marker = "<h3>2. Address Spaces &amp; Virtual Memory"

    if sec2_marker not in content:
        print(f"Error: Could not locate Section 2 marker '{sec2_marker}'.")
        return

    parts = content.split(sec2_marker, 1)

    # Insert FIVE_STATE_SECTION right before Section 2
    updated_content = f"{parts[0]}{FIVE_STATE_SECTION}\n\n    {sec2_marker}{parts[1]}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully appended 5-state model to {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add 5-state process lifecycle model and diagram to Module 3\n\n"
            "Append the classical five-state process lifecycle model (New, Ready,\n"
            "Running, Blocked, Terminated) and corresponding SVG diagram directly\n"
            "after the three-state scheduling section in 03-os-concepts.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for 5-state model addition!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    append_five_state_model()
