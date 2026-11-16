"""Generate flat IEEE/DAC vector PDF for Co-Design Overview (Style A3 unified with Figs 1-4)."""
from pathlib import Path
from pdf_canvas import PDFCanvas


def draw_box(
    cv: PDFCanvas,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str = "",
    fc: str = "#FFFFFF",
    ec: str = "#1F2937",
    lw: float = 0.72,
    fs: float = 6.6,
    bold: bool = False,
    tc: str = "#111111",
    dash: tuple[float, float] | None = None,
    line_gap: float = 1.12,
    z: int = 3,
) -> None:
    cv.rect(x, y, w, h, fc=fc, ec=ec, lw=lw, dash=dash, z=z)
    if text:
        cv.text(x + w / 2.0, y + h / 2.0, text, fs=fs, bold=bold, tc=tc, line_gap=line_gap, z=z + 1)


def block_arrow_h(
    cv: PDFCanvas,
    x1: float,
    x2: float,
    yc: float,
    bidir: bool = False,
    sw: float = 0.72,
    hw: float = 1.55,
    hl: float = 1.25,
    fc: str = "#9CA3AF",
    ec: str = "#374151",
    lw: float = 0.55,
    z: int = 4,
) -> None:
    lo, hi = (x1, x2) if x1 < x2 else (x2, x1)
    if bidir:
        pts = [
            (lo, yc),
            (lo + hl, yc + hw),
            (lo + hl, yc + sw),
            (hi - hl, yc + sw),
            (hi - hl, yc + hw),
            (hi, yc),
            (hi - hl, yc - hw),
            (hi - hl, yc - sw),
            (lo + hl, yc - sw),
            (lo + hl, yc - hw),
        ]
    elif x2 > x1:
        pts = [
            (x1, yc + sw),
            (x2 - hl, yc + sw),
            (x2 - hl, yc + hw),
            (x2, yc),
            (x2 - hl, yc - hw),
            (x2 - hl, yc - sw),
            (x1, yc - sw),
        ]
    else:
        pts = [
            (x1, yc + sw),
            (x2 + hl, yc + sw),
            (x2 + hl, yc + hw),
            (x2, yc),
            (x2 + hl, yc - hw),
            (x2 + hl, yc - sw),
            (x1, yc - sw),
        ]
    cv.polygon(pts, fc=fc, ec=ec, lw=lw, z=z)


def block_arrow_v(
    cv: PDFCanvas,
    xc: float,
    y1: float,
    y2: float,
    bidir: bool = False,
    sw: float = 0.68,
    hw: float = 1.48,
    hl: float = 1.10,
    fc: str = "#9CA3AF",
    ec: str = "#374151",
    lw: float = 0.55,
    z: int = 4,
) -> None:
    lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
    if bidir:
        pts = [
            (xc, hi),
            (xc + hw, hi - hl),
            (xc + sw, hi - hl),
            (xc + sw, lo + hl),
            (xc + hw, lo + hl),
            (xc, lo),
            (xc - hw, lo + hl),
            (xc - sw, lo + hl),
            (xc - sw, hi - hl),
            (xc - hw, hi - hl),
        ]
    elif y2 < y1:
        pts = [
            (xc - sw, y1),
            (xc + sw, y1),
            (xc + sw, y2 + hl),
            (xc + hw, y2 + hl),
            (xc, y2),
            (xc - hw, y2 + hl),
            (xc - sw, y2 + hl),
        ]
    else:
        pts = [
            (xc - sw, y1),
            (xc + sw, y1),
            (xc + sw, y2 - hl),
            (xc + hw, y2 - hl),
            (xc, y2),
            (xc - hw, y2 - hl),
            (xc - sw, y2 - hl),
        ]
    cv.polygon(pts, fc=fc, ec=ec, lw=lw, z=z)


