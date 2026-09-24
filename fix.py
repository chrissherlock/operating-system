#!/usr/bin/env python3
# =====================================================================
# fix.py: Straighten line between Step 2 and Step 3 in Figure 1.2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "01-scheduling-introduction.html")

def straighten_connector():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the faulty S-curve and its label
    old_connector = (
        '        <!-- Step 2 to Step 3 Routed Downward Connector -->\n'
        '        <path d="M 515 222 C 555 222, 555 250, 410 250 C 370 250, 370 278, 370 286" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr-down)" />\n'
        '        <text x="440" y="244" text-anchor="middle" font-size="8.5" font-weight="600" fill="#0284c7">Invoke Dispatcher (switch_to)</text>'
    )

    # Clean, direct vertical drop from bottom of Step 2 (y=270) to top of Step 3 (y=286)
    new_connector = (
        '        <!-- Step 2 to Step 3 Direct Vertical Connector -->\n'
        '        <path d="M 410 270 L 410 286" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr-down)" />\n'
        '        <text x="420" y="280" text-anchor="start" font-size="8.5" font-weight="700" fill="#0284c7">switch_to()</text>'
    )

    if old_connector not in content:
        # Fallback in case of slight whitespace variance: match by path d attribute
        import re
        pattern = re.compile(
            r'<!-- Step 2 to Step 3.*?-->\s*<path d="[^"]*"[^>]*marker-end="url\(#arr-down\)"\s*/>\s*<text[^>]*>.*?</text>',
            re.DOTALL
        )
        if pattern.search(content):
            content = pattern.sub(new_connector.strip(), content)
        else:
            print("Error: Could not locate Step 2 to Step 3 connector in target file.")
            return
    else:
        content = content.replace(old_connector, new_connector)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully straightened connector in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix connector line between scheduler and dispatcher in Figure 1.2\n\n"
            "Replace the tangled S-curve with a direct vertical drop from Step 2 into\n"
            "Step 3 to maintain clean orthogonal flow and eliminate visual clutter."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    straighten_connector()
