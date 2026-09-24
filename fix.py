#!/usr/bin/env python3
# =====================================================================
# fix.py: Syntax highlight Strict Alternation snippet in Module 01
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "01-race-conditions-critical-regions.html"
)

# Highlighted replacement snippet
HIGHLIGHTED_STRICT_ALT = r"""    <pre><code><span class="syn-cmt">/* FLAWED ATTEMPT: Strict Alternation via Turn Variable */</span>
<span class="syn-kw">int</span> turn = <span class="syn-num">0</span>; <span class="syn-cmt">/* turn == 0 &rarr; P0 runs; turn == 1 &rarr; P1 runs */</span>

<span class="syn-cmt">/* --- Process 0 Code --- */</span>
<span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
    <span class="syn-kw">while</span> (turn != <span class="syn-num">0</span>);      <span class="syn-cmt">/* Entry section: wait for turn */</span>
    <span class="syn-fn">critical_region</span>();
    turn = <span class="syn-num">1</span>;               <span class="syn-cmt">/* Exit section: pass turn to P1 */</span>
    <span class="syn-fn">remainder_section</span>();    <span class="syn-cmt">/* Remainder: non-critical work */</span>
}

<span class="syn-cmt">/* --- Process 1 Code --- */</span>
<span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
    <span class="syn-kw">while</span> (turn != <span class="syn-num">1</span>);      <span class="syn-cmt">/* Entry section: wait for turn */</span>
    <span class="syn-fn">critical_region</span>();
    turn = <span class="syn-num">0</span>;               <span class="syn-cmt">/* Exit section: pass turn to P0 */</span>
    <span class="syn-fn">remainder_section</span>();    <span class="syn-cmt">/* Remainder: non-critical work */</span>
}</code></pre>"""

# Syntax CSS rules to ensure colors render
SYNTAX_CSS = r"""    /* Syntax Highlighting */
    .syn-kw { color: #38bdf8; font-weight: 600; }
    .syn-fn { color: #60a5fa; font-weight: 600; }
    .syn-num { color: #f59e0b; }
    .syn-str { color: #34d399; }
    .syn-cmt { color: #64748b; font-style: italic; }"""

def update_strict_alternation_highlighting():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate the Strict Alternation code block
    start_marker = "<h5>The Classic Failure: Strict Alternation (Turn Variable)</h5>"
    div_marker = '<div class="math-callout">'

    start_pos = content.find(start_marker)
    if start_pos == -1:
        print("Error: Could not locate Section 4 marker.")
        return False

    div_pos = content.find(div_marker, start_pos)
    if div_pos == -1:
        print("Error: Could not locate following math-callout.")
        return False

    pre_start = content.find("<pre>", start_pos)
    pre_end = content.find("</pre>", pre_start) + len("</pre>")

    if pre_start == -1 or pre_end == -1 or pre_start > div_pos:
        print("Error: Could not isolate <pre> element for Strict Alternation.")
        return False

    content = content[:pre_start] + HIGHLIGHTED_STRICT_ALT.strip() + content[pre_end:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully syntax-highlighted Strict Alternation snippet in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Syntax highlight Strict Alternation code snippet in Module 01\n\n"
            "Apply semantic syntax tokens (keywords, functions, comments, and numbers)\n"
            "to the turn variable code snippet in Section 4 of Module 01."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_strict_alternation_highlighting():
        run_git_sync()
