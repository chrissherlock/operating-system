#!/usr/bin/env python3
# =====================================================================
# fix.py: Apply grey margin and white container layout to Modules 1 and 2
# =====================================================================
import os
import subprocess

TARGET_FILES = [
    os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html"),
    os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
]

CONTAINER_CSS = """  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    body {
      font-family: var(--font-sans);
      color: #1e293b;
      background: #f8fafc;
      margin: 0;
      padding: 32px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .module-nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid #cbd5e1;
    }
    .module-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      color: #334155;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      transition: all 0.15s ease;
    }
    .module-nav-btn:hover {
      background-color: #f1f5f9;
      color: #0f172a;
      border-color: #94a3b8;
    }
  </style>"""

def update_module_layout():
    for target_path in TARGET_FILES:
        if not os.path.exists(target_path):
            print(f"Skipping {target_path}: file not found.")
            continue

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Ensure container div wraps the content if missing
        if '<div class="container">' not in content:
            content = content.replace("<body>", "<body>\n  <div class=\"container\">")
            content = content.replace("</body>", "  </div>\n</body>")

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py"] + TARGET_FILES, check=True)
        commit_msg = (
            "Apply grey margins and white container layout to Modules 1 and 2\n\n"
            "Ensure week01-operating-system-concepts/01-what-is-an-os-and-history.html\n"
            "and week01-operating-system-concepts/02-hardware-review.html share the exact\n"
            "grey body background with bordered white content containers."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for container layouts!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_module_layout()
