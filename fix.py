#!/usr/bin/env python3
# =====================================================================
# fix.py: Render proper superscripts for CPU utilization formula
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "01-process-model.html")

def update_superscript_formatting():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace raw pre block with a styled formula display card
    old_formula = "<pre>CPU Utilization = 1 - p^n</pre>"
    new_formula = (
        '<div style="background: #0f172a; color: #38bdf8; font-family: var(--font-mono); '
        'font-size: 1.15rem; font-weight: 700; padding: 16px 20px; border-radius: 6px; '
        'margin: 16px 0; text-align: center; letter-spacing: 0.03em;">'
        'CPU Utilization = 1 &minus; <i>p</i><sup style="color: #4ade80; font-size: 0.85em;"><i>n</i></sup>'
        '</div>'
    )
    content = content.replace(old_formula, new_formula)

    # Replace text references like p^n with HTML or Unicode exponent in telemetry and script
    content = content.replace("All-Waiting Probability (p^n)", "All-Waiting Probability (<i>p</i><sup><i>n</i></sup>)")
    content = content.replace("0.80^2 = 0.64", "0.80² = 0.64")
    content = content.replace("0.80^3 = 51.2%", "0.80³ = 51.2%")
    content = content.replace("0.50^2 = 25%", "0.50² = 25%")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully updated superscript formatting in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix formula formatting in Section 3 to properly render superscript exponent\n\n"
            "Replace raw caret notation in the multiprogramming formula block and telemetry\n"
            "with styled HTML <sup> elements and Unicode superscripts across the module."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_superscript_formatting()
