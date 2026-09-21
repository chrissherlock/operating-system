#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand process abstraction and embed SVG diagrams in 03-os-concepts.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

EXPANDED_PROCESS_SECTION = r"""    <h3>1. The Process Abstraction</h3>
    <p>
      At the foundation of operating system design is the <strong>process</strong>: an abstraction representing an active program in execution. While a <em>program</em> is a lifeless, passive collection of machine instructions and static data stored on non-volatile media (such as an ELF binary or Windows PE file on an NVMe SSD), a <em>process</em> is a dynamic, living computational entity with an active execution context managed by the kernel.
    </p>

    <h4>Process vs. Program: The Core Distinction</h4>
    <p>
      A single program can correspond to multiple distinct processes running concurrently. For example, if two users launch separate instances of the text editor <code>nano</code>, or if a user opens three independent terminal shells, each instance constitutes a separate process. Although both instances share the exact same underlying machine code in memory, each maintains completely isolated memory registers, dynamic heap buffers, execution state flags, and private call stacks.
    </p>

    <h4>Anatomy of a Process in Memory</h4>
    <p>
      When an operating system loads a binary executable into physical RAM to execute, it constructs a private virtual address space organized into standardized logical segments:
    </p>
    <ul>
      <li><strong>Text Segment (Code):</strong> The read-only region containing raw machine instructions executed by the CPU. Marking this region read-only prevents self-modifying code vulnerabilities and allows multiple concurrent instances of the same binary to share physical code pages in memory.</li>
      <li><strong>Data Segment (Initialized):</strong> Stores global and static variables explicitly initialized by the programmer before execution (e.g., <code>int max_retries = 5;</code>).</li>
      <li><strong>BSS Segment (Uninitialized):</strong> Block Started by Symbol; holds uninitialized global and static variables. Rather than bloating binary disk images with zeroes, the kernel simply records the size of the BSS section and zeroes out physical pages on demand upon allocation.</li>
      <li><strong>Heap:</strong> A dynamic memory pool managed at runtime by allocators (such as <code>malloc()</code> or <code>new</code>). The heap grows upward from lower virtual memory addresses toward higher addresses as dynamic allocations expand.</li>
      <li><strong>Stack:</strong> A Last-In, First-Out (LIFO) scratchpad region storing active execution frames. Each stack frame houses function arguments, return addresses, saved CPU registers, and local automatic variables. In typical x86 and ARM architectures, the stack originates near the top of the virtual address space and grows downward toward the heap.</li>
    </ul>

    <!-- Diagram 1: Process Memory Layout -->
    <div style="display: flex; justify-content: center; margin: 24px 0;">
      <svg viewBox="0 0 680 340" width="100%" height="100%" style="max-width: 680px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrowUp" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
            <path d="M3,6 L0,0 L6,0 Z" fill="#0284c7" />
          </marker>
          <marker id="arrowDown" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
            <path d="M3,0 L0,6 L6,6 Z" fill="#0284c7" />
          </marker>
        </defs>

        <!-- Outer Boundary -->
        <rect x="180" y="20" width="320" height="300" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />

        <!-- High Memory Address Label -->
        <text x="170" y="32" fill="#64748b" font-size="9" text-anchor="end">0x7FFFFFFFFFFF</text>
        <text x="170" y="44" fill="#94a3b8" font-size="8" text-anchor="end">(High Addresses)</text>

        <!-- Stack Box -->
        <rect x="190" y="28" width="300" height="48" rx="4" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5" />
        <text x="340" y="48" fill="#991b1b" font-size="11" font-weight="700" text-anchor="middle">Stack Segment</text>
        <text x="340" y="64" fill="#b91c1c" font-size="8.5" text-anchor="middle">Function Frames • Local Variables • Return Pointers</text>

        <!-- Stack Growth Arrow -->
        <path d="M 340,78 L 340,94" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#arrowDown)" />
        <text x="350" y="90" fill="#ef4444" font-size="8" font-style="italic">Grows Downward</text>

        <!-- Free Address Space Zone -->
        <rect x="190" y="102" width="300" height="60" rx="4" fill="#ffffff" stroke="#e2e8f0" stroke-dasharray="4,4" />
        <text x="340" y="136" fill="#94a3b8" font-size="9.5" text-anchor="middle">Unallocated Virtual Address Space</text>

        <!-- Heap Growth Arrow -->
        <path d="M 340,186 L 340,170" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowUp)" />
        <text x="350" y="180" fill="#0284c7" font-size="8" font-style="italic">Grows Upward</text>

        <!-- Heap Box -->
        <rect x="190" y="190" width="300" height="42" rx="4" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" />
        <text x="340" y="208" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">Heap Segment</text>
        <text x="340" y="222" fill="#0284c7" font-size="8.5" text-anchor="middle">Dynamic Memory (malloc / brk / mmap)</text>

        <!-- BSS Box -->
        <rect x="190" y="236" width="300" height="26" rx="4" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1" />
        <text x="340" y="253" fill="#334155" font-size="9.5" font-weight="600" text-anchor="middle">BSS Segment (Zero-Initialized Globals)</text>

        <!-- Data Box -->
        <rect x="190" y="266" width="300" height="26" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1" />
        <text x="340" y="283" fill="#92400e" font-size="9.5" font-weight="600" text-anchor="middle">Data Segment (Initialized Globals &amp; Statics)</text>

        <!-- Text Box -->
        <rect x="190" y="296" width="300" height="20" rx="3" fill="#ecfdf5" stroke="#059669" stroke-width="1" />
        <text x="340" y="310" fill="#065f46" font-size="9" font-weight="700" text-anchor="middle">Text Segment (Read-Only Machine Code)</text>

        <!-- Low Memory Address Label -->
        <text x="170" y="310" fill="#64748b" font-size="9" text-anchor="end">0x000000000000</text>
        <text x="170" y="322" fill="#94a3b8" font-size="8" text-anchor="end">(Low Addresses)</text>
      </svg>
    </div>

    <h4>The Process Control Block (PCB)</h4>
    <p>
      Because CPU cores can execute only one sequence of instructions at any given physical moment, the operating system maintains an internal data structure called the <strong>Process Control Block (PCB)</strong>—also referred to as <code>struct task_struct</code> in the Linux kernel—for every active process. When the kernel pauses a running process during a context switch, it saves the current state into its PCB, restoring it later so execution resumes transparently:
    </p>
    <ul>
      <li><strong>Process Identifier (PID &amp; PPID):</strong> A unique positive integer identifying the process, alongside its parent's process identifier.</li>
      <li><strong>CPU Registers:</strong> Saved snapshots of working registers (RAX, RBX, RCX, RSP, etc.), condition flags, and the Program Counter (PC/RIP) designating the exact next instruction to execute.</li>
      <li><strong>Execution State:</strong> The current scheduling condition of the process (Running, Ready, or Blocked).</li>
      <li><strong>CPU Scheduling Priorities:</strong> Priority metrics, nice values, accumulated CPU cycle counts, and execution burst timers.</li>
      <li><strong>Memory Management Descriptors:</strong> Pointers to page directory roots (such as the CR3 register in x86), segment tables, and bounds registers defining the process's valid virtual memory space.</li>
      <li><strong>I/O &amp; File Descriptors:</strong> An index array of pointers mapping open file descriptors (stdin 0, stdout 1, stderr 2, and open sockets) to system-wide file table entries.</li>
    </ul>

    <h4>Process State Transitions: The Three-State Model</h4>
    <p>
      Throughout its lifecycle, a process transitions between three core execution states:
    </p>
    <ol>
      <li><strong>Running:</strong> The process currently occupies a physical CPU core and its instructions are executing in hardware.</li>
      <li><strong>Ready:</strong> The process possesses all prerequisites to execute, but is temporarily stopped waiting for the CPU scheduler to allocate a core.</li>
      <li><strong>Blocked (Waiting):</strong> The process cannot proceed—even if a CPU core is idle—because it is waiting for an external event to finish, such as reading disk sectors, receiving network packets, or waiting on a timer.</li>
    </ol>

    <!-- Diagram 2: Three-State Process Lifecycle -->
    <div style="display: flex; justify-content: center; margin: 24px 0;">
      <svg viewBox="0 0 760 220" width="100%" height="100%" style="max-width: 760px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="stateArrow" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
          </marker>
        </defs>

        <!-- Ready State -->
        <g transform="translate(60, 40)">
          <circle cx="60" cy="60" r="52" fill="#eff6ff" stroke="#0284c7" stroke-width="2" />
          <text x="60" y="58" fill="#0369a1" font-size="12" font-weight="700" text-anchor="middle">READY</text>
          <text x="60" y="74" fill="#64748b" font-size="8.5" text-anchor="middle">In Run Queue</text>
        </g>

        <!-- Running State -->
        <g transform="translate(340, 40)">
          <circle cx="60" cy="60" r="52" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
          <text x="60" y="58" fill="#065f46" font-size="12" font-weight="700" text-anchor="middle">RUNNING</text>
          <text x="60" y="74" fill="#047857" font-size="8.5" text-anchor="middle">Executing on CPU</text>
        </g>

        <!-- Blocked State -->
        <g transform="translate(200, 130)">
          <circle cx="60" cy="50" r="50" fill="#fef2f2" stroke="#ef4444" stroke-width="2" />
          <text x="60" y="48" fill="#991b1b" font-size="12" font-weight="700" text-anchor="middle">BLOCKED</text>
          <text x="60" y="64" fill="#b91c1c" font-size="8.5" text-anchor="middle">Waiting on I/O</text>
        </g>

        <!-- Transition: Ready to Running (Scheduler Dispatch) -->
        <path d="M 172,82 L 338,82" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#stateArrow)" />
        <text x="255" y="74" fill="#0369a1" font-size="8.5" font-weight="700" text-anchor="middle">1. Scheduler Dispatch</text>

        <!-- Transition: Running to Ready (Time-slice Expired / Preempted) -->
        <path d="M 338,110 L 172,110" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#stateArrow)" />
        <text x="255" y="124" fill="#64748b" font-size="8.5" text-anchor="middle">2. Timer Interrupt (Preempted)</text>

        <!-- Transition: Running to Blocked (I/O Wait / System Call) -->
        <path d="M 360,148 C 340,175 320,180 310,180" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#stateArrow)" />
        <text x="365" y="185" fill="#ef4444" font-size="8.5" text-anchor="middle">3. Block for I/O</text>

        <!-- Transition: Blocked to Ready (I/O Complete / Interrupt) -->
        <path d="M 200,180 C 170,180 140,165 130,146" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#stateArrow)" />
        <text x="145" y="185" fill="#059669" font-size="8.5" text-anchor="middle">4. I/O Complete</text>
      </svg>
    </div>"""

def expand_process_section():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate existing Section 1 markup in 03-os-concepts.html
    # Old Section 1 starts with "<h3>1. The Process Abstraction</h3>" and ends before "<h3>2. Address Spaces"
    start_marker = "<h3>1. The Process Abstraction</h3>"
    end_marker = "<h3>2. Address Spaces &amp; Virtual Memory</h3>"

    if start_marker not in content or end_marker not in content:
        print("--> Error: Could not locate Section 1 boundaries.")
        return

    prefix = content.split(start_marker)[0]
    suffix = content.split(end_marker)[1]

    # Combine prefix, expanded section, and remainder of document
    new_content = f"{prefix}{EXPANDED_PROCESS_SECTION}\n\n    {end_marker}{suffix}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand process abstraction and add memory and lifecycle diagrams\n\n"
            "Enrich Section 1 of 03-os-concepts.html with in-depth analysis of process\n"
            "memory anatomy, Process Control Blocks, and state transitions, paired\n"
            "with SVG diagrams of virtual address layouts and the 3-state model."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Process Abstraction expansion!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    expand_process_section()
