#!/usr/bin/env python3
"""Independent static validation for the MAP-001 Pass-02 proof build."""

from __future__ import annotations

import array
import hashlib
import importlib.util
import json
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
EVENT_ROOT = ROOT / "eventwright"
ASSET_ROOT = ROOT / "assets"
SOURCES = REPO.parent / "project_sources"
RESULTS = Path(__file__).with_name("independent_results.json")

EXPECTED_ARCHIVES = {
    "01-EryndraStory.zip": "56f9d5336d7a8736b92745243c1baeb941786c005741a76cd327f573a2654611",
    "02-SampleGenerated.zip": "b09e8c96856098aa94d01b563abc40e97321f3eca99ef7cbe836632d94cfd768",
}

checks: list[dict] = []


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, evidence: str, owner: str = "") -> None:
    checks.append({
        "name": name,
        "status": "PASS" if passed else "FAIL",
        "evidence": evidence,
        "owner": owner,
    })


def commands(page: dict, code: int) -> list[dict]:
    return [command for command in page["list"] if command["code"] == code]


# Immutable input evidence.
for name, expected in EXPECTED_ARCHIVES.items():
    path = SOURCES / name
    observed = digest(path) if path.is_file() else "MISSING"
    check(f"immutable archive: {name}", observed == expected,
          f"sha256={observed}", "Technical")

# Asset manifest integrity and exact source resize.
manifest = json.loads((ROOT / "ASSET_MANIFEST.json").read_text(encoding="utf-8"))
for record in manifest["assets"]:
    path = ROOT / record["file"]
    observed = digest(path) if path.is_file() else "MISSING"
    check(f"manifest hash: {record['file']}", observed == record["sha256"],
          f"sha256={observed}", "Asset")

for record in manifest["review_artifacts"]:
    path = ROOT / record["file"]
    observed = digest(path) if path.is_file() else "MISSING"
    decodes = False
    decode_detail = "missing"
    if path.is_file():
        try:
            with Image.open(path) as image:
                image.verify()
            decodes = True
            decode_detail = "PNG verified"
        except Exception as exc:  # evidence belongs in the validation report
            decode_detail = f"{type(exc).__name__}: {exc}"
    check(f"review integrity: {record['file']}",
          observed == record["sha256"] and decodes,
          f"sha256={observed}; manifest={record['sha256']}; {decode_detail}", "Asset")

