#!/usr/bin/env python3
import os

def fix_page_jump():
    base_dir = "."
    w09_dir = os.path.join(base_dir, "week09-memory-management")
    target_file = os.path.join(w09_dir, "08-aging-algorithm.html")

    if not os.path.exists(target_file):
        print(f"Error: Could not find {target_file}")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update CSS for .tutorial-body to include a stable min-height
    old_css = """.tutorial-body {
      font-size: 0.95rem;
      line-height: 1.6;
      color: #0c4a6e;
    }"""

    new_css = """.tutorial-body {
      font-size: 0.95rem;
      line-height: 1.6;
      color: #0c4a6e;
      min-height: 75px; /* Prevents vertical reflow jumping when text changes */
    }"""

    if old_css in content:
        content = content.replace(old_css, new_css)
        print("[SUCCESS] Added min-height to .tutorial-body CSS.")
    else:
        print("[WARNING] Exact .tutorial-body CSS block not found, checking alternative...")

    # 2. Update stepWtForward and stepWtBackward to include document.activeElement.blur()
    old_js = """    function stepWtForward() {
      if (wtStep < wtSteps.length - 1) { wtStep++; renderWt(); }
    }
    function stepWtBackward() {
      if (wtStep > 0) { wtStep--; renderWt(); }
    }"""

    new_js = """    function stepWtForward() {
      if (wtStep < wtSteps.length - 1) { wtStep++; renderWt(); }
      document.activeElement.blur();
    }
    function stepWtBackward() {
      if (wtStep > 0) { wtStep--; renderWt(); }
      document.activeElement.blur();
    }"""

    if old_js in content:
        content = content.replace(old_js, new_js)
        print("[SUCCESS] Added blur() focus release to step navigation functions.")
    else:
        print("[WARNING] Exact step navigation JS block not found.")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nDone! Successfully updated {target_file}")

if __name__ == "__main__":
    fix_page_jump()
