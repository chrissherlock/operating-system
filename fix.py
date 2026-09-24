#!/usr/bin/env python3
# =====================================================================
# fix.py: Incorporate IPC Message Passing Deadlock Simulator into Week 6
# =====================================================================
import os
import subprocess

TARGET_DIR = "week06-synchronization-and-deadlock"
TARGET_FILE = os.path.join(TARGET_DIR, "ipc-deadlock.html")

SIMULATOR_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPC Message Passing Deadlock - COSC240</title>
    <style>
        :root {
            --primary: #0f172a;
            --accent: #0284c7;
            --accent-hover: #0369a1;
            --border: #e2e8f0;
            --card-bg: #ffffff;
            --text: #334155;
            --text-muted: #64748b;
            --bg: #f8fafc;
            --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
        }
        * { box-sizing: border-box; }
        body {
            font-family: var(--font-sans);
            background-color: var(--bg);
            color: var(--text);
            max-width: 1100px;
            margin: 30px auto;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            background: #fff;
            border: 1px solid var(--border);
        }
        h2 {
            text-align: center;
            color: var(--primary);
            margin-top: 5px;
            font-size: 1.6rem;
        }
        p.instruction {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.95em;
            margin-bottom: 25px;
        }
        #alert-banner {
            max-width: 800px;
            margin: 0 auto 20px auto;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
            font-weight: 600;
            font-size: 1.05em;
            background-color: #f0fdf4;
            color: #166534;
            border: 1px solid #bbf7d0;
            transition: all 0.3s;
        }
        #alert-banner.deadlock {
            background-color: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        .generator-controls {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .grid-container {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: stretch;
        }
        .column {
            flex: 1;
            min-width: 280px;
            background: #fdfefe;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
        }
        .column h3 {
            margin-top: 0;
            text-align: center;
            font-size: 1.05em;
            color: var(--primary);
            border-bottom: 2px solid var(--border);
            padding-bottom: 10px;
        }
        .thread-state {
            text-align: center;
            margin-bottom: 15px;
            font-weight: 700;
            font-size: 0.85em;
            padding: 6px;
            border-radius: 6px;
            font-family: var(--font-mono);
            letter-spacing: 0.04em;
        }
        .state-running { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .state-blocked { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        .state-finished { background-color: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }

        .queue-container {
            flex: 0.8;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            background: #f8fafc;
        }
        .queue-box {
            border: 2px dashed var(--border);
            border-radius: 6px;
            padding: 15px;
            text-align: center;
            min-height: 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: #fff;
            position: relative;
        }
        .queue-title {
            font-weight: 700;
            font-size: 0.82em;
            color: var(--text-muted);
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        .message {
            background-color: #fef3c7;
            color: #92400e;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.82em;
            font-family: var(--font-mono);
            font-weight: 700;
            display: none;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            border: 1px solid #fde68a;
        }

        .code-line {
            font-family: var(--font-mono);
            font-size: 0.82em;
            padding: 8px;
            margin-bottom: 5px;
            border-radius: 4px;
            background: #f8fafc;
            color: var(--text-muted);
            border: 1px solid var(--border);
            transition: all 0.2s;
        }
        .code-line.active-a { background: #e0f2fe; color: #0369a1; border-color: #bae6fd; font-weight: 700; }
        .code-line.active-b { background: #f3e8ff; color: #6b21a8; border-color: #e9d5ff; font-weight: 700; }
        .code-line.waiting { background: #fee2e2; color: #991b1b; border-color: #fecaca; font-weight: 700; border-style: dashed; }
        .code-line.success { background: #dcfce7; color: #166534; border-color: #bbf7d0; font-weight: 700; }

        .controls {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }
        button {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 0.95em;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.15s;
            margin: 0 8px;
        }
        button:hover { background-color: var(--accent); }
        button:disabled { background-color: #cbd5e1; cursor: not-allowed; }

        .btn-safe { background-color: #16a34a; }
        .btn-safe:hover { background-color: #15803d; }
        .btn-deadlock { background-color: #dc2626; }
        .btn-deadlock:hover { background-color: #b91c1c; }

        .module-nav-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            margin-bottom: 20px;
            gap: 12px;
            box-sizing: border-box;
        }
        .module-nav-bar.bottom { margin-top: 30px; }
        .module-nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            font-family: var(--font-mono);
            text-decoration: none;
            color: var(--accent);
            background-color: #f0f9ff;
            border: 1px solid #bae6fd;
            padding: 7px 13px;
            border-radius: 6px;
            transition: all 0.15s ease;
        }
        .module-nav-btn:hover { background-color: var(--accent); color: #ffffff; }
    </style>
</head>
<body>
<nav class="module-nav-bar">
    <a href="dining-philosophers.html" class="module-nav-btn">&larr; Dining Philosophers</a>
    <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid var(--border); border-radius: 6px; color: var(--primary); text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">&#127968; Week 6 Hub</a>
    <span class="module-nav-placeholder">&nbsp;</span>
</nav>

    <h2>IPC Message Passing Deadlock</h2>
    <p class="instruction">Step through a communication sequence to see how blocking receive calls can create a cyclic dependency over logical channels.</p>

    <div class="generator-controls">
        <button class="btn-safe" onclick="loadScenario('safe')">Load Safe IPC Sequence</button>
        <button class="btn-deadlock" onclick="loadScenario('deadlock')">Load Deadlock Sequence</button>
    </div>

    <div id="alert-banner">Select a scenario to begin.</div>

    <div class="grid-container">
        <!-- Process A -->
        <div class="column" style="border-top: 4px solid #0284c7;">
            <h3>Process A</h3>
            <div id="state-a" class="thread-state state-running">State: RUNNING</div>
            <div id="code-a"></div>
        </div>

        <!-- IPC Channels (Middle) -->
        <div class="column queue-container">
            <h3>OS Message Queues</h3>

            <div class="queue-box">
                <div class="queue-title">Queue: A &rarr; B</div>
                <div id="msg-a-to-b" class="message">"Data from A"</div>
            </div>

            <div class="queue-box">
                <div class="queue-title">Queue: B &rarr; A</div>
                <div id="msg-b-to-a" class="message">"Data from B"</div>
            </div>
        </div>

        <!-- Process B -->
        <div class="column" style="border-top: 4px solid #7c3aed;">
            <h3>Process B</h3>
            <div id="state-b" class="thread-state state-running">State: RUNNING</div>
            <div id="code-b"></div>
        </div>
    </div>

    <div class="controls">
        <button id="btn-next" onclick="executeNextStep()">Execute Next Time Step &rarr;</button>
    </div>

<script>
    let currentMode = '';
    let step = 0;

    const scenarios = {
        safe: {
            codeA: [
                { id: "a1", text: "send(Queue_A_to_B, data);" },
                { id: "a2", text: "msg = receive(Queue_B_to_A);" },
                { id: "a3", text: "process(msg);" }
            ],
            codeB: [
                { id: "b1", text: "msg = receive(Queue_A_to_B);" },
                { id: "b2", text: "send(Queue_B_to_A, response);" },
                { id: "b3", text: "process(msg);" }
            ]
        },
        deadlock: {
            codeA: [
                { id: "a1", text: "msg = receive(Queue_B_to_A); // Blocks" },
                { id: "a2", text: "send(Queue_A_to_B, data);" },
                { id: "a3", text: "process(msg);" }
            ],
            codeB: [
                { id: "b1", text: "msg = receive(Queue_A_to_B); // Blocks" },
                { id: "b2", text: "send(Queue_B_to_A, response);" },
                { id: "b3", text: "process(msg);" }
            ]
        }
    };

    function loadScenario(mode) {
        currentMode = mode;
        step = 0;

        document.getElementById('msg-a-to-b').style.display = 'none';
        document.getElementById('msg-b-to-a').style.display = 'none';
        document.getElementById('btn-next').disabled = false;

        updateThreadState('a', 'RUNNING');
        updateThreadState('b', 'RUNNING');

        const banner = document.getElementById('alert-banner');
        banner.className = '';
        if (mode === 'safe') {
            banner.innerText = "Safe Mode: Process A sends before receiving. Process B waits to receive before sending. Click Next Step.";
        } else {
            banner.innerText = "Deadlock Mode: Both processes attempt to receive a message before sending one. Click Next Step.";
        }

        const codeDivA = document.getElementById('code-a');
        const codeDivB = document.getElementById('code-b');
        codeDivA.innerHTML = '';
        codeDivB.innerHTML = '';

        scenarios[mode].codeA.forEach(line => {
            codeDivA.innerHTML += `<div id="${line.id}" class="code-line">${line.text}</div>`;
        });
        scenarios[mode].codeB.forEach(line => {
            codeDivB.innerHTML += `<div id="${line.id}" class="code-line">${line.text}</div>`;
        });
    }

    function updateThreadState(process, state) {
        const el = document.getElementById(`state-${process}`);
        el.className = 'thread-state';
        if (state === 'RUNNING') el.classList.add('state-running');
        if (state === 'BLOCKED') el.classList.add('state-blocked');
        if (state === 'FINISHED') el.classList.add('state-finished');
        el.innerText = `State: ${state}`;
    }

    function setLineState(id, stateClass) {
        document.querySelectorAll('.code-line').forEach(el => el.classList.remove('active-a', 'active-b', 'waiting', 'success'));
        const el = document.getElementById(id);
        if (el) el.classList.add(stateClass);
    }

    function executeNextStep() {
        step++;
        const banner = document.getElementById('alert-banner');

        if (currentMode === 'safe') {
            if (step === 1) {
                setLineState('a1', 'active-a');
                document.getElementById('b1').classList.add('waiting');
                updateThreadState('b', 'BLOCKED');
                document.getElementById('msg-a-to-b').style.display = 'block';
                banner.innerText = "Step 1: Process A sends a message. Process B is blocked waiting for it.";
            } else if (step === 2) {
                setLineState('b1', 'active-b');
                document.getElementById('msg-a-to-b').style.display = 'none';
                updateThreadState('b', 'RUNNING');

                document.getElementById('a2').classList.add('waiting');
                updateThreadState('a', 'BLOCKED');
                banner.innerText = "Step 2: Process B receives the message and unblocks. Process A now blocks waiting for a reply.";
            } else if (step === 3) {
                setLineState('b2', 'active-b');
                document.getElementById('msg-b-to-a').style.display = 'block';
                banner.innerText = "Step 3: Process B sends a reply back to Process A.";
            } else if (step === 4) {
                setLineState('a2', 'active-a');
                document.getElementById('msg-b-to-a').style.display = 'none';
                updateThreadState('a', 'RUNNING');
                banner.innerText = "Step 4: Process A receives the reply and unblocks.";
            } else if (step === 5) {
                setLineState('a3', 'success');
                setLineState('b3', 'success');
                updateThreadState('a', 'FINISHED');
                updateThreadState('b', 'FINISHED');
                banner.innerText = "Step 5: Both processes complete successfully! No circular wait.";
                document.getElementById('btn-next').disabled = true;
            }
        }
        else if (currentMode === 'deadlock') {
            if (step === 1) {
                setLineState('a1', 'waiting');
                updateThreadState('a', 'BLOCKED');
                banner.innerText = "Step 1: Process A calls receive() and suspends execution because the queue from B is empty.";
            } else if (step === 2) {
                document.getElementById('a1').classList.add('waiting');
                document.getElementById('b1').classList.add('waiting');
                updateThreadState('b', 'BLOCKED');

                banner.className = 'deadlock';
                banner.innerText = "Step 2: DEADLOCK! Process B also calls receive() and suspends. Neither can proceed to their send() instructions. Both will wait forever.";
                document.getElementById('btn-next').disabled = true;
            }
        }
    }

    loadScenario('safe');
</script>

<nav class="module-nav-bar bottom">
    <a href="dining-philosophers.html" class="module-nav-btn">&larr; Dining Philosophers</a>
    <span style="font-size: 0.85rem; font-weight: 600; color: var(--text-muted);">Week 6: Synchronization &amp; Deadlock</span>
    <span class="module-nav-placeholder">&nbsp;</span>
</nav>
</body>
</html>
"""

def update_ipc():
    os.makedirs(TARGET_DIR, exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(SIMULATOR_HTML.strip() + "\n")
    print(f"--> Successfully updated IPC deadlock simulator at {TARGET_FILE}")

def run_git_sync():
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
    if not status:
        print("--> Working tree is clean. Nothing to commit.")
        return

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Incorporate IPC Message Passing Deadlock Simulator sandbox into Week 6\n\n"
            "Add interactive IPC deadlock simulation illustrating blocking receive queues,\n"
            "rendezvous communication, and circular wait dependencies between processes."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_ipc()
    run_git_sync()
