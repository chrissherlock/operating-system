#!/usr/bin/env python3
# =====================================================================
# fix.py: Rewrite pipeline inline previews into immersive micro-architecture story
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

def update_immersive_story_previews():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    old_storylines_marker = 'const pipeStorylines = {'
    if old_storylines_marker not in content:
        print("Error: Could not locate pipeline storylines in Module 2.")
        return

    new_storylines_block = """const pipeStorylines = {
            pipeline: [
              {
                cycle: "Cycle 1", phase: "Instruction Fetch (IF)", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "I1: LOAD R1, [A]", decode: "Idle (Bubble)", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch"], forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE • CLOCK CYCLE 1",
                consoleMid: "I1 is fetched from memory address 0x00401000 into the Instruction Register.",
                consoleSub: "Downstream pipeline latches are currently empty.",
                inlinePreview: "<strong>The Spark of Execution:</strong> The Program Counter asserts address <code>0x00401000</code> onto the system bus. Instruction <code>I1 (LOAD R1, [A])</code> is pulled from memory into the fetch latch, while the downstream decoding and execution units wait quietly in anticipation.",
                what: "The CPU begins execution by asserting Program Counter 0x00401000 on the instruction bus, latching I1 into the Instruction Fetch stage.",
                why: "A pipeline requires a brief fill latency before all stages populate. Control logic disables downstream writes until execution reaches steady-state."
              },
              {
                cycle: "Cycle 2", phase: "Fetch & Decode Stages", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "I2: LOAD R2, [B]", decode: "I1: LOAD R1, [A]", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"], forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE • CLOCK CYCLE 2",
                consoleMid: "I1 enters Decode; I2 enters Fetch.",
                consoleSub: "Hardware decodes LOAD opcode while fetching next word.",
                inlinePreview: "<strong>Unpacking Intent:</strong> Instruction <code>I1</code> shifts into the decode stage, where control hardware unpacks its <code>LOAD</code> opcode and isolates register operands. Right behind it, the fetch engine grabs <code>I2 (LOAD R2, [B])</code> to keep the pipeline fed.",
                what: "I1 shifts into Instruction Decode while Fetch retrieves I2: LOAD R2, [B].",
                why: "Functional units operate concurrently without structural collision, increasing instruction throughput."
              },
              {
                cycle: "Cycle 3", phase: "Fetch, Decode, & Execute", retired: "0 / 4", ipc: "0.00 IPC", hazard: "RAW Hazard Managed",
                fetch: "I3: MUL R3, R1, R2", decode: "I2: LOAD R2, [B]", exec: "I1: LOAD R1, [A]", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode", "pipe-node-exec"], forwardingActive: true,
                consoleTop: "STANDARD 4-STAGE PIPELINE • CLOCK CYCLE 3",
                consoleMid: "I1 executes address calculation; I3 is fetched.",
                consoleSub: "Hazard unit primes forwarding bypass for R1.",
                inlinePreview: "<strong>The Plot Thickens:</strong> Instruction <code>I1</code> calculates its memory address inside the ALU. Meanwhile, incoming instruction <code>I3</code> arrives demanding value <code>R1</code>. Sensing the dependency before <code>I1</code> writes back, the hardware routes a <strong>data forwarding bypass</strong> directly from the ALU output.",
                what: "I1 moves to Execute. The hazard unit detects I3 requires R1 before I1 updates the register file.",
                why: "Internal bypass multiplexer buses route the calculated value directly from ALU output into I3 without stalling."
              },
              {
                cycle: "Cycle 4", phase: "Steady-State Full Pipeline", retired: "1 / 4", ipc: "0.25 IPC", hazard: "Forwarding Active",
                fetch: "I4: ADD R4, R4, R3", decode: "I3: MUL R3, R1, R2", exec: "I2: LOAD R2, [B]", wb: "I1: LOAD R1, [A]",
                activeStages: ["pipe-node-fetch", "pipe-node-decode", "pipe-node-exec", "pipe-node-wb"], forwardingActive: true,
                consoleTop: "STANDARD 4-STAGE PIPELINE • CLOCK CYCLE 4 (FULL PIPELINE)",
                consoleMid: "I1 writes back R1 and retires. All stages occupied.",
                consoleSub: "Pipeline reaches full steady-state utilization (1.0 IPC).",
                inlinePreview: "<strong>Symphony in Motion:</strong> All four pipeline stages hum simultaneously! Instruction <code>I1</code> completes writeback, committing its loaded value into register <code>R1</code> and officially retiring from active duty.",
                what: "All 4 stages are occupied. I1 writes back to R1 and retires. I4 enters Fetch.",
                why: "From this point forward, the core retires one instruction every clock cycle."
              },
              {
                cycle: "Cycle 5", phase: "Pipeline Drain & Multiply", retired: "2 / 4", ipc: "0.40 IPC", hazard: "Forwarding Active",
                fetch: "Drained", decode: "I4: ADD R4, R4, R3", exec: "I3: MUL R3, R1, R2", wb: "I2: LOAD R2, [B]",
                activeStages: ["pipe-node-decode", "pipe-node-exec", "pipe-node-wb"], forwardingActive: true,
                consoleTop: "STANDARD 4-STAGE PIPELINE • CLOCK CYCLE 5",
                consoleMid: "I2 writes back R2; I3 multiplies R1*R2 in ALU.",
                consoleSub: "Remaining operations drain down the pipe.",
                inlinePreview: "<strong>Crunching Numbers:</strong> Instruction <code>I2</code> writes back and retires. Simultaneously, instruction <code>I3</code> plunges into the ALU's multiplier array to compute <code>R1 &times; R2</code> utilizing the forwarded register data.",
                what: "I2 writes back and retires. I3 enters the ALU multiplier array to compute R1 * R2.",
                why: "Multiplication circuits are deeply pipelined to maintain high clock frequencies."
              },
              {
                cycle: "Cycle 6", phase: "Pipeline Drain & Accumulate", retired: "3 / 4", ipc: "0.50 IPC", hazard: "None",
                fetch: "Drained", decode: "Drained", exec: "I4: ADD R4, R4, R3", wb: "I3: MUL R3, R1, R2",
                activeStages: ["pipe-node-exec", "pipe-node-wb"], forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE • CLOCK CYCLE 6",
                consoleMid: "I3 writes back R3; I4 adds R4 + R3.",
                consoleSub: "Accumulator stage computing final sum.",
                inlinePreview: "<strong>The Accumulator Chain:</strong> Instruction <code>I3</code> writes its multiplication product into <code>R3</code> and retires. Instantly, instruction <code>I4</code> takes that product and adds it into running accumulator register <code>R4</code>.",
                what: "I3 writes its product into R3 and retires. I4 adds R3 into accumulator R4.",
                why: "Forwarding allowed I4 to begin execution immediately following I3's ALU phase."
              },
              {
                cycle: "Cycle 7", phase: "Workload Complete", retired: "4 / 4", ipc: "0.57 IPC", hazard: "None",
                fetch: "Idle", decode: "Idle", exec: "Idle", wb: "I4: ADD R4, R4, R3",
                activeStages: ["pipe-node-wb"], forwardingActive: false,
                consoleTop: "STANDARD 4-STAGE PIPELINE • CLOCK CYCLE 7 (COMPLETE)",
                consoleMid: "I4 writes back final sum to R4. All 4 instructions retired.",
                consoleSub: "Total execution: 7 cycles for 4 instructions.",
                inlinePreview: "<strong>Mission Accomplished:</strong> Instruction <code>I4</code> completes writeback, committing the final sum to register <code>R4</code> and retiring. All four instructions finish triumphantly in 7 clock cycles!",
                what: "I4 writes back to R4 and retires. Total execution took 7 cycles vs 16 unpipelined cycles.",
                why: "Pipelining achieves nearly a 400% speedup over sequential execution for vector loops."
              }
            ],
            superscalar: [
              {
                cycle: "Cycle 1", phase: "Dual-Issue Fetch", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "I1 & I2 (Dual-Issue)", decode: "Idle (Bubble)", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch"], forwardingActive: false,
                consoleTop: "DUAL-ISSUE SUPERSCALAR • CLOCK CYCLE 1",
                consoleMid: "Wide fetcher reads both I1 and I2 simultaneously.",
                consoleSub: "Dual instruction queues primed.",
                inlinePreview: "<strong>Wide-Body Ignition:</strong> The wide superscalar fetcher shatters single-issue limits by pulling both <code>I1</code> and <code>I2</code> simultaneously from the instruction cache in a single clock tick.",
                what: "The wide instruction fetch unit pulls both I1 and I2 simultaneously in a single cycle.",
                why: "Superscalar processors build parallel pipelines side-by-side, achieving IPC > 1.0."
              },
              {
                cycle: "Cycle 2", phase: "Dual Decode & Fetch", retired: "0 / 4", ipc: "0.00 IPC", hazard: "Scoreboard Validated",
                fetch: "I3 & I4 (Dual-Issue)", decode: "I1 & I2 (Dual Decode)", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"], forwardingActive: false,
                consoleTop: "DUAL-ISSUE SUPERSCALAR • CLOCK CYCLE 2",
                consoleMid: "I1 & I2 decode simultaneously; I3 & I4 fetched.",
                consoleSub: "Scoreboard validates register independence.",
                inlinePreview: "<strong>Parallel Tracks:</strong> Dual decoders process <code>I1</code> and <code>I2</code> side-by-side while the fetch unit grabs <code>I3</code> and <code>I4</code>. The internal hardware scoreboard verifies zero register collisions.",
                what: "Dual decoders process I1 and I2 in parallel while I3 and I4 are fetched side-by-side.",
                why: "Dependency matrices confirm I1 and I2 target different registers and execute concurrently."
              },
              {
                cycle: "Cycle 3", phase: "Dual Memory Load", retired: "2 / 4", ipc: "1.00 IPC", hazard: "Dual Load Active",
                fetch: "Drained", decode: "I3 & I4 (Dual Decode)", exec: "I1 & I2 (Dual Load)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-decode", "pipe-node-exec"], forwardingActive: true,
                consoleTop: "DUAL-ISSUE SUPERSCALAR • CLOCK CYCLE 3",
                consoleMid: "Dual execution units service I1 & I2.",
                consoleSub: "Reorder Buffer tracks in-flight instructions.",
                inlinePreview: "<strong>Twin Load Ports:</strong> Dual memory read channels execute simultaneously across split cache banks, fetching both input numbers from memory in a single clock tick.",
                what: "Dual memory read channels retrieve both input numbers from memory at the exact same moment.",
                why: "Partitioning L1 caches into multiple banks prevents memory bottlenecks."
              },
              {
                cycle: "Cycle 4", phase: "Dual Retirement", retired: "4 / 4", ipc: "1.00 IPC", hazard: "None",
                fetch: "Idle", decode: "Idle", exec: "I3 (MUL) & I4 (ADD)", wb: "I1 & I2 Retired",
                activeStages: ["pipe-node-exec", "pipe-node-wb"], forwardingActive: false,
                consoleTop: "DUAL-ISSUE SUPERSCALAR • CLOCK CYCLE 4 (COMPLETE)",
                consoleMid: "I3 and I4 finish execution and retire simultaneously.",
                consoleSub: "Total execution: 4 clock cycles.",
                inlinePreview: "<strong>Superscalar Triumph:</strong> Instructions <code>I3</code> and <code>I4</code> complete their arithmetic and retire together through the Reorder Buffer. The entire workload concludes in a blistering 4 cycles!",
                what: "I3 and I4 complete execution and retire together through the Reorder Buffer in 4 cycles.",
                why: "Parallel dispatching overcomes single-issue pipeline throughput limits."
              }
            ],
            multicore: [
              {
                cycle: "Cycle 1", phase: "Thread Partitioning", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "Core 0: I1 | Core 1: I2", decode: "Empty", exec: "Empty", wb: "Empty",
                activeStages: ["pipe-node-fetch"], forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR • CLOCK CYCLE 1",
                consoleMid: "OS dispatches Iteration A to Core 0 and Iteration B to Core 1.",
                consoleSub: "Two independent silicon cores with private caches.",
                inlinePreview: "<strong>Dividing the Realm:</strong> The operating system scheduler splits the workload, dispatching loop iteration <code>I1</code> to <strong>Core 0</strong> and iteration <code>I2</code> to <strong>Core 1</strong> across separate silicon dies.",
                what: "The OS divides the workload across two separate CPU cores.",
                why: "Multicore systems feature completely separate execution pipelines, eliminating dependency stalls."
              },
              {
                cycle: "Cycle 2", phase: "Parallel Core Decoding", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "Core 0: I3 | Core 1: I4", decode: "Core 0: I1 | Core 1: I2", exec: "Empty", wb: "Empty",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"], forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR • CLOCK CYCLE 2",
                consoleMid: "Both cores decode simultaneously.",
                consoleSub: "MESI cache coherency protocol active.",
                inlinePreview: "<strong>Autonomous Execution:</strong> Both physical cores decode their respective thread instructions in parallel, relying on dedicated private L1 caches without interfering with each other.",
                what: "Both cores decode their instructions simultaneously using dedicated L1 caches.",
                why: "Private L1 caches prevent memory access contention between cores."
              },
              {
                cycle: "Cycle 3", phase: "Parallel Memory Loads", retired: "2 / 4", ipc: "0.67 IPC", hazard: "MESI Clean",
                fetch: "Drained", decode: "Core 0: I3 | Core 1: I4", exec: "Core 0: I1 | Core 1: I2", wb: "Empty",
                activeStages: ["pipe-node-decode", "pipe-node-exec"], forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR • CLOCK CYCLE 3",
                consoleMid: "Core 0 and Core 1 retire loads simultaneously.",
                consoleSub: "Cache coherence snoops shared interconnect.",
                inlinePreview: "<strong>Concurrent Memory Access:</strong> Core 0 and Core 1 both complete their memory loads concurrently. Hardware bus snooping monitors the shared interconnect to maintain cache consistency.",
                what: "Both cores complete memory loads in parallel and retire their initial instructions.",
                why: "Multicore architectures scale throughput without increasing clock frequencies."
              },
              {
                cycle: "Cycle 4", phase: "Multiprocessing Complete", retired: "4 / 4", ipc: "1.00 IPC", hazard: "None",
                fetch: "Idle", decode: "Idle", exec: "Core 0: I3 | Core 1: I4", wb: "Core 0 & Core 1 Retired",
                activeStages: ["pipe-node-exec", "pipe-node-wb"], forwardingActive: false,
                consoleTop: "DUAL-CORE SMP MULTIPROCESSOR • CLOCK CYCLE 4 (COMPLETE)",
                consoleMid: "Core 0 and Core 1 complete workloads in parallel.",
                consoleSub: "True thread-level parallelism (TLP) achieved.",
                inlinePreview: "<strong>Multicore Harmony:</strong> Core 0 and Core 1 finalize their calculations and retire their thread workloads in unison, demonstrating true multi-core thread-level parallelism.",
                what: "Core 0 and Core 1 complete arithmetic calculations and retire threads in 4 cycles.",
                why: "True hardware parallelism enables high system throughput across multithreaded apps."
              }
            ]
          };"""

    parts = content.split(old_storylines_marker, 1)
    remainder = parts[1].split('function renderPipeState()', 1)

    updated_content = f"{parts[0]}{new_storylines_block}\n\n          function renderPipeState(){remainder[1]}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully transformed pipeline interactive previews into story narrative in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Rewrite pipeline interactive previews into immersive micro-architectural story\n\n"
            "Update 02-hardware-review.html so the inline preview panel narrates the\n"
            "exact story of execution unfolding inside the processor at each step."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_immersive_story_previews()