def main() -> None:
    cv = PDFCanvas(width_pt=516.0, height_pt=164.0, xlim=200.0, ylim=63.6, pad_pt=1.2)

    # Exact color palette shared with Fig. 1, Fig. 2, Fig. 3, and Fig. 4
    c_mem = "#DFE3E8"
    c_front = "#BBDDFB"
    c_slot_bg = "#CFE6FC"
    c_bound = "#E3EBF6"
    c_rcfu = "#CFE3B2"
    c_fu = "#7BAEF7"
    c_rf = "#B4BAC3"
    c_periph = "#D6D8F7"
    c_gate = "#FDF2D0"
    c_isa_bg = "#FDF0F0"
    c_isa_fg = "#B80000"
    c_dash = "#1D6FA5"

    # Outer Subsystem Dashed Enclosures (matching Fig. 4)
    y_zone_bot = 1.0
    y_zone_top = 62.6
    h_zone = y_zone_top - y_zone_bot

    x_l0, x_l1 = 0.5, 114.6
    x_r0, x_r1 = 126.8, 199.5

    draw_box(cv, x_l0, y_zone_bot, x_l1 - x_l0, h_zone, fc="none", ec=c_dash, lw=0.78, dash=(2.6, 1.7), z=1)
    draw_box(cv, x_r0, y_zone_bot, x_r1 - x_r0, h_zone, fc="none", ec=c_dash, lw=0.78, dash=(2.6, 1.7), z=1)

    cv.text(x_l0 + 1.8, y_zone_top - 1.6, "Bound-Guided LLVM VLIW Compiler Backend", fs=7.4, bold=True, ha="left", va="top", z=5)
    cv.text(x_r0 + 1.8, y_zone_top - 1.6, "Streamlined 4-Slot RV32 VLIW Co-Processor", fs=7.4, bold=True, ha="left", va="top", z=5)

    # =========================================================================
    # LEFT ZONE: Bound-Guided LLVM Compiler Flow (Zero Line Crossings)
    # =========================================================================
    # Top Hardware-to-Compiler Contract Channel (y = 49.7 .. 56.2, aligned with Right Zone top!)
    y_ct = 49.7
    h_ct = 6.5
    # Box C1: Admissible Slots & RCFU
    draw_box(cv, 30.2, y_ct, 38.3, h_ct, "", fc="#FFFFFF", ec=c_dash, lw=0.68, dash=(2.2, 1.4), z=3)
    cv.rich_text(49.35, y_ct + 4.40, [("Slot Contract ", "b"), ("S", "i"), ("(", "r"), ("u", "i"), (") & 4x RCFU", "b")], fs=6.3)
    cv.text(49.35, y_ct + 1.75, "Exclusive vs. 4-Slot Pooled Ops", fs=5.75, tc="#374151")

    # Box C2: MCFU & Pipeline Latencies
    draw_box(cv, 72.2, y_ct, 40.8, h_ct, "", fc="#FFFFFF", ec=c_dash, lw=0.68, dash=(2.2, 1.4), z=3)
    cv.rich_text(92.6, y_ct + 4.40, [("Hazard Latencies ", "b"), ("d", "sym"), ("(", "r"), ("u, v", "i"), (")", "r")], fs=6.3)
    cv.text(92.6, y_ct + 1.75, "Non-Stalling MCFU RAW / WAR / WAW", fs=5.65, tc="#374151")

    # Dashed contract feed from Co-Processor (Right Zone) into C2 -> C1 -> DAG / Lower Bound
    cv.polyline([(x_r0, y_ct + h_ct / 2.0), (113.0, y_ct + h_ct / 2.0)], ec=c_dash, lw=0.72, dash=(2.2, 1.4), arrow_end=True, z=4)
    cv.polyline([(72.2, y_ct + h_ct / 2.0), (68.5, y_ct + h_ct / 2.0)], ec=c_dash, lw=0.72, dash=(2.2, 1.4), arrow_end=True, z=4)

    # Main compiler spine centerline
    y_spine = 28.6

    # Col 1: PHY Kernels -> Custom DAG Lowering
    x_c1, w_c1 = 1.8, 20.4
    draw_box(cv, x_c1, 39.4, w_c1, 11.0, "PHY C &\nIntrinsics\n(15 Op Classes)", fc=c_mem, fs=6.35, line_gap=1.10)
    y_low, h_low = y_spine - 6.9, 13.8
    cv.polyline([(x_c1 + w_c1 / 2.0, 39.4), (x_c1 + w_c1 / 2.0, y_low + h_low)], ec="#1F2937", lw=0.75, arrow_end=True)

    draw_box(cv, x_c1, y_low, w_c1, h_low, "", fc=c_front)
    cv.text(x_c1 + w_c1 / 2.0, y_low + 11.0, "Custom DAG\nLowering", fs=6.45, bold=True, line_gap=1.06)
    cv.rich_text(x_c1 + w_c1 / 2.0, y_low + 5.3, [("Dual-Dest ", "r"), ("rd2", "b")], fs=6.1, tc=c_isa_fg)
    cv.text(x_c1 + w_c1 / 2.0, y_low + 2.3, "40b Split-Guard", fs=6.0)

    # Col 2: Dependence DAG G=(V,E)
    x_c2, w_c2 = 25.4, 20.6
    y_dag, h_dag = y_spine - 7.1, 14.2
    draw_box(cv, x_c2, y_dag, w_c2, h_dag, "", fc=c_slot_bg)
    cv.text(x_c2 + w_c2 / 2.0, y_dag + 11.5, "Dependence", fs=6.45, bold=True)
    cv.rich_text(x_c2 + w_c2 / 2.0, y_dag + 8.5, [("DAG ", "b"), ("G", "i"), (" = (", "r"), ("V, E", "i"), (")", "r")], fs=6.35)
    cv.rich_text(x_c2 + w_c2 / 2.0, y_dag + 5.2, [("\xa3", "sym"), ("16 Live Regs", "r")], fs=5.85, tc="#1F2937")
    cv.text(x_c2 + w_c2 / 2.0, y_dag + 2.4, "(Zero Spills)", fs=5.75, tc="#1F2937")

    # Connect Lowering -> DAG (straight along spine)
    cv.polyline([(x_c1 + w_c1, y_spine), (x_c2, y_spine)], ec="#1F2937", lw=0.75, arrow_end=True)

    # Col 3: Split into Coupled Lower Bound (upper) & Stage 1 List Scheduler (on spine)
    x_c3, w_c3 = 50.4, 26.4
    y_lb, h_lb = 35.7, 10.5
    draw_box(cv, x_c3, y_lb, w_c3, h_lb, "", fc=c_bound)
    cv.text(x_c3 + w_c3 / 2.0, y_lb + 8.2, "Coupled Lower Bound", fs=6.35, bold=True)
    cv.rich_text(
        x_c3 + w_c3 / 2.0,
        y_lb + 5.0,
        [("L", "i"), ("LB", "sub"), (" = max(", "r"), ("L", "i"), ("dep", "sub"), (", ", "r"), ("L", "i"), ("res", "sub"), (")", "r")],
        fs=6.25,
    )
    cv.text(x_c3 + w_c3 / 2.0, y_lb + 1.9, "Eq. (1)-(2) IPC Ceiling", fs=5.7, tc="#374151")

    y_s1, h_s1 = y_spine - 5.6, 11.2
    draw_box(cv, x_c3, y_s1, w_c3, h_s1, "", fc=c_slot_bg)
    cv.text(x_c3 + w_c3 / 2.0, y_s1 + 8.8, "Stage 1: List Scheduler", fs=6.35, bold=True)
    cv.text(x_c3 + w_c3 / 2.0, y_s1 + 5.6, "Critical Height & Scarcity", fs=5.85)
    cv.rich_text(x_c3 + w_c3 / 2.0, y_s1 + 2.2, [("Produces ", "r"), ("L", "i"), ("list", "sub"), (" Bundles", "r")], fs=6.05)

    # Connect Contract C1 down into DAG & Lower Bound
    cv.polyline([(35.7, y_ct), (35.7, y_dag + h_dag)], ec=c_dash, lw=0.68, dash=(2.2, 1.4), arrow_end=True)
    cv.polyline([(61.5, y_ct), (61.5, y_lb + h_lb)], ec=c_dash, lw=0.68, dash=(2.2, 1.4), arrow_end=True)

    # Fork from DAG -> Straight into Stage 1 & Upper branch into Coupled Lower Bound
    x_fork = 48.0
    cv.polyline([(x_c2 + w_c2, y_spine), (x_c3, y_spine)], ec="#1F2937", lw=0.75, arrow_end=True)
    cv.polyline([(x_fork, y_spine), (x_fork, y_lb + h_lb / 2.0), (x_c3, y_lb + h_lb / 2.0)], ec="#1F2937", lw=0.75, arrow_end=True)

    # Col 4: Optimality Gate Diamond + Stage 2 Window-Pruned 0-1 ILP
    cx_g, cy_g = 88.8, y_spine
    hw_g, hh_g = 7.9, 6.4
    cv.polygon(
        [(cx_g, cy_g + hh_g), (cx_g + hw_g, cy_g), (cx_g, cy_g - hh_g), (cx_g - hw_g, cy_g)],
        fc=c_gate,
        ec="#1F2937",
        lw=0.75,
        z=3,
    )
    cv.text(cx_g, cy_g + 1.7, "Gate", fs=5.9, bold=True, z=5)
    cv.rich_text(cx_g, cy_g - 1.5, [("L", "i"), ("list", "sub"), (" = ", "r"), ("L", "i"), ("LB", "sub"), ("?", "r")], fs=6.15, z=5)

    # Feed LB (orthogonal top entry) & Stage 1 (straight horizontal entry) into Gate
    cv.polyline([(x_c3 + w_c3, y_lb + h_lb / 2.0), (cx_g, y_lb + h_lb / 2.0), (cx_g, cy_g + hh_g)], ec="#1F2937", lw=0.75, arrow_end=True)
    cv.polyline([(x_c3 + w_c3, cy_g), (cx_g - hw_g, cy_g)], ec="#1F2937", lw=0.75, arrow_end=True)

    # Stage 2: 0-1 ILP below Gate
    x_ilp, w_ilp, y_ilp, h_ilp = 78.3, 21.0, 4.0, 11.2
    draw_box(cv, x_ilp, y_ilp, w_ilp, h_ilp, "", fc=c_periph)
    cv.text(x_ilp + w_ilp / 2.0, y_ilp + 8.7, "Stage 2: 0-1 ILP", fs=6.35, bold=True)
    cv.text(x_ilp + w_ilp / 2.0, y_ilp + 5.4, "ASAP/ALAP Window", fs=5.75)
    cv.text(x_ilp + w_ilp / 2.0, y_ilp + 2.2, "Exact Refinement", fs=5.75, italic=True)

    cv.polyline([(cx_g, cy_g - hh_g), (cx_g, y_ilp + h_ilp)], ec="#1F2937", lw=0.75, arrow_end=True)
    cv.text(cx_g + 1.2, (cy_g - hh_g + y_ilp + h_ilp) / 2.0, "No\n(Gap > 0)", fs=5.55, ha="left", line_gap=1.02)

    # Col 5: 3-bit [slot, e] Prefix Packer (accented with Fig. 1's #FDF0F0 / #B80000!)
    x_pk, w_pk, y_pk, h_pk = 101.2, 11.8, cy_g - 7.7, 15.4
    draw_box(cv, x_pk, y_pk, w_pk, h_pk, "", fc=c_isa_bg, ec=c_isa_fg, lw=0.78)
    cv.text(x_pk + w_pk / 2.0, y_pk + 10.6, "3-bit\nPrefix\nPacker", fs=6.15, bold=True, tc=c_isa_fg, line_gap=1.02)
    cv.text(x_pk + w_pk / 2.0, y_pk + 3.3, "[slot, e]\nNo NOPs", fs=5.5, tc="#111111", line_gap=1.04)

    # Yes -> Prefix Packer; Stage 2 -> Prefix Packer
    cv.polyline([(cx_g + hw_g, cy_g), (x_pk, cy_g)], ec="#1F2937", lw=0.75, arrow_end=True)
    cv.text((cx_g + hw_g + x_pk) / 2.0, cy_g + 2.3, "Yes", fs=5.7, bold=True)
    cv.polyline([(x_ilp + w_ilp, y_ilp + h_ilp / 2.0), (x_pk + w_pk / 2.0, y_ilp + h_ilp / 2.0), (x_pk + w_pk / 2.0, y_pk)], ec="#1F2937", lw=0.75, arrow_end=True)

    # Bottom Diagnostic Feedback Note (Left Zone bottom-left)
    draw_box(cv, 1.8, 4.0, 74.2, 8.6, "", fc="#F8FAFC", ec="#64748B", lw=0.62, dash=(2.0, 1.4))
    cv.rich_text(
        38.9,
        9.8,
        [("Structured Diagnostics: ", "b"), ("S", "i"), ("(", "r"), ("u", "i"), ("), ", "r"), ("d", "sym"), ("(", "r"), ("u, v", "i"), ("), and Gap (", "r"), ("L", "i"), ("list", "sub"), (" - ", "r"), ("L", "i"), ("LB", "sub"), (")", "r")],
        fs=5.95,
    )
    cv.text(38.9, 6.2, "Machine-Verifiable Feedback for Rapid PHY & Agentic Compiler Retargeting", fs=5.65, italic=True, tc="#374151")

    # Bridge from Prefix Packer -> ITCM in Right Zone
    block_arrow_h(cv, x_pk + w_pk + 0.35, 127.85, cy_g, bidir=False, sw=0.82, hw=1.75, hl=1.35)
    cv.text(120.7, cy_g + 4.3, "1-4 Words\n/ Bundle", fs=5.25, bold=True, line_gap=1.04)

    # =========================================================================
    # RIGHT ZONE: Streamlined 4-Slot RV32 VLIW Co-Processor (Mirrors Fig. 2!)
    # =========================================================================
    x_itcm, w_itcm = 128.2, 8.8
    y_hw_bot, y_hw_top = 4.0, 56.2
    draw_box(cv, x_itcm, y_hw_bot, w_itcm, y_hw_top - y_hw_bot, "ITCM\n(Prog.\nMem.)", fc=c_mem, fs=6.2, line_gap=1.10)

    x_hc0 = x_itcm + w_itcm + 3.0
    x_hc1 = 197.8
    w_hc = x_hc1 - x_hc0

    # Fetch & Unpack + VLIW Dispatch
    h_hbar = 4.5
    y_ifd = y_hw_top - h_hbar
    draw_box(cv, x_hc0, y_ifd, w_hc, h_hbar, "Fetch & 3-bit [slot, e] Prefix Unpack", fc=c_front, fs=6.4, bold=True)
    block_arrow_h(cv, x_itcm + w_itcm + 0.22, x_hc0 - 0.22, y_ifd + h_hbar / 2.0, bidir=False, sw=0.65, hw=1.38, hl=1.05)

    y_disp = y_ifd - 2.1 - h_hbar
    draw_box(cv, x_hc0, y_disp, w_hc, h_hbar, "VLIW Dispatch (Idle-Slot NOP Inject)", fc=c_front, fs=6.3, bold=True)
    block_arrow_v(cv, x_hc0 + w_hc / 2.0, y_ifd - 0.18, y_disp + h_hbar + 0.18, bidir=False, sw=0.62, hw=1.35, hl=0.95)

    # 4 Parallel Slots (Slot 0, Slot 1, Slot 2, Slot 3)
    slot_gap = 1.15
    w_slot = (w_hc - 3 * slot_gap) / 4.0
    y_s_top = y_disp - 2.2
    y_s_bot = 18.2
    h_slot = y_s_top - y_s_bot

    slots_cfg = [
        ("Slot 0", ["BJ / SYS", "VALU", "VMOD/ROT"]),
        ("Slot 1", ["SALU", "VSCH/VEI", "VSHF/AGU"]),
        ("Slot 2", ["SLSU", "VLSU", "VMSK/COM"]),
        ("Slot 3", ["SMUL/DIV", "VMUL/DEM", "VCOR/DIV"]),
    ]
    for i, (sname, fu_groups) in enumerate(slots_cfg):
        sx = x_hc0 + i * (w_slot + slot_gap)
        draw_box(cv, sx, y_s_bot, w_slot, h_slot, "", fc=c_slot_bg, z=2)
        cv.text(sx + w_slot / 2.0, y_s_top - 1.9, sname, fs=6.2, bold=True, z=4)
        block_arrow_v(cv, sx + w_slot / 2.0, y_disp - 0.18, y_s_top + 0.18, bidir=False, sw=0.55, hw=1.22, hl=0.88)

        y_rcfu = y_s_top - 3.8 - 3.3
        draw_box(cv, sx, y_rcfu, w_slot, 3.3, "RCFU", fc=c_rcfu, fs=6.1, bold=True, z=3)

        avail = (y_rcfu - 0.7) - (y_s_bot + 0.7)
        g_fu = 0.62
        h_fu = (avail - (len(fu_groups) - 1) * g_fu) / len(fu_groups)
        for j, fg in enumerate(fu_groups):
            fy = (y_rcfu - 0.7) - (j + 1) * h_fu - j * g_fu
            draw_box(cv, sx, fy, w_slot, h_fu, fg, fc=c_fu, fs=5.5, z=3)

    # Streamlined Register Files Bar
    y_rf, h_rf = 11.7, 4.4
    w_srf = w_hc * 0.27
    w_vrf = w_hc * 0.50
    w_mrf = w_hc - w_srf - w_vrf
    draw_box(cv, x_hc0, y_rf, w_srf, h_rf, "16x32b SRF", fc=c_rf, fs=5.9)
    draw_box(cv, x_hc0 + w_srf, y_rf, w_vrf, h_rf, "16x640b Guarded VRF", fc=c_rf, fs=5.9)
    draw_box(cv, x_hc0 + w_srf + w_vrf, y_rf, w_mrf, h_rf, "Mask RF", fc=c_rf, fs=5.8)

    # Bottom Subsystem Row: DTCM | Semaphore | DMA
    h_sub = 5.1
    g_b = 1.0
    w_dtcm = (w_hc - 2 * g_b) * 0.36
    w_sem = (w_hc - 2 * g_b) * 0.33
    w_dma = (w_hc - 2 * g_b) - w_dtcm - w_sem
    x_dtcm = x_hc0
    x_sem = x_dtcm + w_dtcm + g_b
    x_dma = x_sem + w_sem + g_b
    draw_box(cv, x_dtcm, y_hw_bot, w_dtcm, h_sub, "DTCM", fc=c_periph, fs=6.2)
    draw_box(cv, x_sem, y_hw_bot, w_sem, h_sub, "Semaphore", fc=c_periph, fs=6.0)
    draw_box(cv, x_dma, y_hw_bot, w_dma, h_sub, "DMA", fc=c_periph, fs=6.2)

    for bx, bw in [(x_dtcm, w_dtcm), (x_sem, w_sem), (x_dma, w_dma)]:
        block_arrow_v(cv, bx + bw / 2.0, y_hw_bot + h_sub + 0.16, y_rf - 0.16, bidir=True, sw=0.52, hw=1.12, hl=0.72)

    cv.save(Path(__file__).with_name("fig_codesign.pdf"))


if __name__ == "__main__":
    main()
