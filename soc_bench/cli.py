"""⚡ SoC-Bench - Comprehensive Multi-Tier Hardware Benchmark CLI for SBCs, PCs, and Servers."""

import argparse
import sys
import platform
import os
import time
import hashlib
import concurrent.futures
import tempfile
from typing import List, Dict, Any

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED = "\033[31m"


def run_single_core_bench(duration: float = 1.0) -> int:
    """Run single-core integer and hashing operations for a given duration."""
    t_end = time.perf_counter() + duration
    ops = 0
    data = b"benchmark_workload_sample_string_for_single_core"
    while time.perf_counter() < t_end:
        hashlib.sha256(data).digest()
        ops += 100
    return int(ops / duration)


def run_multi_core_bench(cores: int, duration: float = 1.0) -> int:
    """Run multi-core worker threads."""
    with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
        futures = [executor.submit(run_single_core_bench, duration) for _ in range(cores)]
        results = [f.result() for f in futures]
    return sum(results)


def run_ram_deep_bench(buffer_mb: int = 64) -> Dict[str, Any]:
    """Benchmark RAM memory bandwidth and latency."""
    size_bytes = buffer_mb * 1024 * 1024
    chunk = b"\xaa" * (1024 * 1024)  # 1MB chunk

    # RAM Write
    t0 = time.perf_counter()
    mem = bytearray()
    for _ in range(buffer_mb):
        mem.extend(chunk)
    t_write = time.perf_counter() - t0
    write_speed = round(buffer_mb / t_write, 2) if t_write > 0 else 0

    # RAM Read
    t0 = time.perf_counter()
    _ = bytes(mem)
    t_read = time.perf_counter() - t0
    read_speed = round(buffer_mb / t_read, 2) if t_read > 0 else 0

    return {
        "write_mb_s": write_speed,
        "read_mb_s": read_speed,
        "latency_ns": round((t_read / max(1, len(mem))) * 1e9, 2)
    }


def run_disk_deep_bench(target_mb: int = 32) -> Dict[str, Any]:
    """Benchmark disk sequential read/write and random 4KB IOPS."""
    tmp_dir = tempfile.gettempdir()
    test_file = os.path.join(tmp_dir, f"socbench_test_{os.getpid()}.bin")
    chunk_1mb = os.urandom(1024 * 1024)

    # 1. Sequential Write
    t0 = time.perf_counter()
    with open(test_file, "wb") as f:
        for _ in range(target_mb):
            f.write(chunk_1mb)
            f.flush()
            os.fsync(f.fileno())
    t_seq_w = time.perf_counter() - t0
    seq_w_speed = round(target_mb / t_seq_w, 2) if t_seq_w > 0 else 0

    # 2. Sequential Read
    t0 = time.perf_counter()
    with open(test_file, "rb") as f:
        while f.read(1024 * 1024):
            pass
    t_seq_r = time.perf_counter() - t0
    seq_r_speed = round(target_mb / t_seq_r, 2) if t_seq_r > 0 else 0

    # 3. 4KB Random IOPS Simulation
    chunk_4k = b"\xff" * 4096
    iops_count = 500
    t0 = time.perf_counter()
    with open(test_file, "r+b") as f:
        for i in range(iops_count):
            pos = (i * 4096) % (target_mb * 1024 * 1024 - 4096)
            f.seek(pos)
            f.write(chunk_4k)
    t_iops = time.perf_counter() - t0
    iops = int(iops_count / t_iops) if t_iops > 0 else 0

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

    return {
        "seq_write_mb_s": seq_w_speed,
        "seq_read_mb_s": seq_r_speed,
        "iops_4k": iops
    }


def evaluate_tier(single_ops: int, multi_ops: int, ram_read: float) -> str:
    """Classify hardware into tier grade S, A, B, C, D."""
    if multi_ops > 1_500_000 or ram_read > 20_000:
        return f"{MAGENTA}{BOLD}🏆 Tier S (Workstation / Apple Silicon / High-End Core){RESET}"
    elif multi_ops > 600_000 or ram_read > 5_000:
        return f"{GREEN}{BOLD}🥇 Tier A (Performance Laptop / High-Core Desktop){RESET}"
    elif multi_ops > 200_000:
        return f"{CYAN}{BOLD}🥈 Tier B (Mainstream PC / Ultrabook){RESET}"
    elif multi_ops > 50_000:
        return f"{YELLOW}{BOLD}🥉 Tier C (Single Board Computer: Raspberry Pi 4/5, Orange Pi 5){RESET}"
    else:
        return f"{DIM}⚙️  Tier D (Low-Power SBC / STB HG680P/B860H Armbian){RESET}"


