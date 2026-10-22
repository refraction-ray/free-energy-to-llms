"""Generate coordinate files for schematic slide figures.

Each output is a small TikZ/pgfplots snippet under slides/shared/figures/ that
the slides \\input. Curves come from exact formulas for 1D/2D Gaussian mixtures,
so the pictures are faithful, but they are illustrations, not experiments.
"""
import struct
import zlib
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
rng = np.random.default_rng(3)

W = np.array([0.5, 0.5])
MU = np.array([-2.0, 2.0])
S2 = 0.3**2


def coords(xs, ys):
    return " ".join(f"({x:.3f},{y:.3f})" for x, y in zip(xs, ys))


def write(name, text):
    (OUT / name).write_text(text)


def langevin_path():
    # Overdamped Langevin in the double well E(x)=(x^2-1)^2/T.
    T, eta, n = 0.22, 0.01, 2400
    x = -1.0
    xs = []
    for _ in range(n):
        grad = 4 * x * (x * x - 1) / T
        x = x - 0.5 * eta * grad + np.sqrt(eta) * rng.standard_normal()
        xs.append(x)
    xs = np.array(xs)[::12]
    ks = np.arange(len(xs)) * 12
    rows = "\n".join(f"{k} {x:.3f}" for k, x in zip(ks, xs))
    write("langevin_path.dat", "k x\n" + rows + "\n")


def score_field():
    mus = np.array([[-1.6, -0.4], [1.5, 0.6]])
    s2 = 0.45
    lines = []
    for gx in np.linspace(-3.2, 3.2, 15):
        for gy in np.linspace(-2.0, 2.0, 9):
            x = np.array([gx, gy])
            d2 = ((x - mus) ** 2).sum(1)
            lw = -d2 / (2 * s2)
            r = np.exp(lw - lw.max())
            r /= r.sum()
            s = (r[:, None] * (mus - x) / s2).sum(0)
            norm = np.linalg.norm(s)
            ln = 0.34 * np.tanh(norm / 3) / max(norm, 1e-9)
            lines.append(
                f"\\draw[-{{Latex[length=0.9mm,width=0.8mm]}},GOrange,line width=0.45pt] "
                f"({gx:.2f},{gy:.2f}) -- ++({s[0]*ln:.3f},{s[1]*ln:.3f});"
            )
    write("score_field.tex", "\n".join(lines) + "\n")


def mixture_posterior(x, mean_k, var_k):
    lw = np.log(W) - 0.5 * (x - mean_k) ** 2 / var_k - 0.5 * np.log(var_k)
    r = np.exp(lw - lw.max())
    return r / r.sum()


def flow_matching():
    n = 14
    z = np.sort(rng.standard_normal(n))
    y = rng.choice(MU, n) + 0.3 * rng.standard_normal(n)
    lines = "\n".join(
        f"\\draw[GSlate!70,line width=0.5pt] (0,{a:.3f}) -- (1,{b:.3f});" for a, b in zip(z, y)
    )
    write("fm_lines.tex", lines + "\n")
    out = []
    for z0 in np.linspace(-2.2, 2.2, 15):
        x, r, dr = z0, 0.0, 0.002
        rs, xs = [0.0], [x]
        while r < 1 - 1e-9:
            var = (r**2) * S2 + (1 - r) ** 2
            post = mixture_posterior(x, r * MU, var)
            ey = MU + r * S2 / var * (x - r * MU)
            ez = (1 - r) / var * (x - r * MU)
            v = (post * (ey - ez)).sum()
            x += dr * v
            r += dr
            rs.append(r)
            xs.append(x)
        rs, xs = np.array(rs)[::25], np.array(xs)[::25]
        out.append(f"\\draw[GTeal,line width=0.7pt] plot[smooth] coordinates {{{coords(rs, xs)}}};")
    write("fm_traj.tex", "\n".join(out) + "\n")


