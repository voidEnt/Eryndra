#!/usr/bin/env python3
"""Build the MAP-001 Pass-02 visual/audio asset package deterministically.

Requires Pillow and ffmpeg. The approved generated concept remains the visual
master; this script only resizes it and derives transparent runtime overlays.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import shutil
import struct
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "MAP001_CanonCorrected_CameraFit.jpg"
ASSETS = ROOT / "assets"
PARALLAXES = ASSETS / "img" / "parallaxes"
PICTURES = ASSETS / "img" / "pictures"
TILESETS = ASSETS / "img" / "tilesets"
AUDIO = ASSETS / "audio" / "se"
DATA = ASSETS / "data"
REVIEW = ROOT / "review"

MAP_SIZE = (1392, 1008)  # 29 x 21 MZ tiles at 48 px.
CAMERA_SIZE = (816, 624)  # 17 x 13 MZ tiles at 48 px.
TILE = 48
RING_CAMERA_ORIGIN = (6 * TILE, 2 * TILE)
CHAMBER_CAMERA_ORIGIN = (6 * TILE, 4 * TILE)

# Measured on the approved concept after exact map-size scaling.
RING_CENTER = (691, 280)
RING_OUTER_RADII = (74, 66)
RING_INNER_RADII = (50, 44)
FRACTURE_GAP = (263, 278)  # Top division; all light effects exclude this arc.


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        image.save(temporary, format="PNG", optimize=False, compress_level=9)
        # Readers see either the previous complete PNG or the new complete PNG.
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def save_indexed_png(image: Image.Image, path: Path, colors: int) -> None:
    """Save an opaque adaptive-palette PNG for connector-safe packaging."""
    indexed = image.convert("RGB").quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.FLOYDSTEINBERG,
    )
    save_png(indexed, path)


def save_review_jpeg(image: Image.Image, path: Path, quality: int = 88) -> None:
    """Save color-faithful review evidence below the connector file ceiling."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        image.convert("RGB").save(
            temporary,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True,
            subsampling=1,
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        temporary.write_text(content)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def draw_glowing_arc(start: float, end: float, strength: float = 1.0) -> Image.Image:
    """Return a map-space RGBA ring arc while preserving the black fracture."""
    scale = 4
    size = (MAP_SIZE[0] * scale, MAP_SIZE[1] * scale)
    core = Image.new("RGBA", size, (0, 0, 0, 0))
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(core)
    dg = ImageDraw.Draw(glow)
    cx, cy = RING_CENTER[0] * scale, RING_CENTER[1] * scale
    radius_x = ((RING_OUTER_RADII[0] + RING_INNER_RADII[0]) / 2) * scale
    radius_y = ((RING_OUTER_RADII[1] + RING_INNER_RADII[1]) / 2) * scale
    bbox = (cx - radius_x, cy - radius_y, cx + radius_x, cy + radius_y)
    # A broad low-alpha halo and a narrow cold-white/cyan core.
    dg.arc(bbox, start, end, fill=(105, 222, 244, int(112 * strength)), width=24 * scale)
    dc.arc(bbox, start, end, fill=(205, 248, 255, int(220 * strength)), width=4 * scale)
    dc.arc(bbox, start, end, fill=(115, 226, 245, int(205 * strength)), width=9 * scale)
    glow = glow.filter(ImageFilter.GaussianBlur(10 * scale))
    out = Image.alpha_composite(glow, core).resize(MAP_SIZE, Image.Resampling.LANCZOS)
    # Remove blur spill from the deliberate top fracture. This mask makes the
    # fracture truly unlit rather than merely darker than the surrounding arc.
    mask_draw = ImageDraw.Draw(out)
    reach_x = RING_OUTER_RADII[0] + 24
    reach_y = RING_OUTER_RADII[1] + 24
    points = [(RING_CENTER[0], RING_CENTER[1])]
    for angle in FRACTURE_GAP:
        radians = math.radians(angle)
        points.append((
            round(RING_CENTER[0] + reach_x * math.cos(radians)),
            round(RING_CENTER[1] + reach_y * math.sin(radians)),
        ))
    mask_draw.polygon(points, fill=(0, 0, 0, 0))
    return out


