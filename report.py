#!/usr/bin/env python3

import shutil
import platform
from datetime import datetime
from pathlib import Path
import sys


def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)


def disk_report(path: str = "/") -> dict:
    total, used, free = shutil.disk_usage(path)
    percent = (used / total) * 100 if total else 0

    return {
        "path": path,
        "total_gb": bytes_to_gb(total),
        "used_gb": bytes_to_gb(used),
        "free_gb": bytes_to_gb(free),
        "used_percent": round(percent, 2),
    }


def main() -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host = platform.node()
    os_info = f"{platform.system()} {platform.release()}"

    disk = disk_report("/")

    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    report_file = out_dir / "system_report.txt"

    lines = [
        "SYSTEM REPORT",
        "==============",
        f"Generated: {now}",
        f"Host: {host}",
        f"OS: {os_info}",
        "",
        "DISK USAGE",
        "----------",
        f"Path: {disk['path']}",
        f"Total: {disk['total_gb']} GB",
        f"Used:  {disk['used_gb']} GB ({disk['used_percent']}%)",
        f"Free:  {disk['free_gb']} GB",
    ]

    report_file.write_text("\n".join(lines))
    print(f"Report written to {report_file}")

    if disk["used_percent"] > 80:
        print("WARNING: Disk usage exceeds 80%")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
