"""Keep the snk snake inside the contribution grid.

snk lets the snake travel through the empty border around the grid.
This clips the snake to the grid area and trims the unused margin.
"""

import re
import sys

CELL = 16  # grid spacing used by snk
PAD = 4  # space kept around the image


def clip(path):
    svg = open(path, encoding="utf-8").read()

    cells = re.findall(r'<rect class="c[^"]*" x="([\d.]+)" y="([\d.]+)"', svg)
    width = max(float(x) for x, _ in cells) - 2 + CELL
    height = max(float(y) for _, y in cells) - 2 + CELL

    # Progress bar under the grid; keep it in view.
    bars = re.findall(r'<rect class="u[^"]*" height="([\d.]+)" width="[\d.]+" x="[\d.]+" y="([\d.]+)"', svg)
    bottom = max((float(y) + float(h) for h, y in bars), default=height)

    box_w = width + 2 * PAD
    box_h = bottom + 2 * PAD
    svg = re.sub(
        r'<svg viewBox="[^"]*" width="[^"]*" height="[^"]*"',
        f'<svg viewBox="{-PAD} {-PAD} {box_w:g} {box_h:g}" width="{box_w:g}" height="{box_h:g}"',
        svg,
        count=1,
    )

    snake = re.findall(r'<rect class="s [^>]*/>', svg)
    if not snake:
        sys.exit(f"{path}: no snake found")
    start = svg.index(snake[0])
    end = svg.index(snake[-1]) + len(snake[-1])
    group = (
        f'<defs><clipPath id="grid"><rect width="{width:g}" height="{height:g}"/></clipPath></defs>'
        f'<g clip-path="url(#grid)">{svg[start:end]}</g>'
    )
    svg = svg[:start] + group + svg[end:]

    open(path, "w", encoding="utf-8").write(svg)
    print(f"{path}: snake clipped to {width:g}x{height:g}")


for p in sys.argv[1:]:
    clip(p)
