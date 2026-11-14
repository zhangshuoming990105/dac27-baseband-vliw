# Paper Config: Baseband VLIW (DAC 2027)

- **Full Title**: Post-Layout Evaluation and Tapeout of a Streamlined Domain-Specific VLIW Architecture with Custom RISC-V Extensions for Wireless Baseband
- **Target Venue**: DAC 2027 (7 pages: 6 body pages + 1 page references, anonymous double-blind submission)
- **Sync Mode**: Submission PDF Archived Locally (`./submissions/dac2027-submission.pdf`; LaTeX source / Overleaf repo not yet linked)
- **Archived Submission**: [submissions/dac2027-submission.pdf](./submissions/dac2027-submission.pdf)
- **Core Highlights (from submission PDF)**:
  - 4-way variable-length RV32-based custom VLIW co-processor (10-stage pipeline, 16×32-bit scalar RF, 16×640-bit SIMD vector RF with 16×40-bit guarded elements, Replicated Common Functional Units across all 4 slots, dual-destination `rd2` encoding).
  - LLVM-based compiler backend with hybrid list + ILP instruction scheduling guided by a data-flow IPC upper-bound model.
  - Full sign-off post-layout implementation & tapeout in TSMC 22 nm ULL at 800 MHz (`0.98 mm²` core STD cell area, `573.4 mW` dynamic power), integrated into a 3-core SparkLink SLB 2.0 baseband SoC (`2T2R@80MHz`, `800 Mbps` peak throughput), meeting all symbol-level and link-level real-time latency constraints.