def main(args: List[str] = None):
    parser = argparse.ArgumentParser(
        prog="soc-bench",
        description="⚡ SoC-Bench - Comprehensive Multi-Tier Hardware Benchmark CLI for SBCs, PCs, and Servers",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="Output benchmark metrics as JSON")
    parser.add_argument("--fast", action="store_true", help="Fast 3-second speedrun mode")
    parsed = parser.parse_args(args)

    cores = os.cpu_count() or 1
    bench_duration = 0.5 if parsed.fast else 1.0

    if not parsed.json:
        print(f"\n{CYAN}{BOLD}⚡ SoC-Bench{RESET} {DIM}v2.0.0 — Comprehensive Micro Hardware Benchmark{RESET}")
        print(f"{DIM}Host:{RESET} {BOLD}{platform.node()}{RESET} | {DIM}Arch:{RESET} {platform.machine()} | {DIM}OS:{RESET} {platform.system()} {platform.release()} ({cores} Cores)")
        print("═" * 72)
        print("⏳ Running Single-Core Compute Test...")

    # 1. Single-Core
    single_ops = run_single_core_bench(bench_duration)

    if not parsed.json:
        print(f"⏳ Running Multi-Core Stress Test ({cores} Workers)...")

    # 2. Multi-Core
    multi_ops = run_multi_core_bench(cores, bench_duration)
    scaling = round(multi_ops / max(1, single_ops), 2)

    if not parsed.json:
        print("⏳ Measuring RAM Memory Bandwidth & Micro-Latency...")

    # 3. RAM
    ram = run_ram_deep_bench(buffer_mb=64)

    if not parsed.json:
        print("⏳ Benchmarking Storage (Sequential Read/Write + 4K Random IOPS)...\n")

    # 4. Disk
    disk = run_disk_deep_bench(target_mb=32)
    tier_label = evaluate_tier(single_ops, multi_ops, ram["read_mb_s"])

    if parsed.json:
        import json
        out_data = {
            "host": platform.node(),
            "os": platform.system(),
            "cores": cores,
            "single_core_ops_sec": single_ops,
            "multi_core_ops_sec": multi_ops,
            "multi_core_scaling": scaling,
            "ram_write_mb_s": ram["write_mb_s"],
            "ram_read_mb_s": ram["read_mb_s"],
            "disk_seq_write_mb_s": disk["seq_write_mb_s"],
            "disk_seq_read_mb_s": disk["seq_read_mb_s"],
            "disk_4k_iops": disk["iops_4k"]
        }
        print(json.dumps(out_data, indent=2))
        return

    print(f"{BOLD}📊 Comprehensive Hardware Benchmark Scorecard:{RESET}")
    print("─" * 72)
    print(f"  {BOLD}⚙️  Single-Core CPU    :{RESET} {CYAN}{single_ops:,} ops/s{RESET}")
    print(f"  {BOLD}🚀 Multi-Core CPU     :{RESET} {GREEN}{BOLD}{multi_ops:,} ops/s{RESET} ({scaling}x Multi-Core Scaling)")
    print(f"  {BOLD}🧠 RAM Write / Read   :{RESET} {CYAN}{ram['write_mb_s']:,} MB/s{RESET} / {CYAN}{ram['read_mb_s']:,} MB/s{RESET}")
    print(f"  {BOLD}💽 Disk Seq Write/Read:{RESET} {YELLOW}{disk['seq_write_mb_s']} MB/s{RESET} / {YELLOW}{disk['seq_read_mb_s']} MB/s{RESET}")
    print(f"  {BOLD}⚡ Storage 4K IOPS    :{RESET} {MAGENTA}{disk['iops_4k']:,} IOPS{RESET}")
    print("─" * 72)
    print(f"  {BOLD}🏆 Performance Grade  :{RESET} {tier_label}")
    print("═" * 72 + "\n")


if __name__ == "__main__":
    main()