source = ROOT / manifest["source"]["file"]
base = ASSET_ROOT / "img/parallaxes/MAP001_WatcherStation_Base.png"
build_spec = importlib.util.spec_from_file_location("map001_asset_builder", ROOT / "build_assets.py")
asset_builder = importlib.util.module_from_spec(build_spec)
assert build_spec.loader is not None
build_spec.loader.exec_module(asset_builder)
with Image.open(source) as original, Image.open(base) as runtime:
    expected_runtime = original.convert("RGB").resize((1392, 1008), Image.Resampling.LANCZOS)
    if hasattr(asset_builder, "finalize_engineered_division"):
        expected_runtime = asset_builder.finalize_engineered_division(expected_runtime)
    if runtime.mode == "P":
        expected_runtime = expected_runtime.quantize(
            colors=96,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
    check("base matches documented deterministic source treatment",
          ImageChops.difference(expected_runtime.convert("RGB"), runtime.convert("RGB")).getbbox() is None,
          f"source={source.name}; runtime=1392x1008/{runtime.mode}", "Asset")

required_images = {
    "img/parallaxes/MAP001_WatcherStation_Base.png": ((1392, 1008), "P"),
    "img/pictures/MAP001_Ring_Pulse.png": ((816, 624), "RGBA"),
    "img/pictures/MAP001_Ring_Residual.png": ((816, 624), "RGBA"),
    "img/pictures/MAP001_Ring_Propagated.png": ((816, 624), "RGBA"),
    "img/pictures/MAP001_Dust_Tremor.png": ((816, 624), "RGBA"),
    "img/pictures/SYS_Eryndra_Title.png": ((816, 624), "RGBA"),
    "img/tilesets/Eryndra_CinematicCollision_A5.png": ((768, 768), "RGBA"),
}
for relative, (size, mode) in required_images.items():
    with Image.open(ASSET_ROOT / relative) as image:
        image.load()
        check(f"image contract: {relative}", image.size == size and image.mode == mode,
              f"size={image.size}; mode={image.mode}", "Asset")

max_file_bytes = 700 * 1024
package_files = [path for path in ROOT.rglob("*")
                 if path.is_file() and "__pycache__" not in path.parts]
oversized = [(str(path.relative_to(ROOT)), path.stat().st_size)
             for path in package_files if path.stat().st_size > max_file_bytes]
largest = max(package_files, key=lambda path: path.stat().st_size)
check("Git-facing package file ceiling", not oversized,
      f"largest={largest.relative_to(ROOT)} ({largest.stat().st_size} bytes); ceiling={max_file_bytes}",
      "Asset")

# Map geometry, collision substrate, parallax contract, anchors, and event pages.
map_data = json.loads((EVENT_ROOT / "Map001.json").read_text(encoding="utf-8"))
check("map dimensions", (map_data["width"], map_data["height"]) == (29, 21),
      f"{map_data['width']}x{map_data['height']}", "Mapper")
check("tileset registration", map_data["tilesetId"] == 7,
      f"tilesetId={map_data['tilesetId']}", "Technical")
check("camera-tracked map parallax",
      map_data["parallaxName"] == "MAP001_WatcherStation_Base"
      and not map_data["parallaxLoopX"] and not map_data["parallaxLoopY"],
      f"name={map_data['parallaxName']}; loops={map_data['parallaxLoopX']}/{map_data['parallaxLoopY']}",
      "Eventwright")

cell_count = 29 * 21
layer0 = map_data["data"][:cell_count]
upper = map_data["data"][cell_count:]
check("collision tile domain", set(layer0) <= {1536, 1537} and {1536, 1537} <= set(layer0),
      f"layer0 tile IDs={sorted(set(layer0))}", "Mapper")
check("upper tile layers clear", set(upper) == {0},
      f"upper layer IDs={sorted(set(upper))}", "Mapper")

expected_anchors = {
    1: ("EV_Story_PrologueOpening", 14, 10),
    2: ("EV_Story_PrologueOmen", 14, 10),
    3: ("EV_Visual_FracturedRing", 14, 6),
    4: ("EV_FX_DustTremor", 14, 12),
    5: ("EV_Camera_Chamber", 14, 10),
    6: ("EV_Camera_Ring", 14, 8),
}
events = {event["id"]: event for event in map_data["events"] if event}
observed_anchors = {event_id: (event["name"], event["x"], event["y"])
                    for event_id, event in events.items()}
check("six stable anchors", observed_anchors == expected_anchors,
      repr(observed_anchors), "Eventwright")

opening = events[1]["pages"]
omen = events[2]["pages"]
check("opening page gates",
      len(opening) == 2 and opening[0]["trigger"] == 3
      and opening[1]["conditions"]["switch1Valid"]
      and opening[1]["conditions"]["switch1Id"] == 101
      and opening[1]["trigger"] == 0,
      "page 1 autorun; page 2 inert when SW101 ON", "Eventwright")
check("omen page gates",
      len(omen) == 3 and omen[0]["trigger"] == 3
      and omen[0]["conditions"]["variableValid"]
      and omen[0]["conditions"]["variableId"] == 1
      and omen[0]["conditions"]["variableValue"] == 1012
      and omen[1]["conditions"]["selfSwitchValid"]
      and omen[2]["conditions"]["switch1Valid"]
      and omen[2]["conditions"]["switch1Id"] == 112,
      "V1>=1012 autorun; Self A stop; SW112 final stop", "Eventwright")

opening_list = opening[0]["list"]
omen_list = omen[0]["list"]
forbidden_codes = {101, 102, 201, 301, 302, 355, 356, 357}
found_forbidden = sorted({command["code"] for command in opening_list + omen_list
                          if command["code"] in forbidden_codes})
check("no forbidden command classes", not found_forbidden,
      f"found={found_forbidden}", "Eventwright")

opening_se = [command["parameters"][0]["name"] for command in commands(opening[0], 250)]
omen_se = [command["parameters"][0]["name"] for command in commands(omen[0], 250)]
check("three-note asset invoked once per sequence",
      opening_se == ["Ancient_ThreeNote_Resonance"]
      and omen_se == ["Ancient_ThreeNote_Resonance"],
      f"opening={opening_se}; omen={omen_se}", "Eventwright")

switch_writes = [command["parameters"] for command in commands(opening[0], 121)]
variable_writes = [command["parameters"] for command in commands(opening[0], 122)]
check("opening state result",
      [100, 100, 0] in switch_writes and [101, 101, 0] in switch_writes
      and [1, 1, 0, 0, 1001] in variable_writes
      and [1, 1, 0, 0, 1002] in variable_writes,
      f"switches={switch_writes}; variables={variable_writes}", "Eventwright")

omen_global_completion = any(
    (command["code"] == 121 and command["parameters"][:2] == [112, 112])
    or (command["code"] == 122 and command["parameters"][-1] == 2001)
    for command in omen_list
)
check("closing defers global completion", not omen_global_completion,
      "SW112 and stage 2001 absent", "Eventwright")

def index_of(code: int, predicate=lambda command: True, start: int = 0) -> int:
    for index, command in enumerate(opening_list[start:], start):
        if command["code"] == code and predicate(command):
            return index
    return -1

pulse_erase = index_of(235, lambda c: c["parameters"] == [2])
residual_show = index_of(231, lambda c: c["parameters"][0:2] == [3, "MAP001_Ring_Residual"])
dark_pause = [command["parameters"][0] for command in opening_list[pulse_erase + 1:residual_show]
              if command["code"] == 230]
check("canon pause before residual", pulse_erase >= 0 and residual_show > pulse_erase
      and any(frames >= 20 for frames in dark_pause),
      f"wait frames between pulse death and residual={dark_pause}", "Eventwright")

fade_out = index_of(221)
title_show = index_of(231, lambda c: c["parameters"][0:2] == [6, "SYS_Eryndra_Title"], fade_out + 1)
fade_in = index_of(222, start=title_show + 1)
full_black_tint = any(command["code"] == 223
                      and command["parameters"][0] == [-255, -255, -255, 0]
                      for command in opening_list[fade_out + 1:fade_in])
check("title reveals against black", fade_out >= 0 and title_show > fade_out
      and fade_in > title_show and full_black_tint,
      "Fade Out -> full-black base tint -> transparent title -> Fade In", "Eventwright")

# Camera math: 816x624 at 48px uses center offsets (8,6). Start (14,10)
# therefore resolves to map origin (6,4); north-two scroll resolves to (6,2).
check("camera/map-space alignment",
      manifest["camera_frames"]["chamber"]["origin_px"] == [288, 192]
      and manifest["camera_frames"]["ring"]["origin_px"] == [288, 96]
      and any(command["code"] == 204 and command["parameters"] == [8, 2, 4, True]
              for command in opening_list)
      and any(command["code"] == 204 and command["parameters"] == [8, 2, 4, True]
              for command in omen_list),
      "start origin=(6,4) tiles; ring origin=(6,2) tiles; scroll north 2", "Eventwright")

ring_center = tuple(manifest["ring"]["center_map_px"])
if hasattr(asset_builder, "RING_OUTER_RADII"):
    ring_radius_x, ring_radius_y = asset_builder.RING_OUTER_RADII
else:
    ring_radius_x = ring_radius_y = asset_builder.RING_OUTER_RADIUS
ring_bounds = (ring_center[0] - ring_radius_x, ring_center[1] - ring_radius_y,
               ring_center[0] + ring_radius_x, ring_center[1] + ring_radius_y)
camera_containment = []
for camera_name in ("chamber", "ring"):
    origin = manifest["camera_frames"][camera_name]["origin_px"]
    size = manifest["camera_frames"][camera_name]["size_px"]
    contained = (ring_bounds[0] >= origin[0] and ring_bounds[1] >= origin[1]
                 and ring_bounds[2] <= origin[0] + size[0]
                 and ring_bounds[3] <= origin[1] + size[1])
    camera_containment.append((camera_name, contained))
check("base ring remains inside both approved camera frames",
      all(contained for _, contained in camera_containment),
      f"ring_bounds={ring_bounds}; containment={camera_containment}", "Asset")

# Decode audio and independently measure active regions and headroom.
audio_path = ASSET_ROOT / "audio/se/Ancient_ThreeNote_Resonance.ogg"
with tempfile.NamedTemporaryFile(suffix=".f32") as raw:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(audio_path),
                    "-f", "f32le", "-acodec", "pcm_f32le", "-ac", "1", "-ar", "48000",
                    raw.name], check=True)
    samples = array.array("f")
    samples.frombytes(Path(raw.name).read_bytes())
