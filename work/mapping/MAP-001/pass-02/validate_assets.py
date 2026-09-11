#!/usr/bin/env python3
"""Validate MAP-001 Pass-02 asset dimensions, alpha, flags, and audio."""

from __future__ import annotations

import json
import hashlib
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
checks: list[dict] = []


def check(name: str, condition: bool, detail: str) -> None:
    checks.append({"name": name, "pass": bool(condition), "detail": detail})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


required_images = {
    "assets/img/parallaxes/MAP001_WatcherStation_Base.png": ((1392, 1008), "P", False),
    "assets/img/pictures/MAP001_Ring_Pulse.png": ((816, 624), "RGBA", True),
    "assets/img/pictures/MAP001_Ring_Residual.png": ((816, 624), "RGBA", True),
    "assets/img/pictures/MAP001_Ring_Propagated.png": ((816, 624), "RGBA", True),
    "assets/img/pictures/MAP001_Dust_Tremor.png": ((816, 624), "RGBA", True),
    "assets/img/pictures/SYS_Eryndra_Title.png": ((816, 624), "RGBA", True),
    "assets/img/tilesets/Eryndra_CinematicCollision_A5.png": ((768, 768), "RGBA", False),
}

# Full stream integrity: verify each encoded image and then force a complete
# pixel decode. This covers runtime PNGs and review JPEGs.
all_images = (sorted((ROOT / "assets").rglob("*.png"))
              + sorted((ROOT / "review").rglob("*.png"))
              + sorted((ROOT / "review").rglob("*.jpg")))
for path in all_images:
    relative = str(path.relative_to(ROOT))
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image.load()
        check(f"image-integrity:{relative}", True, "verify and full decode succeeded")
    except Exception as exc:
        check(f"image-integrity:{relative}", False, f"{type(exc).__name__}: {exc}")

alpha_sums = {}
for relative, (size, mode, needs_visible_alpha) in required_images.items():
    path = ROOT / relative
    check(f"exists:{relative}", path.exists(), str(path))
    if not path.exists():
        continue
    with Image.open(path) as image:
        check(f"size:{relative}", image.size == size, f"observed={image.size}, expected={size}")
        check(f"mode:{relative}", image.mode == mode, f"observed={image.mode}, expected={mode}")
        if image.mode == "RGBA":
            alpha = image.getchannel("A")
            extrema = alpha.getextrema()
            total = sum(value * count for value, count in enumerate(alpha.histogram()))
            alpha_sums[relative] = total
            if needs_visible_alpha:
                check(f"alpha:{relative}", extrema[0] == 0 and extrema[1] > 0,
                      f"alpha_range={extrema}")
            else:
                check(f"transparent:{relative}", extrema == (0, 0), f"alpha_range={extrema}")

check("ring-state-order",
      alpha_sums.get("assets/img/pictures/MAP001_Ring_Pulse.png", 0)
      > alpha_sums.get("assets/img/pictures/MAP001_Ring_Propagated.png", 0)
      > alpha_sums.get("assets/img/pictures/MAP001_Ring_Residual.png", 0) > 0,
      "pulse alpha > propagated alpha > residual alpha")

# In ring-camera space the top fracture crosses x≈403 and y≈100..140. It must
# remain transparent in all illuminated states.
for name in ("Pulse", "Residual", "Propagated"):
    image = Image.open(ROOT / f"assets/img/pictures/MAP001_Ring_{name}.png").convert("RGBA")
    alpha = image.getchannel("A")
    samples = [alpha.getpixel((x, y)) for x in range(398, 409) for y in range(92, 145)]
    check(f"fracture-unlit:{name}", max(samples) == 0, f"max_fracture_alpha={max(samples)}")

fragment_path = ROOT / "assets/data/Tileset007.fragment.json"
fragment = json.loads(fragment_path.read_text())
check("tileset-id", fragment["id"] == 7, f"id={fragment['id']}")
check("tile-1536-blocked", fragment["flags"][1536] == 15, f"flag={fragment['flags'][1536]}")
check("tile-1537-passable", fragment["flags"][1537] == 0, f"flag={fragment['flags'][1537]}")
unused_ok = all(value == 16 for index, value in enumerate(fragment["flags"]) if index not in (1536, 1537))
check("unused-star-skip", unused_ok, "all flags except 1536/1537 equal 16")

