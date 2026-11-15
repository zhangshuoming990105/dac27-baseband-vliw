"""Generate flat vector PDF for Fig. 4 (Overview of the Co-Pro-based Baseband SoC)."""
from pathlib import Path
from pdf_canvas import PDFCanvas


def draw_box(cv: PDFCanvas, x, y, w, h, text="", fc="#FFFFFF", ec="#1F2937", lw=0.68, fs=6.0, bold=False, dash=None, z=3):
    cv.rect(x, y, w, h, fc=fc, ec=ec, lw=lw, dash=dash, z=z)
    if text:
        cv.text(x + w / 2.0, y + h / 2.0, text, fs=fs, bold=bold, line_gap=1.08, z=z + 1)


def arrow_h_bi(cv: PDFCanvas, x1, x2, yc, sw=0.58, hw=1.28, hl=0.92, fc="#A3AAB4", ec="#374151", lw=0.52, z=4):
    lo, hi = (x1, x2) if x1 < x2 else (x2, x1)
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
    cv.polygon(pts, fc=fc, ec=ec, lw=lw, z=z)


def arrow_v_bi(cv: PDFCanvas, xc, y1, y2, sw=0.58, hw=1.28, hl=0.92, fc="#A3AAB4", ec="#374151", lw=0.52, z=4):
    lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
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
    cv.polygon(pts, fc=fc, ec=ec, lw=lw, z=z)


