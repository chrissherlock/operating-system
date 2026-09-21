#!/usr/bin/env python3
# =====================================================================
# fix.py: Clarify Multiply-Accumulate scenario in pipeline simulator
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

NEW_INSTRUCTIONS_BOX = """        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">The Scenario: Computing a Multiply-Accumulate (MAC) Step</div>
          <p style="margin: 0 0 8px 0; color: #1e293b; font-size: 0.9rem; line-height: 1.5;">
            We are computing one single term of a vector dot product: <strong><code>sum = sum + (A &times; B)</code></strong>. This Multiply-Accumulate operation is the foundational math kernel used in 3D graphics transforms, audio DSP filters, and machine learning tensor operations:
          </p>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; margin-bottom: 10px;">
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #0284c7; font-family: var(--font-mono);">I1: LOAD R1, [A]</strong>
              <div style="color: #64748b; margin-top: 2px;">Fetch value <em>A</em> from RAM into scratch register <code>R1</code>.</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #0284c7; font-family: var(--font-mono);">I2: LOAD R2, [B]</strong>
              <div style="color: #64748b; margin-top: 2px;">Fetch value <em>B</em> from RAM into scratch register <code>R2</code>.</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #0284c7; font-family: var(--font-mono);">I3: MUL R3, R1, R2</strong>
              <div style="color: #64748b; margin-top: 2px;">Multiply <code>R1 &times; R2</code> and store product in <code>R3</code>.</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #0284c7; font-family: var(--font-mono);">I4: ADD R4, R4, R3</strong>
              <div style="color: #64748b; margin-top: 2px;">Accumulate: add product <code>R3</code> into total <code>R4</code>.</div>
            </div>
          </div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.84rem; line-height: 1.5;">
            <li><strong>Independent Operations (I1 &amp; I2):</strong> Reading <em>A</em> and <em>B</em> have zero dependencies on each other—demonstrating how superscalar dual-issue cores and multicore CPUs execute loads concurrently.</li>
            <li><strong>Data Dependencies (RAW Hazards):</strong> <code>I3</code> cannot multiply until <code>I1</code> and <code>I2</code> deliver their data, and <code>I4</code> cannot accumulate until <code>I3</code> finishes multiplying—revealing why hardware requires data forwarding bypasses.</li>
            <li><strong>Throughput Comparison:</strong> Observe how execution drops from <strong>16 cycles</strong> (unpipelined) &rarr; <strong>7 cycles</strong> (pipelined) &rarr; <strong>4 cycles</strong> (superscalar/multicore).</li>
          </ol>
        </div>"""

def update_scenario_briefing():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Match the previous instructions block inside interactive-pipeline-simulator
    pattern = r'<!-- Instructions Guide -->\s*<div style="background: #f1f5f9;.*?</div>\s*<!-- Action Controls'
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        replacement = NEW_INSTRUCTIONS_BOX + "\n\n        <!-- Action Controls"
        content = content[:match.start()] + replacement + content[match.end():]
        print("--> Replaced scenario instructions guide with detailed MAC explanation.")
    else:
        # Fallback: target by text substring
        fallback_pattern = r'<div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">\s*<div style="font-family: var\(--font-mono\); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">Workload Scenario &amp; Instructions</div>.*?</div>'
        match_fallback = re.search(fallback_pattern, content, flags=re.DOTALL)
        if match_fallback:
            content = content[:match_fallback.start()] + NEW_INSTRUCTIONS_BOX.strip() + content[match_fallback.end():]
            print("--> Replaced scenario instructions via fallback pattern.")
        else:
            print("--> Error: could not locate scenario instructions block in 02-hardware-review.html.")
            return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Clarify vector dot-product scenario in instruction pipeline walkthrough\n\n"
            "Clarify the mathematical Multiply-Accumulate formula (sum = sum + A * B)\n"
            "and provide plain-English explanations for I1-I4 in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for 02-hardware-review.html!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_scenario_briefing()
