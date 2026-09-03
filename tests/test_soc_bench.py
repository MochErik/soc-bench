"""Unit tests for SoC-Bench."""

import unittest
from soc_bench.cpu_bench import run_cpu_benchmark
from soc_bench.mem_bench import run_mem_benchmark, run_disk_benchmark


class TestSocBench(unittest.TestCase):

    def test_cpu_bench_execution(self):
        res = run_cpu_benchmark()
        self.assertIn("score", res)
        self.assertGreater(res["score"], 0)

    def test_mem_bench_execution(self):
        res = run_mem_benchmark(buffer_mb=4)
        self.assertIn("write_speed_mb_s", res)
        self.assertIn("read_speed_mb_s", res)

    def test_disk_bench_execution(self):
        res = run_disk_benchmark(target_mb=2)
        self.assertIn("disk_write_mb_s", res)
        self.assertIn("disk_read_mb_s", res)


if __name__ == "__main__":
    unittest.main()
