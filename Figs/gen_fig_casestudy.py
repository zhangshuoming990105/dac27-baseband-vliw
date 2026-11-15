"""Generate flat IEEE/DAC vector PDF for Section III-D Case Study (Style B1 unified with Figs 1-4)."""
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
    lw: float = 0.70,
    fs: float = 6.3,
    bold: bool = False,
    tc: str = "#111111",
    dash: tuple[float, float] | None = None,
    line_gap: float = 1.08,
    z: int = 3,
) -> None:
    cv.rect(x, y, w, h, fc=fc, ec=ec, lw=lw, dash=dash, z=z)
    if text:
        cv.text(x + w / 2.0, y + h / 2.0, text, fs=fs, bold=bold, tc=tc, line_gap=line_gap, z=z + 1)


def block_arrow_v(
    cv: PDFCanvas,
    xc: float,
    y1: float,
    y2: float,
    sw: float = 0.68,
    hw: float = 1.48,
    hl: float = 1.05,
    fc: str = "#9CA3AF",
    ec: str = "#374151",
    lw: float = 0.55,
    z: int = 4,
) -> None:
    pts = [
        (xc - sw, y1),
        (xc + sw, y1),
        (xc + sw, y2 + hl),
        (xc + hw, y2 + hl),
        (xc, y2),
        (xc - hw, y2 + hl),
        (xc - sw, y2 + hl),
    ]
    cv.polygon(pts, fc=fc, ec=ec, lw=lw, z=z)


