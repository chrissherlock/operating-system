#!/usr/bin/env python3
# =====================================================================
# fix.py: Rewrite interactive pipeline preview text into a narrative arc
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

def update_narrative_stepper_storylines():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # We replace the JSON storyline blocks inside the pipeline simulator script
    # to deliver a rich, story-driven narrative arc matching your pedagogical standards.
    old_storylines_marker = 'const pipeStorylines = {'
    if old_storylines_marker not in content:
        print("Error: Could not locate pipeline storylines in Module 2.")
        return

    new_storylines_block = """const pipeStorylines = {
            pipeline: [
              {
                cycle: "Cycle 1", phase: "The Spark: Fetching I1", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "I1: LOAD R1, [A]", decode: "Idle (Bubble)", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch"], forwardingActive: false,
                consoleTop: "THE STORY BEGINS • CLOCK CYCLE 1",
                consoleMid: "The Program Counter points to 0x00401000. I1 is pulled into the fetch stage.",
                consoleSub: "The processor wakes up, eager to load the first vector element.",
                inlinePreview: "<strong>The Journey Begins:</strong> The CPU asserts address <code>0x00401000</code> on the instruction bus. Instruction <code>I1 (LOAD R1, [A])</code> is pulled from memory into the fetch latch, while downstream stages sit quiet.",
                what: "The instruction fetch unit asserts the PC on the address bus, latching the first machine instruction into the pipeline registers.",
                why: "Processors require an initial pipeline fill latency before functional units can operate at peak cadence."
              },
              {
                cycle: "Cycle 2", phase: "Decoding & Fetching Next", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "I2: LOAD R2, [B]", decode: "I1: LOAD R1, [A]", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"], forwardingActive: false,
                consoleTop: "PARALLEL MOMENTUM • CLOCK CYCLE 2",
                consoleMid: "I1 enters Decode; I2 is fetched from memory right behind it.",
                consoleSub: "The control logic begins unpacking opcodes and register operands.",
                inlinePreview: "<strong>Unpacking Intent:</strong> Instruction <code>I1</code> moves into the decode stage to unpack its operands, while the fetch unit immediately grabs <code>I2 (LOAD R2, [B])</code> to keep the pipeline fed.",
                what: "The control unit decodes I1's opcode while the fetch unit retrieves the second instruction concurrently.",
                why: "Overlapping fetch and decode operations ensures the execution units never starve for work."
              },
              {
                cycle: "Cycle 3", phase: "Encountering Dependencies", retired: "0 / 4", ipc: "0.00 IPC", hazard: "RAW Hazard Managed",
                fetch: "I3: MUL R3, R1, R2", decode: "I2: LOAD R2, [B]", exec: "I1: LOAD R1, [A]", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode", "pipe-node-exec"], forwardingActive: true,
                consoleTop: "THE DEPENDENCY WEB • CLOCK CYCLE 3",
                consoleMid: "I1 calculates address in ALU; I3 arrives needing R1 before it's written.",
                consoleSub: "The hazard unit activates the internal data forwarding bypass path.",
                inlinePreview: "<strong>The Plot Thickens:</strong> Instruction <code>I1</code> calculates its memory address in the ALU. Meanwhile, incoming instruction <code>I3</code> demands value <code>R1</code>. Because <code>I1</code> hasn't reached writeback yet, the hardware primes a <strong>forwarding bypass</strong>.",
                what: "The execution unit computes I1's memory address while the hazard unit detects a Read-After-Write (RAW) dependency for I3.",
                why: "Modern CPUs avoid catastrophic pipeline stalls by piping ALU results directly back into dependent instruction inputs."
              },
              {
                cycle: "Cycle 4", phase: "Steady-State Harmony", retired: "1 / 4", ipc: "0.25 IPC", hazard: "Forwarding Active",
                fetch: "I4: ADD R4, R4, R3", decode: "I3: MUL R3, R1, R2", exec: "I2: LOAD R2, [B]", wb: "I1: LOAD R1, [A]",
                activeStages: ["pipe-node-fetch", "pipe-node-decode", "pipe-node-exec", "pipe-node-wb"], forwardingActive: true,
                consoleTop: "SYMPHONY IN MOTION • CLOCK CYCLE 4",
                consoleMid: "All four stages hum simultaneously. I1 writes back R1 and retires.",
                consoleSub: "The instruction throughput engine reaches full steady-state velocity.",
                inlinePreview: "<strong>Full Throttle:</strong> All four pipeline stages are now humming simultaneously! Instruction <code>I1</code> writes its loaded data into register <code>R1</code> and successfully retires.",
                what: "All pipeline stages are occupied. I1 commits its results to the register file and retires.",
                why: "Once fully primed, a pipelined architecture successfully retires one instruction per clock cycle."
              },
              {
                cycle: "Cycle 5", phase: "The Multiplication Array", retired: "2 / 4", ipc: "0.40 IPC", hazard: "Forwarding Active",
                fetch: "Drained", decode: "I4: ADD R4, R4, R3", exec: "I3: MUL R3, R1, R2", wb: "I2: LOAD R2, [B]",
                activeStages: ["pipe-node-decode", "pipe-node-exec", "pipe-node-wb"], forwardingActive: true,
                consoleTop: "CRUNCHING NUMBERS • CLOCK CYCLE 5",
                consoleMid: "I2 retires; I3 enters the heavy multiplier array in the ALU.",
                consoleSub: "Multiplication units execute deep pipelined arithmetic.",
                inlinePreview: "<strong>Heavy Computation:</strong> Instruction <code>I2</code> retires via writeback. Instruction <code>I3</code> plunges into the ALU's multiplier array to calculate <code>R1 &times; R2</code> utilizing the forwarded data.",
                what: "I2 writes back and retires while I3 performs vector multiplication in the arithmetic logic unit.",
                why: "Complex arithmetic operations like multiplication require dedicated multi-stage execution logic."
              },
              {
                cycle: "Cycle 6", phase: "Accumulating the Sum", retired: "3 / 4", ipc: "0.50 IPC", hazard: "None",
                fetch: "Drained", decode: "Drained", exec: "I4: ADD R4, R4, R3", wb: "I3: MUL R3, R1, R2",
                activeStages: ["pipe-node-exec", "pipe-node-wb"], forwardingActive: false,
                consoleTop: "THE CRESCENT ACCUMULATOR • CLOCK CYCLE 6",
                consoleMid: "I3 writes product R3; I4 accumulates into final sum R4.",
                consoleSub: "The vector dot product loop nears its culmination.",
                inlinePreview: "<strong>Accumulation:</strong> Instruction <code>I3</code> writes its product into <code>R3</code> and retires. Immediately, <code>I4</code> takes that product and adds it into accumulator register <code>R4</code>.",
                what: "I3 commits its multiplication product to R3 and retires. I4 adds R3 into the running sum register R4.",
                why: "Accumulator loops rely on tight chaining between multiplication products and sum registers."
              },
              {
                cycle: "Cycle 7", phase: "Grand Finale: Workload Complete", retired: "4 / 4", ipc: "0.57 IPC", hazard: "None",
                fetch: "Idle", decode: "Idle", exec: "Idle", wb: "I4: ADD R4, R4, R3",
                activeStages: ["pipe-node-wb"], forwardingActive: false,
                consoleTop: "MISSION ACCOMPLISHED • CLOCK CYCLE 7",
                consoleMid: "I4 writes back final sum R4. All 4 instructions successfully retired.",
                consoleSub: "The vector calculation concludes with high hardware efficiency.",
                inlinePreview: "<strong>Mission Accomplished:</strong> Instruction <code>I4</code> commits the final sum to <code>R4</code> and retires. Four instructions completed in just 7 cycles instead of 16 unpipelined cycles!",
                what: "I4 completes writeback and retires. The vector multiply-accumulate sequence successfully terminates.",
                why: "Hardware pipelining achieves dramatic performance multipliers without requiring higher clock frequencies."
              }
            ],
            superscalar: [
              {
                cycle: "Cycle 1", phase: "Dual-Issue Ignition", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "I1 & I2 (Dual-Issue)", decode: "Idle (Bubble)", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch"], forwardingActive: false,
                consoleTop: "WIDE-BODY FETCH • CLOCK CYCLE 1",
                consoleMid: "The wide instruction fetcher pulls both I1 and I2 simultaneously.",
                consoleSub: "Two instructions enter the execution pipeline in lockstep.",
                inlinePreview: "<strong>Dual-Issue Ignition:</strong> Instead of fetching a single instruction, the wide superscalar fetcher pulls both <code>I1</code> and <code>I2</code> simultaneously in a single clock tick.",
                what: "The wide instruction cache fetches two independent instructions concurrently.",
                why: "Superscalar architectures duplicate execution pathways to break the single-instruction-per-cycle barrier."
              },
              {
                cycle: "Cycle 2", phase: "Parallel Scoreboarding", retired: "0 / 4", ipc: "0.00 IPC", hazard: "Scoreboard Validated",
                fetch: "I3 & I4 (Dual-Issue)", decode: "I1 & I2 (Dual Decode)", exec: "Idle (Bubble)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"], forwardingActive: false,
                consoleTop: "PARALLEL DECODE • CLOCK CYCLE 2",
                consoleMid: "Dual decoders verify register independence while I3 & I4 fetch.",
                consoleSub: "The hardware scoreboard checks for structural hazards.",
                inlinePreview: "<strong>Independent Tracks:</strong> Dual decoders analyze <code>I1</code> and <code>I2</code> in parallel while the fetch engine grabs <code>I3</code> and <code>I4</code>. The hardware scoreboard confirms zero register collisions.",
                what: "Dual instruction decoders process two streams concurrently while checking dependency scoreboards.",
                why: "Parallel decoding ensures instructions sharing no dependencies can execute without waiting."
              },
              {
                cycle: "Cycle 3", phase: "Dual Memory Ports", retired: "2 / 4", ipc: "1.00 IPC", hazard: "Dual Load Active",
                fetch: "Drained", decode: "I3 & I4 (Dual Decode)", exec: "I1 & I2 (Dual Load)", wb: "Idle (Bubble)",
                activeStages: ["pipe-node-decode", "pipe-node-exec"], forwardingActive: true,
                consoleTop: "DUAL MEMORY BUS • CLOCK CYCLE 3",
                consoleMid: "Dual load execution units fetch both operands in parallel.",
                consoleSub: "Cache banking feeds twin execution channels.",
                inlinePreview: "<strong>Twin Load Ports:</strong> Dual execution units simultaneously service <code>I1</code> and <code>I2</code>, pulling memory inputs across split cache banks with zero bus contention.",
                what: "Twin execution ports execute memory loads for both instructions simultaneously.",
                why: "Multi-ported cache architectures prevent memory bottlenecks during wide instruction dispatch."
              },
              {
                cycle: "Cycle 4", phase: "Simultaneous Retirement", retired: "4 / 4", ipc: "1.00 IPC", hazard: "None",
                fetch: "Idle", decode: "Idle", exec: "I3 (MUL) & I4 (ADD)", wb: "I1 & I2 Retired",
                activeStages: ["pipe-node-exec", "pipe-node-wb"], forwardingActive: false,
                consoleTop: "SUPERSCALAR TRIUMPH • CLOCK CYCLE 4 (COMPLETE)",
                consoleMid: "All instructions finish and retire in pairs. Total: 4 cycles.",
                consoleSub: "Maximum instruction-level parallelism achieved.",
                inlinePreview: "<strong>Superscalar Triumph:</strong> Instructions <code>I3</code> and <code>I4</code> complete their math and retire alongside their peers. The entire workload finishes in a blistering 4 cycles!",
                what: "Instructions complete execution in parallel pairs and retire through the Reorder Buffer.",
                why: "Superscalar execution maximizes silicon utilization by dispatching multiple instructions per clock cycle."
              }
            ],
            multicore: [
              {
                cycle: "Cycle 1", phase: "Spawning Across Dies", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "Core 0: I1 | Core 1: I2", decode: "Empty", exec: "Empty", wb: "Empty",
                activeStages: ["pipe-node-fetch"], forwardingActive: false,
                consoleTop: "SMP MULTIPROCESSOR • CLOCK CYCLE 1",
                consoleMid: "The OS scheduler dispatches Iteration A to Core 0 and Iteration B to Core 1.",
                consoleSub: "True hardware multitasking across separate silicon dies.",
                inlinePreview: "<strong>Dividing the Realm:</strong> The operating system scheduler splits the workload, assigning iteration <code>I1</code> to <strong>Core 0</strong> and iteration <code>I2</code> to <strong>Core 1</strong> simultaneously.",
                what: "The operating system kernel assigns distinct thread workloads to separate physical processor cores.",
                why: "Multicore architectures achieve true thread-level parallelism (TLP) rather than relying solely on instruction-level tricks."
              },
              {
                cycle: "Cycle 2", phase: "Independent Execution Dies", retired: "0 / 4", ipc: "0.00 IPC", hazard: "None",
                fetch: "Core 0: I3 | Core 1: I4", decode: "Core 0: I1 | Core 1: I2", exec: "Empty", wb: "Empty",
                activeStages: ["pipe-node-fetch", "pipe-node-decode"], forwardingActive: false,
                consoleTop: "SMP MULTIPROCESSOR • CLOCK CYCLE 2",
                consoleMid: "Both cores decode their assigned thread instructions in parallel.",
                consoleSub: "Private L1 instruction caches operate independently.",
                inlinePreview: "<strong>Autonomous Realms:</strong> Both cores decode their respective instructions in parallel using dedicated private L1 caches, completely isolated from each other's execution quirks.",
                what: "Both physical cores execute decode stages independently using private on-die resources.",
                why: "Private core caches eliminate cross-core resource contention and bus arbitration delays."
              },
              {
                cycle: "Cycle 3", phase: "Parallel Memory Operations", retired: "2 / 4", ipc: "0.67 IPC", hazard: "MESI Coherent",
                fetch: "Drained", decode: "Core 0: I3 | Core 1: I4", exec: "Core 0: I1 | Core 1: I2", wb: "Empty",
                activeStages: ["pipe-node-decode", "pipe-node-exec"], forwardingActive: false,
                consoleTop: "SMP MULTIPROCESSOR • CLOCK CYCLE 3",
                consoleMid: "Core 0 and Core 1 complete memory loads concurrently.",
                consoleSub: "Cache coherency bus snooping ensures data consistency.",
                inlinePreview: "<strong>Concurrent Memory:</strong> Core 0 and Core 1 both complete their memory loads at the exact same moment. Hardware bus snooping maintains a unified view of system memory.",
                what: "Both cores execute memory load operations in parallel while cache controllers maintain coherency.",
                why: "Symmetric multiprocessing scales computational throughput linearly with physical core count."
              },
              {
                cycle: "Cycle 4", phase: "Multiprocessing Complete", retired: "4 / 4", ipc: "1.00 IPC", hazard: "None",
                fetch: "Idle", decode: "Idle", exec: "Core 0: I3 | Core 1: I4", wb: "Core 0 & Core 1 Retired",
                activeStages: ["pipe-node-exec", "pipe-node-wb"], forwardingActive: false,
                consoleTop: "SMP MULTIPROCESSOR • CLOCK CYCLE 4 (COMPLETE)",
                consoleMid: "Both physical cores finish their workloads in unison.",
                consoleSub: "Maximum multi-core efficiency achieved.",
                inlinePreview: "<strong>Multicore Harmony:</strong> Core 0 and Core 1 complete their calculations and retire their threads together. True multi-threaded execution triumphs!",
                what: "Both processor cores finalize calculations and commit thread retirement states simultaneously.",
                why: "Multicore parallelism delivers massive computing power for concurrent operating system environments."
              }
            ]
          };"""

    # Replace the old storylines block with the new narrative version
    parts = content.split(old_storylines_marker, 1)
    # Find where pipeStorylines block ends (before function renderPipeState)
    remainder = parts[1].split('function renderPipeState()', 1)

    updated_content = f"{parts[0]}{new_storylines_block}\n\n          function renderPipeState(){remainder[1]}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully updated pipeline interactive walkthrough to story mode in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Transform instruction pipeline walkthrough into a narrative story arc\n\n"
            "Update the interactive pipeline simulator in 02-hardware-review.html to\n"
            "feature scenario-driven storytelling instead of static transition labels."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_narrative_stepper_storylines()
