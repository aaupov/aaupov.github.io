#!/usr/bin/env python3
"""Generate ETM aux-action pause/resume timing diagrams for the csspgo-etm post."""

from pathlib import Path
from xml.sax.saxutils import escape

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "2026-10-csspgo-etm"

RESUME_COLOR = "#c8742c"
PAUSE_COLOR = "#1d6b57"
WINDOW_FILL = "#d9e5e0"
GUIDE_COLOR = "#999"
TEXT_COLOR = "#555"
FONT = "'Segoe UI', Helvetica, Arial, sans-serif"

WIDTH = 1000
LANE_LEFT = 150
LANE_RIGHT = WIDTH - 20
PULSE_W = 12
PULSE_H = 14
TRACE_H = 22
DOT_R = 7


def periodic(period, phase, t_end):
    return [phase + i * period for i in range(int((t_end - phase) // period) + 1)]


def simulate(resumes, pauses, t_end):
    """Return trace windows [(start, end)] and samples [(t, has_trace)]."""
    events = sorted([(t, "resume") for t in resumes] + [(t, "pause") for t in pauses])
    windows, samples, start = [], [], None
    for t, kind in events:
        if kind == "resume":
            if start is None:
                start = t
        else:
            samples.append((t, start is not None))
            if start is not None:
                windows.append((start, t))
                start = None
    if start is not None:
        windows.append((start, t_end))
    return windows, samples


def diagram(resumes, pauses, t_end, title=None, caption=None,
            resume_label="resume (period R)", pause_label="pause (period P)"):
    def x(t):
        return LANE_LEFT + t / t_end * (LANE_RIGHT - LANE_LEFT)

    def pulse_path(times, base):
        d = f"M{LANE_LEFT},{base}"
        for t in times:
            d += f" H{x(t) - PULSE_W / 2:.1f} V{base - PULSE_H} H{x(t) + PULSE_W / 2:.1f} V{base}"
        return d + f" H{LANE_RIGHT}"

    def label(text, y, color):
        return (f'<text x="20" y="{y}" fill="{color}" font-size="14">{escape(text)}</text>')

    def guide(xp, y1, y2):
        return (f'<line x1="{xp:.1f}" y1="{y1}" x2="{xp:.1f}" y2="{y2}" '
                f'stroke="{GUIDE_COLOR}" stroke-dasharray="3 3"/>')

    windows, samples = simulate(resumes, pauses, t_end)

    top = 45 if title else 15
    resume_y = top + 35
    pause_y = resume_y + 60
    trace_y = pause_y + 65
    dots_y = trace_y + 35
    caption_y = dots_y + 30
    height = (caption_y if caption else dots_y + DOT_R) + 15

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
           f'width="{WIDTH}" height="{height}" font-family="{FONT}">',
           f'<rect width="{WIDTH}" height="{height}" fill="#fff"/>']
    if title:
        out.append(f'<text x="20" y="28" fill="#111" font-size="17" font-weight="600">'
                   f'{escape(title)}</text>')

    for start, _ in windows:
        out.append(guide(x(start), resume_y, trace_y))
    for t, has_trace in samples:
        if has_trace:
            out.append(guide(x(t), pause_y, dots_y - DOT_R))

    out.append(label(resume_label, resume_y - PULSE_H - 8, RESUME_COLOR))
    out.append(f'<path d="{pulse_path(resumes, resume_y)}" fill="none" '
               f'stroke="{RESUME_COLOR}" stroke-width="2"/>')

    out.append(label(pause_label, pause_y - PULSE_H - 8, PAUSE_COLOR))
    out.append(f'<path d="{pulse_path(pauses, pause_y)}" fill="none" '
               f'stroke="{PAUSE_COLOR}" stroke-width="2"/>')

    out.append(label("ETM trace", trace_y - TRACE_H - 8, TEXT_COLOR))
    trace = f"M{LANE_LEFT},{trace_y}"
    for start, end in windows:
        out.append(f'<rect x="{x(start):.1f}" y="{trace_y - TRACE_H}" '
                   f'width="{x(end) - x(start):.1f}" height="{TRACE_H}" fill="{WINDOW_FILL}"/>')
        trace += f" H{x(start):.1f} V{trace_y - TRACE_H} H{x(end):.1f} V{trace_y}"
    trace += f" H{LANE_RIGHT}"
    out.append(f'<path d="{trace}" fill="none" stroke="{PAUSE_COLOR}" stroke-width="2"/>')

    for t, has_trace in samples:
        style = (f'fill="{PAUSE_COLOR}"' if has_trace else
                 f'fill="none" stroke="{GUIDE_COLOR}" stroke-dasharray="2 2"')
        out.append(f'<circle cx="{x(t):.1f}" cy="{dots_y}" r="{DOT_R}" {style}/>')

    if caption:
        out.append(f'<text x="{LANE_RIGHT-300}" y="{caption_y}" fill="{TEXT_COLOR}" '
                   f'font-size="12" text-anchor="end">{escape(caption)}</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"


def write(name, svg):
    path = OUT_DIR / name
    path.write_text(svg)
    print(path)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t_end = 1000
    write("independent-periods.svg", diagram(
        resumes=periodic(532, 193, t_end),
        pauses=periodic(211, 70, t_end),
        t_end=t_end,
#        title="A. Independent periods (plain aux-action): the pause lands anywhere",
        caption='"empty" (no-brstack) samples',
    ))

    period, stagger = 200, 40
    pauses = periodic(period, 100, t_end)
    write("staggered.svg", diagram(
        resumes=[t - stagger for t in pauses],
        pauses=pauses,
        t_end=t_end,
    ))

    t_end = 35
    write("kernel-example.svg", diagram(
        resumes=periodic(1.05, 1.05, t_end),
        pauses=periodic(10, 10, t_end),
        t_end=t_end,
        resume_label="resume (period 1.05M)",
        pause_label="pause (period 10M)",
    ))

    write("kernel-example-swapped.svg", diagram(
        resumes=periodic(10, 10, t_end),
        pauses=periodic(1.05, 1.05, t_end),
        t_end=t_end,
        resume_label="resume (period 10M)",
        pause_label="pause (period 1.05M)",
    ))


if __name__ == "__main__":
    main()
