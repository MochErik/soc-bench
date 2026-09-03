# ⚡ SoC-Bench (`soc-bench`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Hardware Benchmark](https://img.shields.io/badge/Benchmark-10%20Seconds%20Speedrun-teal.svg)](https://github.com/MochErik/soc-bench)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)](https://github.com/MochErik/soc-bench)

> **10-Second CPU, Memory & Disk I/O Micro-Benchmark CLI.** Quickly evaluate multi-core CPU compute scores, RAM bandwidth throughput, and disk sequential I/O write/read speeds on Single Board Computers (Armbian STB HG680P/B860H, Raspberry Pi, Orange Pi) and PCs without heavy benchmark suites.

---

## 🚀 Quick Install

```bash
pip install soc-bench
```

---

## 🖥️ Usage

```bash
soc-bench
```

```
⚡ SoC-Bench v1.0.0 — Micro Hardware Benchmark
Host: armbian-stb-hg680p | Arch: aarch64 | OS: Linux 5.15.0-arm64
══════════════════════════════════════════════════════════════════════
📊 Benchmark Scorecard:
──────────────────────────────────────────────────────────────────────
  ⚙️  CPU Score       : 42,850 pts (4 Cores, 42,850 ops/s)
  🧠 RAM Write / Read : 1,420 MB/s / 2,150 MB/s
  💽 Disk Write / Read: 48.2 MB/s / 112.5 MB/s
══════════════════════════════════════════════════════════════════════
```

---

## 📜 License

MIT License © 2026 [Moch. Erik Irriansyah](https://github.com/MochErik)
