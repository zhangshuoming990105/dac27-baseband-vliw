"""Zero-dependency pure PDF-1.4 vector canvas using Core-14 Type-1 Times fonts."""
from __future__ import annotations
from pathlib import Path
import math
import subprocess
import zlib


def _load_afm_widths(afm_name: str, default_w: float = 500.0) -> dict[str, float]:
    widths: dict[str, float] = {}
    try:
        afm_path = subprocess.check_output(["kpsewhich", afm_name], text=True).strip()
        if afm_path and Path(afm_path).is_file():
            for line in Path(afm_path).read_text(encoding="latin-1").splitlines():
                if line.startswith("C ") and " ; WX " in line and " ; N " in line:
                    parts = [p.strip() for p in line.split(";")]
                    c_code = int(parts[0].split()[1])
                    wx = float(parts[1].split()[1])
                    if 32 <= c_code <= 126:
                        widths[chr(c_code)] = wx
    except Exception:
        pass
    if not widths:
        for ch in "il.,:;|! ":
            widths[ch] = 250.0
        for ch in "frt()-I1":
            widths[ch] = 350.0
        for ch in "acegmnopsuvz023456789#":
            widths[ch] = 480.0
        for ch in "bdhkqxyABCEFGKLPQRSTUVXYZ":
            widths[ch] = 620.0
        for ch in "DHNOwMW":
            widths[ch] = 760.0
    widths.setdefault(" ", default_w * 0.5)
    return widths


_W_ROMAN = _load_afm_widths("utmr8a.afm", 500.0)
_W_BOLD = _load_afm_widths("utmb8a.afm", 530.0)
_W_ITALIC = _load_afm_widths("utmri8a.afm", 500.0)


