"""Generate flat vector PDF for Fig. 1 (Key ISA Encoding Customizations)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

plt.rcParams["pdf.use14corefonts"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times"]


def main() -> None:
    fig, ax = plt.subplots(figsize=(3.5, 0.87))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 25.0)
    ax.axis("off")

    w_panel = 44.5
    u = w_panel / 7.0
    x_l = 1.5
    x_r = 54.0
    h_box = 5.1
    y_top = 16.7
    y_bot = 4.3
    lw = 0.8

    def draw_box(x, y, w, h, text, fc="#FFFFFF", tc="#000000", bold=False, fs=8.3):
        rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor="#111111", linewidth=lw, zorder=3)
        ax.add_patch(rect)
        ax.text(
            x + w / 2.0,
            y + h / 2.0 - 0.12,
            text,
            ha="center",
            va="center",
            fontsize=fs,
            fontweight=("bold" if bold else "normal"),
            color=tc,
            zorder=4,
        )

    def bit_lbl(x, y, s):
        ax.text(x, y, s, ha="center", va="bottom", fontsize=6.8, color="#111111", zorder=5)

    def draw_down_arrow(xc, y_hi, y_lo):
        sw = 0.72
        hw = 1.60
        ym = y_lo + 1.45
        pts = [
            (xc - sw, y_hi),
            (xc + sw, y_hi),
            (xc + sw, ym),
            (xc + hw, ym),
            (xc, y_lo),
            (xc - hw, ym),
            (xc - sw, ym),
        ]
        ax.add_patch(Polygon(pts, closed=True, facecolor="#1D70B8", edgecolor="none", zorder=4))

    # --- Left Panel: opcode[6:0] -> opcode[6:3] | slot[2:1] | e[0] ---
    draw_box(x_l, y_top, 7 * u, h_box, "opcode", fc="#FFFFFF")
    bit_lbl(x_l + 0.35 * u, y_top + h_box + 0.45, "6")
    bit_lbl(x_l + 6.65 * u, y_top + h_box + 0.45, "0")

    for boundary in (0, 7 * u):
        ax.plot([x_l + boundary, x_l + boundary], [y_bot + h_box, y_top], color="#BCC4CE", lw=0.5, ls="--", zorder=1)

    draw_down_arrow(x_l + 3.5 * u, y_top - 0.55, y_bot + h_box + 3.55)

    draw_box(x_l, y_bot, 4 * u, h_box, "opcode", fc="#FFFFFF")
    draw_box(x_l + 4 * u, y_bot, 2 * u, h_box, "slot", fc="#FDF0F0", tc="#B80000", bold=True)
    draw_box(x_l + 6 * u, y_bot, 1 * u, h_box, "e", fc="#FDF0F0", tc="#B80000", bold=True)

    bit_lbl(x_l + 0.35 * u, y_bot + h_box + 0.4, "6")
    bit_lbl(x_l + 3.62 * u, y_bot + h_box + 0.4, "3")
    bit_lbl(x_l + 4.38 * u, y_bot + h_box + 0.4, "2")
    bit_lbl(x_l + 5.62 * u, y_bot + h_box + 0.4, "1")
    bit_lbl(x_l + 6.50 * u, y_bot + h_box + 0.4, "0")

    # --- Right Panel: funct7[31:25] -> rd2[31:28] | reserved[27:25] ---
    draw_box(x_r, y_top, 7 * u, h_box, "funct7", fc="#FFFFFF")
    bit_lbl(x_r + 0.45 * u, y_top + h_box + 0.45, "31")
    bit_lbl(x_r + 6.55 * u, y_top + h_box + 0.45, "25")

    for boundary in (0, 7 * u):
        ax.plot([x_r + boundary, x_r + boundary], [y_bot + h_box, y_top], color="#BCC4CE", lw=0.5, ls="--", zorder=1)

    draw_down_arrow(x_r + 3.5 * u, y_top - 0.55, y_bot + h_box + 3.55)

    draw_box(x_r, y_bot, 4 * u, h_box, "rd2", fc="#FDF0F0", tc="#B80000", bold=True)
    draw_box(x_r + 4 * u, y_bot, 3 * u, h_box, "reserved", fc="#E2E5E9", tc="#222222", bold=False, fs=7.8)

    bit_lbl(x_r + 0.45 * u, y_bot + h_box + 0.4, "31")
    bit_lbl(x_r + 3.52 * u, y_bot + h_box + 0.4, "28")
    bit_lbl(x_r + 4.48 * u, y_bot + h_box + 0.4, "27")
    bit_lbl(x_r + 6.55 * u, y_bot + h_box + 0.4, "25")

    ax.text(x_l + 3.5 * u, 0.3, "(a) VLIW bundle/slot prefix", ha="center", va="bottom", fontsize=7.2, color="#111111")
    ax.text(x_r + 3.5 * u, 0.3, "(b) Dual-destination R-type field", ha="center", va="bottom", fontsize=7.2, color="#111111")

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out_pdf = Path(__file__).with_name("fig1_isa_mod.pdf")
    fig.savefig(out_pdf, format="pdf", bbox_inches="tight", pad_inches=0.015)


if __name__ == "__main__":
    main()
