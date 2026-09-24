#!/usr/bin/env python3
# =====================================================================
# fix.py: Recalculate chopstick geometry in Module 04 Dining Philosophers
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "04-classic-synchronization-real-world-defenses.html"
)

NEW_SVG_CANVAS = r"""            <!-- Circular Table SVG Canvas with Accurate Radial Geometry -->
            <svg viewBox="0 0 300 240" style="width: 100%; height: 100%; min-height: 220px; background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 6px;">
              <!-- Central Dining Table (Center at 150, 120, Radius 62) -->
              <circle cx="150" cy="120" r="62" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" />
              <text x="150" y="124" fill="#94a3b8" font-size="11" font-weight="700" text-anchor="middle">Table</text>

              <!-- Chopsticks/Forks C0..C4 positioned on the table boundary between philosophers -->
              <!-- C0: Between P0 (-90 deg) and P1 (-18 deg) at -54 deg -->
              <g id="grp-c0">
                <rect id="dp-c0" x="182" y="62" width="7" height="22" rx="2" fill="#d97706" transform="rotate(36 185 73)" />
                <text x="175" y="62" fill="#b45309" font-size="8" font-weight="700">C0</text>
              </g>

              <!-- C1: Between P1 (-18 deg) and P2 (+54 deg) at +18 deg -->
              <g id="grp-c1">
                <rect id="dp-c1" x="206" y="128" width="7" height="22" rx="2" fill="#d97706" transform="rotate(108 209 139)" />
                <text x="216" y="126" fill="#b45309" font-size="8" font-weight="700">C1</text>
              </g>

              <!-- C2: Between P2 (+54 deg) and P3 (+126 deg) at +90 deg -->
              <g id="grp-c2">
                <rect id="dp-c2" x="146.5" y="171" width="7" height="22" rx="2" fill="#d97706" transform="rotate(0 150 182)" />
                <text x="150" y="202" fill="#b45309" font-size="8" font-weight="700" text-anchor="middle">C2</text>
              </g>

              <!-- C3: Between P3 (+126 deg) and P4 (+198 deg) at +162 deg -->
              <g id="grp-c3">
                <rect id="dp-c3" x="87" y="128" width="7" height="22" rx="2" fill="#d97706" transform="rotate(-108 90 139)" />
                <text x="74" y="126" fill="#b45309" font-size="8" font-weight="700">C3</text>
              </g>

              <!-- C4: Between P4 (+198 deg) and P0 (+270 deg) at +234 deg -->
              <g id="grp-c4">
                <rect id="dp-c4" x="111" y="62" width="7" height="22" rx="2" fill="#d97706" transform="rotate(-36 114 73)" />
                <text x="115" y="62" fill="#b45309" font-size="8" font-weight="700">C4</text>
              </g>

              <!-- Philosopher Nodes (Radius ~92 from center) -->
              <!-- P0: Top center (angle -90 deg) -->
              <circle id="dp-p0" cx="150" cy="28" r="17" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="150" y="32" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P0</text>

              <!-- P1: Top right (angle -18 deg) -->
              <circle id="dp-p1" cx="238" cy="92" r="17" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="238" y="96" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P1</text>

              <!-- P2: Bottom right (angle +54 deg) -->
              <circle id="dp-p2" cx="204" cy="194" r="17" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="204" y="198" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P2</text>

              <!-- P3: Bottom left (angle +126 deg) -->
              <circle id="dp-p3" cx="96" cy="194" r="17" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="96" y="198" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P3</text>

              <!-- P4: Top left (angle +198 deg) -->
              <circle id="dp-p4" cx="62" cy="92" r="17" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="62" y="96" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">P4</text>
            </svg>"""

def replace_svg_canvas():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "            <!-- Circular Table SVG Canvas -->"
    end_marker = '<div style="font-size: 0.8rem; color: var(--text-muted); text-align: center; margin-top: 8px;" id="dp-canvas-banner">'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate SVG canvas boundaries in target file.")
        return False

    updated_content = content[:start_idx] + NEW_SVG_CANVAS + "\n\n            " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully updated chopstick geometry in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if replace_svg_canvas():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix chopstick coordinate geometry in Dining Philosophers SVG canvas\n\n"
                "Recalculate radial bisector coordinates for C0-C4 so forks sit cleanly\n"
                "between adjacent philosopher nodes on the table perimeter."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
