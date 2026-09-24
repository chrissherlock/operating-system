#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix SVG arrowheads and trajectories in Figure 3.1 of Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "04-thread-implementation.html")

def adjust_figure_arrows():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate Figure 3.1 container
    start_idx = content.find("Figure 3.1: Linux Thread Group Hierarchy")
    if start_idx == -1:
        print("Error: Figure 3.1 not found in target file.")
        return

    div_start = content.rfind("<div style=", 0, start_idx)
    div_end = content.find("</div>", start_idx)
    div_end = content.find("</div>", div_end + 1) + 6  # Outer wrapper closing div

    clean_svg_block = r"""<div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.1: Linux Thread Group Hierarchy (PID vs. TGID Representation)</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Every thread is an independent task_struct, unified under a shared TGID matching the Group Leader's PID.</div>

      <svg viewBox="0 0 820 330" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <!-- Blue Arrow for Horizontal Sibling Links -->
          <marker id="nptl-arr-right" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 2 L 8 5 L 0 8 z" fill="#0284c7" />
          </marker>
          <marker id="nptl-arr-left" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 2 L 8 5 L 0 8 z" fill="#0284c7" />
          </marker>
          <!-- Slate Upward Arrow for Parent Linkage -->
          <marker id="parent-up-arr" viewBox="0 0 10 10" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 8 L 5 1 L 9 8 z" fill="#475569" />
          </marker>
          <!-- Upward Arrow for Circular List Return Arc -->
          <marker id="circ-up-arr" viewBox="0 0 10 10" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 8 L 5 1 L 9 8 z" fill="#0284c7" />
          </marker>
        </defs>

        <!-- Outer Parent (bash shell) at top center -->
        <g id="box-parent-bash" transform="translate(270, 10)">
          <rect width="280" height="46" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 3"/>
          <text x="140" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">PARENT PROCESS: bash (PID 2000)</text>
          <text x="140" y="37" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">Shared real_parent for all thread tasks</text>
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

        <!-- Upward Lines pointing into bottom of bash (PID 2000) -->
        <!-- Task 1 upward link -->
        <path d="M 145 95 C 145 74, 320 74, 320 58" fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#parent-up-arr)"/>
        <!-- Task 2 upward link -->
        <path d="M 410 95 L 410 58" fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#parent-up-arr)"/>
        <!-- Task 3 upward link -->
        <path d="M 675 95 C 675 74, 500 74, 500 58" fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#parent-up-arr)"/>

        <!-- Horizontal Bidirectional Sibling Links (thread_group) -->
        <!-- Task 1 -> Task 2 -->
        <path d="M 260 215 L 293 215" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr-right)"/>
        <!-- Task 2 -> Task 1 -->
        <path d="M 295 230 L 262 230" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr-left)"/>

        <!-- Task 2 -> Task 3 -->
        <path d="M 525 215 L 558 215" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr-right)"/>
        <!-- Task 3 -> Task 2 -->
        <path d="M 560 230 L 527 230" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#nptl-arr-left)"/>

        <!-- Circular Return Link: Task 3 (bottom) returning upward into Task 1 -->
        <path d="M 675 285 C 675 318, 145 318, 145 288" fill="none" stroke="#0284c7" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#circ-up-arr)"/>
        <text x="410" y="322" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#0284c7">thread_group circular list (sibling 3 &rarr; leader 1)</text>
      </svg>
    </div>"""

    content = content[:div_start] + clean_svg_block + content[div_end:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully corrected arrow endpoints in Figure 3.1 of {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix arrow directions and marker orientations in Figure 3.1\n\n"
            "Correct SVG marker definitions and path vector trajectories so arrowheads\n"
            "point directly into target nodes for parent linkages and circular lists."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    adjust_figure_arrows()