def ring_state(kind: str) -> Image.Image:
    if kind == "pulse":
        # Full circumference except for the deliberate black top fracture.
        return Image.alpha_composite(
            draw_glowing_arc(FRACTURE_GAP[1], 360, 0.84),
            draw_glowing_arc(0, FRACTURE_GAP[0], 0.84),
        )
    if kind == "residual":
        # One narrow surviving line/arc on the lower-right circumference.
        return draw_glowing_arc(38, 64, 0.54)
    if kind == "propagated":
        # A substantial, incomplete spread around the ring, still divided above.
        return Image.alpha_composite(
            draw_glowing_arc(FRACTURE_GAP[1], 360, 0.64),
            draw_glowing_arc(0, 150, 0.64),
        )
    raise ValueError(kind)


def camera_crop(map_image: Image.Image, origin: tuple[int, int]) -> Image.Image:
    x, y = origin
    return map_image.crop((x, y, x + CAMERA_SIZE[0], y + CAMERA_SIZE[1]))


def make_dust_overlay() -> Image.Image:
    """Create restrained, deterministic disturbed dust in ring-camera space."""
    rng = random.Random(1001)
    high = Image.new("RGBA", (CAMERA_SIZE[0] * 2, CAMERA_SIZE[1] * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(high)
    # Floor in the ring-camera frame begins near y=275; keep particles sparse.
    for _ in range(105):
        x = rng.randint(170, 650) * 2
        y = rng.randint(315, 565) * 2
        rx = rng.choice((1, 1, 2, 3)) * 2
        ry = rng.choice((1, 2, 3)) * 2
        alpha = rng.randint(18, 64)
        color = (184, 189, 190, alpha)
        d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=color)
    # Very faint floor-level haze; no footprint pattern.
    haze = Image.new("RGBA", high.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze)
    hd.ellipse((250, 760, 1380, 1190), fill=(150, 158, 161, 18))
    haze = haze.filter(ImageFilter.GaussianBlur(30))
    return Image.alpha_composite(haze, high).resize(CAMERA_SIZE, Image.Resampling.LANCZOS)


def make_title() -> Image.Image:
    image = Image.new("RGBA", CAMERA_SIZE, (0, 0, 0, 0))
    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    font = ImageFont.truetype(str(font_path), 74)
    d = ImageDraw.Draw(image)
    text = "ERYNDRA"
    box = d.textbbox((0, 0), text, font=font, stroke_width=1)
    width = box[2] - box[0]
    height = box[3] - box[1]
    x = (CAMERA_SIZE[0] - width) // 2
    y = (CAMERA_SIZE[1] - height) // 2 - box[1]
    d.text((x, y), text, font=font, fill=(230, 234, 236, 244), stroke_width=1,
           stroke_fill=(88, 98, 106, 180))
    return image


def make_collision_sheet() -> Image.Image:
    # Collision is encoded in Tileset007.fragment.json, so the sheet is invisible.
    return Image.new("RGBA", (768, 768), (0, 0, 0, 0))


def make_tileset_fragment() -> dict:
    flags = [16] * 8192  # Star/skip by default.
    flags[1536] = 15     # Fully blocked in all four passage directions.
    flags[1537] = 0      # Passable invisible tile.
    return {
        "id": 7,
        "flags": flags,
        "mode": 0,
        "name": "Cinematic Parallax Collision",
        "note": "TIL-007; 1536 blocked, 1537 passable, all unused tiles star/skip",
        "tilesetNames": ["", "", "", "", "Eryndra_CinematicCollision_A5", "", "", "", ""],
    }


def write_audio() -> Path:
    sample_rate = 48000
    pre_silence = 0.20
    tone_duration = 0.55
    gap_duration = 0.65
    tail_silence = 0.25
    frequencies = (73.42, 87.31, 77.78)
    samples: list[int] = []

    def silence(seconds: float) -> None:
        samples.extend([0] * round(seconds * sample_rate))

    def tone(freq: float) -> None:
        count = round(tone_duration * sample_rate)
        fade = round(0.075 * sample_rate)
        for i in range(count):
            envelope = min(1.0, i / fade, (count - 1 - i) / fade)
            t = i / sample_rate
            # A restrained low signal with weak harmonics, well below clipping.
            value = envelope * (
                0.205 * math.sin(2 * math.pi * freq * t)
                + 0.037 * math.sin(2 * math.pi * freq * 2.01 * t)
                + 0.018 * math.sin(2 * math.pi * freq * 3.97 * t)
            )
            samples.append(round(max(-1.0, min(1.0, value)) * 32767))

    silence(pre_silence)
    for index, frequency in enumerate(frequencies):
        tone(frequency)
        if index < 2:
            silence(gap_duration)
    silence(tail_silence)

    AUDIO.mkdir(parents=True, exist_ok=True)
    wav_path = ROOT / "review" / "Ancient_ThreeNote_Resonance.source.wav"
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(wav_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"".join(struct.pack("<h", value) for value in samples))

    ogg_path = AUDIO / "Ancient_ThreeNote_Resonance.ogg"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav_path),
        "-c:a", "libvorbis", "-q:a", "5", str(ogg_path)
    ], check=True)
    wav_path.unlink()
    return ogg_path


