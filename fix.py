#!/usr/bin/env python3
# =====================================================================
# fix.py: Align Modules 1 and 2 styling with Module 3 clean card layout
# =====================================================================
import os
import subprocess

FILES_TO_FIX = [
    os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html"),
    os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
]

SHARED_STYLE_BLOCK = """  <style>
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
    h1, h2, h3 {
      color: #0f172a;
    }
    h2 {
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      margin-top: 36px;
    }
    h3 {
      margin-top: 28px;
      margin-bottom: 8px;
      color: #0284c7;
      font-size: 1.15rem;
    }
    p {
      color: #475569;
      margin-bottom: 12px;
    }
    ul, ol {
      margin-left: 20px;
      color: #475569;
      margin-bottom: 12px;
    }
    li {
      margin-bottom: 4px;
    }
    code {
      font-family: var(--font-mono);
      background: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.88rem;
      color: #0369a1;
    }
    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.85rem;
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

def apply_styling_updates():
    for target_path in FILES_TO_FIX:
        if not os.path.exists(target_path):
            print(f"Skipping {target_path}: file not found.")
            continue

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace existing <style> block(s) or insert before </head>
        # For simplicity and robust consistency, let's inject the standard shared styles
        # or update body/container wrappers if needed.
        print(f"--> Updating styling for {target_path}...")

        # Ensure container div wraps the content inside body if not already present
        if '<div class="container">' not in content:
            content = content.replace("<body>", "<body>\n  <div class=\"container\">")
            content = content.replace("</body>", "  </div>\n</body>")

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py"] + FILES_TO_FIX, check=True)
        commit_msg = (
            "Align styling of hardware review and OS history modules with Module 3\n\n"
            "Update week01-operating-system-concepts/01-what-is-an-os-and-history.html\n"
            "and week01-operating-system-concepts/02-hardware-review.html to use the\n"
            "clean white background layout, padding, and typography from Module 3."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Modules 1 and 2 styling!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    apply_styling_updates()
