#!/usr/bin/env python3
# =====================================================================
# fix.py: Integrate KaTeX and format equations using standard LaTeX in Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

KATEX_HEAD_SNIPPET = r"""  <!-- KaTeX CSS & JS CDN -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css" crossorigin="anonymous">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" crossorigin="anonymous" onload="renderMathInElement(document.body, { delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}] });"></script>"""

KATEX_DEADLOCK_SECTION = r"""    <h3>1. Formal Definition of System Deadlock</h3>
    <p>
      In operating systems and concurrent computing theory, a <strong>system deadlock</strong> is defined as a permanent blockade state where a set of two or more execution entities (threads or processes) are unable to make forward progress because each entity is waiting for a resource that is currently held by another entity in the set.
    </p>

    <h4>Formal Mathematical Formulation</h4>
    <p>
      Let $P = \{P_1, P_2, \dots, P_n\}$ be a finite set of concurrent processes, and let $R = \{R_1, R_2, \dots, R_m\}$ represent the available resource types in the operating system, where each resource type $R_j$ may consist of one or more identical instances.
    </p>
    <p>
      A subset of processes $P' \subset P$ is said to be in a <strong>deadlock state</strong> if and only if every process $P_i \in P'$ is indefinitely waiting for an event that can only be caused by another process $P_k \in P'$ (where $k \neq i$).
    </p>

    <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
      <strong style="color: var(--primary);">Closed-Set Deadlock Condition:</strong>
      <br><br>
      $$ \forall P_i \in P', \quad \text{State}(P_i) = \text{BLOCKED} \quad (\text{waiting on resource } R_j \text{ held by } P_k \in P') $$
    </div>

    <p>
      Because every entity in the closed chain is blocked waiting for a predecessor or successor, no process can ever release its currently allocated resources. Consequently, the entire set remains frozen indefinitely unless an external agent intervenes (such as a kernel detection-and-recovery subsystem or a watchdog timer).
    </p>"""

def update_with_katex():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert KaTeX into head if not already present
    if "katex.min.css" not in content:
        content = content.replace("</head>", KATEX_HEAD_SNIPPET + "\n</head>")

    start_marker = "<h3>1. Formal Definition of System Deadlock</h3>"
    end_marker = "<h3>2. The Four Coffman Conditions</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 02.")
        return False

    updated_content = content[:start_idx] + KATEX_DEADLOCK_SECTION + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully integrated KaTeX into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_with_katex():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Integrate KaTeX math rendering into Module 02 Section 1\n\n"
                "Add KaTeX CDN assets and auto-render scripts, and convert mathematical\n"
                "expressions to standard LaTeX inline and display math syntax."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