def diffusion_paths():
    # x_t = a(t) x0 + b(t) eps with a = cos(pi t/2), b = sin(pi t/2).
    def ab(t):
        return np.cos(np.pi * t / 2), np.sin(np.pi * t / 2)

    def dab(t):
        return -np.pi / 2 * np.sin(np.pi * t / 2), np.pi / 2 * np.cos(np.pi * t / 2)

    def score(x, t):
        a, b = ab(t)
        var = a * a * S2 + b * b
        post = mixture_posterior(x, a * MU, var)
        return (post * (a * MU - x) / var).sum()

    t0, t1, n = 0.985, 0.0, 1200
    ts = np.linspace(t0, t1, n + 1)
    ode, sde = [], []
    starts = np.linspace(-2.1, 2.1, 9)
    for x0 in starts:
        for kind in ("ode", "sde"):
            if kind == "sde" and x0 not in starts[::2]:
                continue
            x = x0
            xs = [x]
            for i in range(n):
                t, dt = ts[i], ts[i + 1] - ts[i]
                (a, b), (da, db) = ab(t), dab(t)
                f = da / a * x
                g2 = 2 * b * db - 2 * da / a * b * b
                s = score(x, t)
                if kind == "ode":
                    x = x + (f - 0.5 * g2 * s) * dt
                else:
                    x = x + (f - g2 * s) * dt + np.sqrt(g2 * abs(dt)) * rng.standard_normal()
                xs.append(x)
            gen_time = 1 - ts
            sel = slice(None, None, 20)
            line = coords(gen_time[sel], np.array(xs)[sel])
            if kind == "ode":
                ode.append(f"\\draw[GTeal,line width=0.7pt] plot[smooth] coordinates {{{line}}};")
            else:
                sde.append(f"\\draw[GOrange,line width=0.45pt,opacity=0.85] plot coordinates {{{line}}};")
    write("diff_ode.tex", "\n".join(ode) + "\n")
    write("diff_sde.tex", "\n".join(sde) + "\n")


def write_png(name, rgb):
    # Minimal RGB PNG writer, so the background needs no plotting library.
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[i].tobytes() for i in range(h))

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    (OUT / name).write_bytes(png)


def river():
    # Background p_t(x) for the overview slide, with generation time r on the
    # horizontal axis (r=0 noise, r=1 data), matching diff_*.tex and fm_*.tex.
    rs = np.linspace(0, 1, 320)
    xs = np.linspace(3.5, -3.5, 360)
    teal = np.array([14, 116, 144], float)
    tint = 255 - 0.42 * (255 - teal)

    def image(mean_scale, var):
        cols = []
        for r in rs:
            m, v = mean_scale(r), var(r)
            p = (W[:, None] * np.exp(-0.5 * (xs[None, :] - m * MU[:, None]) ** 2 / v)).sum(0) / np.sqrt(v)
            cols.append((p / p.max()) ** 0.7)
        u = np.array(cols).T[..., None]
        return (255 + u * (tint - 255)).round().astype(np.uint8)

    a = lambda r: np.cos(np.pi * min(1 - r, 0.985) / 2)
    b = lambda r: np.sin(np.pi * min(1 - r, 0.985) / 2)
    write_png("river_diff.png", image(a, lambda r: a(r) ** 2 * S2 + b(r) ** 2))
    write_png("river_fm.png", image(lambda r: r, lambda r: r * r * S2 + (1 - r) ** 2))

    # Forward noising paths: data at the right edge diffusing to the left.
    # Exact Gaussian transitions keep the paths stable as a(t) -> 0.
    rg = np.random.default_rng(11)

    def ab(t):
        return np.cos(np.pi * t / 2), np.sin(np.pi * t / 2)

    ts = np.linspace(0.0, 0.985, 241)
    fwd = []
    for x0 in rg.choice(MU, 5) + 0.3 * rg.standard_normal(5):
        x, path = x0, [x0]
        for i in range(len(ts) - 1):
            (a0, b0), (a1, b1) = ab(ts[i]), ab(ts[i + 1])
            k = a1 / a0
            x = k * x + np.sqrt(max(b1 * b1 - k * k * b0 * b0, 0.0)) * rg.standard_normal()
            path.append(x)
        sel = slice(None, None, 4)
        line = coords((1 - ts)[sel], np.array(path)[sel])
        fwd.append(f"\\draw[GOrange,line width=0.45pt,opacity=0.85] plot coordinates {{{line}}};")
    write("river_fwd.tex", "\n".join(fwd) + "\n")

    # Score arrows on a few time slices.
    arrows = []
    for r in (0.1, 0.3, 0.5, 0.7, 0.9):
        at, bt = ab(1 - r)
        var = at * at * S2 + bt * bt
        for x in np.arange(-3.0, 3.01, 0.75):
            post = mixture_posterior(x, at * MU, var)
            s = (post * (at * MU - x) / var).sum()
            ln = 0.7 * np.tanh(abs(s) / 2) * np.sign(s)
            if abs(ln) > 0.04:
                arrows.append(
                    f"\\draw[-{{Latex[length=0.8mm,width=0.8mm]}},GOrange,line width=0.5pt] "
                    f"({r:.2f},{x:.2f}) -- ++(0,{ln:.3f});"
                )
    write("river_score.tex", "\n".join(arrows) + "\n")


if __name__ == "__main__":
    langevin_path()
    score_field()
    flow_matching()
    diffusion_paths()
    river()
