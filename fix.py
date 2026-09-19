#!/usr/bin/env python3
import os

def fix_aging_algorithm_mathjax():
    base_dir = "."
    w09_dir = os.path.join(base_dir, "week09-memory-management")
    target_file = os.path.join(w09_dir, "08-aging-algorithm.html")

    if not os.path.exists(target_file):
        print(f"Error: Could not find {target_file}")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find renderWt function and add MathJax typesetting call
    old_render_wt = """    function renderWt() {
      const s = wtSteps[wtStep];
      document.getElementById("wtCounter").textContent = `Step ${wtStep + 1} of ${wtSteps.length}`;
      document.getElementById("wtTitle").textContent = s.title;
      document.getElementById("wtText").innerHTML = s.text;"""

    new_render_wt = """    function renderWt() {
      const s = wtSteps[wtStep];
      document.getElementById("wtCounter").textContent = `Step ${wtStep + 1} of ${wtSteps.length}`;
      document.getElementById("wtTitle").textContent = s.title;
      document.getElementById("wtText").innerHTML = s.text;

      // Re-run MathJax typesetting for dynamic content
      if (window.MathJax && window.MathJax.typeset) {
        MathJax.typeset();
      }"""

    if old_render_wt in content:
        updated_content = content.replace(old_render_wt, new_render_wt)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"[SUCCESS] Added dynamic MathJax typesetting to renderWt() in {target_file}")
    else:
        print(f"[WARNING] Could not find exact renderWt signature in {target_file}. Trying alternative patch...")

        # Fallback regex patch if needed
        import re
        pattern = r'(function renderWt\s*\(\)\s*\{[^}]*document\.getElementById\("wtText"\)\.innerHTML\s*=\s*s\.text;)'
        replacement = r'\1\n      if (window.MathJax && window.MathJax.typeset) { MathJax.typeset(); }'
        updated_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"[SUCCESS] Patched {target_file} using regex.")
        else:
            print("[ERROR] Failed to apply MathJax patch.")

if __name__ == "__main__":
    fix_aging_algorithm_mathjax()
