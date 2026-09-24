#!/usr/bin/env python3
# =====================================================================
# fix.py: Add syntax highlighting to code snippet in Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "03-classical-threads.html")

def apply_syntax_highlighting():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Add syntax token styles if not already present
    syntax_css = """
    /* Code Syntax Highlighting Tokens */
    .syn-kwd { color: #c084fc; font-weight: 600; }
    .syn-fn  { color: #38bdf8; font-weight: 500; }
    .syn-cmt { color: #94a3b8; font-style: italic; }
    .syn-var { color: #f8fafc; }
"""
    if ".syn-kwd" not in content:
        content = content.replace("pre {", syntax_css + "\n    pre {")

    # Target the unhighlighted loop snippet
    plain_snippet = (
        '<pre>while (application_running) {\n'
        '    check_keyboard_and_mouse_events();\n'
        '    recalculate_entire_document_pagination();\n'
        '    if (autosave_timer_expired) {\n'
        '        write_document_to_disk_blocking(); /* Stalls for 50-200ms */\n'
        '    }\n'
        '}</pre>'
    )

    highlighted_snippet = (
        '<pre><code><span class="syn-kwd">while</span> (<span class="syn-var">application_running</span>) {\n'
        '    <span class="syn-fn">check_keyboard_and_mouse_events</span>();\n'
        '    <span class="syn-fn">recalculate_entire_document_pagination</span>();\n'
        '    <span class="syn-kwd">if</span> (<span class="syn-var">autosave_timer_expired</span>) {\n'
        '        <span class="syn-fn">write_document_to_disk_blocking</span>(); <span class="syn-cmt">/* Stalls for 50-200ms */</span>\n'
        '    }\n'
        '}</code></pre>'
    )

    content = content.replace(plain_snippet, highlighted_snippet)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully added syntax highlighting to {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add syntax highlighting to word processor code block in Module 03\n\n"
            "Introduce token styles and span classes to highlight keywords, functions,\n"
            "and comments in the single-threaded word processor interleaved loop snippet."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    apply_syntax_highlighting()