def main() -> None:
    cv = PDFCanvas(width_pt=516.0, height_pt=160.0, xlim=200.0, ylim=62.0, pad_pt=1.2)

    # Exact color palette shared with Fig. 1, Fig. 2, Fig. 3, and Fig. 4
    c_front = "#BBDDFB"
    c_slot_bg = "#CFE6FC"
    c_rcfu = "#CFE3B2"
    c_fu = "#7BAEF7"
    c_nop = "#E2E5E9"
    c_gate = "#FDF2D0"
    c_isa_bg = "#FDF0F0"
    c_isa_fg = "#B80000"
    c_dash = "#1D6FA5"

    y_pbot = 5.4
    y_ptop = 61.2
    h_pan = y_ptop - y_pbot

    # Panel X ranges
    xa0, xa1 = 0.5, 61.5
    xb0, xb1 = 64.2, 134.8
    xc0, xc1 = 137.5, 199.5

    for x0, x1 in [(xa0, xa1), (xb0, xb1), (xc0, xc1)]:
        draw_box(cv, x0, y_pbot, x1 - x0, h_pan, fc="none", ec=c_dash, lw=0.75, dash=(2.6, 1.7), z=1)

    # IEEE Fig. 1-style bottom subcaptions
    cv.rich_text((xa0 + xa1) / 2.0, 2.1, [("(a) Software-pipelined loop DAG (|", "r"), ("V", "i"), ("| = 8)", "r")], fs=7.1)
    cv.text((xb0 + xb1) / 2.0, 2.1, "(b) 4-slot schedule & packing comparison", fs=7.1)
    cv.text((xc0 + xc1) / 2.0, 2.1, "(c) 7-bundle routine prefix compaction", fs=7.1)

    # =========================================================================
    # PANEL (a): Software-Pipelined Loop DAG (|V| = 8)
    # =========================================================================
    # Critical path highlight frame behind u7 -> u8
    draw_box(cv, 44.5, 11.8, 15.2, 46.8, "", fc=c_gate, ec="#B45309", lw=0.62, dash=(2.0, 1.3), z=2)
    cv.text(52.1, 56.8, "Critical Path", fs=5.8, bold=True, tc="#92400E", z=4)

    cv.text(14.8, 56.8, "Vector Compute", fs=5.9, bold=True, tc="#1F2937")
    cv.text(35.6, 56.8, "Mem & Ptr", fs=5.9, bold=True, tc="#1F2937")

    # Nodes u2, u3 -> u4
    w_n, h_n = 12.2, 10.6
    y_top_n = 43.2
    y_mid_n = 24.4

    # u2: VROT (Slot 0)
    draw_box(cv, 2.2, y_top_n, w_n, h_n, "", fc=c_fu)
    cv.rich_text(2.2 + w_n / 2.0, y_top_n + 7.6, [("u", "i"), ("2", "sub"), (": VROT", "b")], fs=6.2)
    cv.text(2.2 + w_n / 2.0, y_top_n + 3.1, "(Slot 0)", fs=5.7)

    # u3: VSHF (Slot 1)
    draw_box(cv, 15.6, y_top_n, w_n, h_n, "", fc=c_fu)
    cv.rich_text(15.6 + w_n / 2.0, y_top_n + 7.6, [("u", "i"), ("3", "sub"), (": VSHF", "b")], fs=6.2)
    cv.text(15.6 + w_n / 2.0, y_top_n + 3.1, "(Slot 1)", fs=5.7)

    # u4: VMUL (Slot 3)
    x_u4 = 8.4
    w_u4 = 13.2
    draw_box(cv, x_u4, y_mid_n, w_u4, h_n, "", fc=c_fu)
    cv.rich_text(x_u4 + w_u4 / 2.0, y_mid_n + 7.6, [("u", "i"), ("4", "sub"), (": VMUL", "b")], fs=6.2)
    cv.text(x_u4 + w_u4 / 2.0, y_mid_n + 3.1, "(Slot 3)", fs=5.7)

    cv.polyline([(2.2 + w_n / 2.0, y_top_n), (x_u4 + 3.6, y_mid_n + h_n)], ec="#1F2937", lw=0.75, arrow_end=True)
    cv.polyline([(15.6 + w_n / 2.0, y_top_n), (x_u4 + w_u4 - 3.6, y_mid_n + h_n)], ec="#1F2937", lw=0.75, arrow_end=True)
    cv.text(6.6, 39.0, "RAW", fs=5.5, bold=True)
    cv.text(23.2, 39.0, "RAW", fs=5.5, bold=True)

    # u1: VLSU (Slot 2) -> u5: addi (RCFU)
    x_u1 = 29.5
    draw_box(cv, x_u1, y_top_n, w_n, h_n, "", fc=c_fu)
    cv.rich_text(x_u1 + w_n / 2.0, y_top_n + 7.6, [("u", "i"), ("1", "sub"), (": VLSU", "b")], fs=6.2)
    cv.text(x_u1 + w_n / 2.0, y_top_n + 3.1, "(Slot 2)", fs=5.7)

    draw_box(cv, x_u1, y_mid_n, w_n, h_n, "", fc=c_rcfu)
    cv.rich_text(x_u1 + w_n / 2.0, y_mid_n + 7.6, [("u", "i"), ("5", "sub"), (": addi", "b")], fs=6.2)
    cv.text(x_u1 + w_n / 2.0, y_mid_n + 3.1, "(RCFU)", fs=5.7)

    cv.polyline([(x_u1 + w_n / 2.0, y_top_n), (x_u1 + w_n / 2.0, y_mid_n + h_n)], ec="#1F2937", lw=0.75, arrow_end=True)
    cv.text(x_u1 + w_n / 2.0 + 3.8, 39.0, "WAR", fs=5.5, bold=True)

    # u6: addi (RCFU, independent)
    draw_box(cv, 3.0, 11.8, 38.5, 8.6, "", fc=c_rcfu)
    cv.rich_text(22.25, 17.7, [("u", "i"), ("6", "sub"), (": addi (RCFU)", "b")], fs=6.2)
    cv.text(22.25, 13.9, "Indep. phasor ptr update (h = 1)", fs=5.6, tc="#1F2937")

    # u7: addi (RCFU) -> u8: BJ (Slot 0)
    x_u7 = 46.0
    draw_box(cv, x_u7, y_top_n, w_n, h_n, "", fc=c_rcfu, ec=c_isa_fg, lw=0.80)
    cv.rich_text(x_u7 + w_n / 2.0, y_top_n + 7.6, [("u", "i"), ("7", "sub"), (": addi", "b")], fs=6.2)
    cv.text(x_u7 + w_n / 2.0, y_top_n + 3.1, "(RCFU, h=2)", fs=5.5, tc=c_isa_fg)

    draw_box(cv, x_u7, 13.4, w_n, h_n, "", fc=c_fu)
    cv.rich_text(x_u7 + w_n / 2.0, 13.4 + 7.6, [("u", "i"), ("8", "sub"), (": BJ", "b")], fs=6.2)
    cv.text(x_u7 + w_n / 2.0, 13.4 + 3.1, "(Slot 0)", fs=5.7)

    cv.polyline([(x_u7 + w_n / 2.0, y_top_n), (x_u7 + w_n / 2.0, 13.4 + h_n)], ec=c_isa_fg, lw=0.88, arrow_end=True)
    draw_box(cv, 46.4, 30.8, 11.4, 5.8, "", fc=c_isa_bg, ec=c_isa_fg, lw=0.58, z=5)
    cv.text(52.1, 34.8, "RAW", fs=5.5, bold=True, tc=c_isa_fg, z=6)
    cv.rich_text(52.1, 32.1, [("(", "r"), ("d", "sym"), (" = 1)", "r")], fs=5.5, tc=c_isa_fg, z=6)

    # Mini Legend at bottom of Panel (a)
    draw_box(cv, 3.0, 6.8, 3.2, 2.8, "", fc=c_fu, lw=0.55)
    cv.text(7.0, 8.2, "Exclusive FU", fs=5.5, ha="left")
    draw_box(cv, 24.5, 6.8, 3.2, 2.8, "", fc=c_rcfu, lw=0.55)
    cv.text(28.5, 8.2, "4-Slot RCFU", fs=5.5, ha="left")
    cv.hatched_rect(45.2, 6.8, 3.2, 2.8, fc=c_nop, lw=0.55, step_pt=3.6)
    cv.text(49.2, 8.2, "NOP", fs=5.5, ha="left")

    # =========================================================================
    # PANEL (b): 4-Slot Schedule Comparison
    # =========================================================================
    cv.text((xb0 + xb1) / 2.0, 58.7, "Without RCFU (SALU-Only): 4 Bundles, 50% (IPC=2.0)", fs=5.95, bold=True)

    bw_lbl = 6.2
    cw = 14.6
    gx0 = xb0 + (xb1 - xb0 - (bw_lbl + 4 * cw)) / 2.0 + bw_lbl
    rh_hdr = 3.6
    rh1 = 4.35
    gy1_top = 52.8

    draw_box(cv, gx0 - bw_lbl, gy1_top, bw_lbl, rh_hdr, "", fc="#DFE3E8", lw=0.60, z=3)
    for s_idx in range(4):
        draw_box(cv, gx0 + s_idx * cw, gy1_top, cw, rh_hdr, f"Slot {s_idx}", fc=c_front, lw=0.60, fs=5.7, bold=True, z=3)

    rows_no_rcfu = [
        ("B1", [("u2", c_fu), ("u3", c_fu), ("u1", c_fu), ("NOP", "nop")]),
        ("B2", [("NOP", "nop"), ("u5", c_rcfu), ("NOP", "nop"), ("u4", c_fu)]),
        ("B3", [("NOP", "nop"), ("u7", c_rcfu), ("NOP", "nop"), ("NOP", "nop")]),
        ("B4", [("u8", c_fu), ("u6", c_rcfu), ("NOP", "nop"), ("NOP", "nop")]),
    ]
    for r_i, (b_lbl, cells) in enumerate(rows_no_rcfu):
        ry = gy1_top - (r_i + 1) * rh1
        draw_box(cv, gx0 - bw_lbl, ry, bw_lbl, rh1, b_lbl, fc="#DFE3E8", lw=0.60, fs=5.6, bold=True, z=3)
        for c_i, (ctxt, ctype) in enumerate(cells):
            cx = gx0 + c_i * cw
            if ctype == "nop":
                cv.hatched_rect(cx, ry, cw, rh1, fc=c_nop, ec="#1F2937", lw=0.60, step_pt=4.5, z=2)
                cv.text(cx + cw / 2.0, ry + rh1 / 2.0, "NOP", fs=5.4, tc="#4B5563", z=4)
            else:
                draw_box(cv, cx, ry, cw, rh1, "", fc=ctype, lw=0.60, z=3)
                cv.rich_text(cx + cw / 2.0, ry + rh1 / 2.0, [("u", "i"), (ctxt[1:], "sub")], fs=6.1, z=4)

    # Highlight Slot 1 Bottleneck with Fig. 1 crimson border
    draw_box(cv, gx0 + cw, gy1_top - 4 * rh1, cw, 4 * rh1, "", fc="none", ec=c_isa_fg, lw=1.25, z=6)
    cv.rich_text(
        (xb0 + xb1) / 2.0,
        32.7,
        [("Slot 1 Bottleneck (|", "b"), ("V", "i"), ("1", "sub"), ("| = 4 ", "b"), ("\xae", "sym"), (" 8 Idle NOP Slots)", "b")],
        fs=5.65,
        tc=c_isa_fg,
    )

    block_arrow_v(cv, (xb0 + xb1) / 2.0, 31.0, 27.5)

    # Proposed 2-Bundle Schedule Box
    cv.text((xb0 + xb1) / 2.0, 25.4, "Proposed 4x RCFU + Bound-Guided: 2 Bundles, 100% (IPC=4.0)", fs=5.9, bold=True)
    gy2_top = 19.8
    rh2 = 6.3
    draw_box(cv, gx0 - bw_lbl, gy2_top, bw_lbl, rh_hdr, "", fc="#DFE3E8", lw=0.60, z=3)
    for s_idx in range(4):
        draw_box(cv, gx0 + s_idx * cw, gy2_top, cw, rh_hdr, f"Slot {s_idx}", fc=c_front, lw=0.60, fs=5.7, bold=True, z=3)

    rows_opt = [
        ("B1", [("2", "VROT", "[00,0]", c_fu), ("3", "VSHF", "[01,0]", c_fu), ("1", "VLSU", "[10,0]", c_fu), ("7", "RCFU", "[11,1]", c_rcfu)]),
        ("B2", [("8", "BJ", "[00,0]", c_fu), ("6", "RCFU", "[01,0]", c_rcfu), ("5", "RCFU", "[10,0]", c_rcfu), ("4", "VMUL", "[11,1]", c_fu)]),
    ]
    for r_i, (b_lbl, cells) in enumerate(rows_opt):
        ry = gy2_top - (r_i + 1) * rh2
        draw_box(cv, gx0 - bw_lbl, ry, bw_lbl, rh2, b_lbl, fc="#DFE3E8", lw=0.60, fs=5.7, bold=True, z=3)
        for c_i, (uid, fu_lbl, pfx, fc_cell) in enumerate(cells):
            cx = gx0 + c_i * cw
            is_crit = (r_i == 0 and c_i == 3)
            draw_box(cv, cx, ry, cw, rh2, "", fc=fc_cell, ec=(c_isa_fg if is_crit else "#1F2937"), lw=(1.05 if is_crit else 0.65), z=3)
            cv.rich_text(cx + cw / 2.0, ry + 4.3, [("u", "i"), (uid, "sub"), (f": {fu_lbl}", "b")], fs=5.6, z=4)
            cv.text(cx + cw / 2.0, ry + 1.55, pfx, fs=5.35, bold=(pfx.endswith("1]")), tc=(c_isa_fg if pfx.endswith("1]") else "#1F2937"), z=4)

    # =========================================================================
    # PANEL (c): Full-Routine Code Compaction (7 Bundles)
    # =========================================================================
    bx0 = xc0 + 3.0
    bw_tot = (xc1 - xc0) - 6.0  # 56.0 units = 28 words (2.0 units / word!)
    uw = bw_tot / 28.0

    # Top Strip: Fixed 128-bit VLIW (28 Words = 112 B)
    cv.text((xc0 + xc1) / 2.0, 57.8, "Fixed 128-bit VLIW: 28 Words (112 B)", fs=6.2, bold=True)
    cv.text(bx0 + 4.0 * uw, 53.6, "Prologue (2B)", fs=5.6)
    cv.text(bx0 + 12.0 * uw, 53.6, "Loop (2B)", fs=5.6)
    cv.text(bx0 + 22.0 * uw, 53.6, "Epilogue (3B)", fs=5.6)

    yb1, hb = 43.8, 7.8
    # Prologue: 3w active + 5w NOP
    draw_box(cv, bx0, yb1, 3 * uw, hb, "3w", fc=c_front, fs=6.0, bold=True)
    cv.hatched_rect(bx0 + 3 * uw, yb1, 5 * uw, hb, fc=c_nop, lw=0.65, step_pt=4.5)
    cv.text(bx0 + 5.5 * uw, yb1 + hb / 2.0, "5 NOP", fs=5.6, tc="#374151")
    # Loop: 8w active
    draw_box(cv, bx0 + 8 * uw, yb1, 8 * uw, hb, "8w Active", fc=c_rcfu, fs=6.0, bold=True)
    # Epilogue: 4w active + 8w NOP
    draw_box(cv, bx0 + 16 * uw, yb1, 4 * uw, hb, "4w", fc=c_front, fs=6.0, bold=True)
    cv.hatched_rect(bx0 + 20 * uw, yb1, 8 * uw, hb, fc=c_nop, lw=0.65, step_pt=4.5)
    cv.text(bx0 + 24 * uw, yb1 + hb / 2.0, "8 NOP", fs=5.8, tc="#374151")

    draw_box(cv, bx0 + 5.0, 36.2, bw_tot - 10.0, 5.2, "13 Mandatory NOP Words (46.4% Waste)", fc=c_nop, ec="#4B5563", lw=0.60, fs=5.7, bold=True)

    block_arrow_v(cv, (xc0 + xc1) / 2.0, 34.8, 31.2)

    # Bottom Strip: Proposed 3-bit [slot, e] Prefix (15 Active Words = 60 B)
    cv.text((xc0 + xc1) / 2.0, 28.8, "Proposed 3-bit Prefix: 15 Active Words (60 B)", fs=6.1, bold=True)
    cv.text(bx0, 24.8, "Prologue (3w) | Loop (8w) | Epilogue (4w)", fs=5.4, ha="left")

    yb2 = 15.0
    # Show exact 7 bundles: 1 + 2 | 4 + 4 | 2 + 1 + 1 = 15 words
    b_segs = [
        (1, "1", c_front),
        (2, "2", c_front),
        (4, "4w", c_rcfu),
        (4, "4w", c_rcfu),
        (2, "2", c_front),
        (1, "1", c_front),
        (1, "1", c_front),
    ]
    cur_w = 0
    for nw, lbl, col in b_segs:
        draw_box(cv, bx0 + cur_w * uw, yb2, nw * uw, hb, lbl, fc=col, fs=5.6, bold=True)
        cur_w += nw

    # Saved 13-word region highlighted in Fig. 1 rose/crimson dashed box
    draw_box(
        cv,
        bx0 + 15 * uw,
        yb2,
        13 * uw,
        hb,
        "-46.4%\nCode & Fetch",
        fc=c_isa_bg,
        ec=c_isa_fg,
        lw=0.75,
        dash=(2.2, 1.4),
        fs=5.9,
        bold=True,
        tc=c_isa_fg,
        line_gap=1.05,
    )

    cv.text(
        (xc0 + xc1) / 2.0,
        9.8,
        "Hardware dispatch injects idle-slot bubbles\ndynamically at zero cycle penalty.",
        fs=5.65,
        italic=True,
        tc="#1F2937",
        line_gap=1.08,
    )

    cv.save(Path(__file__).with_name("fig_casestudy.pdf"))


if __name__ == "__main__":
    main()
