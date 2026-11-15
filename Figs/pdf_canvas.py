"""Zero-dependency pure PDF-1.4 vector canvas using Core-14 Type-1 Times fonts."""
from __future__ import annotations
from pathlib import Path
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
        # Standard Adobe Times-Roman / Times-Bold fallback widths (1/1000 em)
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

    def text_width_pt(self, s: str, fs: float, bold: bool = False) -> float:
        tbl = _W_BOLD if bold else _W_ROMAN
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

    def text(
        self,
        x: float,
        y: float,
        s: str,
        fs: float = 7.2,
        bold: bool = False,
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
        else:  # bottom
            top_base = py_anchor + (n - 1) * lh

        font_ref = "/F2" if bold else "/F1"
        r, g, b = _hex_rgb(tc)
        px_anchor = self._px(x)
        ops = ["q", f"{r:.4f} {g:.4f} {b:.4f} rg"]
        for i, ln in enumerate(lines):
            tw = self.text_width_pt(ln, fs, bold=bold)
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

    def save(self, out_path: Path) -> None:
        ordered = []
        for z in sorted(self.layers):
            ordered.extend(self.layers[z])
        stream_bytes = ("\n".join(ordered) + "\n").encode("ascii")
        comp = zlib.compress(stream_bytes, 9)

        objs: list[bytes] = []
        objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        objs.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width_pt:.3f} {self.height_pt:.3f}] "
            f"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>".encode("ascii")
        )
        objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
        objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>")
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
