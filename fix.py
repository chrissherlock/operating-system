#!/usr/bin/env python3
import os

target_path = "week09-memory-management/08-aging-algorithm.html"

if os.path.exists(target_path):
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    old_css = "gap: 20px;"
    new_css = "gap: 32px;"  # Increased column gap

    if old_css in content:
        content = content.replace(old_css, new_css)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully updated grid gap in {target_path}")
