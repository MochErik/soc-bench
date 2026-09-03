"""CPU Integer & Hash compute speed benchmark."""

import hashlib
import time
import concurrent.futures
import os


def cpu_worker(iterations: int = 200_000) -> int:
    """Worker performing SHA256 hashing and integer arithmetic."""
    data = b"benchmark_data_for_soc_eval"
    count = 0
    for i in range(iterations):
        data = hashlib.sha256(data).digest()
        count += (i % 7)
    return count


def run_cpu_benchmark(duration_target: float = 3.0) -> dict:
    """Run multi-core CPU benchmark and calculate score."""
    cores = os.cpu_count() or 1
    t0 = time.perf_counter()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor:
        futures = [executor.submit(cpu_worker, 300_000) for _ in range(cores)]
        for f in concurrent.futures.as_completed(futures):
            f.result()
            
    elapsed = time.perf_counter() - t0
    ops_total = (300_000 * cores) / max(0.001, elapsed)
    score = int(ops_total / 1000)

    return {
        "cores": cores,
        "elapsed_sec": round(elapsed, 2),
        "ops_per_sec": int(ops_total),
        "score": score
    }