audio_path = ROOT / "assets/audio/se/Ancient_ThreeNote_Resonance.ogg"
probe = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,sample_rate,channels",
    "-of", "json", str(audio_path)
], check=True, capture_output=True, text=True)
audio = json.loads(probe.stdout)
stream = audio["streams"][0]
duration = float(audio["format"]["duration"])
check("audio-codec", stream["codec_name"] == "vorbis", f"codec={stream['codec_name']}")
check("audio-sample-rate", stream["sample_rate"] == "48000", f"rate={stream['sample_rate']}")
check("audio-mono", stream["channels"] == 1, f"channels={stream['channels']}")
check("audio-duration", abs(duration - 3.4) < 0.02, f"duration={duration:.6f}s")

manifest_path = ROOT / "ASSET_MANIFEST.json"
check("manifest-exists", manifest_path.exists(), str(manifest_path))
manifest = json.loads(manifest_path.read_text())
check("manifest-assets", len(manifest["assets"]) == 9, f"asset_records={len(manifest['assets'])}")
check("manifest-review-artifacts", len(manifest["review_artifacts"]) == 8,
      f"review_records={len(manifest['review_artifacts'])}")

# Ensure packaging does not erase the cold cyan that appears in the runtime
# composite. Check both the dedicated pulse frame and the four-state sheet.
for label, path in (
    ("pulse", ROOT / "review/RingCamera_Pulse_816x624.jpg"),
    ("contact-sheet", ROOT / "review/Ring_States_ContactSheet_1632x1248.jpg"),
):
    review = Image.open(path).convert("RGB")
    encoded = review.tobytes()
    cyan_pixels = sum(1 for index in range(0, len(encoded), 3)
                      if encoded[index + 2] >= encoded[index] + 18
                      and encoded[index + 1] >= encoded[index] + 8)
    check(f"review-cyan-preserved:{label}", cyan_pixels >= 250,
          f"cyan_pixels={cyan_pixels}")

ring_bounds = manifest["ring"]["visual_bounds_map_px"]
for label, camera in manifest["camera_frames"].items():
    ox, oy = camera["origin_px"]
    width, height = camera["size_px"]
    fits = (ox <= ring_bounds[0] and oy <= ring_bounds[1]
            and ring_bounds[2] < ox + width and ring_bounds[3] < oy + height)
    check(f"ring-fits-camera:{label}", fits,
          f"ring={ring_bounds}, camera={[ox, oy, ox + width - 1, oy + height - 1]}")

# Every hash published by the manifest must resolve to the bytes currently on
# disk. Include the corrected source, production records, and review records.
hash_records = [manifest["source"], *manifest["assets"], *manifest["review_artifacts"]]
for record in hash_records:
    relative = record["file"]
    path = ROOT / relative
    observed = sha256(path) if path.exists() else "missing"
    check(f"manifest-hash:{relative}", observed == record["sha256"],
          f"observed={observed}, expected={record['sha256']}")

temporary_files = sorted(ROOT.rglob(".*.tmp"))
check("no-atomic-temporaries", not temporary_files,
      "none" if not temporary_files else ", ".join(str(path.relative_to(ROOT)) for path in temporary_files))

max_file_bytes = 700 * 1024
oversized = []
for path in ROOT.rglob("*"):
    if not path.is_file() or "__pycache__" in path.parts:
        continue
    if path.stat().st_size > max_file_bytes:
        oversized.append((str(path.relative_to(ROOT)), path.stat().st_size))
check("git-package-file-ceiling", not oversized,
      f"all files <= {max_file_bytes} bytes" if not oversized else repr(oversized))

result = {"outcome": "PASS" if all(item["pass"] for item in checks) else "FAIL", "checks": checks}
(ROOT / "asset_validation.json").write_text(json.dumps(result, indent=2) + "\n")
passed = sum(item["pass"] for item in checks)
report = [
    "# MAP-001 Asset Pass 02 - Validation",
    "",
    f"**Outcome:** {result['outcome']}",
    f"**Checks:** {passed}/{len(checks)} passed",
    "",
    "The approved generated master was retained and resized to the exact map canvas. "
    "Runtime PNG dimensions, alpha channels, ring-state ordering, black-fracture mask, "
    "collision flags, OGG codec/sample rate/channel count/duration, and manifest coverage were checked.",
    "",
    "Inter-tone silence was synthesized as two equal 0.65-second intervals. Runtime playback and "
    "subjective mix level remain integration checks for RPG Maker MZ.",
    "",
]
for item in checks:
    report.append(f"- {'PASS' if item['pass'] else 'FAIL'} - `{item['name']}`: {item['detail']}")
(ROOT / "ASSET_VALIDATION.md").write_text("\n".join(report) + "\n")
print(f"{result['outcome']}: {passed}/{len(checks)} checks passed")
raise SystemExit(0 if result["outcome"] == "PASS" else 1)
