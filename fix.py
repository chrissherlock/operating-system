#!/usr/bin/env python3
import os

MATHJAX_SNIPPET = """  <!-- Configure MathJax to recognize single dollar signs for inline math -->
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]
      }
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

def fix_latex_in_html():
    modified_count = 0
    for root, dirs, files in os.walk("."):
        # Skip hidden directories like .git
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                fpath = os.path.join(root, file)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check if the file contains inline math ($...$) but lacks MathJax
                if "$" in content and "mathjax" not in content.lower():
                    head_idx = content.find("</head>")
                    if head_idx != -1:
                        new_content = content[:head_idx] + MATHJAX_SNIPPET + content[head_idx:]
                        with open(fpath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"[FIXED] Added MathJax to: {fpath}")
                        modified_count += 1
                    else:
                        print(f"[SKIPPED] No </head> tag found in: {fpath}")

    print(f"\nDone! Successfully updated {modified_count} HTML file(s) with MathJax support.")

if __name__ == "__main__":
    fix_latex_in_html()