peak = max(abs(sample) for sample in samples)
bin_samples = 2400  # 50 ms
active = []
for offset in range(0, len(samples), bin_samples):
    chunk = samples[offset:offset + bin_samples]
    rms = math.sqrt(sum(value * value for value in chunk) / max(1, len(chunk)))
    active.append(rms > 10 ** (-50 / 20))
runs = []
run_start = None
for index, is_active in enumerate(active + [False]):
    if is_active and run_start is None:
        run_start = index
    elif not is_active and run_start is not None:
        runs.append((round(run_start * 0.05, 2), round(index * 0.05, 2)))
        run_start = None
starts = [run[0] for run in runs]
intervals = [round(starts[index + 1] - starts[index], 2)
             for index in range(len(starts) - 1)]
check("audio has three measured tones", len(runs) == 3,
      f"active regions={runs}", "Asset")
check("audio tone spacing equal", len(intervals) == 2 and abs(intervals[0] - intervals[1]) <= 0.05,
      f"onset intervals={intervals}", "Asset")
check("audio has clipping headroom", peak < 0.95,
      f"peak={peak:.6f}; peak_dBFS={20 * math.log10(peak):.2f}", "Asset")

# Installer safety, including refusal without any target-tree mutation.
test_module_path = EVENT_ROOT / "test_installer.py"
spec = importlib.util.spec_from_file_location("map001_installer_test", test_module_path)
test_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(test_module)
installer = EVENT_ROOT / "install_into_blank_mz_project.py"
with tempfile.TemporaryDirectory(prefix="eryndra-independent-installer-") as temporary:
    temp = Path(temporary)
    blank = temp / "UserOwnedBlank"
    test_module.make_blank(blank)
    installed = subprocess.run(["python3", str(installer), str(blank)],
                               capture_output=True, text=True)
    installed_map = blank / "data/Map001.json"
    installed_assets = [
        blank / "img/parallaxes/!MAP001_WatcherStation_Base.png",
        blank / "img/pictures/MAP001_Ring_Pulse.png",
        blank / "img/pictures/MAP001_Ring_Residual.png",
        blank / "img/pictures/MAP001_Ring_Propagated.png",
        blank / "img/pictures/MAP001_Dust_Tremor.png",
        blank / "img/pictures/SYS_Eryndra_Title.png",
        blank / "img/tilesets/Eryndra_CinematicCollision_A5.png",
        blank / "audio/se/Ancient_ThreeNote_Resonance.ogg",
    ]
    check("installer completes in a fresh blank project",
          installed.returncode == 0 and digest(installed_map) == digest(EVENT_ROOT / "Map001.json")
          and all(path.is_file() for path in installed_assets),
          f"returncode={installed.returncode}; assets={sum(path.is_file() for path in installed_assets)}/8",
          "Technical")

    forbidden = temp / "SampleGenerated"
    test_module.make_blank(forbidden)
    before = {str(path.relative_to(forbidden)): digest(path)
              for path in forbidden.rglob("*") if path.is_file()}
    refused = subprocess.run(["python3", str(installer), str(forbidden)],
                             capture_output=True, text=True)
    after = {str(path.relative_to(forbidden)): digest(path)
             for path in forbidden.rglob("*") if path.is_file()}
    check("installer refuses reference tree without mutation",
          refused.returncode != 0 and before == after,
          refused.stderr.strip(), "Technical")

    occupied = temp / "OccupiedTileset"
    test_module.make_blank(occupied)
    tilesets_path = occupied / "data/Tilesets.json"
    tilesets = json.loads(tilesets_path.read_text())
    while len(tilesets) <= 7:
        tilesets.append(None)
    tilesets[7] = {"id": 7, "name": "Occupied"}
    tilesets_path.write_text(json.dumps(tilesets), encoding="utf-8")
    before = {str(path.relative_to(occupied)): digest(path)
              for path in occupied.rglob("*") if path.is_file()}
    refused = subprocess.run(["python3", str(installer), str(occupied)],
                             capture_output=True, text=True)
    after = {str(path.relative_to(occupied)): digest(path)
             for path in occupied.rglob("*") if path.is_file()}
    check("installer preflights occupied IDs without mutation",
          refused.returncode != 0 and before == after,
          f"stderr={refused.stderr.strip()}; new={sorted(set(after) - set(before))}", "Technical")

status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
payload = {
    "status": status,
    "verdict": "STATIC_PASS" if status == "PASS" else "STATIC_FAIL",
    "final_room_acceptance": "CONDITIONAL_RUNTIME_PLAYTEST" if status == "PASS" else "BLOCKED",
    "scope": "independent static and artifact validation; RPG Maker MZ runtime playtest excluded",
    "checks": checks,
    "check_count": len(checks),
    "passed": sum(item["status"] == "PASS" for item in checks),
    "failed": sum(item["status"] == "FAIL" for item in checks),
}
RESULTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"{status}: {payload['passed']}/{payload['check_count']} checks passed")
raise SystemExit(0 if status == "PASS" else 1)