def main() -> None:
    cv = PDFCanvas(width_pt=252.0, height_pt=178.0, xlim=100.0, ylim=70.6, pad_pt=1.2)

    c_bus = "#C4C9D0"
    c_mod = "#CBE4F2"
    c_copro = "#8FC1F9"
    c_dash = "#1D6FA5"

    # Top External Memories: DDR | SPI Nor | BootROM
    y_top_mem = 64.4
    h_top_mem = 5.8
    x_bus0 = 28.0
    w_bus = 54.6  # [28.0, 82.6]

    draw_box(cv, 28.0, y_top_mem, 9.4, h_top_mem, "DDR", fc=c_mod, fs=6.2)
    draw_box(cv, 49.8, y_top_mem, 10.6, h_top_mem, "SPI Nor", fc=c_mod, fs=6.2)
    draw_box(cv, 70.0, y_top_mem, 12.6, h_top_mem, "BootROM", fc=c_mod, fs=6.2)

    # AXI-Share
    y_axishare = 56.6
    h_hbar = 4.2
    draw_box(cv, x_bus0, y_axishare, w_bus, h_hbar, "AXI-Share", fc=c_bus, fs=6.5, bold=True)

    for xc in (28.0 + 4.7, 49.8 + 5.3, 70.0 + 6.3):
        arrow_v_bi(cv, xc, y_axishare + h_hbar + 0.22, y_top_mem - 0.22)

    # Dashed Subsystem Enclosures
    y_sub_bot = 15.2
    y_sub_top = 53.2
    h_sub = y_sub_top - y_sub_bot
    x_mid = 55.4

    draw_box(cv, 0.3, y_sub_bot, x_mid - 0.3, h_sub, "", fc="none", ec=c_dash, lw=0.75, dash=(2.4, 1.6), z=2)
    draw_box(cv, x_mid, y_sub_bot, 99.7 - x_mid, h_sub, "", fc="none", ec=c_dash, lw=0.75, dash=(2.4, 1.6), z=2)

    # Labels positioned cleanly inside open corners
    cv.text(1.4, y_sub_top - 2.0, "PHY-Subsystem", fs=5.5, bold=True, ha="left", va="top", z=5)
    cv.text(98.5, y_sub_top - 2.0, "PS-Subsystem", fs=5.5, bold=True, ha="right", va="top", z=5)

    # Vertical Bus Bars: AXI-PHY and AXI-PS
    y_vbus_bot = 16.4
    y_vbus_top = 51.8
    h_vbus = y_vbus_top - y_vbus_bot
    w_vbus = 6.6
    x_axiphy = 28.4
    x_axips = 75.4

    draw_box(cv, x_axiphy, y_vbus_bot, w_vbus, h_vbus, "AXI-\nPHY", fc=c_bus, fs=6.2, bold=True)
    draw_box(cv, x_axips, y_vbus_bot, w_vbus, h_vbus, "AXI-\nPS", fc=c_bus, fs=6.2, bold=True)

    arrow_v_bi(cv, x_axiphy + w_vbus / 2.0, y_vbus_top + 0.22, y_axishare - 0.22)
    arrow_v_bi(cv, x_axips + w_vbus / 2.0, y_vbus_top + 0.22, y_axishare - 0.22)

    # PHY-Subsystem internals
    draw_box(cv, 18.0, 45.6, 6.6, 6.2, "L1C-\nCPU", fc=c_mod, fs=5.9)
    arrow_h_bi(cv, 18.0 + 6.6 + 0.2, x_axiphy - 0.2, 45.6 + 3.1)

    x_xbar = 18.0
    w_xbar = 6.6
    draw_box(cv, x_xbar, 24.4, w_xbar, 43.6 - 24.4, "AXI\nCross\nBar", fc=c_bus, fs=5.9)
    arrow_h_bi(cv, x_xbar + w_xbar + 0.2, x_axiphy - 0.2, 34.0)

    copro_w = 12.6
    copro_h = 5.5
    copro_x = 1.6
    for idx, cy in enumerate([38.1, 31.25, 24.4]):
        draw_box(cv, copro_x, cy, copro_w, copro_h, f"Co-Pro#{idx}", fc=c_copro, fs=6.1, bold=True)
        arrow_h_bi(cv, copro_x + copro_w + 0.2, x_xbar - 0.2, cy + copro_h / 2.0)

    draw_box(cv, 12.0, 16.4, 12.6, 5.9, "DFE", fc=c_mod, fs=6.2)
    arrow_h_bi(cv, 12.0 + 12.6 + 0.2, x_axiphy - 0.2, 16.4 + 2.95)

    x_phy_r = 38.8
    w_mod = 13.4
    for by, bh, btxt in [(45.6, 6.2, "DMA-PHY"), (31.1, 5.9, "Local\nMemory"), (16.4, 5.9, "ASIC-ACCs")]:
        draw_box(cv, x_phy_r, by, w_mod, bh, btxt, fc=c_mod, fs=6.0)
        arrow_h_bi(cv, x_axiphy + w_vbus + 0.2, x_phy_r - 0.2, by + bh / 2.0)

    # PS-Subsystem internals
    x_ps_l = 58.2
    for by, bh, btxt in [(45.6, 6.2, "DMA-PS"), (31.1, 5.9, "Local\nMemory"), (16.4, 5.9, "ASIC-ACCs")]:
        draw_box(cv, x_ps_l, by, w_mod, bh, btxt, fc=c_mod, fs=6.0)
        arrow_h_bi(cv, x_ps_l + w_mod + 0.2, x_axips - 0.2, by + bh / 2.0)

    draw_box(cv, 85.8, 41.2, 7.2, 6.2, "PS-\nCPU", fc=c_mod, fs=5.9)
    arrow_h_bi(cv, x_axips + w_vbus + 0.2, 85.8 - 0.2, 41.2 + 3.1)

    draw_box(cv, 85.8, 31.1, 12.4, 5.9, "USB", fc=c_mod, fs=6.2)
    arrow_h_bi(cv, x_axips + w_vbus + 0.2, 85.8 - 0.2, 31.1 + 2.95)

    draw_box(cv, 85.8, 16.4, 12.4, 5.9, "SDIO", fc=c_mod, fs=6.2)
    arrow_h_bi(cv, x_axips + w_vbus + 0.2, 85.8 - 0.2, 16.4 + 2.95)

    # APB Bus & Peripherals
    y_apb = 8.8
    draw_box(cv, x_bus0, y_apb, w_bus, h_hbar, "APB", fc=c_bus, fs=6.5, bold=True)
    arrow_v_bi(cv, x_axiphy + w_vbus / 2.0, y_apb + h_hbar + 0.22, y_vbus_bot - 0.22)
    arrow_v_bi(cv, x_axips + w_vbus / 2.0, y_apb + h_hbar + 0.22, y_vbus_bot - 0.22)

    periphs = ["Timers", "GPIO", "UART", "INTC", "PMU"]
    w_p = 8.8
    h_p = 5.0
    y_p = 0.4
    gap_p = (w_bus - len(periphs) * w_p) / (len(periphs) - 1)
    for i, pname in enumerate(periphs):
        px = x_bus0 + i * (w_p + gap_p)
        draw_box(cv, px, y_p, w_p, h_p, pname, fc=c_mod, fs=6.1)
        arrow_v_bi(cv, px + w_p / 2.0, y_p + h_p + 0.22, y_apb - 0.22)

    cv.save(Path(__file__).with_name("fig4_soc.pdf"))


if __name__ == "__main__":
    main()
