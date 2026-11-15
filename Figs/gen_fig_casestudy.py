"""Generate single-column IEEE/DAC vector PDF for Section III-D Case Study (Style B1 unified with Figs 1-4)."""
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
    lw: float = 0.68,
    fs: float = 5.8,
    bold: bool = False,
    tc: str = "#111111",
    dash: tuple[float, float] | None = None,
    line_gap: float = 1.06,
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
    sw: float = 0.72,
    hw: float = 1.55,
    hl: float = 1.25,
    fc: str = "#9CA3AF",
    ec: str = "#374151",
    lw: float = 0.52,
    z: int = 4,
) -> None:
    pts = [
        (x1, yc + sw),
        (x2 - hl, yc + sw),
        (x2 - hl, yc + hw),
        (x2, yc),
        (x2 - hl, yc - hw),
        (x2 - hl, yc - sw),
        (x1, yc - sw),
    ]
    cv.polygon(pts, fc=fc, ec=ec, lw=lw, z=z)


def main() -> None:
    # Exact IEEE single-column width = 252 pt, isotropic 1 unit = 2.50 pt
    cv = PDFCanvas(width_pt=252.0, height_pt=207.0, xlim=100.0, ylim=82.0, pad_pt=1.0)

    # Exact color palette shared with Fig. 1, Fig. 2, Fig. 3, and Fig. 4
    c_mem = "#DFE3E8"
    c_front = "#BBDDFB"
    c_rcfu = "#CFE3B2"
    c_fu = "#7BAEF7"
    c_nop = "#E2E5E9"
    c_gate = "#FDF2D0"
    c_isa_bg = "#FDF0F0"
    c_isa_fg = "#B80000"
    c_dash = "#1D6FA5"

    # =========================================================================
    # PANEL (a): Software-Pipelined Steady-State Loop DAG (|V| = 8)
    # =========================================================================
    ya0, ya1 = 55.2, 81.6
    draw_box(cv, 0.4, ya0, 99.2, ya1 - ya0, fc="none", ec=c_dash, lw=0.75, dash=(2.5, 1.6), z=1)
    cv.rich_text(
        1.8,
        80.6,
        [("(a) Software-Pipelined Loop DAG (|", "b"), ("V", "i"), ("| = 8)", "b")],
        fs=6.3,
        ha="left",
        va="top",
        z=5,
    )

    # Top-right compact legend inside Panel (a)
    draw_box(cv, 57.0, 78.0, 2.6, 2.2, "", fc=c_fu, lw=0.52)
    cv.text(60.2, 79.1, "Excl. FU", fs=5.15, ha="left")
    draw_box(cv, 72.4, 78.0, 2.6, 2.2, "", fc=c_rcfu, lw=0.52)
    cv.text(75.6, 79.1, "4x RCFU", fs=5.15, ha="left")
    cv.hatched_rect(88.8, 78.0, 2.6, 2.2, fc=c_nop, lw=0.52, step_pt=3.2)
    cv.text(92.0, 79.1, "NOP", fs=5.15, ha="left")

    # Nodes y-bands
    yt_n, yb_n, hn = 68.2, 56.4, 7.6

    # Group 1: u2 (VROT), u3 (VSHF) -> u4 (VMUL)
    draw_box(cv, 1.8, yt_n, 14.8, hn, "", fc=c_fu)
    cv.rich_text(9.2, yt_n + 5.3, [("u", "i"), ("2", "sub"), (": VROT", "b")], fs=5.8)
    cv.text(9.2, yt_n + 2.1, "(Slot 0)", fs=5.15)

    draw_box(cv, 17.8, yt_n, 14.8, hn, "", fc=c_fu)
    cv.rich_text(25.2, yt_n + 5.3, [("u", "i"), ("3", "sub"), (": VSHF", "b")], fs=5.8)
    cv.text(25.2, yt_n + 2.1, "(Slot 1)", fs=5.15)

    draw_box(cv, 9.0, yb_n, 16.4, hn, "", fc=c_fu)
    cv.rich_text(17.2, yb_n + 5.3, [("u", "i"), ("4", "sub"), (": VMUL", "b")], fs=5.8)
    cv.text(17.2, yb_n + 2.1, "(Slot 3, 40b)", fs=5.1)

    cv.polyline([(9.2, yt_n), (13.8, yb_n + hn)], ec="#1F2937", lw=0.70, arrow_end=True)
    cv.polyline([(25.2, yt_n), (20.6, yb_n + hn)], ec="#1F2937", lw=0.70, arrow_end=True)
    cv.text(7.2, 66.1, "RAW", fs=5.0, bold=True)
    cv.text(27.2, 66.1, "RAW", fs=5.0, bold=True)

    # Group 2: u1 (VLSU) -> u5 (addi, RCFU)
    draw_box(cv, 34.6, yt_n, 15.2, hn, "", fc=c_fu)
    cv.rich_text(42.2, yt_n + 5.3, [("u", "i"), ("1", "sub"), (": VLSU", "b")], fs=5.8)
    cv.text(42.2, yt_n + 2.1, "(Slot 2)", fs=5.15)

    draw_box(cv, 34.6, yb_n, 15.2, hn, "", fc=c_rcfu)
    cv.rich_text(42.2, yb_n + 5.3, [("u", "i"), ("5", "sub"), (": addi", "b")], fs=5.8)
    cv.text(42.2, yb_n + 2.1, "(RCFU)", fs=5.15)

    cv.polyline([(42.2, yt_n), (42.2, yb_n + hn)], ec="#1F2937", lw=0.70, arrow_end=True)
    cv.text(46.2, 66.1, "WAR", fs=5.0, bold=True)

    # Group 3: u6 (independent RCFU)
    draw_box(cv, 51.8, 59.6, 20.6, 11.4, "", fc=c_rcfu)
    cv.rich_text(62.1, 68.3, [("u", "i"), ("6", "sub"), (": addi", "b")], fs=5.8)
    cv.text(62.1, 65.1, "(4-Slot RCFU)", fs=5.15)
    cv.text(62.1, 61.9, "Indep. ptr (h = 1)", fs=5.0, italic=True, tc="#374151")

    # Group 4: Critical Path highlight around u7 -> u8
    draw_box(cv, 74.2, 55.8, 24.0, 21.4, "", fc=c_gate, ec="#B45309", lw=0.58, dash=(1.8, 1.2), z=2)
    draw_box(cv, 75.8, yt_n, 20.8, hn, "", fc=c_rcfu, ec=c_isa_fg, lw=0.78)
    cv.rich_text(86.2, yt_n + 5.3, [("u", "i"), ("7", "sub"), (": addi", "b")], fs=5.8)
    cv.text(86.2, yt_n + 2.1, "(RCFU, h = 2)", fs=5.1, tc=c_isa_fg, bold=True)

    draw_box(cv, 75.8, yb_n, 20.8, hn, "", fc=c_fu)
    cv.rich_text(86.2, yb_n + 5.3, [("u", "i"), ("8", "sub"), (": BJ", "b")], fs=5.8)
    cv.text(86.2, yb_n + 2.1, "(Slot 0)", fs=5.15)

    cv.polyline([(81.4, yt_n), (81.4, yb_n + hn)], ec=c_isa_fg, lw=0.82, arrow_end=True)
    cv.rich_text(83.2, 66.1, [("RAW (", "b"), ("d", "sym"), ("=1)", "b")], fs=5.05, tc=c_isa_fg, ha="left")

    # =========================================================================
    # PANEL (b): 4-Slot Schedule Comparison (Side-by-Side Grids)
    # =========================================================================
    yb0, yb1 = 24.8, 53.6
    draw_box(cv, 0.4, yb0, 99.2, yb1 - yb0, fc="none", ec=c_dash, lw=0.75, dash=(2.5, 1.6), z=1)
    cv.text(1.8, 52.6, "(b) 4-Slot Schedule & Packing Comparison", fs=6.3, bold=True, ha="left", va="top", z=5)

    # Left Grid: Without RCFU (SALU-Only: 4B, 50%, IPC=2.0)
    gx1 = 1.8
    bw1 = 5.2
    cw1 = 8.65  # total width = 5.2 + 34.6 = 39.8
    cv.text(gx1 + (bw1 + 4 * cw1) / 2.0, 47.6, "No RCFU: 4B, 50% (IPC=2.0)", fs=5.45, bold=True)

    gy_hdr = 42.6
    rh_hdr = 3.3
    rh1 = 3.55
    draw_box(cv, gx1, gy_hdr, bw1, rh_hdr, "", fc=c_mem, lw=0.55)
    for s_i in range(4):
        draw_box(cv, gx1 + bw1 + s_i * cw1, gy_hdr, cw1, rh_hdr, f"S{s_i}", fc=c_front, lw=0.55, fs=5.35, bold=True)

    rows_no_rcfu = [
        ("B1", [("2", c_fu), ("3", c_fu), ("1", c_fu), ("NOP", "nop")]),
        ("B2", [("NOP", "nop"), ("5", c_rcfu), ("NOP", "nop"), ("4", c_fu)]),
        ("B3", [("NOP", "nop"), ("7", c_rcfu), ("NOP", "nop"), ("NOP", "nop")]),
        ("B4", [("8", c_fu), ("6", c_rcfu), ("NOP", "nop"), ("NOP", "nop")]),
    ]
    for r_i, (blbl, cells) in enumerate(rows_no_rcfu):
        ry = gy_hdr - (r_i + 1) * rh1
        draw_box(cv, gx1, ry, bw1, rh1, blbl, fc=c_mem, lw=0.55, fs=5.2, bold=True)
        for c_i, (val, ctype) in enumerate(cells):
            cx = gx1 + bw1 + c_i * cw1
            if ctype == "nop":
                cv.hatched_rect(cx, ry, cw1, rh1, fc=c_nop, ec="#1F2937", lw=0.55, step_pt=3.8, z=2)
                cv.text(cx + cw1 / 2.0, ry + rh1 / 2.0, "NOP", fs=4.85, tc="#4B5563", z=4)
            else:
                draw_box(cv, cx, ry, cw1, rh1, "", fc=ctype, lw=0.55, z=3)
                cv.rich_text(cx + cw1 / 2.0, ry + rh1 / 2.0, [("u", "i"), (val, "sub")], fs=5.6, z=4)

    # Highlight S1 Bottleneck
    draw_box(cv, gx1 + bw1 + cw1, gy_hdr - 4 * rh1, cw1, 4 * rh1, "", fc="none", ec=c_isa_fg, lw=1.15, z=6)
    cv.rich_text(
        gx1 + (bw1 + 4 * cw1) / 2.0,
        26.5,
        [("S1 Bottleneck (|", "b"), ("V", "i"), ("1", "sub"), ("|=4 ", "b"), ("\xae", "sym"), (" 8 NOPs)", "b")],
        fs=5.15,
        tc=c_isa_fg,
    )

    # Center Horizontal Block Arrow
    block_arrow_h(cv, 42.3, 46.5, 36.6)

    # Right Grid: Proposed 4x RCFU + Bound-Guided (2B, 100%, IPC=4.0)
    gx2 = 47.2
    bw2 = 5.0
    cw2 = 11.5  # total width = 5.0 + 46.0 = 51.0 (ends at 98.2)
    cv.text(gx2 + (bw2 + 4 * cw2) / 2.0, 47.6, "Proposed 4x RCFU + Gate: 2B, 100% (IPC=4.0)", fs=5.45, bold=True)

    rh2 = 6.2
    draw_box(cv, gx2, gy_hdr, bw2, rh_hdr, "", fc=c_mem, lw=0.55)
    for s_i in range(4):
        draw_box(cv, gx2 + bw2 + s_i * cw2, gy_hdr, cw2, rh_hdr, f"Slot {s_i}", fc=c_front, lw=0.55, fs=5.35, bold=True)

    rows_opt = [
        ("B1", [("2", "VROT", "[00,0]", c_fu), ("3", "VSHF", "[01,0]", c_fu), ("1", "VLSU", "[10,0]", c_fu), ("7", "RCFU", "[11,1]", c_rcfu)]),
        ("B2", [("8", "BJ", "[00,0]", c_fu), ("6", "RCFU", "[01,0]", c_rcfu), ("5", "RCFU", "[10,0]", c_rcfu), ("4", "VMUL", "[11,1]", c_fu)]),
    ]
    for r_i, (blbl, cells) in enumerate(rows_opt):
        ry = gy_hdr - (r_i + 1) * rh2
        draw_box(cv, gx2, ry, bw2, rh2, blbl, fc=c_mem, lw=0.55, fs=5.3, bold=True)
        for c_i, (uid, fulbl, pfx, col) in enumerate(cells):
            cx = gx2 + bw2 + c_i * cw2
            is_crit = (r_i == 0 and c_i == 3)
            draw_box(cv, cx, ry, cw2, rh2, "", fc=col, ec=(c_isa_fg if is_crit else "#1F2937"), lw=(0.98 if is_crit else 0.58), z=3)
            cv.rich_text(cx + cw2 / 2.0, ry + 4.25, [("u", "i"), (uid, "sub"), (f":{fulbl}", "b")], fs=5.2, z=4)
            cv.text(cx + cw2 / 2.0, ry + 1.55, pfx, fs=5.0, bold=pfx.endswith("1]"), tc=(c_isa_fg if pfx.endswith("1]") else "#1F2937"), z=4)

    cv.rich_text(
        gx2 + (bw2 + 4 * cw2) / 2.0,
        27.4,
        [("Certified Optimal: ", "b"), ("L", "i"), ("list", "sub"), (" = ", "r"), ("L", "i"), ("LB", "sub"), (" = 2 (Zero NOPs)", "b")],
        fs=5.2,
        tc="#1F2937",
    )

    # =========================================================================
    # PANEL (c): Full-Routine 7-Bundle 3-Bit Prefix Compaction
    # =========================================================================
    yc0, yc1 = 0.4, 23.6
    draw_box(cv, 0.4, yc0, 99.2, yc1 - yc0, fc="none", ec=c_dash, lw=0.75, dash=(2.5, 1.6), z=1)
    cv.text(1.8, 22.7, "(c) 7-Bundle Routine 3-Bit [slot, e] Prefix Compaction", fs=6.3, bold=True, ha="left", va="top", z=5)

    bx0 = 26.8
    uw = 2.55  # 28 words * 2.55 = 71.4 (bx0..98.2)
    hb = 5.3

    # Top Strip: Fixed 128b VLIW (28 Words = 112 B)
    yb_top = 11.7
    cv.text(13.6, yb_top + hb / 2.0, "Fixed 128b VLIW\n28 Words (112 B)", fs=5.35, bold=True, line_gap=1.05)
    cv.text(bx0 + 4.0 * uw, 18.2, "Prologue (2B)", fs=4.95)
    cv.text(bx0 + 12.0 * uw, 18.2, "Loop (2B)", fs=4.95)
    cv.text(bx0 + 22.0 * uw, 18.2, "Epilogue (3B)", fs=4.95)

    draw_box(cv, bx0, yb_top, 3 * uw, hb, "3w", fc=c_front, fs=5.2, bold=True)
    cv.hatched_rect(bx0 + 3 * uw, yb_top, 5 * uw, hb, fc=c_nop, lw=0.58, step_pt=3.8)
    cv.text(bx0 + 5.5 * uw, yb_top + hb / 2.0, "5 NOP", fs=5.0, tc="#374151")
    draw_box(cv, bx0 + 8 * uw, yb_top, 8 * uw, hb, "8w Active", fc=c_rcfu, fs=5.3, bold=True)
    draw_box(cv, bx0 + 16 * uw, yb_top, 4 * uw, hb, "4w", fc=c_front, fs=5.2, bold=True)
    cv.hatched_rect(bx0 + 20 * uw, yb_top, 8 * uw, hb, fc=c_nop, lw=0.58, step_pt=3.8)
    cv.text(bx0 + 24 * uw, yb_top + hb / 2.0, "8 NOP", fs=5.1, tc="#374151")

    # Bottom Strip: Proposed 3-Bit Prefix (15 Active Words = 60 B)
    yb_bot = 4.4
    cv.text(13.6, yb_bot + hb / 2.0, "Proposed Prefix\n15 Words (60 B)", fs=5.35, bold=True, tc=c_isa_fg, line_gap=1.05)

    b_segs = [
        (1, "1", c_front),
        (2, "2", c_front),
        (4, "4w", c_rcfu),
        (4, "4w", c_rcfu),
        (2, "2", c_front),
        (1, "1", c_front),
        (1, "1", c_front),
    ]
    cur = 0
    for nw, lbl, col in b_segs:
        draw_box(cv, bx0 + cur * uw, yb_bot, nw * uw, hb, lbl, fc=col, fs=5.1, bold=True)
        cur += nw

    draw_box(
        cv,
        bx0 + 15 * uw,
        yb_bot,
        13 * uw,
        hb,
        "-46.4% Code & Fetch\n(13 NOPs Stripped)",
        fc=c_isa_bg,
        ec=c_isa_fg,
        lw=0.68,
        dash=(2.0, 1.3),
        fs=5.1,
        bold=True,
        tc=c_isa_fg,
        line_gap=1.02,
    )

    cv.text(
        50.0,
        2.1,
        "Hardware dispatch injects idle-slot NOP bubbles dynamically at zero cycle penalty.",
        fs=5.15,
        italic=True,
        tc="#374151",
    )

    cv.save(Path(__file__).with_name("fig_casestudy.pdf"))


if __name__ == "__main__":
    main()
