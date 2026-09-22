#!/usr/bin/env python3
# =====================================================================
# fix.py: Rebuild 3-state process diagram with clean geometry and arrows
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

NEW_THREE_STATE_DIAGRAM = r"""    <!-- Diagram 2: Three-State Process Lifecycle -->
    <div style="display: flex; justify-content: center; margin: 28px 0;">
      <svg viewBox="0 0 760 300" width="100%" height="100%" style="max-width: 760px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="trans-arrow-blue" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
          </marker>
          <marker id="trans-arrow-slate" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#64748b" />
          </marker>
          <marker id="trans-arrow-red" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#ef4444" />
          </marker>
          <marker id="trans-arrow-green" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#059669" />
          </marker>
          <filter id="state-shadow" x="-5%" y="-5%" width="110%" height="110%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06" />
          </filter>
        </defs>

        <!-- 1. Ready State Circle (Left) -->
        <g transform="translate(150, 75)" filter="url(#state-shadow)">
          <circle cx="0" cy="0" r="52" fill="#eff6ff" stroke="#0284c7" stroke-width="2" />
          <text x="0" y="-4" fill="#0369a1" font-size="12" font-weight="700" text-anchor="middle">READY</text>
          <text x="0" y="14" fill="#64748b" font-size="8.5" text-anchor="middle">In Run Queue</text>
        </g>

        <!-- 2. Running State Circle (Right) -->
        <g transform="translate(610, 75)" filter="url(#state-shadow)">
          <circle cx="0" cy="0" r="52" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
          <text x="0" y="-4" fill="#065f46" font-size="12" font-weight="700" text-anchor="middle">RUNNING</text>
          <text x="0" y="14" fill="#047857" font-size="8.5" text-anchor="middle">Executing on CPU</text>
        </g>

        <!-- 3. Blocked State Circle (Bottom Center) -->
        <g transform="translate(380, 225)" filter="url(#state-shadow)">
          <circle cx="0" cy="0" r="52" fill="#fef2f2" stroke="#ef4444" stroke-width="2" />
          <text x="0" y="-4" fill="#991b1b" font-size="12" font-weight="700" text-anchor="middle">BLOCKED</text>
          <text x="0" y="14" fill="#b91c1c" font-size="8.5" text-anchor="middle">Waiting for I/O</text>
        </g>

        <!-- PATH 1: Ready -> Running (Scheduler Dispatch - Top Forward) -->
        <path d="M 204,60 C 310,25 450,25 554,60" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#trans-arrow-blue)" />
        <rect x="305" y="16" width="150" height="20" rx="3" fill="#ffffff" stroke="#bae6fd" />
        <text x="380" y="30" fill="#0369a1" font-size="8.5" font-weight="700" text-anchor="middle">1. Scheduler Dispatch</text>

        <!-- PATH 2: Running -> Ready (Timer Preempted - Bottom Return) -->
        <path d="M 554,90 C 450,125 310,125 206,90" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#trans-arrow-slate)" />
        <rect x="295" y="102" width="170" height="20" rx="3" fill="#ffffff" stroke="#cbd5e1" />
        <text x="380" y="116" fill="#475569" font-size="8.5" font-weight="600" text-anchor="middle">2. Timer Expiry (Preempted)</text>

        <!-- PATH 3: Running -> Blocked (Initiate I/O) -->
        <path d="M 576,112 C 540,175 480,215 435,223" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#trans-arrow-red)" />
        <rect x="495" y="170" width="130" height="20" rx="3" fill="#ffffff" stroke="#fca5a5" />
        <text x="560" y="184" fill="#b91c1c" font-size="8.5" font-weight="700" text-anchor="middle">3. Blocked for I/O</text>

        <!-- PATH 4: Blocked -> Ready (I/O Complete Interrupt) -->
        <path d="M 326,223 C 280,215 220,175 184,112" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#trans-arrow-green)" />
        <rect x="135" y="170" width="130" height="20" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="200" y="184" fill="#065f46" font-size="8.5" font-weight="700" text-anchor="middle">4. I/O Completed</text>
      </svg>
    </div>"""

def replace_three_state_diagram():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate Diagram 2 container block
    start_tag = "<!-- Diagram 2: Three-State Process Lifecycle -->"
    end_tag = "</div>"

    if start_tag not in content:
        print("--> Error: Diagram 2 comment marker not found.")
        return

    before, remainder = content.split(start_tag, 1)
    svg_close = remainder.find("</svg>")
    if svg_close == -1:
        print("--> Error: </svg> tag not found after start marker.")
        return

    div_close = remainder.find("</div>", svg_close)
    if div_close == -1:
        print("--> Error: closing </div> not found.")
        return

    after = remainder[div_close + 6:]
    new_content = f"{before}{NEW_THREE_STATE_DIAGRAM}{after}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"--> Successfully replaced Diagram 2 in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix clipping and rebuild transition curves in 3-state process diagram\n\n"
            "Expand the SVG canvas height to 300px in 03-os-concepts.html and lay out\n"
            "the Ready, Running, and Blocked states in a balanced triangular geometry\n"
            "with clean arc paths and auto-orienting arrowheads."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for 3-state diagram fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    replace_three_state_diagram()
