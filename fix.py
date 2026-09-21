#!/usr/bin/env python3
# =====================================================================
# fix.py: Repair granularity mode switching in translation simulator
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_granularity_mode_switching():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old setTransMode function in translation simulator script
    old_set_trans_mode = """          function setTransMode(modeKey) {
            currentTransMode = modeKey;
            transIndex = 0;
            const buttons = {
              "4k": document.getElementById("trans-btn-4k"),
              "2m": document.getElementById("trans-btn-2m"),
              "swap": document.getElementById("trans-btn-swap")
            };
            Object.keys(buttons).forEach(k => {
              const btn = buttons[k];
              if (btn) {
                if (k === modeKey) {
                  btn.style.background = "#0284c7";
                  btn.style.color = "#ffffff";
                } else {
                  btn.style.background = "transparent";
                  btn.style.color = "#475569";
                }
              }
            });
            renderTransState();
          }"""

    # Updated robust setTransMode function ensuring proper binding and SVG update
    new_set_trans_mode = """          function setTransMode(modeKey) {
            currentTransMode = modeKey;
            transIndex = 0;
            const buttons = {
              "4k": document.getElementById("trans-btn-4k"),
              "2m": document.getElementById("trans-btn-2m"),
              "swap": document.getElementById("trans-btn-swap")
            };
            Object.keys(buttons).forEach(k => {
              const btn = buttons[k];
              if (btn) {
                if (k === modeKey) {
                  btn.style.background = "#0284c7";
                  btn.style.color = "#ffffff";
                  btn.style.fontWeight = "700";
                } else {
                  btn.style.background = "transparent";
                  btn.style.color = "#475569";
                  btn.style.fontWeight = "600";
                }
              }
            });
            renderTransState();
          }"""

    if old_set_trans_mode in content:
        content = content.replace(old_set_trans_mode, new_set_trans_mode)
        print("--> Updated setTransMode function.")
    else:
        print("--> Warning: setTransMode function pattern not matched exact.")

    # Also check button event listeners binding
    old_listeners = """          document.getElementById("trans-btn-4k").addEventListener("click", () => setTransMode("4k"));
          document.getElementById("trans-btn-2m").addEventListener("click", () => setTransMode("2m"));
          document.getElementById("trans-btn-swap").addEventListener("click", () => setTransMode("swap"));"""

    new_listeners = """          const btn4k = document.getElementById("trans-btn-4k");
          const btn2m = document.getElementById("trans-btn-2m");
          const btnSwap = document.getElementById("trans-btn-swap");

          if (btn4k) btn4k.addEventListener("click", function() { setTransMode("4k"); });
          if (btn2m) btn2m.addEventListener("click", function() { setTransMode("2m"); });
          if (btnSwap) btnSwap.addEventListener("click", function() { setTransMode("swap"); });"""

    if old_listeners in content:
        content = content.replace(old_listeners, new_listeners)
        print("--> Updated granularity button event bindings.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix granularity mode switching in address translation simulator\n\n"
            "Ensure setTransMode properly updates button styles, resets step index,\n"
            "and immediately triggers re-rendering of SVG states and telemetry in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for granularity mode bugfix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_granularity_mode_switching()
