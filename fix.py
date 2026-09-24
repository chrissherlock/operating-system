#!/usr/bin/env python3
# =====================================================================
# fix.py: Add visual thread topology comparison diagram to Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "04-thread-implementation.html")

def inject_topology_diagram():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    svg_diagram_html = r"""
    <h4>Visual Topology Comparison: Windows NT vs. Linux Task Groups</h4>
    <p>
      The core architectural difference lies in whether the kernel maintains distinct, hierarchical thread objects (Windows) or uniform tasks sharing resource pointers (Linux):
    </p>

    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 20px 0; overflow-x: auto;">
      <svg viewBox="0 0 860 380" style="width: 100%; min-width: 760px; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="link-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
          <marker id="shared-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Left Column: Windows NT Model -->
        <g transform="translate(10, 10)">
          <rect x="0" y="0" width="400" height="350" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
          <text x="20" y="28" font-size="13" font-weight="700" fill="#0f172a">WINDOWS NT: LAYERED THREAD OBJECTS</text>

          <!-- User Mode Ring 3 Boundary -->
          <rect x="20" y="45" width="360" height="75" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 4" />
          <text x="35" y="65" font-size="11" font-weight="700" fill="#64748b">USER MODE (Ring 3) &mdash; Accessed via %gs Register</text>
          <rect x="35" y="75" width="330" height="35" rx="4" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
          <text x="45" y="96" font-family="var(--font-mono)" font-size="11" font-weight="600" fill="#0369a1">TEB / TIB: Stack Bounds | TLS Array | GetLastError</text>

          <!-- Executive Ring 0 -->
          <rect x="20" y="145" width="360" height="190" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
          <text x="35" y="165" font-size="11" font-weight="700" fill="#0f172a">ETHREAD (Executive Object &mdash; Ring 0)</text>
          <text x="35" y="180" font-size="10" fill="#64748b">Tracks: Process Pointer | Client ID (CID) | IRP List | Security Token</text>

          <!-- Microkernel Embedded KTHREAD -->
          <rect x="35" y="195" width="330" height="125" rx="5" fill="#f1f5f9" stroke="#0284c7" stroke-width="1.5" />
          <text x="45" y="215" font-size="11" font-weight="700" fill="#0284c7">KTHREAD (Microkernel Schedulable Unit)</text>
          <rect x="45" y="225" width="310" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1" />
          <text x="55" y="241" font-family="var(--font-mono)" font-size="10" fill="#334155">Kernel Stack (24KB) &amp; Machine Trap Frame</text>
          <rect x="45" y="255" width="310" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1" />
          <text x="55" y="271" font-family="var(--font-mono)" font-size="10" fill="#334155">Dispatcher Header (Signaled/Non-Signaled State)</text>
          <rect x="45" y="285" width="310" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1" />
          <text x="55" y="301" font-family="var(--font-mono)" font-size="10" fill="#334155">Scheduling Priority (0-31) &amp; Quantum Counters</text>

          <!-- Connecting Pointer -->
          <path d="M 200 145 L 200 115" stroke="#0284c7" stroke-width="2" marker-end="url(#link-arr)" />
        </g>

        <!-- Right Column: Linux Task Group Model -->
        <g transform="translate(430, 10)">
          <rect x="0" y="0" width="415" height="350" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
          <text x="20" y="28" font-size="13" font-weight="700" fill="#0f172a">LINUX: UNIFIED TASK_STRUCT GROUP</text>

          <!-- Task 1 (Group Leader) -->
          <g transform="translate(20, 45)">
            <rect x="0" y="0" width="175" height="135" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
            <text x="12" y="20" font-size="11" font-weight="700" fill="#0f172a">task_struct (Leader)</text>
            <text x="12" y="36" font-family="var(--font-mono)" font-size="9" fill="#0369a1">PID: 401 | TGID: 401</text>
            <rect x="10" y="45" width="155" height="22" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
            <text x="16" y="60" font-family="var(--font-mono)" font-size="9" fill="#0369a1">mm_struct *mm</text>
            <rect x="10" y="72" width="155" height="22" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
            <text x="16" y="87" font-family="var(--font-mono)" font-size="9" fill="#0369a1">files_struct *files</text>
            <rect x="10" y="99" width="155" height="22" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
            <text x="16" y="114" font-family="var(--font-mono)" font-size="9" fill="#0369a1">sighand_struct *sig</text>
          </g>

          <!-- Task 2 (Sibling Thread) -->
          <g transform="translate(220, 45)">
            <rect x="0" y="0" width="175" height="135" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
            <text x="12" y="20" font-size="11" font-weight="700" fill="#0f172a">task_struct (Sibling)</text>
            <text x="12" y="36" font-family="var(--font-mono)" font-size="9" fill="#0369a1">PID: 402 | TGID: 401</text>
            <rect x="10" y="45" width="155" height="22" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
            <text x="16" y="60" font-family="var(--font-mono)" font-size="9" fill="#0369a1">mm_struct *mm</text>
            <rect x="10" y="72" width="155" height="22" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
            <text x="16" y="87" font-family="var(--font-mono)" font-size="9" fill="#0369a1">files_struct *files</text>
            <rect x="10" y="99" width="155" height="22" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
            <text x="16" y="114" font-family="var(--font-mono)" font-size="9" fill="#0369a1">sighand_struct *sig</text>
          </g>

          <!-- Thread Group Double Linkage -->
          <path d="M 195 70 L 220 70" stroke="#0284c7" stroke-width="2" marker-end="url(#link-arr)" />
          <path d="M 220 85 L 195 85" stroke="#0284c7" stroke-width="2" marker-end="url(#link-arr)" />
          <text x="207" y="64" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#64748b">thread_group</text>

          <!-- Shared Kernel Resources Below -->
          <rect x="20" y="215" width="375" height="115" rx="6" fill="#ffffff" stroke="#059669" stroke-width="1.5" />
          <text x="35" y="235" font-size="11" font-weight="700" fill="#059669">SHARED RESOURCE STRUCTURES (Count &gt; 1)</text>

          <rect x="35" y="245" width="110" height="70" rx="4" fill="#f0fdf4" stroke="#86efac" />
          <text x="45" y="265" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">mm_struct</text>
          <text x="45" y="282" font-size="9" fill="#334155">Page Tables</text>
          <text x="45" y="296" font-size="9" fill="#334155">Virtual Maps</text>

          <rect x="155" y="245" width="115" height="70" rx="4" fill="#f0fdf4" stroke="#86efac" />
          <text x="165" y="265" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">files_struct</text>
          <text x="165" y="282" font-size="9" fill="#334155">File Descriptors</text>
          <text x="165" y="296" font-size="9" fill="#334155">Socket Tables</text>

          <rect x="280" y="245" width="105" height="70" rx="4" fill="#f0fdf4" stroke="#86efac" />
          <text x="290" y="265" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">sighand</text>
          <text x="290" y="282" font-size="9" fill="#334155">Signal Actions</text>
          <text x="290" y="296" font-size="9" fill="#334155">Mask Rules</text>

          <!-- Converging Shared Pointers -->
          <path d="M 105 180 L 105 240" stroke="#059669" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#shared-arr)" />
          <path d="M 305 180 L 105 240" stroke="#059669" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#shared-arr)" />
        </g>
      </svg>
    </div>
"""

    anchor = "    <h3>4. Direct Architectural Comparison: Windows vs. POSIX/Linux</h3>"
    if "Visual Topology Comparison: Windows NT vs. Linux Task Groups" not in content:
        content = content.replace(anchor, anchor + "\n" + svg_diagram_html)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully injected visual topology diagram into {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add visual topology diagram of Windows vs Linux threads to Module 04\n\n"
            "Embed SVG architectural diagrams illustrating Windows ETHREAD/KTHREAD/TEB\n"
            "layering alongside Linux task_struct thread group pointer linkages."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_topology_diagram()
