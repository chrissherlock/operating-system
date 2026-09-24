#!/usr/bin/env python3
# =====================================================================
# fix.py: Remove YouTube video references from Module 02 Section 1
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

CLEAN_DEADLOCK_SECTION = r"""    <h3>1. Formal Definition of System Deadlock</h3>
    <p>
      In operating systems and concurrent computing theory, a <strong>system deadlock</strong> is defined as a permanent blockade state where a set of two or more execution entities (threads or processes) are unable to make forward progress because each entity is waiting for a resource that is currently held by another entity in the set.
    </p>

    <h4>Formal Mathematical Formulation</h4>
    <p>
      Let <code>P = {P_1, P_2, ..., P_n}</code> be a finite set of concurrent processes, and let <code>R = {R_1, R_2, ..., R_m}</code> represent the available resource types in the operating system, where each resource type <code>R_j</code> may consist of one or more identical instances.
    </p>
    <p>
      A subset of processes <code>P' &subset; P</code> is said to be in a <strong>deadlock state</strong> if and only if every process <code>P_i &isin; P'</code> is indefinitely waiting for an event that can only be caused by another process <code>P_k &isin; P'</code> (where <code>k &ne; i</code>).
    </p>

    <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
      <strong style="color: var(--primary);">Closed-Set Deadlock Condition:</strong>
      <br>
      <code>&forall; P_i &isin; P', \quad State(P_i) = BLOCKED \quad \text{waiting on resource } R_j \text{ held by } P_k &isin; P'</code>
    </div>

    <p>
      Because every entity in the closed chain is blocked waiting for a predecessor or successor, no process can ever release its currently allocated resources. Consequently, the entire set remains frozen indefinitely unless an external agent intervenes (such as a kernel detection-and-recovery subsystem or a watchdog timer).
    </p>"""

def update_module_two_without_video():
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

    updated_content = content[:start_idx] + CLEAN_DEADLOCK_SECTION + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully removed video and cleaned up Section 1 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_module_two_without_video():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Remove YouTube video card from Section 1 in Module 02\n\n"
                "Clean up Module 02 Section 1 by removing the embedded video card and links,\n"
                "retaining only the formal mathematical definition and closed-set equations."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