def make_review(base: Image.Image, map_overlays: dict[str, Image.Image], dust: Image.Image) -> None:
    ring_base = camera_crop(base, RING_CAMERA_ORIGIN)
    states: dict[str, Image.Image] = {"Dormant": ring_base}
    for label, overlay in map_overlays.items():
        states[label] = Image.alpha_composite(ring_base.convert("RGBA"), camera_crop(overlay, RING_CAMERA_ORIGIN))
    states["Dust tremor"] = Image.alpha_composite(ring_base.convert("RGBA"), dust)

    for label, image in states.items():
        save_review_jpeg(image, REVIEW / f"RingCamera_{label.replace(' ', '_')}_816x624.jpg")

    sheet = Image.new("RGB", (CAMERA_SIZE[0] * 2, CAMERA_SIZE[1] * 2), (8, 10, 12))
    labels = ("Dormant", "Pulse", "Residual", "Propagated")
    d = ImageDraw.Draw(sheet)
    for index, label in enumerate(labels):
        x = (index % 2) * CAMERA_SIZE[0]
        y = (index // 2) * CAMERA_SIZE[1]
        sheet.paste(states[label].convert("RGB"), (x, y))
        d.rectangle((x + 8, y + 8, x + 156, y + 36), fill=(0, 0, 0))
        d.text((x + 16, y + 14), label, fill=(235, 240, 242))
    save_review_jpeg(sheet, REVIEW / "Ring_States_ContactSheet_1632x1248.jpg", quality=86)

    default = camera_crop(base, CHAMBER_CAMERA_ORIGIN)
    save_review_jpeg(default, REVIEW / "ChamberCamera_Dormant_816x624.jpg")
    save_review_jpeg(Image.alpha_composite(default.convert("RGBA"), dust),
                     REVIEW / "ChamberCamera_Dust_816x624.jpg")


def image_record(path: Path, asset_id: str, runtime_folder: str, origin: str) -> dict:
    with Image.open(path) as image:
        alpha = image.mode in ("RGBA", "LA") or "transparency" in image.info
        alpha_range = None
        if alpha:
            channel = image.getchannel("A")
            alpha_range = list(channel.getextrema())
        return {
            "asset_id": asset_id,
            "file": str(path.relative_to(ROOT)),
            "runtime_folder": runtime_folder,
            "dimensions": list(image.size),
            "mode": image.mode,
            "has_alpha": alpha,
            "alpha_range": alpha_range,
            "sha256": sha256(path),
            "origin": origin,
        }


def build() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("ffmpeg and ffprobe are required")

    # Remove only stale atomic-write files from interrupted prior builds.
    for temporary in ROOT.rglob(".*.tmp"):
        temporary.unlink()
    # Review evidence switched from indexed PNG to color-faithful JPEG.
    for superseded_review in REVIEW.glob("*.png"):
        superseded_review.unlink()

    approved = Image.open(SOURCE).convert("RGB")
    base = approved.resize(MAP_SIZE, Image.Resampling.LANCZOS)
    base_path = PARALLAXES / "MAP001_WatcherStation_Base.png"
    save_indexed_png(base, base_path, colors=96)

    states = {
        "Pulse": ring_state("pulse"),
        "Residual": ring_state("residual"),
        "Propagated": ring_state("propagated"),
    }
    state_paths = {}
    for label, image in states.items():
        cropped = camera_crop(image, RING_CAMERA_ORIGIN)
        path = PICTURES / f"MAP001_Ring_{label}.png"
        save_png(cropped, path)
        state_paths[label] = path

    dust = make_dust_overlay()
    dust_path = PICTURES / "MAP001_Dust_Tremor.png"
    save_png(dust, dust_path)
    title_path = PICTURES / "SYS_Eryndra_Title.png"
    save_png(make_title(), title_path)
    collision_path = TILESETS / "Eryndra_CinematicCollision_A5.png"
    save_png(make_collision_sheet(), collision_path)

    DATA.mkdir(parents=True, exist_ok=True)
    fragment_path = DATA / "Tileset007.fragment.json"
    write_text_atomic(fragment_path, json.dumps(make_tileset_fragment(), separators=(",", ":")) + "\n")
    ogg_path = write_audio()
    make_review(base, states, dust)

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,sample_rate,channels",
        "-of", "json", str(ogg_path)
    ], check=True, capture_output=True, text=True)
    audio_info = json.loads(probe.stdout)

    records = [
        image_record(base_path, "PIC-001", "img/parallaxes", "Approved generated concept, exact resize"),
        image_record(state_paths["Pulse"], "PIC-002", "img/pictures", "Deterministic Pillow overlay"),
        image_record(state_paths["Residual"], "PIC-003", "img/pictures", "Deterministic Pillow overlay"),
        image_record(state_paths["Propagated"], "PIC-004", "img/pictures", "Deterministic Pillow overlay"),
        image_record(dust_path, "PIC-005", "img/pictures", "Deterministic seeded Pillow overlay"),
        image_record(title_path, "PIC-006", "img/pictures", "Deterministic Pillow title rendering"),
        image_record(collision_path, "TIL-007", "img/tilesets", "Deterministic transparent collision sheet"),
        {
            "asset_id": "TIL-007",
            "file": str(fragment_path.relative_to(ROOT)),
            "runtime_folder": "data registration source",
            "sha256": sha256(fragment_path),
            "flags": {"1536": 15, "1537": 0, "all_unused": 16},
            "origin": "Deterministic database fragment",
        },
        {
            "asset_id": "SE-001",
            "file": str(ogg_path.relative_to(ROOT)),
            "runtime_folder": "audio/se",
            "sha256": sha256(ogg_path),
            "audio_probe": audio_info,
            "timing_seconds": {
                "pre_silence": 0.20,
                "tone_duration": 0.55,
                "equal_intertone_silence": 0.65,
                "tail_silence": 0.25,
                "tone_starts": [0.20, 1.40, 2.60],
                "frequencies_hz": [73.42, 87.31, 77.78],
            },
            "origin": "Deterministic Python synthesis, ffmpeg libvorbis encoding",
        },
    ]
    review_records = []
    for path in sorted(REVIEW.glob("*.jpg")):
        with Image.open(path) as review_image:
            review_records.append({
                "file": str(path.relative_to(ROOT)),
                "dimensions": list(review_image.size),
                "mode": review_image.mode,
                "sha256": sha256(path),
                "purpose": "Camera/composite review only; not a runtime asset",
            })

    manifest = {
        "scope": "MAP-001 Asset Pass 02",
        "source": {
            "file": str(SOURCE.relative_to(ROOT)),
            "dimensions": list(approved.size),
            "sha256": sha256(SOURCE),
            "treatment": "Canon and camera-fit image edit; high-quality JPEG provenance source; exact resize to 1392x1008 and adaptive 96-color indexed runtime PNG; no crop",
        },
        "camera_frames": {
            "ring": {"origin_px": list(RING_CAMERA_ORIGIN), "size_px": list(CAMERA_SIZE)},
            "chamber": {"origin_px": list(CHAMBER_CAMERA_ORIGIN), "size_px": list(CAMERA_SIZE)},
        },
        "ring": {
            "center_map_px": list(RING_CENTER),
            "center_ring_camera_px": [RING_CENTER[0] - RING_CAMERA_ORIGIN[0], RING_CENTER[1] - RING_CAMERA_ORIGIN[1]],
            "outer_radii_px": list(RING_OUTER_RADII),
            "inner_radii_px": list(RING_INNER_RADII),
            "visual_bounds_map_px": [617, 214, 765, 346],
            "fracture_unlit_degrees": list(FRACTURE_GAP),
        },
        "license_source_notes": "Approved AI-generated Eryndra concept; no third-party stock art copied. Project distribution record remains subject to Foreman review.",
        "packaging": {
            "max_file_bytes": 716800,
            "reason": "GitHub connector individual-upload payload constraint",
            "lossless_sources": "Retained locally outside the Git-facing package",
        },
        "assets": records,
        "review_artifacts": review_records,
    }
    write_text_atomic(ROOT / "ASSET_MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
    print("Built MAP-001 Pass-02 asset package and review composites.")


if __name__ == "__main__":
    build()
