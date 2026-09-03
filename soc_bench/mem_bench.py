"""Memory RAM bandwidth and Disk I/O benchmark modules."""

import time
import tempfile
import os


def run_mem_benchmark(buffer_mb: int = 64) -> dict:
    """Measure sequential memory write and read throughput."""
    size_bytes = buffer_mb * 1024 * 1024
    buf = bytearray(size_bytes)
    
    # 1. Write benchmark
    t0 = time.perf_counter()
    for i in range(0, size_bytes, 4096):
        buf[i:i+4] = b"\xaa\xbb\xcc\xdd"
    t_write = time.perf_counter() - t0
    write_speed_mb = round(buffer_mb / max(0.0001, t_write), 1)

    # 2. Read benchmark
    t0 = time.perf_counter()
    total = sum(buf[0:size_bytes:4096])
    t_read = time.perf_counter() - t0
    read_speed_mb = round(buffer_mb / max(0.0001, t_read), 1)

    return {
        "buffer_mb": buffer_mb,
        "write_speed_mb_s": write_speed_mb,
        "read_speed_mb_s": read_speed_mb
    }


def run_disk_benchmark(target_mb: int = 32) -> dict:
    """Measure local storage sequential write and read throughput."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        filepath = f.name

    data = os.urandom(1024 * 1024)  # 1MB block
    try:
        # Write test
        t0 = time.perf_counter()
        with open(filepath, "wb") as f:
            for _ in range(target_mb):
                f.write(data)
            f.flush()
            os.fsync(f.fileno())
        t_write = time.perf_counter() - t0
        write_mb_s = round(target_mb / max(0.0001, t_write), 1)

        # Read test
        t0 = time.perf_counter()
        with open(filepath, "rb") as f:
            while f.read(1024 * 1024):
                pass
        t_read = time.perf_counter() - t0
        read_mb_s = round(target_mb / max(0.0001, t_read), 1)

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return {
        "file_size_mb": target_mb,
        "disk_write_mb_s": write_mb_s,
        "disk_read_mb_s": read_mb_s
    }
