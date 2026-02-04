#!/usr/bin/env python3
import argparse
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal



def bytes_to_gb(value: int) -> float:
    return round(value / (1024**3), 2)


def disk_report(path: str) -> dict:
    total, used, free = shutil.disk_usage(path)
    percent = (used / total) * 100 if total else 0.0
    return {
        "path": path,
        "total_gb": bytes_to_gb(total),
        "used_gb": bytes_to_gb(used),
        "free_gb": bytes_to_gb(free),
        "used_percent": round(percent, 2),
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a simple system disk report.")
    p.add_argument("--path", default="/", help="Filesystem path to inspect (default: /)")
    p.add_argument(
        "--threshold",
        type=float,
        default=80.0,
        help="Warning threshold for disk usage percent (default: 80)",
    )
    return p


def main() -> int:
    args = build_parser().parse_args()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host = platform.node()
    os_info = f"{platform.system()} {platform.release()}"

    disk = disk_report(args.path)
    status: Literal["OK", "WARN"] = "OK"
    if disk["used_percent"] > args.threshold:
        status = "WARN"


    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = out_dir / f"system_report_{stamp}.txt"


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

    report_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {report_file}")
    print(f"Threshold: {args.threshold}% | Current usage: {disk['used_percent']}%")
    log_file = out_dir / "run.log"
    log_line = (
        f"{now} | path={args.path} | threshold={args.threshold} "
        f"| usage={disk['used_percent']} | status={status}\n"
    )
    with log_file.open("a", encoding="utf-8") as f:
        f.write(log_line)


    if disk["used_percent"] > args.threshold:
        print(f"WARNING: Disk usage exceeds {args.threshold}%")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
