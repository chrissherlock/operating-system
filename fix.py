#!/usr/bin/env python3
# =====================================================================
# fix.py: Sanitize all LaTeX math leaks in week03-process-scheduling
# =====================================================================
import os
import re
import subprocess

TARGET_DIR = "week03-process-scheduling"

def clean_latex_in_text(text: str) -> str:
    # 1. Turnaround, wait, burst, response formulas
    replacements = [
        (r"\$T_{\\text\{turnaround\}}\$", "<i>T</i><sub>turnaround</sub>"),
        (r"\$T_{\\text\{wait\}}\$", "<i>T</i><sub>wait</sub>"),
        (r"\$T_{\\text\{burst\}}\$", "<i>T</i><sub>burst</sub>"),
        (r"\$T_{\\text\{response\}}\$", "<i>T</i><sub>response</sub>"),
        (r"T_turnaround = T_completion - T_arrival", "<i>T</i><sub>turnaround</sub> = <i>T</i><sub>completion</sub> &minus; <i>T</i><sub>arrival</sub>"),
        (r"T_wait = T_turnaround - T_burst", "<i>T</i><sub>wait</sub> = <i>T</i><sub>turnaround</sub> &minus; <i>T</i><sub>burst</sub>"),
        (r"T_response = T_first_execution - T_arrival", "<i>T</i><sub>response</sub> = <i>T</i><sub>first_execution</sub> &minus; <i>T</i><sub>arrival</sub>"),
        # Exponential smoothing formula
        (r"tau_\{n\+1\}\s*=\s*alpha\s*\*\s*t_n\s*\+\s*\(1\s*-\s*alpha\)\s*\*\s*tau_n",
         "&tau;<sub><i>n</i>+1</sub> = &alpha;<i>t</i><sub><i>n</i></sub> + (1 &minus; &alpha;)&tau;<sub><i>n</i></sub>"),
        (r"<code>tau_\{n\+1\} = alpha \* t_n \+ \(1 - alpha\) \* tau_n</code>",
         "<code>&tau;<sub><i>n</i>+1</sub> = &alpha;<i>t</i><sub><i>n</i></sub> + (1 &minus; &alpha;)&tau;<sub><i>n</i></sub></code>"),
        # Real-time schedulability formula
        (r"\$m\$", "<i>m</i>"),
        (r"\$P_i\$", "<i>P</i><sub><i>i</i></sub>"),
        (r"\$C_i\$", "<i>C</i><sub><i>i</i></sub>"),
        (r"sum_\{i=1\}\^\{m\}\s*\(C_i\s*/\s*P_i\)\s*<=\s*1",
         "&sum;<sub><i>i</i>=1</sub><sup><i>m</i></sup> (<i>C</i><sub><i>i</i></sub> / <i>P</i><sub><i>i</i></sub>) &le; 1"),
        (r"<code>sum_\{i=1\}\^\{m\} \(C_i / P_i\) &lt;= 1</code>",
         "<code>&sum;<sub><i>i</i>=1</sub><sup><i>m</i></sup> (<i>C</i><sub><i>i</i></sub> / <i>P</i><sub><i>i</i></sub>) &le; 1</code>"),
        (r"<code>sum_\{i=1\}\^\{m\} \(C_i / P_i\) <= 1</code>",
         "<code>&sum;<sub><i>i</i>=1</sub><sup><i>m</i></sup> (<i>C</i><sub><i>i</i></sub> / <i>P</i><sub><i>i</i></sub>) &le; 1</code>"),
        (r"<code>t_n</code>", "<code><i>t</i><sub><i>n</i></sub></code>"),
        (r"<code>tau_n</code>", "<code>&tau;<sub><i>n</i></sub></code>"),
        (r"<code>alpha</code>", "<code>&alpha;</code>"),
    ]

    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)

    # General cleanup for any residual LaTeX math tags $...$
    def math_token_repl(m):
        content = m.group(1)
        content = content.replace(r"\text{", "").replace("}", "")
        content = content.replace("_", " ")
        return f"<i>{content}</i>"

    text = re.sub(r"\$([a-zA-Z0-9_\{\}\\]+)\$", math_token_repl, text)
    return text

def execute_latex_cleanup():
    modified_files = []

    if not os.path.exists(TARGET_DIR):
        print(f"Error: Directory {TARGET_DIR} not found.")
        return

    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    original = f.read()

                cleaned = clean_latex_in_text(original)
                if cleaned != original:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(cleaned)
                    modified_files.append(path)
                    print(f"--> Cleaned LaTeX math leaks in {path}")

    if not modified_files:
        print("--> No LaTeX leaks detected in target files.")
        return

    try:
        subprocess.run(["git", "add"] + modified_files + ["fix.py"], check=True)
        commit_msg = (
            "Sanitize LaTeX math leaks into semantic HTML entities in Week 3\n\n"
            "Convert raw LaTeX math delimiters and subscript notation to HTML italic\n"
            "variables, sub/sup tags, and Unicode mathematical entities (&tau;, &alpha;)."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_latex_cleanup()
