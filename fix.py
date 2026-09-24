#!/usr/bin/env python3
# =====================================================================
# fix.py: Standardize all weekly hub index.html pages to match Week 6
# =====================================================================
import os
import subprocess

HUB_TEMPLATES = {
    "week01-operating-system-concepts": {
        "title": "Week 1: Operating System Concepts & Architecture",
        "prev": None,
        "next": "../week02-processes/index.html",
        "prev_label": None,
        "next_label": "Week 2: Processes & Threads",
        "lead": "Explore the fundamental hardware-software interface, system call dispatch mechanisms, dual-mode CPU protection rings, and trap handling.",
        "modules": [
            ("01", "What is an Operating System & History", "Trace the historical evolution of mainframe, minicomputer, personal, and mobile operating systems.", ["Batch Systems", "Multiprogramming", "Time-Sharing", "VM"]),
            ("02", "Hardware Review & CPU Modes", "Examine Von Neumann architecture, CPU execution cycles, memory hierarchies, and dual-mode user/kernel execution.", ["CPU Registers", "Cache Coherency", "Privileged Instructions", "MMU"]),
            ("03", "Fundamental OS Concepts", "Analyze processes, address spaces, files, system calls, protection domains, and the shell interface.", ["Process Model", "Filesystem Tree", "System Calls", "API Abstraction"]),
            ("04", "OS Structure & Kernel Models", "Contrast Monolithic kernels, Layered architectures, Microkernels, Exokernels, and Hybrid systems.", ["Monolithic", "Microkernel", "Layered", "Hybrid OS"])
        ]
    },
    "week02-processes": {
        "title": "Week 2: Processes & Threads",
        "prev": "../week01-operating-system-concepts/index.html",
        "next": "../week03-process-scheduling/index.html",
        "prev_label": "Week 1: OS Concepts",
        "next_label": "Week 3: Scheduling",
        "lead": "Examine process address space anatomy, Process Control Blocks (PCB), Linux task_struct internals, lifecycle state transitions, and kernel threading models.",
        "modules": [
            ("01", "The Process Model & Memory Layout", "Dissect process memory segments (text, data, bss, heap, stack) and Process Control Block structures.", ["Address Space", "PCB", "task_struct", "Context Switch"]),
            ("02", "Process Lifecycle & State Transitions", "Trace process creation (fork, exec), termination, zombie states, orphan processes, and waitpid synchronization.", ["fork()", "execve()", "Zombie Process", "Signals"]),
            ("03", "Classical Thread Concepts", "Understand lightweight concurrency, shared address spaces, thread control blocks, and concurrency benefits.", ["Concurrency", "TCB", "Shared Memory", "Lightweight"]),
            ("04", "Thread Implementation & POSIX APIs", "Master user-space threads vs. kernel-supported threads and POSIX pthread creation and synchronization.", ["pthread_create", "Mutexes", "Join/Detach", "TLS"])
        ]
    },
    "week03-process-scheduling": {
        "title": "Week 3: CPU Scheduling & Resource Allocation",
        "prev": "../week02-processes/index.html",
        "next": "../week04-concurrency-and-mutual-exclusion/index.html",
        "prev_label": "Week 2: Processes",
        "next_label": "Week 4: Concurrency",
        "lead": "Analyze CPU burst distributions, dispatch latency, batch scheduling algorithms, interactive multi-level feedback queues, and real-time scheduling.",
        "modules": [
            ("01", "Introduction to Scheduling", "Examine scheduling criteria, CPU-I/O burst cycles, dispatcher latency, and preemptive vs. non-preemptive design.", ["CPU Burst", "Dispatcher", "Preemption", "Throughput"]),
            ("02", "Batch Scheduling Algorithms", "Evaluate FCFS, SJF, Shortest Remaining Time Next (SRTN), and Highest Response Ratio Next (HRRN).", ["FCFS", "SJF", "SRTN", "Convoy Effect"]),
            ("03", "Interactive Scheduling Algorithms", "Master Round Robin, Multi-Level Feedback Queues (MLFQ), and Stride scheduling.", ["Round Robin", "MLFQ", "Quantum", "Priority Boost"]),
            ("04", "Real-Time & Multiprocessor Scheduling", "Explore Rate Monotonic Scheduling (RMS), Earliest Deadline First (EDF), and SMP work-stealing.", ["RMS", "EDF", "Work Stealing", "Affinity"])
        ]
    },
    "week04-concurrency-and-mutual-exclusion": {
        "title": "Week 4: Concurrency & Mutual Exclusion",
        "prev": "../week03-process-scheduling/index.html",
        "next": "../week05-io-and-disk-scheduling/index.html",
        "prev_label": "Week 3: Scheduling",
        "next_label": "Week 5: I/O & Disks",
        "lead": "Confront race conditions on shared memory. Master critical sections, software synchronization, hardware atomic primitives, and semaphores.",
        "modules": [
            ("01", "Race Conditions & Critical Regions", "Define critical sections, mutual exclusion requirements, race conditions, and progress invariants.", ["Critical Section", "Race Condition", "Mutual Exclusion", "Progress"]),
            ("02", "Hardware Primitives & Spinlocks", "Analyze disable interrupts, Test-And-Set (TAS), Compare-And-Swap (CAS), and busy-waiting spinlocks.", ["TAS", "CAS", "Spinlocks", "Atomic Instructions"]),
            ("03", "Semaphores, Mutexes & Monitors", "Master Dijkstra counting semaphores, binary mutexes, condition variables, and language-level monitors.", ["Semaphores", "Mutexes", "Monitors", "Condition Variables"]),
            ("04", "Classical Synchronization Problems", "Solve Producer-Consumer, Readers-Writers, and Dining Philosophers concurrency challenges.", ["Producer-Consumer", "Readers-Writers", "Bounded Buffer", "Synchronization"])
        ]
    },
    "week05-io-and-disk-scheduling": {
        "title": "Week 5: I/O Subsystems & Disk Scheduling",
        "prev": "../week04-concurrency-and-mutual-exclusion/index.html",
        "next": "../week06-synchronization-and-deadlock/index.html",
        "prev_label": "Week 4: Concurrency",
        "next_label": "Week 6: Deadlocks",
        "lead": "Examine device controllers, programmed I/O vs. memory-mapped I/O, APIC interrupts, DMA transfers, mechanical disk geometry, and RAID architectures.",
        "modules": [
            ("01", "I/O Hardware & Device Controllers", "Explore device controller registers, data buffers, PMIO vs. MMIO hazards, and volatile memory fencing.", ["PMIO", "MMIO", "Device Registers", "Memory Fencing"]),
            ("02", "Interrupts, APIC & DMA Transfers", "Study hardware interrupt vectors, top-halves vs. bottom-halves, MSI-X, and Direct Memory Access.", ["APIC", "MSI-X", "Softirqs", "DMA Controller"]),
            ("03", "Disk Geometry & Arm Scheduling", "Analyze platters, seek time, rotational latency, ZBR, and arm algorithms (FCFS, SSTF, SCAN, C-LOOK).", ["Seek Time", "Rotational Delay", "SSTF", "C-LOOK"]),
            ("04", "RAID Storage Architectures", "Evaluate RAID levels 0 through 6, XOR parity math, Galois Field P+Q codes, and MTTDL reliability modeling.", ["RAID 5", "RAID 6", "XOR Parity", "MTTDL"])
        ]
    },
    "week06-synchronization-and-deadlock": {
        "title": "Week 6: Synchronization & Deadlock",
        "prev": "../week05-io-and-disk-scheduling/index.html",
        "next": "../week09-memory-management/index.html",
        "prev_label": "Week 5: I/O & Disks",
        "next_label": "Week 7: Virtual Memory",
        "lead": "Investigate synchronization pathologies including livelock, starvation, priority inversion, Coffman conditions, Banker's Algorithm, and kernel defenses.",
        "modules": [
            ("01", "Livelock, Starvation & PIP", "Contrast livelock and starvation, analyze the Mars Pathfinder anomaly, and study Priority Inheritance Protocols.", ["Livelock", "Starvation", "Priority Inversion", "Mars Pathfinder"]),
            ("02", "Coffman Conditions & RAGs", "Dissect the four necessary and sufficient Coffman conditions and Resource Allocation Graph cycle detection.", ["Coffman Conditions", "RAGs", "Wait-For Graphs", "Cycle Detection"]),
            ("03", "Banker's Algorithm & Prevention", "Master static deadlock prevention, the Ostrich algorithm, and Dijkstra's Banker's Algorithm safety vectors.", ["Banker's Algorithm", "Safe State", "Lock Ordering", "Prevention"]),
            ("04", "Classic Problems & Defenses", "Analyze Dining Philosophers, Readers-Writers starvation, and modern OS static/runtime defenses (lockdep).", ["Dining Philosophers", "Readers-Writers", "lockdep", "Driver Verifier"])
        ]
    },
    "week09-memory-management": {
        "title": "Week 7 & 8: Memory Management & Virtual Memory",
        "prev": "../week06-synchronization-and-deadlock/index.html",
        "next": "../week10-file-management/index.html",
        "prev_label": "Week 6: Deadlocks",
        "next_label": "Week 9: File Systems",
        "lead": "Master physical memory allocation, buddy allocators, hardware address translation, page tables, TLB caching, page faults, and replacement algorithms.",
        "modules": [
            ("01", "Free-Used Lists & Buddy Allocator", "Explore contiguous memory allocation, bitmap tracking, free lists, and binary buddy allocator splitting/merging.", ["Buddy Allocator", "Free Lists", "Fragmentation", "Allocation"]),
            ("02", "Paging Hardware & Page Tables", "Examine PTE sandbox bit flags (present, dirty, user/kernel, read/write) and multi-level page tables.", ["Page Table Entry", "PTE Flags", "Multi-Level PT", "CR3 Register"]),
            ("03", "Translation Lookaside Buffer (TLB)", "Understand hardware TLB caching, associative lookups, tagged entries, and context-switch flushing.", ["TLB", "Associative Memory", "Hit Ratio", "ASID"]),
            ("04", "Virtual Memory & Replacement", "Analyze VM page faults, FIFO, Optimal, LRU, Clock, Aging, Working Set model, and WSClock policies.", ["Page Fault", "LRU", "Clock Algorithm", "Working Set"])
        ]
    },
    "week10-file-management": {
        "title": "Week 9: File System Architecture & Implementation",
        "prev": "../week09-memory-management/index.html",
        "next": "../week11-multiprocessors/index.html",
        "prev_label": "Week 7/8: Memory",
        "next_label": "Week 10: Multiprocessors",
        "lead": "Explore file abstractions, directory structures, Unix inode design, extent allocation, journaling, and storage optimization.",
        "modules": [
            ("01", "The File Abstraction", "Study file types, file attributes, access methods (sequential vs. direct), and file control blocks.", ["File Abstraction", "Attributes", "Sequential Access", "FCB"]),
            ("02", "Directories & Hierarchical Paths", "Examine single-level, two-level, and tree-structured directory namespaces and path resolution.", ["Directories", "Path Resolution", "Hard Links", "Symbolic Links"]),
            ("03", "File System Implementation", "Dissect Unix inodes, direct/indirect block pointers, extent trees, and free-space bitmap management.", ["Inode", "Indirect Blocks", "Extent Tree", "Bitmap"]),
            ("04", "Reliability, Layout & Optimization", "Master journaling filesystems (ext4), log-structured storage, block caching, and disk defragmentation.", ["Journaling", "Write-Ahead Log", "Block Cache", "Recovery"])
        ]
    },
    "week11-multiprocessors": {
        "title": "Week 10: Multiprocessors & Distributed Systems",
        "prev": "../week10-file-management/index.html",
        "next": "../week12-security/index.html",
        "prev_label": "Week 9: File Systems",
        "next_label": "Week 12: Security",
        "lead": "Master symmetric multiprocessing (SMP), hardware cache coherency protocols (MESI), NUMA architectures, RPC, and distributed middleware.",
        "modules": [
            ("01", "Multiprocessor Hardware & Caches", "Study UMA vs. NUMA architectures, bus snooping, and MESI cache coherency state machines.", ["SMP", "NUMA", "Bus Snooping", "MESI Protocol"]),
            ("02", "Multiprocessor Scheduling & Affinity", "Examine coarse-grained/fine-grained multithreading, load balancing, and processor affinity.", ["Processor Affinity", "Load Balancing", "Migration", "Gang Scheduling"]),
            ("03", "Multicomputers & Interconnects", "Explore loosely coupled clusters, message passing interfaces, network topologies, and latency/bandwidth.", ["Clusters", "Message Passing", "Interconnect", "Latency"]),
            ("04", "Distributed Shared Memory & RPC", "Master Remote Procedure Call (RPC) marshaling/stub generation and Distributed Shared Memory (DSM).", ["RPC", "Stub Generation", "DSM", "Marshalling"])
        ]
    },
    "week12-security": {
        "title": "Week 12: Operating System Security & Protection",
        "prev": "../week11-multiprocessors/index.html",
        "next": "../index.html",
        "prev_label": "Week 10: Multiprocessors",
        "next_label": "Course Index",
        "lead": "Investigate operating system security environments, access control lists, capability lists, hardware protection rings, and vulnerability containment.",
        "modules": [
            ("01", "Protection Domains & Access Matrices", "Examine protection domains, access control lists (ACLs), capability lists, and reference monitor design.", ["Protection Domain", "ACL", "Capabilities", "Reference Monitor"]),
            ("02", "Hardware Protection & Rings", "Master CPU privilege rings (Ring 0 to Ring 3), system call gates, and hardware virtualization separation.", ["Privilege Rings", "System Gate", "Virtualization", "Isolation"]),
            ("03", "Security Vulnerabilities & Containment", "Analyze buffer overflows, stack smashing, privilege escalation, sandboxing, and modern exploit mitigation.", ["Buffer Overflow", "Stack Smashing", "Sandboxing", "ASLR/DEP"])
        ]
    }
}

