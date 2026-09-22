#!/usr/bin/env python3
# =====================================================================
# fix.py: Update 01-limited-direct-execution.html with full Tanenbaum depth
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "01-limited-direct-execution.html")

FULL_MODULE_1 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>01. Limited Direct Execution &amp; Process Tables | Week 2: Processes &amp; Concurrency</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    body {
      font-family: var(--font-sans);
      color: #1e293b;
      background: #f8fafc;
      margin: 0;
      padding: 32px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3, h4 { color: #0f172a; }
    h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 28px; }
    h3 { margin-top: 20px; margin-bottom: 8px; color: #0284c7; font-size: 1.15rem; }
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 6px; }
    code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }
    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      margin: 16px 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="02-process-api.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 02. Process APIs &rarr;</a>
    </nav>

    <h2>01. Limited Direct Execution &amp; Process Tables</h2>
    <p>
      At the core of operating system design lies a fundamental tension: how to achieve maximum execution performance while enforcing absolute system protection[cite: 1]. As explored in <em>Operating Systems: Three Easy Pieces</em> (OSTEP) and Andrew S. Tanenbaum's <em>Modern Operating Systems</em>, running programs directly on the bare CPU hardware yields peak execution speeds[cite: 1]. However, without strict oversight, unconstrained user applications could monopolize the processor, corrupt memory, or execute unauthorized I/O operations[cite: 1].
    </p>

    <h3>1. The Mechanics of Limited Direct Execution</h3>
    <p>
      Direct execution means the CPU fetches, decodes, and executes user instructions natively without kernel intervention for every instruction[cite: 1]. To maintain control, the OS must limit this direct execution across two distinct phases: <em>boot-time setup</em> and <em>runtime interposition</em>[cite: 1].
    </p>
    <ul>
      <li><strong>Boot-Time Initialization:</strong> When the machine boots, the kernel initializes trap tables, configures interrupt descriptor tables (IDT), and sets up hardware memory protection registers[cite: 1]. The CPU is instructed where to jump when hardware traps or timer interrupts occur[cite: 1].</li>
      <li><strong>Runtime Interposition:</strong> Once a user program is launched, the CPU switches to unprivileged User Mode (Ring 3)[cite: 1]. The program executes instructions directly until it either attempts a restricted operation or a hardware timer interrupt fires[cite: 1].</li>
    </ul>

    <h3>2. Dual-Mode Operation and Privilege Rings</h3>
    <p>
      Hardware protection relies on hierarchical privilege levels, commonly referred to as <strong>rings</strong>[cite: 1]. On x86-64 architectures, Ring 0 represents Supervisor Mode (Kernel Mode), while Ring 3 represents User Mode[cite: 1].
    </p>
    <ul>
      <li><strong>Privileged Instructions:</strong> Operations such as disabling interrupts, modifying page table root pointers (<code>CR3</code>), altering power states, or issuing direct disk I/O commands can only be executed in Ring 0[cite: 1]. Attempting these instructions in Ring 3 triggers an immediate hardware exception[cite: 1].</li>
      <li><strong>The Trap Gate:</strong> When a user program requires kernel services (e.g., reading a file or allocating memory), it executes a <code>syscall</code> or trap instruction[cite: 1]. This hardware instruction acts as a controlled gateway, elevating privilege levels and transferring control to a verified kernel entry address[cite: 1].</li>
    </ul>

    <h3>3. Tanenbaum's View: Process Tables and Interrupt Vectors</h3>
    <p>
      Andrew Tanenbaum emphasizes the exact kernel data structures required to manage this lifecycle[cite: 1]. The central repository for process metadata is the <strong>Process Table</strong>, an array or linked list of Process Control Blocks (PCBs) maintained in kernel memory[cite: 1].
    </p>
    <pre>struct process_control_block {
    int pid;
    enum process_state state;
    struct cpu_registers saved_regs;
    uint64_t cr3_page_table_root;
    struct file_descriptor_table files;
};</pre>
    <p>
      When an interrupt or trap occurs, the CPU hardware consults the <strong>Interrupt Vector Table</strong>[cite: 1]. As Tanenbaum outlines, the low-level interrupt handling sequence proceeds through distinct phases[cite: 1]:
    </p>
    <ol>
      <li>Hardware stacks the program counter (RIP), program status word (PSW), and general registers[cite: 1].</li>
      <li>Hardware loads a new program counter from the interrupt vector into the CPU[cite: 1].</li>
      <li>An assembly-language procedure saves the remaining registers into the process table entry[cite: 1].</li>
      <li>The assembly-language procedure sets up a new stack for kernel execution[cite: 1].</li>
      <li>The C interrupt service routine runs to handle the event (e.g., buffering input or servicing a timer tick)[cite: 1].</li>
      <li>The scheduler decides which process is to run next[cite: 1].</li>
    </ol>

    <h3>4. Modeling Multiprogramming Efficiency</h3>
    <p>
      Tanenbaum utilizes a probabilistic model to demonstrate how multiprogramming improves CPU utilization[cite: 1]. If a process spends a fraction $p$ of its time waiting for I/O, the probability that $n$ processes in memory are simultaneously waiting for I/O is $p^n$[cite: 1]. Thus, CPU utilization is expressed as:
    </p>
    <pre>CPU Utilization = 1 - p^n</pre>
    <p>
      This mathematical formulation proves that increasing the degree of multiprogramming is essential to mask I/O latency and prevent expensive CPU cores from sitting idle[cite: 1].
    </p>

    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="02-process-api.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 02. Process APIs &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

def update_expanded_module():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(FULL_MODULE_1.strip() + "\n")

    print(f"--> Successfully updated {TARGET_FILE} with Tanenbaum text details.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand 01-limited-direct-execution.html with Tanenbaum text details\n\n"
            "Incorporate Tanenbaum's detailed descriptions of interrupt vectors, process\n"
            "tables, assembly-level save routines, and multiprogramming probability models."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_expanded_module()
