#!/usr/bin/env python3
# =====================================================================
# fix.py: Incorporate formal deadlock definition and math into Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

FORMAL_DEADLOCK_SECTION = r"""    <h3>1. Formal Definition of System Deadlock</h3>
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
    </p>

    <p style="margin-top: 20px;">
      For a comprehensive video walkthrough explaining these theoretical conditions and how system deadlocks manifest in practice, review the <a href="https://www.youtube.com/watch?v=e8gMbYOmGr0" target="_blank" style="color: var(--accent); font-weight: 600; text-decoration: none;">Coffman Conditions video overview &rarr;</a>
    </p>

    <!-- YouTube Thumbnail Card -->
    <a href="https://www.youtube.com/watch?v=e8gMbYOmGr0" target="_blank" style="display: block; position: relative; max-width: 640px; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); box-shadow: 0 4px 12px rgba(0,0,0,0.06); text-decoration: none; background: #000; margin: 16px 0; transition: transform 0.15s ease, box-shadow 0.15s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.12)';" onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.06)';">
      <img src="https://img.youtube.com/vi/e8gMbYOmGr0/hqdefault.jpg" alt="Coffman Conditions Explained Thumbnail" style="width: 100%; display: block; opacity: 0.9; transition: opacity 0.15s;" onmouseover="this.style.opacity='1';" onmouseout="this.style.opacity='0.9';">
      <!-- Play Button Overlay -->
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 68px; height: 48px; background: rgba(23, 23, 23, 0.85); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <div style="width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 18px solid #ffffff; margin-left: 3px;"></div>
      </div>
      <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 14px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: #fff; font-size: 0.88rem; font-weight: 600;">
        Watch Video: Coffman Conditions &amp; Deadlock Theory &rarr;
      </div>
    </a>"""

def update_module_two():
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

    updated_content = content[:start_idx] + FORMAL_DEADLOCK_SECTION + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully incorporated formal definition into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_module_two():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Incorporate formal deadlock definition and math into Module 02\n\n"
                "Add mathematical formulation of closed-set process blocking, resource\n"
                "instances, and Coffman Conditions video link into Module 02."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
