#!/usr/bin/env python3
# =====================================================================
# fix.py: Safely sanitize leaked LaTeX across all HTML files
# =====================================================================
import os
import re
import subprocess

def format_sub_and_sup(content: str) -> str:
    """Replaces LaTeX-style subscripts and superscripts in a string."""
    # Subscripts: _{var} or _x
    content = re.sub(r'_\{([^{}]+)\}', r'<sub>\1</sub>', content)
    content = re.sub(r'_([a-zA-Z0-9]+)', r'<sub>\1</sub>', content)
    # Superscripts: ^{var} or ^x
    content = re.sub(r'\^\{([^{}]+)\}', r'<sup>\1</sup>', content)
    content = re.sub(r'\^([a-zA-Z0-9]+)', r'<sup>\1</sup>', content)
    return content

def convert_latex_math(text: str) -> str:
    # 1. Transform fractions: \frac{num}{den} -> <sup>num</sup>&frasl;<sub>den</sub>
    def replace_frac(match):
        num = match.group(1).strip()
        den = match.group(2).strip()
        return f"<sup>{num}</sup>&frasl;<sub>{den}</sub>"

    text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', replace_frac, text)

    # 2. Map standard LaTeX symbols to HTML entities
    latex_symbols = [
        (r'\times', '&times;'),
        (r'\cdot', '&sdot;'),
        (r'\approx', '&asymp;'),
        (r'\sim', '&sim;'),
        (r'\oplus', '&oplus;'),
        (r'\rightarrow', '&rarr;'),
        (r'\leftarrow', '&larr;'),
        (r'\leq', '&le;'),
        (r'\geq', '&ge;'),
        (r'\le', '&le;'),
        (r'\ge', '&ge;'),
        (r'\neq', '&ne;'),
        (r'\ne', '&ne;'),
        (r'\dots', '&hellip;'),
        (r'\ldots', '&hellip;'),
        (r'\mu s', '&mu;s'),
        (r'\mu', '&mu;'),
        (r'\,', ' '),
        (r'\;', ' '),
        (r'\quad', ' &nbsp; ')
    ]
    for symbol, entity in latex_symbols:
        text = text.replace(symbol, entity)

    # 3. Clean common font wrappers: \text{...}, \mathbf{...}, \mathit{...}
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathbf\{([^}]+)\}', r'<strong>\1</strong>', text)
    text = re.sub(r'\\mathit\{([^}]+)\}', r'<i>\1</i>', text)

    # 4. Display Math: $$ ... $$
    def replace_display_math(match):
        inner = match.group(1).strip()
        inner = format_sub_and_sup(inner)
        inner = inner.replace('{', '').replace('}', '')
        return f'<div class="math-callout">{inner}</div>'

    text = re.sub(r'\$\$(.*?)\$\$', replace_display_math, text, flags=re.DOTALL)

    # 5. Inline Math: $ ... $
    def replace_inline_math(match):
        inner = match.group(1).strip()
        # Avoid matching currency or single digit references
        if not inner or inner.isdigit():
            return f"${inner}$"
        inner = format_sub_and_sup(inner)
        inner = inner.replace('{', '').replace('}', '')
        if inner.startswith('<div') or inner.startswith('<span'):
            return inner
        return f"<i>{inner}</i>"

    text = re.sub(r'\$([^\$\n\r]+?)\$', replace_inline_math, text)

    # 6. Specific mathematical notation cleanup
    text = text.replace('<i>10^9&times;</i>', '10<sup>9</sup>&times;')
    text = text.replace('10^{14}', '10<sup>14</sup>')
    text = text.replace('10^{-14}', '10<sup>-14</sup>')
    text = text.replace('10^{-15}', '10<sup>-15</sup>')
    text = text.replace('GF(2^8)', 'GF(2<sup>8</sup>)')
    text = text.replace('O(N^2)', '<i>O</i>(<i>N</i><sup>2</sup>)')

    return text

def sanitize_html_file(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Partition out <script>, <style>, and <pre> blocks so we don't alter JavaScript or CSS
    protected_blocks = []
    def stash_protected(match):
        protected_blocks.append(match.group(0))
        return f"___PROTECTED_BLOCK_{len(protected_blocks) - 1}___"

    # Protect script, style, pre, and svg blocks
    stashed_content = re.sub(
        r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>|<pre[\s\S]*?</pre>|<svg[\s\S]*?</svg>)',
        stash_protected,
        content,
        flags=re.IGNORECASE
    )

    # Apply LaTeX conversion only on regular HTML markup & text
    sanitized_body = convert_latex_math(stashed_content)

    # Restore protected blocks
    def restore_protected(match):
        idx = int(match.group(1))
        return protected_blocks[idx]

    final_content = re.sub(r'___PROTECTED_BLOCK_(\d+)___', restore_protected, sanitized_body)

    if final_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        return True
    return False

def scan_and_sanitize():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    modified = []

    for dirpath, _, filenames in os.walk(root_dir):
        if ".git" in dirpath or "__pycache__" in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".html"):
                path = os.path.join(dirpath, filename)
                if sanitize_html_file(path):
                    rel = os.path.relpath(path, root_dir)
                    modified.append(rel)
                    print(f"--> Cleaned LaTeX in: {rel}")

    return modified

def run_git_sync(modified):
    if not modified:
        print("No files required sanitization.")
        return

    try:
        subprocess.run(["git", "add", "fix.py"] + modified, check=True)
        commit_msg = (
            "Fix LaTeX sanitization regex handler and clean HTML math notation\n\n"
            "Resolve AttributeError in string replacement pipeline, safely convert\n"
            "inline and display LaTeX math into semantic HTML tags and entities,\n"
            "and skip script/pre blocks to preserve code blocks."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    changed_files = scan_and_sanitize()
    run_git_sync(changed_files)
