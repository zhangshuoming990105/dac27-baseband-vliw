"""Generate flat vector PDF for Fig. 2 (Core Architecture Block Diagram)."""
from pathlib import Path
from pdf_canvas import PDFCanvas


def draw_box(cv: PDFCanvas, x, y, w, h, text="", fc="#FFFFFF", ec="#1F2937", lw=0.72, fs=7.2, bold=False, tc="#111111", z=3):
    cv.rect(x, y, w, h, fc=fc, ec=ec, lw=lw, z=z)
    if text:
        cv.text(x + w / 2.0, y + h / 2.0, text, fs=fs, bold=bold, tc=tc, line_gap=1.10, z=z + 1)


def arrow_h(cv: PDFCanvas, x1, x2, yc, bidir=False, sw=0.78, hw=1.70, hl=1.35, fc="#9CA3AF", ec="#374151", lw=0.58, z=4):
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


def arrow_v(cv: PDFCanvas, xc, y1, y2, bidir=False, sw=0.75, hw=1.65, hl=1.20, fc="#9CA3AF", ec="#374151", lw=0.58, z=4):
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
    cv = PDFCanvas(width_pt=252.0, height_pt=164.0, xlim=100.0, ylim=65.2, pad_pt=1.2)

    c_mem = "#DFE3E8"
    c_front = "#BBDDFB"
    c_slot_bg = "#CFE6FC"
    c_rcfu = "#CFE3B2"
    c_fu = "#7BAEF7"
    c_rf = "#B4BAC3"
    c_periph = "#D6D8F7"

    y_mem_bot = 4.6
    y_mem_top = 64.6
    w_mem = 12.2
    x_pmem = 0.3
    x_dmem = 100.0 - 0.3 - w_mem

    draw_box(cv, x_pmem, y_mem_bot, w_mem, y_mem_top - y_mem_bot, "Program\nMemory", fc=c_mem, fs=7.2)
    draw_box(cv, x_dmem, y_mem_bot, w_mem, y_mem_top - y_mem_bot, "Data\nMemory", fc=c_mem, fs=7.2)

    x_c0 = x_pmem + w_mem + 4.7
    x_c1 = x_dmem - 4.7
    w_center = x_c1 - x_c0

    h_bar = 4.25
    y_ifd = y_mem_top - h_bar
    draw_box(cv, x_c0, y_ifd, w_center, h_bar, "Instruction Fetch and Decode", fc=c_front, fs=7.3, bold=True)
    arrow_h(cv, x_pmem + w_mem + 0.3, x_c0 - 0.3, y_ifd + h_bar / 2.0, bidir=False)

    y_disp = y_ifd - 2.35 - h_bar
    draw_box(cv, x_c0, y_disp, w_center, h_bar, "VLIW Dispatch", fc=c_front, fs=7.3, bold=True)
    arrow_v(cv, x_c0 + w_center / 2.0, y_ifd - 0.22, y_disp + h_bar + 0.22, bidir=False, hl=1.05)

    slot_gap = 1.65
    w_slot = (w_center - 3 * slot_gap) / 4.0
    y_slot_top = y_disp - 2.65
    y_slot_bot = 19.5
    h_slot = y_slot_top - y_slot_bot
    h_slot_hdr = 4.0
    h_rcfu = 3.25

    slots = [
        ("Slot 0", ["BJ", "SYS", "VALU", "VMOD", "VROT"]),
        ("Slot 1", ["SALU", "VSCH", "VEI", "VBCT", "VSHF", "VAGU"]),
        ("Slot 3", ["SMUL", "SDIV", "VDIV", "VCOR", "VMUL", "VDEM"]),
        ("Slot 2", ["SLSU", "VLSU", "VMSK", "VCOM"]),
    ]

    for idx, (sname, fus) in enumerate(slots):
        sx = x_c0 + idx * (w_slot + slot_gap)
        draw_box(cv, sx, y_slot_bot, w_slot, h_slot, "", fc=c_slot_bg, z=2)
        cv.text(sx + w_slot / 2.0, y_slot_top - h_slot_hdr / 2.0, sname, fs=7.2, bold=True, z=4)
        arrow_v(cv, sx + w_slot / 2.0, y_disp - 0.22, y_slot_top + 0.22, bidir=False, sw=0.68, hw=1.48, hl=1.10)

        y_rcfu = y_slot_top - h_slot_hdr - h_rcfu
        draw_box(cv, sx, y_rcfu, w_slot, h_rcfu, "RCFU", fc=c_rcfu, fs=6.8, bold=True, z=3)

        pad_t = 0.85
        pad_b = 0.85
        gap_fu = 0.78
        n_fu = len(fus)
        avail_h = (y_rcfu - pad_t) - (y_slot_bot + pad_b)
        h_fu = (avail_h - (n_fu - 1) * gap_fu) / n_fu
        for j, fu_name in enumerate(fus):
            fy = (y_rcfu - pad_t) - (j + 1) * h_fu - j * gap_fu
            draw_box(cv, sx, fy, w_slot, h_fu, fu_name, fc=c_fu, fs=6.7, z=3)
            if sname == "Slot 2" and fu_name == "VLSU":
                arrow_h(cv, sx + w_slot + 0.3, x_dmem - 0.3, fy + h_fu * 0.45, bidir=True, sw=0.72, hw=1.55, hl=1.18)

    h_rf = 3.95
    y_rf = 14.3
    w_srf = w_center * 0.255
    w_vrf = w_center * 0.405
    w_mrf = w_center - w_srf - w_vrf
    draw_box(cv, x_c0, y_rf, w_srf, h_rf, "Scalar RF", fc=c_rf, fs=6.9)
    draw_box(cv, x_c0 + w_srf, y_rf, w_vrf, h_rf, "Vector RF", fc=c_rf, fs=6.9)
    draw_box(cv, x_c0 + w_srf + w_vrf, y_rf, w_mrf, h_rf, "Vector Mask RF", fc=c_rf, fs=6.7)

    y_bot = y_mem_bot
    h_bot = 8.4
    gap_b = 1.2
    w_axi = (w_center - 2 * gap_b) * 0.285
    w_sem = (w_center - 2 * gap_b) * 0.36
    w_dma = (w_center - 2 * gap_b) - w_axi - w_sem

    x_axi = x_c0
    x_sem = x_axi + w_axi + gap_b
    x_dma = x_sem + w_sem + gap_b

    draw_box(cv, x_axi, y_bot, w_axi, h_bot, "AXI Interface", fc=c_periph, fs=6.9)
    draw_box(cv, x_sem, y_bot, w_sem, h_bot, "Semaphore", fc=c_periph, fs=7.0)
    draw_box(cv, x_dma, y_bot, w_dma, h_bot, "DMA", fc=c_periph, fs=7.0)

    arrow_h(cv, x_axi - 0.3, x_pmem + w_mem + 0.3, y_bot + h_bot / 2.0, bidir=False, sw=0.72, hw=1.55, hl=1.25)
    arrow_h(cv, x_dma + w_dma + 0.3, x_dmem - 0.3, y_bot + h_bot / 2.0, bidir=True, sw=0.72, hw=1.55, hl=1.18)

    for bx, bw in [(x_axi, w_axi), (x_sem, w_sem), (x_dma, w_dma)]:
        arrow_v(cv, bx + bw / 2.0, 0.3, y_bot - 0.22, bidir=True, sw=0.68, hw=1.48, hl=1.08)

    cv.save(Path(__file__).with_name("fig2_arch.pdf"))


if __name__ == "__main__":
    main()
