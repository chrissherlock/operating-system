#!/usr/bin/env python3
# =====================================================================
# fix.py: Refine code block syntax highlighting palette in Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "03-classical-threads.html")

def adjust_palette():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace old high-contrast neon tokens with balanced editorial colors
    old_css = """    /* Code Syntax Highlighting Tokens */
    .syn-kwd { color: #c084fc; font-weight: 600; }
    .syn-fn  { color: #38bdf8; font-weight: 500; }
    .syn-cmt { color: #94a3b8; font-style: italic; }
    .syn-var { color: #f8fafc; }"""

    new_css = """    /* Code Syntax Highlighting Tokens (Refined Palette) */
    .syn-kwd { color: #f472b6; font-weight: 600; }      /* Soft rose keyword */
    .syn-fn  { color: #60a5fa; font-weight: 500; }      /* Clean sky blue function */
    .syn-cmt { color: #64748b; font-style: italic; }    /* Muted comment */
    .syn-var { color: #e2e8f0; }                        /* Soft white text */
    .syn-punc{ color: #94a3b8; }                        /* Subtle punctuation */"""

    if old_css in content:
        content = content.replace(old_css, new_css)
    else:
        # Direct class replacements if formatted slightly differently
        content = content.replace("color: #c084fc;", "color: #f472b6;")
        content = content.replace("color: #38bdf8; font-weight: 500;", "color: #60a5fa; font-weight: 500;")
        content = content.replace("color: #94a3b8; font-style: italic;", "color: #64748b; font-style: italic;")

    # Refine the code block markup to use punctuation spans for extra balance
    old_block = (
        '<pre><code><span class="syn-kwd">while</span> (<span class="syn-var">application_running</span>) {\n'
        '    <span class="syn-fn">check_keyboard_and_mouse_events</span>();\n'
        '    <span class="syn-fn">recalculate_entire_document_pagination</span>();\n'
        '    <span class="syn-kwd">if</span> (<span class="syn-var">autosave_timer_expired</span>) {\n'
        '        <span class="syn-fn">write_document_to_disk_blocking</span>(); <span class="syn-cmt">/* Stalls for 50-200ms */</span>\n'
        '    }\n'
        '}</code></pre>'
    )

    new_block = (
        '<pre><code><span class="syn-kwd">while</span> <span class="syn-punc">(</span><span class="syn-var">application_running</span><span class="syn-punc">) {</span>\n'
        '    <span class="syn-fn">check_keyboard_and_mouse_events</span><span class="syn-punc">();</span>\n'
        '    <span class="syn-fn">recalculate_entire_document_pagination</span><span class="syn-punc">();</span>\n'
        '    <span class="syn-kwd">if</span> <span class="syn-punc">(</span><span class="syn-var">autosave_timer_expired</span><span class="syn-punc">) {</span>\n'
        '        <span class="syn-fn">write_document_to_disk_blocking</span><span class="syn-punc">();</span>  <span class="syn-cmt">/* Stalls for 50-200ms */</span>\n'
        '    <span class="syn-punc">}</span>\n'
        '<span class="syn-punc">}</span></code></pre>'
    )

    content = content.replace(old_block, new_block)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully updated syntax highlighting palette in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Refine code syntax highlighting palette in Module 03\n\n"
            "Replace harsh neon syntax tokens with a muted, readable palette\n"
            "complementing the slate and dark-navy background of the code blocks."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    adjust_palette()