def generate_hub(dir_name, data):
    folder_path = dir_name
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "index.html")

    prev_link = f'<a href="{data["prev"]}" class="nav-btn">&larr; {data["prev_label"]}</a>' if data["prev"] else '<span class="nav-btn" style="visibility:hidden;">&larr; Prev</span>'
    next_link = f'<a href="{data["next"]}" class="nav-btn">{data["next_label"]} &rarr;</a>' if data["next"] else '<span class="nav-btn" style="visibility:hidden;">Next &rarr;</span>'

    modules_html = ""
    for num, title, desc, tags in data["modules"]:
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in tags])
        mod_filename = f"{num.lower()}-{title.lower().replace('&', 'and').replace(' ', '-').replace('--', '-')}.html"
        modules_html += f"""
      <!-- Module {num} -->
      <div class="module-card">
        <div>
          <div class="module-num">Module {num}</div>
          <h2 class="module-title">{title}</h2>
          <p class="module-desc">{desc}</p>
          <div class="module-tags">{tags_html}</div>
        </div>
        <a href="#" class="launch-btn">Module Overview &rarr;</a>
      </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data['title']} - COSC240</title>
  <style>
    :root {{
      --primary: #0f172a;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --border: #e2e8f0;
      --card-bg: #ffffff;
      --text: #334155;
      --text-muted: #64748b;
      --bg: #f8fafc;
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 24px;
    }}
    .container {{ max-width: 1040px; margin: 0 auto; }}
    .nav-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #ffffff;
      border: 1px solid var(--border);
      padding: 12px 20px;
      border-radius: 8px;
      margin-bottom: 24px;
    }}
    .nav-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--accent);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background 0.15s ease;
    }}
    .nav-btn:hover {{ background: #f0f9ff; }}
    .hero-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 32px;
      margin-bottom: 28px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }}
    .week-tag {{
      display: inline-block;
      background: #e0f2fe;
      color: #0369a1;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 999px;
      margin-bottom: 12px;
    }}
    h1 {{ margin: 0 0 12px 0; font-size: 1.85rem; color: var(--primary); }}
    .lead-text {{ margin: 0 0 20px 0; font-size: 1.05rem; color: var(--text); line-height: 1.7; }}
    .briefing-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 24px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
    }}
    .briefing-box {{
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 20px;
    }}
    .briefing-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--primary);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .briefing-list {{ margin: 0; padding-left: 18px; font-size: 0.88rem; color: var(--text); }}
    .briefing-list li {{ margin-bottom: 6px; }}
    .modules-heading {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--primary);
      margin: 28px 0 16px 0;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .modules-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}
    .module-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }}
    .module-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    }}
    .module-num {{
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }}
    .module-title {{ font-size: 1.15rem; font-weight: 700; color: var(--primary); margin: 0 0 10px 0; }}
    .module-desc {{ font-size: 0.88rem; color: var(--text-muted); margin: 0 0 14px 0; line-height: 1.55; }}
    .module-tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }}
    .tag {{
      background: #f1f5f9;
      color: #475569;
      font-size: 0.72rem;
      font-family: var(--font-mono);
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .launch-btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: var(--primary);
      color: #ffffff;
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      padding: 10px 16px;
      border-radius: 6px;
      transition: background 0.15s ease;
      width: 100%;
    }}
    .launch-btn:hover {{ background: var(--accent-hover); }}
    @media (max-width: 768px) {{
      .briefing-grid, .modules-grid {{ grid-template-columns: 1fr; }}
      body {{ padding: 16px; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      {prev_link}
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      {next_link}
    </nav>

    <div class="hero-card">
      <span class="week-tag">COSC240 &bull; Operating Systems</span>
      <h1>{data['title']}</h1>
      <p class="lead-text">
        {data['lead']}
      </p>

      <div class="briefing-grid">
        <div class="briefing-box">
          <div class="briefing-title">
            <span>&#128218;</span> What You Will Learn
          </div>
          <ul class="briefing-list">
            <li>Core architectural mechanics and low-level data structures.</li>
            <li>Kernel operational states, hardware interrupts, and protection boundaries.</li>
            <li>Theoretical trade-offs, performance implications, and industry standards.</li>
          </ul>
        </div>

        <div class="briefing-box">
          <div class="briefing-title">
            <span>&#9989;</span> What You Should Do
          </div>
          <ul class="briefing-list">
            <li>Review lecture notes and assigned textbook chapters.</li>
            <li>Explore interactive pedagogical steppers and simulation modules.</li>
            <li>Complete weekly tutorials, practical lab assignments, and review quizzes.</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="modules-heading">
      <span>&#128194;</span> Course Modules &amp; Deep-Dive Texts
    </div>

    <div class="modules-grid">
      {modules_html}
    </div>

    <nav class="nav-bar">
      {prev_link}
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      {next_link}
    </nav>
  </div>
</body>
</html>
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html.strip() + "\n")
    print(f"--> Updated hub index: {file_path}")

def update_all_hubs():
    for dir_name, data in HUB_TEMPLATES.items():
        generate_hub(dir_name, data)

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py"] + list(HUB_TEMPLATES.keys()), check=True)
        status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
        if not status:
            print("--> Working tree is clean. Nothing to commit.")
            return

        commit_msg = (
            "Adopt Week 6 hub card format across all COSC240 weekly indices\n\n"
            "Standardize Weeks 1 through 12 hub index pages with the responsive\n"
            "two-column briefing and module grid layout."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_all_hubs()
    run_git_sync()
