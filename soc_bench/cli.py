"""SoC-Bench CLI Main Entrypoint."""

import argparse
import sys
import platform
from typing import List

from soc_bench.cpu_bench import run_cpu_benchmark
from soc_bench.mem_bench import run_mem_benchmark, run_disk_benchmark

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"


def main(args: List[str] = None):
    parser = argparse.ArgumentParser(
        prog="soc-bench",
        description="⚡ SoC-Bench - 10-Second CPU, Memory & Disk I/O Micro-Benchmark CLI",
        epilog="Examples:\n"
               "  soc-bench                  # Run full quick benchmark\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parsed = parser.parse_args(args)

    print(f"\n{CYAN}{BOLD}⚡ SoC-Bench{RESET} {DIM}v1.0.0 — Micro Hardware Benchmark{RESET}")
    print(f"{DIM}Host:{RESET} {BOLD}{platform.node()}{RESET} | {DIM}Arch:{RESET} {platform.machine()} | {DIM}OS:{RESET} {platform.system()} {platform.release()}")
    print("═" * 70)

    # 1. CPU
    print(f"⏳ Running Multi-Core CPU Compute Benchmark...")
    cpu_res = run_cpu_benchmark()
    
    # 2. RAM
    print(f"⏳ Testing RAM Memory Bandwidth...")
    mem_res = run_mem_benchmark(buffer_mb=64)

    # 3. Disk
    print(f"⏳ Testing Storage Sequential Read/Write Speed...\n")
    disk_res = run_disk_benchmark(target_mb=32)

    print(f"{BOLD}📊 Benchmark Scorecard:{RESET}")
    print("─" * 70)
    print(f"  {BOLD}⚙️  CPU Score       :{RESET} {GREEN}{BOLD}{cpu_res['score']:,} pts{RESET} ({cpu_res['cores']} Cores, {cpu_res['ops_per_sec']:,} ops/s)")
    print(f"  {BOLD}🧠 RAM Write / Read :{RESET} {CYAN}{mem_res['write_speed_mb_s']:,} MB/s{RESET} / {CYAN}{mem_res['read_speed_mb_s']:,} MB/s{RESET}")
    print(f"  {BOLD}💽 Disk Write / Read:{RESET} {YELLOW}{disk_res['disk_write_mb_s']} MB/s{RESET} / {YELLOW}{disk_res['disk_read_mb_s']} MB/s{RESET}")
    print("═" * 70 + "\n")


if __name__ == "__main__":
    main()
