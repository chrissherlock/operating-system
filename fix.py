#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix code background bleed and contrast in 03-classical-threads
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "03-classical-threads.html")

def apply_style_correction():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure pre code resets the inline code background and padding
    code_reset_css = """
    code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }
    pre code { background: transparent !important; color: inherit !important; padding: 0 !important; border-radius: 0 !important; font-size: inherit !important; }
"""
    if "pre code {" not in content:
        content = content.replace(
            "code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }",
            code_reset_css.strip()
        )

    # High-contrast, clean palette for dark code container
    refined_tokens_css = """    /* Code Syntax Highlighting Tokens (High Contrast) */
    .syn-kwd { color: #f43f5e; font-weight: 700; }      /* Crisp Coral Rose */
    .syn-fn  { color: #38bdf8; font-weight: 600; }      /* Bright Sky Blue */
    .syn-cmt { color: #94a3b8; font-style: italic; }    /* Visible Slate Gray */
    .syn-var { color: #f8fafc; font-weight: 500; }      /* Clean White */
    .syn-punc{ color: #cbd5e1; }                        /* Off-white brackets */"""

    # Replace syntax tokens
    if "/* Code Syntax Highlighting Tokens" in content:
        import re
        content = re.sub(
            r"/\* Code Syntax Highlighting Tokens.*?\*/.*?(?=\n\s*pre|\n\s*\.nav-bar|\n\s*code)",
            refined_tokens_css,
            content,
            flags=re.DOTALL
        )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully fixed code background and contrast in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix code block background inheritance and improve token readability\n\n"
            "Strip light inline code background from pre code blocks in Module 03 to\n"
            "prevent washed-out text and ensure high-contrast, clean code rendering."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    apply_style_correction()
