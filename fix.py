#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace broken LaTeX markup with clean semantic HTML math in Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

CORRECTED_DEADLOCK_SECTION = r"""    <h3>1. Formal Definition of System Deadlock</h3>
    <p>
      In operating systems and concurrent computing theory, a <strong>system deadlock</strong> is defined as a permanent blockade state where a set of two or more execution entities (threads or processes) are unable to make forward progress because each entity is waiting for a resource that is currently held by another entity in the set.
    </p>

    <h4>Formal Mathematical Formulation</h4>
    <p>
      Let <i>P</i> = {<i>P</i><sub>1</sub>, <i>P</i><sub>2</sub>, ..., <i>P<sub>n</sub></i>} be a finite set of concurrent processes, and let <i>R</i> = {<i>R</i><sub>1</sub>, <i>R</i><sub>2</sub>, ..., <i>R<sub>m</sub></i>} represent the available resource types in the operating system, where each resource type <i>R<sub>j</sub></i> may consist of one or more identical instances.
    </p>
    <p>
      A subset of processes <i>P'</i> &sub; <i>P</i> is said to be in a <strong>deadlock state</strong> if and only if every process <i>P<sub>i</sub></i> &isin; <i>P'</i> is indefinitely waiting for an event that can only be caused by another process <i>P<sub>k</sub></i> &isin; <i>P'</i> (where <i>k</i> &ne; <i>i</i>).
    </p>

    <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
      <strong style="color: var(--primary);">Closed-Set Deadlock Condition:</strong>
      <br><br>
      &forall; <i>P<sub>i</sub></i> &isin; <i>P'</i>, &nbsp;&nbsp; State(<i>P<sub>i</sub></i>) = BLOCKED &nbsp;&nbsp; (waiting on resource <i>R<sub>j</sub></i> held by <i>P<sub>k</sub></i> &isin; <i>P'</i>)
    </div>

    <p>
      Because every entity in the closed chain is blocked waiting for a predecessor or successor, no process can ever release its currently allocated resources. Consequently, the entire set remains frozen indefinitely unless an external agent intervenes (such as a kernel detection-and-recovery subsystem or a watchdog timer).
    </p>"""

def update_math_markup():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. Formal Definition of System Deadlock</h3>"
    end_marker = "<h3>2. The Four Coffman Conditions</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 02.")
        return False

    updated_content = content[:start_idx] + CORRECTED_DEADLOCK_SECTION + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully fixed math markup in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_math_markup():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix broken math formatting in Module 02 Section 1\n\n"
                "Replace unsupported LaTeX commands with clean semantic HTML entities,\n"
                "italics, and subscripts to ensure proper browser rendering."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
