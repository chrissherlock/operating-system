#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct dashed line paths in Figure 3.1 of Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "04-thread-implementation.html")

def correct_thread_group_paths():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacement for Figure 3.1 SVG block with clean, mathematically aligned paths
    old_figure = content[content.find("Figure 3.1: Linux Thread Group Hierarchy") - 120 : content.find("</svg>\n    </div>", content.find("Figure 3.1")) + 17]

    clean_svg_block = r"""<div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.1: Linux Thread Group Hierarchy (PID vs. TGID Representation)</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Every thread is an independent task_struct, unified under a shared TGID matching the Group Leader's PID.</div>

      <svg viewBox="0 0 820 330" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="nptl-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
          <marker id="parent-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748b" />
          </marker>
        </defs>

        <!-- Outer Parent (bash shell) at top center -->
        <g id="box-parent-bash" transform="translate(270, 10)">
          <rect width="280" height="46" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 3"/>
          <text x="140" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">PARENT PROCESS: bash (PID 2000)</text>
          <text x="140" y="37" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">Direct real_parent of all threads below</text>
        </g>

        <!-- Task 1: Thread Group Leader -->
        <g transform="translate(30, 95)">
          <rect width="230" height="190" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <rect width="230" height="26" rx="6" fill="#0284c7"/>
          <text x="115" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">task_struct (Group Leader)</text>

          <rect x="15" y="36" width="200" height="24" rx="3" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="25" y="52" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">pid  = 4010 (TID: 4010)</text>

          <rect x="15" y="65" width="200" height="24" rx="3" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="81" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">tgid = 4010 (POSIX PID)</text>

          <rect x="15" y="94" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="109" font-family="var(--font-mono)" font-size="9" fill="#334155">group_leader &rarr; points to self</text>

          <rect x="15" y="121" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="136" font-family="var(--font-mono)" font-size="9" fill="#475569">real_parent  &rarr; bash (2000)</text>

          <rect x="15" y="148" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="163" font-family="var(--font-mono)" font-size="9" fill="#334155">mm, files, sighand (Shared)</text>
        </g>

        <!-- Task 2: Sibling Thread 1 -->
        <g transform="translate(295, 95)">
          <rect width="230" height="190" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <rect width="230" height="26" rx="6" fill="#0284c7"/>
          <text x="115" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">task_struct (Sibling 1)</text>

          <rect x="15" y="36" width="200" height="24" rx="3" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="25" y="52" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">pid  = 4011 (TID: 4011)</text>

          <rect x="15" y="65" width="200" height="24" rx="3" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="81" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">tgid = 4010 (POSIX PID)</text>

          <rect x="15" y="94" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="109" font-family="var(--font-mono)" font-size="9" fill="#334155">group_leader &rarr; Task 4010</text>

          <rect x="15" y="121" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="136" font-family="var(--font-mono)" font-size="9" fill="#475569">real_parent  &rarr; bash (2000)</text>

          <rect x="15" y="148" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="163" font-family="var(--font-mono)" font-size="9" fill="#334155">mm, files, sighand (Shared)</text>
        </g>

        <!-- Task 3: Sibling Thread 2 -->
        <g transform="translate(560, 95)">
          <rect width="230" height="190" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <rect width="230" height="26" rx="6" fill="#0284c7"/>
          <text x="115" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">task_struct (Sibling 2)</text>

          <rect x="15" y="36" width="200" height="24" rx="3" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="25" y="52" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">pid  = 4012 (TID: 4012)</text>

          <rect x="15" y="65" width="200" height="24" rx="3" fill="#f0fdf4" stroke="#86efac"/>
          <text x="25" y="81" font-family="var(--font-mono)" font-size="10" font-weight="700" fill="#166534">tgid = 4010 (POSIX PID)</text>

          <rect x="15" y="94" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="109" font-family="var(--font-mono)" font-size="9" fill="#334155">group_leader &rarr; Task 4010</text>

          <rect x="15" y="121" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="136" font-family="var(--font-mono)" font-size="9" fill="#475569">real_parent  &rarr; bash (2000)</text>

          <rect x="15" y="148" width="200" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="163" font-family="var(--font-mono)" font-size="9" fill="#334155">mm, files, sighand (Shared)</text>
        </g>

        <!-- Upward Dashed Lines: real_parent pointers from each task to bash -->
        <!-- From Task 1 (x=145) upward to bash bottom (x=330, y=56) -->
        <path d="M 145 95 C 145 72, 330 72, 330 56" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#parent-arr)"/>
        <!-- From Task 2 (x=410) upward to bash bottom (x=410, y=56) -->
        <path d="M 410 95 L 410 56" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#parent-arr)"/>
        <!-- From Task 3 (x=675) upward to bash bottom (x=490, y=56) -->
        <path d="M 675 95 C 675 72, 490 72, 490 56" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#parent-arr)"/>

        <!-- thread_group Circular Doubly-Linked List Pointers Between Siblings -->
        <!-- Link between Task 1 and Task 2 -->
        <path d="M 260 215 L 295 215" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr)"/>
        <path d="M 295 228 L 260 228" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr)"/>

        <!-- Link between Task 2 and Task 3 -->
        <path d="M 525 215 L 560 215" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr)"/>
        <path d="M 560 228 L 525 228" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr)"/>

        <!-- Clean Bottom Circular Return Arc: Task 3 back to Task 1 -->
        <path d="M 675 285 C 675 315, 145 315, 145 285" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#nptl-arr)"/>
        <text x="410" y="322" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#0284c7">thread_group circular list (sibling 3 &rarr; leader 1)</text>
      </svg>
    </div>"""

    content = content.replace(old_figure, clean_svg_block)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully cleaned dashed paths in Figure 3.1 of {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix dashed connector lines in Linux thread group diagram in Module 04\n\n"
            "Correct orientation and coordinate anchors for real_parent pointers to\n"
            "bash and clean up the thread_group circular linked list path in Figure 3.1."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    correct_thread_group_paths()
