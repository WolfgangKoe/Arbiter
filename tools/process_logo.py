"""Reproducible logo processing for Arbiter.

Takes the raw crest export (binary alpha, with a light 1px cut-out fringe and a
cool/silver metal) and produces app-ready assets:

  - <out>/arbiter_logo.png  : halo removed + warm gold grade, trimmed
  - <out>/arbiter_icon.png  : square favicon variant derived from the logo

The cut-out fringe is the outermost 1px ring of opaque pixels (flattened
anti-aliasing); eroding the alpha by 1px removes it and exposes the design's own
dark border as the new clean edge.

Usage: python tools/process_logo.py <input.png> <out_dir>
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Warm gold ramp for the metallic (low-saturation) parts. Dark -> light.
# Stays metallic (not pure accent yellow) but reads as gold next to #d4a017.
GOLD_DARK = np.array([46, 36, 16], dtype=np.float32)
GOLD_LIGHT = np.array([245, 224, 150], dtype=np.float32)
GOLD_STRENGTH = 0.75  # 0 = keep silver, 1 = full gold remap

# Palette red the shield is nudged toward (constants/colors RED-ish / --arb-red).
SHIELD_RED = np.array([140, 26, 24], dtype=np.float32)
RED_STRENGTH = 0.45


def _erode_alpha_1px(alpha: np.ndarray) -> np.ndarray:
    """Set a pixel transparent if any 4-neighbour is transparent (1px erosion)."""
    transp = alpha == 0
    grow = transp.copy()
    grow[1:, :] |= transp[:-1, :]
    grow[:-1, :] |= transp[1:, :]
    grow[:, 1:] |= transp[:, :-1]
    grow[:, :-1] |= transp[:, 1:]
    out = alpha.copy()
    out[grow] = 0
    return out


def _grade(rgb: np.ndarray) -> np.ndarray:
    """Warm-gold the metal, deepen the shield red toward the palette."""
    out = rgb.astype(np.float32)
    r, g, b = out[..., 0], out[..., 1], out[..., 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    sat = out.max(axis=2) - out.min(axis=2)

    metal = sat < 45  # silver/grey frame, blades, scroll
    t = (luma[metal] / 255.0)[:, None]
    gold = GOLD_DARK + (GOLD_LIGHT - GOLD_DARK) * t
    out[metal] = out[metal] * (1 - GOLD_STRENGTH) + gold * GOLD_STRENGTH

    redmask = (r - g > 40) & (r - b > 40)  # shield red
    out[redmask] = out[redmask] * (1 - RED_STRENGTH) + SHIELD_RED * RED_STRENGTH

    return np.clip(out, 0, 255).astype(np.uint8)


def _trim(img: Image.Image, pad: int = 8) -> Image.Image:
    """Crop to the alpha bounding box plus padding."""
    alpha = np.array(img)[..., 3]
    ys, xs = np.where(alpha > 0)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    h, w = alpha.shape
    box = (max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + 1 + pad, w), min(y1 + 1 + pad, h))
    return img.crop(box)


def _square(img: Image.Image) -> Image.Image:
    """Pad the (already trimmed) image to a centered transparent square."""
    w, h = img.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - w) // 2, (side - h) // 2), img)
    return canvas


def process(src: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(src).convert("RGBA")
    arr = np.array(img)

    arr[..., 3] = _erode_alpha_1px(arr[..., 3])
    arr[..., :3] = _grade(arr[..., :3])
    graded = Image.fromarray(arr, "RGBA")

    logo = _trim(graded)
    logo.save(out_dir / "arbiter_logo.png")

    icon = _square(logo).resize((512, 512), Image.LANCZOS)
    icon.save(out_dir / "arbiter_icon.png")
    print(f"wrote {out_dir/'arbiter_logo.png'} {logo.size}")
    print(f"wrote {out_dir/'arbiter_icon.png'} {icon.size}")


if __name__ == "__main__":
    process(Path(sys.argv[1]), Path(sys.argv[2]))