def _hex_rgb(c: str) -> tuple[float, float, float]:
    h = c.lstrip("#")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def _pdf_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class PDFCanvas:
    """Lightweight coordinate-mapped PDF-1.4 vector builder."""

    def __init__(self, width_pt: float, height_pt: float, xlim: float = 100.0, ylim: float = 100.0, pad_pt: float = 1.2):
        self.pad_pt = pad_pt
        self.inner_w = width_pt - 2 * pad_pt
        self.inner_h = height_pt - 2 * pad_pt
        self.width_pt = width_pt
        self.height_pt = height_pt
        self.sx = self.inner_w / xlim
        self.sy = self.inner_h / ylim
        self.layers: dict[int, list[str]] = {}

    def _px(self, x: float) -> float:
        return self.pad_pt + x * self.sx

    def _py(self, y: float) -> float:
        return self.pad_pt + y * self.sy

    def _add(self, z: int, cmd: str) -> None:
        self.layers.setdefault(z, []).append(cmd)

    def text_width_pt(self, s: str, fs: float, bold: bool = False, italic: bool = False, symbol: bool = False) -> float:
        if symbol:
            sym_w = {"\xae": 0.99, "\xa3": 0.55, "d": 0.50}
            return sum(sym_w.get(ch, 0.55) * fs for ch in s)
        tbl = _W_BOLD if bold else (_W_ITALIC if italic else _W_ROMAN)
        return sum(tbl.get(ch, 520.0) for ch in s) * fs / 1000.0

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fc: str | None = "#FFFFFF",
        ec: str | None = "#111111",
        lw: float = 0.75,
        dash: tuple[float, float] | None = None,
        z: int = 2,
    ) -> None:
        px, py = self._px(x), self._py(y)
        pw, ph = w * self.sx, h * self.sy
        ops = ["q", f"{lw:.3f} w", "0 J 0 j"]
        if dash is not None:
            ops.append(f"[{dash[0]:.2f} {dash[1]:.2f}] 0 d")
        else:
            ops.append("[] 0 d")
        has_f = fc is not None and fc != "none"
        has_s = ec is not None and ec != "none" and lw > 0
        if has_f:
            r, g, b = _hex_rgb(fc)  # type: ignore[arg-type]
            ops.append(f"{r:.4f} {g:.4f} {b:.4f} rg")
        if has_s:
            r, g, b = _hex_rgb(ec)  # type: ignore[arg-type]
            ops.append(f"{r:.4f} {g:.4f} {b:.4f} RG")
        paint = "B" if (has_f and has_s) else ("f" if has_f else "S")
        ops.append(f"{px:.3f} {py:.3f} {pw:.3f} {ph:.3f} re {paint}")
        ops.append("Q")
        self._add(z, "\n".join(ops))

    def hatched_rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fc: str = "#E2E5E9",
        ec: str = "#1F2937",
        hatch_c: str = "#B8C0CC",
        lw: float = 0.65,
        step_pt: float = 5.0,
        z: int = 2,
    ) -> None:
        self.rect(x, y, w, h, fc=fc, ec="none", lw=0, z=z)
        px, py = self._px(x), self._py(y)
        pw, ph = w * self.sx, h * self.sy
        r, g, b = _hex_rgb(hatch_c)
        ops = [
            "q",
            f"{px:.3f} {py:.3f} {pw:.3f} {ph:.3f} re W n",
            "0.48 w",
            f"{r:.4f} {g:.4f} {b:.4f} RG",
        ]
        d = -ph
        while d <= pw + ph:
            ops.append(f"{px + d:.3f} {py:.3f} m {px + d + ph:.3f} {py + ph:.3f} l S")
            d += step_pt
        ops.append("Q")
        self._add(z, "\n".join(ops))
        if ec and ec != "none" and lw > 0:
            self.rect(x, y, w, h, fc="none", ec=ec, lw=lw, z=z + 1)

    def polygon(
        self,
        pts: list[tuple[float, float]],
        fc: str | None = "#9CA3AF",
        ec: str | None = "#374151",
        lw: float = 0.58,
        z: int = 4,
    ) -> None:
        ops = ["q", f"{lw:.3f} w", "1 J 0 j", "[] 0 d"]
        has_f = fc is not None and fc != "none"
        has_s = ec is not None and ec != "none" and lw > 0
        if has_f:
            r, g, b = _hex_rgb(fc)  # type: ignore[arg-type]
            ops.append(f"{r:.4f} {g:.4f} {b:.4f} rg")
        if has_s:
            r, g, b = _hex_rgb(ec)  # type: ignore[arg-type]
            ops.append(f"{r:.4f} {g:.4f} {b:.4f} RG")
        x0, y0 = self._px(pts[0][0]), self._py(pts[0][1])
        ops.append(f"{x0:.3f} {y0:.3f} m")
        for x, y in pts[1:]:
            ops.append(f"{self._px(x):.3f} {self._py(y):.3f} l")
        paint = "b" if (has_f and has_s) else ("f" if has_f else "s")
        ops.append(f"h {paint}")
        ops.append("Q")
        self._add(z, "\n".join(ops))

    def polyline(
        self,
        pts: list[tuple[float, float]],
        ec: str = "#1F2937",
        lw: float = 0.72,
        dash: tuple[float, float] | None = None,
        arrow_end: bool = False,
        arrow_start: bool = False,
        head_len_pt: float = 4.2,
        head_w_pt: float = 2.3,
        z: int = 4,
    ) -> None:
        ppts = [(self._px(x), self._py(y)) for x, y in pts]
        p_draw = list(ppts)

        def _trim_and_head(p_from: tuple[float, float], p_tip: tuple[float, float]) -> tuple[tuple[float, float], str]:
            dx, dy = p_tip[0] - p_from[0], p_tip[1] - p_from[1]
            dist = math.hypot(dx, dy) or 1.0
            ux, uy = dx / dist, dy / dist
            nx, ny = -uy, ux
            bx, by = p_tip[0] - ux * head_len_pt, p_tip[1] - uy * head_len_pt
            lx, ly = bx + nx * head_w_pt, by + ny * head_w_pt
            rx, ry = bx - nx * head_w_pt, by - ny * head_w_pt
            r, g, b = _hex_rgb(ec)
            head_cmd = (
                f"q {r:.4f} {g:.4f} {b:.4f} rg "
                f"{p_tip[0]:.3f} {p_tip[1]:.3f} m {lx:.3f} {ly:.3f} l {rx:.3f} {ry:.3f} l h f Q"
            )
            return (bx + ux * 0.6, by + uy * 0.6), head_cmd

        heads: list[str] = []
        if arrow_end and len(p_draw) >= 2:
            new_end, hc = _trim_and_head(p_draw[-2], p_draw[-1])
            p_draw[-1] = new_end
            heads.append(hc)
        if arrow_start and len(p_draw) >= 2:
            new_start, hc = _trim_and_head(p_draw[1], p_draw[0])
            p_draw[0] = new_start
            heads.append(hc)

        r, g, b = _hex_rgb(ec)
        ops = ["q", f"{lw:.3f} w", "0 J 0 j"]
        if dash is not None:
            ops.append(f"[{dash[0]:.2f} {dash[1]:.2f}] 0 d")
        else:
            ops.append("[] 0 d")
        ops.append(f"{r:.4f} {g:.4f} {b:.4f} RG")
        ops.append(f"{p_draw[0][0]:.3f} {p_draw[0][1]:.3f} m")
        for px, py in p_draw[1:]:
            ops.append(f"{px:.3f} {py:.3f} l")
        ops.append("S Q")
        ops.extend(heads)
        self._add(z, "\n".join(ops))

    def text(
        self,
        x: float,
        y: float,
        s: str,
        fs: float = 7.2,
        bold: bool = False,
        italic: bool = False,
        tc: str = "#111111",
        ha: str = "center",
        va: str = "center",
        line_gap: float = 1.12,
        z: int = 5,
    ) -> None:
        lines = s.split("\n")
        n = len(lines)
        lh = fs * line_gap
        cap_h = fs * 0.67
        total_h = cap_h + (n - 1) * lh
        py_anchor = self._py(y)
        if va == "center":
            top_base = py_anchor + total_h / 2.0 - cap_h
        elif va == "top":
            top_base = py_anchor - cap_h
        else:
            top_base = py_anchor + (n - 1) * lh

        font_ref = "/F2" if bold else ("/F3" if italic else "/F1")
        r, g, b = _hex_rgb(tc)
        px_anchor = self._px(x)
        ops = ["q", f"{r:.4f} {g:.4f} {b:.4f} rg"]
        for i, ln in enumerate(lines):
            tw = self.text_width_pt(ln, fs, bold=bold, italic=italic)
            if ha == "center":
                tx = px_anchor - tw / 2.0
            elif ha == "right":
                tx = px_anchor - tw
            else:
                tx = px_anchor
            ty = top_base - i * lh
            ops.append(f"BT {font_ref} {fs:.2f} Tf {tx:.3f} {ty:.3f} Td ({_pdf_escape(ln)}) Tj ET")
        ops.append("Q")
        self._add(z, "\n".join(ops))

    def rich_text(
        self,
        x: float,
        y: float,
        spans: list[tuple[str, str]],
        fs: float = 7.0,
        tc: str = "#111111",
        ha: str = "center",
        va: str = "center",
        z: int = 5,
    ) -> None:
        """Render single-line rich mathematical/styled text.
        Each span is (text, mode) where mode in {'r','b','i','sub','sup','isub','sym'}.
        """
        pieces: list[tuple[str, str, float, float, float]] = []
        total_w = 0.0
        for txt, mode in spans:
            if mode == "b":
                fref, fsz, dy, w = "/F2", fs, 0.0, self.text_width_pt(txt, fs, bold=True)
            elif mode == "i":
                fref, fsz, dy, w = "/F3", fs, 0.0, self.text_width_pt(txt, fs, italic=True)
            elif mode == "sub":
                fref, fsz, dy, w = "/F1", fs * 0.74, -fs * 0.20, self.text_width_pt(txt, fs * 0.74)
            elif mode == "isub":
                fref, fsz, dy, w = "/F3", fs * 0.74, -fs * 0.20, self.text_width_pt(txt, fs * 0.74, italic=True)
            elif mode == "sup":
                fref, fsz, dy, w = "/F1", fs * 0.74, fs * 0.34, self.text_width_pt(txt, fs * 0.74)
            elif mode == "sym":
                fref, fsz, dy, w = "/F4", fs, 0.0, self.text_width_pt(txt, fs, symbol=True)
            else:
                fref, fsz, dy, w = "/F1", fs, 0.0, self.text_width_pt(txt, fs)
            pieces.append((txt, fref, fsz, dy, w))
            total_w += w

        px_anchor, py_anchor = self._px(x), self._py(y)
        cap_h = fs * 0.67
        if va == "center":
            base_y = py_anchor - cap_h / 2.0
        elif va == "top":
            base_y = py_anchor - cap_h
        else:
            base_y = py_anchor

        if ha == "center":
            cur_x = px_anchor - total_w / 2.0
        elif ha == "right":
            cur_x = px_anchor - total_w
        else:
            cur_x = px_anchor

        r, g, b = _hex_rgb(tc)
        ops = ["q", f"{r:.4f} {g:.4f} {b:.4f} rg"]
        for txt, fref, fsz, dy, w in pieces:
            ops.append(f"BT {fref} {fsz:.2f} Tf {cur_x:.3f} {base_y + dy:.3f} Td ({_pdf_escape(txt)}) Tj ET")
            cur_x += w
        ops.append("Q")
        self._add(z, "\n".join(ops))

    def save(self, out_path: Path) -> None:
        ordered = []
        for z in sorted(self.layers):
            ordered.extend(self.layers[z])
        stream_bytes = ("\n".join(ordered) + "\n").encode("latin-1")
        comp = zlib.compress(stream_bytes, 9)

        objs: list[bytes] = []
        objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        objs.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width_pt:.3f} {self.height_pt:.3f}] "
            f"/Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R /F4 7 0 R >> >> /Contents 8 0 R >>".encode("ascii")
        )
        objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
        objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>")
        objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic /Encoding /WinAnsiEncoding >>")
        objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Symbol >>")
        objs.append(f"<< /Length {len(comp)} /Filter /FlateDecode >>\nstream\n".encode("ascii") + comp + b"\nendstream")

        buf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets: list[int] = []
        for idx, obj in enumerate(objs, start=1):
            offsets.append(len(buf))
            buf.extend(f"{idx} 0 obj\n".encode("ascii"))
            buf.extend(obj)
            buf.extend(b"\nendobj\n")

        xref_pos = len(buf)
        buf.extend(f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode("ascii"))
        for off in offsets:
            buf.extend(f"{off:010d} 00000 n \n".encode("ascii"))
        buf.extend(
            f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
        )
        out_path.write_bytes(bytes(buf))
