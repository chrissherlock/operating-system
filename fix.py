#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 1 on Deadlock Prevention vs Avoidance in Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "03-deadlock-handling-bankers-algorithm.html"
)

PREVENTION_VS_AVOIDANCE_SECTION = r"""      <h3>1. Deadlock Prevention vs. Avoidance</h3>
      <p>
        When designing operating system resource management subsystems, concurrency architects face a fundamental choice between <strong>Deadlock Prevention</strong> and <strong>Deadlock Avoidance</strong>. Both strategies guarantee that the system will never enter a deadlocked state, but they achieve this security through radically different philosophical and architectural mechanisms.
      </p>

      <h4>1. Deadlock Prevention: Structural Constraint Enforcement</h4>
      <p>
        Deadlock prevention operates on a static principle: <em>design the operating system rules such that at least one of the Four Coffman Conditions can never possibly be satisfied</em>. By structurally prohibiting one of the necessary preconditions, deadlock becomes mathematically impossible.
      </p>
      <ul>
        <li>
          <strong>Negating Mutual Exclusion:</strong> Spooling device outputs (such as printer queues) so that physical devices appear shareable. However, non-shareable hardware resources like exclusive locks or hardware registers cannot have mutual exclusion eliminated.
        </li>
        <li>
          <strong>Negating Hold and Wait:</strong> Requiring processes to request and be allocated <em>all</em> required resources simultaneously at startup before execution begins. While effective, this creates severe resource underutilization (holding devices idly for hours).
        </li>
        <li>
          <strong>Negating No Preemption:</strong> Forcibly expropriating resources from a waiting process if its additional requests cannot be immediately satisfied. This works well for CPU registers and memory pages, but fails for stateful hardware devices or active database write transactions.
        </li>
        <li>
          <strong>Negating Circular Wait:</strong> Imposing a strict global partial ordering on all resource types ($R_1, R_2, \dots, R_m$) and requiring processes to request resources in an increasing numerical sequence.
        </li>
      </ul>

      <h4>2. Deadlock Avoidance: Dynamic State Inspection</h4>
      <p>
        Deadlock prevention often results in poor device utilization and unnecessary process blocking because its restrictions are overly conservative. <strong>Deadlock avoidance</strong>, by contrast, takes a more flexible approach. It permits processes to request resources dynamically, but subjects every request to a runtime safety audit.
      </p>
      <p>
        Instead of constraining system rules upfront, the operating system requires each process to declare its <strong>maximum lifetime resource claims</strong> in advance (${\text{Max}}_{ij}$). Before granting any immediate resource request, the kernel evaluates the future trajectory of the system:
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">The Avoidance Invariant:</strong>
        <br><br>
        $$ \text{Grant Request} \iff \exists \text{ a safe execution sequence } \langle P_0, P_1, \dots, P_n \rangle \text{ such that all claims can be satisfied} $$
      </div>

      <p>
        If granting a request leads to a <em>safe state</em> (where the kernel can guarantee every process eventually gets its maximum declared resources), the request is approved. If the allocation leads to an <em>unsafe state</em> (a state from which deadlock is mathematically possible if all processes suddenly demand their maximum claims), the kernel suspends the requesting process until resources can be safely allocated.
      </p>

      <h4>3. Architectural Trade-Offs</h4>
      <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.88rem;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px; text-align: left; color: var(--primary);">Metric</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Deadlock Prevention</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Deadlock Avoidance</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">A Priori Information</td>
            <td style="padding: 10px;">Not required. Operates purely on runtime rules.</td>
            <td style="padding: 10px;">Required. Processes must declare maximum resource claims upfront.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Resource Utilization</td>
            <td style="padding: 10px; color: #dc2626;">Low to Moderate (due to strict static constraints).</td>
            <td style="padding: 10px; color: #16a34a;">High (resources allocated dynamically based on live needs).</td>
          </tr>
          <tr>
            <td style="padding: 10px; font-weight: 600;">Runtime Overhead</td>
            <td style="padding: 10px; color: #16a34a;">Minimal (simple rule enforcement).</td>
            <td style="padding: 10px; color: #d97706;">Moderate to High ($O(m \times n^2)$ matrix safety checks per request).</td>
          </tr>
        </tbody>
      </table>"""

def update_section_one():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. Deadlock Prevention vs. Avoidance</h3>"
    end_marker = "<h3>2. Dijkstra's Banker's Algorithm</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 03.")
        return False

    updated_content = content[:start_idx] + PREVENTION_VS_AVOIDANCE_SECTION + "\n\n      " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_section_one():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Section 1 on Deadlock Prevention vs Avoidance in Module 03\n\n"
                "Provide rigorous architectural comparisons between static Coffman condition\n"
                "prevention and dynamic state inspection avoidance strategies."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
