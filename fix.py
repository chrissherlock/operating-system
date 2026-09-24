#!/usr/bin/env python3
# =====================================================================
# fix.py: Purge leaked LaTeX in Module 01 and sweep all course HTML files
# =====================================================================
import os
import re
import subprocess

def clean_latex_string(content: str) -> str:
    """Converts raw LaTeX fragments to pure semantic HTML."""
    # 1. Custom replacement for the double-hop arrow expression
    content = content.replace(
        r"$$\text{Controller} \xrightarrow[\text{PCIe Bus}]{\text{Hop 1}} \text{CPU General-Purpose Register} \xrightarrow[\text{System Memory Interconnect}]{\text{Hop 2}} \text{DRAM}$$",
        """<div class="math-callout" style="text-align: center; font-family: var(--font-mono); font-size: 0.88rem;">
  Controller &mdash;[PCIe Bus (Hop 1)]&rarr; CPU Register &mdash;[Memory Interconnect (Hop 2)]&rarr; Host DRAM
</div>"""
    )

    # 2. Custom replacement for the packet rate fraction formula
    packet_formula_latex = r"$$\text{Packet Rate} = \frac{100 \times 10^9\text{ bits/sec}}{(64 + 20\text{ bytes preamble/gap}) \times 8\text{ bits/byte}} \approx \mathbf{148{,}800{,}000\text{ packets/second}}$$"
    packet_formula_html = """<div class="math-callout" style="text-align: center; font-size: 0.92rem;">
  <strong>Packet Rate</strong> = <sup>100 &times; 10<sup>9</sup> bits/sec</sup>&frasl;<sub>(64 + 20 bytes) &times; 8 bits/byte</sub> &asymp; <strong>148,800,000 packets/second</strong>
</div>"""
    content = content.replace(packet_formula_latex, packet_formula_html)

    # 3. Handle \frac{numerator}{denominator}
    def replace_fraction(match):
        num = match.group(1).strip()
        den = match.group(2).strip()
        num = re.sub(r'\\text\{([^}]+)\}', r'\1', num)
        den = re.sub(r'\\text\{([^}]+)\}', r'\1', den)
        return f"<sup>{num}</sup>&frasl;<sub>{den}</sub>"

    content = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', replace_fraction, content)

    # 4. Handle \text{...}, \mathbf{...}, \mathit{...}
    content = re.sub(r'\\text\{([^}]+)\}', r'\1', content)
    content = re.sub(r'\\mathbf\{([^}]+)\}', r'<strong>\1</strong>', content)
    content = re.sub(r'\\mathit\{([^}]+)\}', r'<i>\1</i>', content)

    # 5. Replace standard LaTeX tokens with HTML entities
    token_pairs = [
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
        (r'\,', ' '),
        (r'\;', ' '),
        (r'\quad', ' &nbsp; '),
        (r'\mu s', '&mu;s'),
        (r'\mu', '&mu;'),
        ('{,}', ',')
    ]
    for lat, htm in token_pairs:
        content = content.replace(lat, htm)

    # 6. Clean subscripts and superscripts
    content = re.sub(r'_\{([^{}]+)\}', r'<sub>\1</sub>', content)
    content = re.sub(r'\^\{([^{}]+)\}', r'<sup>\1</sup>', content)

    # 7. Display math blocks: $$ ... $$
    def replace_display(match):
        inner = match.group(1).strip()
        inner = inner.replace('{', '').replace('}', '')
        return f'<div class="math-callout">{inner}</div>'

    content = re.sub(r'\$\$(.*?)\$\$', replace_display, content, flags=re.DOTALL)

    # 8. Inline math tokens: $ ... $
    def replace_inline(match):
        inner = match.group(1).strip()
        if not inner or inner.isdigit():
            return f"${inner}$"
        inner = inner.replace('{', '').replace('}', '')
        if inner.startswith('<div') or inner.startswith('<span'):
            return inner
        return f"<i>{inner}</i>"

    content = re.sub(r'\$([^\$\n\r]+?)\$', replace_inline, content)

    # 9. Clean residual formatting
    content = content.replace('<i>10^9&times;</i>', '10<sup>9</sup>&times;')
    content = content.replace('10^{14}', '10<sup>14</sup>')
    content = content.replace('10^{-14}', '10<sup>-14</sup>')
    content = content.replace('10^{-15}', '10<sup>-15</sup>')
    content = content.replace('GF(2^8)', 'GF(2<sup>8</sup>)')
    content = content.replace('O(N^2)', '<i>O</i>(<i>N</i><sup>2</sup>)')

    return content

def sweep_and_clean_file(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    # Isolate and preserve pre, code, script, style, and svg blocks
    stashed = []
    def stash(m):
        stashed.append(m.group(0))
        return f"___LATEX_CLEAN_STASH_{len(stashed)-1}___"

    protected_pattern = r'(<pre[\s\S]*?</pre>|<script[\s\S]*?</script>|<style[\s\S]*?</style>|<svg[\s\S]*?</svg>)'
    body_masked = re.sub(protected_pattern, stash, original, flags=re.IGNORECASE)

    # Clean LaTeX in markup and prose
    cleaned_body = clean_latex_string(body_masked)

    # Restore stashed blocks
    def unstash(m):
        idx = int(m.group(1))
        return stashed[idx]

    final_content = re.sub(r'___LATEX_CLEAN_STASH_(\d+)___', unstash, cleaned_body)

    if final_content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        return True
    return False

def sweep_repository():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    changed = []

    for dirpath, _, filenames in os.walk(root_dir):
        if ".git" in dirpath or "__pycache__" in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".html"):
                path = os.path.join(dirpath, filename)
                if sweep_and_clean_file(path):
                    rel = os.path.relpath(path, root_dir)
                    changed.append(rel)
                    print(f"--> Sanitized LaTeX in: {rel}")

    return changed

def run_git_sync(changed):
    if not changed:
        print("All HTML files are already clean of LaTeX.")
        return

    try:
        subprocess.run(["git", "add", "fix.py"] + changed, check=True)
        commit_msg = (
            "Purge leaked LaTeX in Module 01 and sweep all repository HTML files\n\n"
            "Convert raw LaTeX display math and fractions into semantic HTML and\n"
            "clean mathematical entities across Week 5 and all course modules."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    modified = sweep_repository()
    run_git_sync(modified)
