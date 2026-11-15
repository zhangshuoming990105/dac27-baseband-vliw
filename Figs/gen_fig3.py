"""Generate flat vector PDF for Fig. 3 (Basic SIMD Vector Element Structure)."""
from pathlib import Path
from pdf_canvas import PDFCanvas


def main() -> None:
    cv = PDFCanvas(width_pt=252.0, height_pt=32.0, xlim=100.0, ylim=12.6, pad_pt=1.2)

    x0 = 0.4
    total_w = 99.2
    y_box = 0.8
    h_box = 6.8
    lw = 0.8

    w_gh = total_w * 0.130
    w_gl = total_w * 0.130
    w_hi = (total_w - w_gh - w_gl) / 2.0
    w_lo = w_hi

    segments = [
        (x0, w_gh, "guard.h", "39", "36", "#E3EBF6"),
        (x0 + w_gh, w_gl, "guard.l", "35", "32", "#FDF2D0"),
        (x0 + w_gh + w_gl, w_hi, "high", "31", "16", "#E3EBF6"),
        (x0 + w_gh + w_gl + w_hi, w_lo, "low", "15", "0", "#FDF2D0"),
    ]

    for sx, sw, label, b_hi, b_lo, fc in segments:
        cv.rect(sx, y_box, sw, h_box, fc=fc, ec="#111111", lw=lw, z=2)
        cv.text(sx + sw / 2.0, y_box + h_box / 2.0, label, fs=7.8, bold=False, tc="#111111", z=4)
        pad_l = 1.95 if len(b_hi) == 2 else 1.35
        pad_r = 1.95 if len(b_lo) == 2 else 1.30
        cv.text(sx + pad_l, y_box + h_box + 0.75, b_hi, fs=6.7, va="bottom", z=5)
        cv.text(sx + sw - pad_r, y_box + h_box + 0.75, b_lo, fs=6.7, va="bottom", z=5)

    cv.save(Path(__file__).with_name("fig3_simd.pdf"))


if __name__ == "__main__":
    main()
