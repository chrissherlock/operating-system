#!/usr/bin/env python3
# =====================================================================
# expand_generation_five.py: Expand Generation 5 historical description
# =====================================================================
import os
import subprocess

def execute_gen5_expansion():
    file_path = os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    header_str = "<h3>Generation 5: Mobile, Cloud, &amp; Ubiquitous Computing (Present)</h3>"
    pos = content.find(header_str)
    if pos != -1:
        end_pos = content.find("</p>", pos) + 4

        new_block = (
            "<h3>Generation 5: Mobile, Cloud, &amp; Ubiquitous Computing (Present)</h3>\n"
            "      <p>\n"
            "        The contemporary computing era has shifted dramatically away from stationary desktop environments toward highly distributed, heterogeneous, and mobile ecosystems. Modern operating systems must span an immense spectrum of hardware scales—ranging from miniature battery-powered wearable sensors and smartphones to massive hyperscale cloud datacenters comprising millions of server cores.\n"
            "      </p>\n"
            "      <p>\n"
            "        Key architectural paradigms defining Generation 5 include:\n"
            "      </p>\n"
            "      <ul style=\"margin-left: 20px; color: var(--text-muted); line-height: 1.6;\">\n"
            "        <li><strong>Mobile &amp; Power-Aware Operating Systems:</strong> Platforms like Android and iOS introduced aggressive power management frameworks, thermal throttling, context-aware sensor integration, strict application sandboxing, and wireless cellular/Wi-Fi stack management to maximize battery longevity and user responsiveness.</li>\n"
            "        <li><strong>Cloud Computing &amp; Hypervisors:</strong> Hyperscale cloud infrastructures rely on robust Type-1 hypervisors (such as KVM, Xen, and VMware ESXi) to virtualize compute, storage, and networking layers, allowing cloud providers to dynamically provision and migrate virtual machines across elastic server clusters.</li>\n"
            "        <li><strong>Containerization &amp; Orchestration:</strong> Operating system-level virtualization through container runtimes (such as Docker) and orchestrators (such as Kubernetes) enables lightweight, isolated application packaging that shares a common host kernel, optimizing resource utilization and microservices deployment.</li>\n"
            "        <li><strong>Ubiquitous &amp; IoT Computing:</strong> Billions of smart devices, industrial sensors, and embedded appliances run specialized lightweight real-time operating systems (RTOS) and micro-kernels (such as FreeRTOS or Zephyr) that integrate seamlessly into ambient networks with minimal memory and power footprints.</li>\n"
            "      </ul>"
        )

        content = content[:pos] + new_block + content[end_pos:]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("--> Generation 5 description successfully expanded.")

    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", "Expand Generation 5 mobile, cloud, and ubiquitous computing historical description in Module 1"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git note: {e}")

if __name__ == "__main__":
    execute_gen5_expansion()
