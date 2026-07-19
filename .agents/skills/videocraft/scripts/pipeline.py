#!/usr/bin/env python3
"""Deterministic acquisition, evidence normalization, rendering, and validation."""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
from urllib.parse import parse_qs, urlparse


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "artifact-template.html"
REQUIRED_TOP_LEVEL = {
    "artifact", "source", "summary", "learning_objectives", "chapters",
    "concepts", "cheatsheet", "quiz", "takeaways", "method",
}
EVIDENCE_COLLECTIONS = ("chapters", "concepts", "quiz")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path}: {exc}")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_youtube(value: str) -> tuple[str, str]:
    parsed = urlparse(value.strip())
    host = parsed.netloc.lower().split(":")[0]
    video_id = ""
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith(("/shorts/", "/embed/")):
            video_id = parsed.path.rstrip("/").split("/")[-1]
    elif host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        fail("Only a valid youtube.com or youtu.be video URL is accepted")
    return video_id, f"https://www.youtube.com/watch?v={video_id}"


def run_ingest(args: argparse.Namespace) -> None:
    _, url = canonical_youtube(args.url)
    work_dir = Path(args.work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable, "-m", "yt_dlp", "--skip-download", "--no-playlist",
        "--write-subs", "--write-auto-subs", "--sub-langs", args.language,
        "--sub-format", "vtt", "--write-info-json",
        "--output", str(work_dir / "source.%(ext)s"), url,
    ]
    completed = subprocess.run(command, shell=False, text=True)
    if completed.returncode:
        fail("Caption acquisition failed. Update yt-dlp or supply a local VTT/SRT file.")
    candidates = sorted(work_dir.glob("source.*.vtt"))
    if not candidates:
        fail(f"No {args.language} caption track was downloaded")
    print(f"captions={candidates[0]}")
    print(f"metadata={work_dir / 'source.info.json'}")


def parse_timestamp(value: str) -> float:
    parts = value.replace(",", ".").split(":")
    if len(parts) == 2:
        parts.insert(0, "0")
    if len(parts) != 3:
        fail(f"Invalid caption timestamp: {value}")
    hours, minutes, seconds = parts
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


TAG_RE = re.compile(r"<[^>]+>")


def parse_vtt(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    blocks = re.split(r"\n{2,}", raw)
    cues: list[dict[str, Any]] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        timing = lines[timing_index].split("-->")
        if len(timing) != 2:
            continue
        start_raw = timing[0].strip().split()[0]
        end_raw = timing[1].strip().split()[0]
        text = " ".join(lines[timing_index + 1 :])
        text = html.unescape(TAG_RE.sub("", text))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        cues.append({
            "id": f"T{len(cues) + 1:04d}",
            "start": round(parse_timestamp(start_raw), 3),
            "end": round(parse_timestamp(end_raw), 3),
            "text": text,
        })
    if not cues:
        fail(f"No caption cues found in {path}")
    return cues


def run_normalize(args: argparse.Namespace) -> None:
    vtt_path = Path(args.vtt)
    metadata = read_json(Path(args.metadata)) if args.metadata else {}
    cues = parse_vtt(vtt_path)
    video_id = str(metadata.get("id", ""))
    canonical_url = metadata.get("webpage_url") or metadata.get("original_url")
    if video_id and not canonical_url:
        canonical_url = f"https://www.youtube.com/watch?v={video_id}"
    evidence = {
        "schema_version": 1,
        "source": {
            "video_id": video_id,
            "url": canonical_url,
            "title": metadata.get("title", ""),
            "channel": metadata.get("channel") or metadata.get("uploader", ""),
            "duration_seconds": metadata.get("duration"),
            "caption_language": args.language,
            "chapters": metadata.get("chapters") or [],
        },
        "caption_file_sha256": sha256(vtt_path),
        "cues": cues,
    }
    out = Path(args.out)
    write_json(out, evidence)
    print(f"normalized_cues={len(cues)}")
    print(f"evidence={out}")


def collect_evidence_ids(study: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for collection in EVIDENCE_COLLECTIONS:
        for item in study.get(collection, []):
            values.extend(item.get("evidence", []))
    return values


def validate_study(study: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL - study.keys()
    if missing:
        errors.append("missing top-level keys: " + ", ".join(sorted(missing)))
    cue_ids = {cue["id"] for cue in evidence.get("cues", [])}
    for collection in EVIDENCE_COLLECTIONS:
        values = study.get(collection)
        if not isinstance(values, list) or not values:
            errors.append(f"{collection} must be a non-empty list")
            continue
        for index, item in enumerate(values):
            refs = item.get("evidence") if isinstance(item, dict) else None
            if not isinstance(refs, list) or not refs:
                errors.append(f"{collection}[{index}] has no evidence")
                continue
            invalid = [ref for ref in refs if ref not in cue_ids]
            if invalid:
                errors.append(f"{collection}[{index}] has invalid evidence: {invalid}")
    for index, question in enumerate(study.get("quiz", [])):
        options = question.get("options", [])
        answer = question.get("answer_index")
        if len(options) != 4:
            errors.append(f"quiz[{index}] must have exactly four options")
        if not isinstance(answer, int) or not 0 <= answer < len(options):
            errors.append(f"quiz[{index}] answer_index is invalid")
    source = study.get("source", {})
    evidence_source = evidence.get("source", {})
    if source.get("video_id") != evidence_source.get("video_id"):
        errors.append("study and evidence video IDs do not match")
    return errors


def enriched_payload(study: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    cue_map = {cue["id"]: cue for cue in evidence["cues"]}
    payload = json.loads(json.dumps(study))
    video_id = study["source"]["video_id"]
    for collection in EVIDENCE_COLLECTIONS:
        for item in payload[collection]:
            citations = []
            for cue_id in item["evidence"]:
                cue = cue_map[cue_id]
                second = int(cue["start"])
                citations.append({
                    "id": cue_id,
                    "start": cue["start"],
                    "end": cue["end"],
                    "label": format_time(second),
                    "url": f"https://youtu.be/{video_id}?t={second}",
                })
            item["citations"] = citations
    return payload


def format_time(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"


class PortableHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.external_assets: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(str(values["id"]))
        if tag in {"script", "link", "img", "source"}:
            candidate = values.get("src") or values.get("href")
            if candidate and str(candidate).startswith(("http://", "https://", "//")):
                self.external_assets.append(str(candidate))


def run_render(args: argparse.Namespace) -> None:
    study_path = Path(args.study)
    evidence_path = Path(args.evidence)
    study = read_json(study_path)
    evidence = read_json(evidence_path)
    errors = validate_study(study, evidence)
    if errors:
        fail("; ".join(errors))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if template.count("__STUDY_JSON__") != 1:
        fail("Template must contain exactly one __STUDY_JSON__ marker")
    payload = enriched_payload(study, evidence)
    json_text = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    rendered = template.replace("__STUDY_JSON__", json_text)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    provenance = {
        "schema_version": 1,
        "source": study["source"],
        "inputs": {
            "study_sha256": sha256(study_path),
            "evidence_sha256": sha256(evidence_path),
            "caption_file_sha256": evidence.get("caption_file_sha256"),
        },
        "output": {"file": out.name, "sha256": sha256(out)},
        "generator": {
            "script": "videocraft/scripts/pipeline.py",
            "agent_surface": study.get("generation", {}).get("agent_surface", "not-recorded"),
            "model": study.get("generation", {}).get("model", "not-recorded"),
            "session_id": study.get("generation", {}).get("session_id", "not-recorded"),
        },
        "rights": "Source media and full captions are not redistributed; output contains original paraphrases and timestamp links.",
    }
    provenance_path = out.with_name("provenance.json")
    write_json(provenance_path, provenance)
    print(f"artifact={out}")
    print(f"sha256={provenance['output']['sha256']}")


def run_validate(args: argparse.Namespace) -> None:
    study = read_json(Path(args.study))
    evidence = read_json(Path(args.evidence))
    errors = validate_study(study, evidence)
    html_path = Path(args.html)
    if not html_path.exists():
        errors.append(f"HTML file not found: {html_path}")
    else:
        parser = PortableHTMLParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        if parser.external_assets:
            errors.append(f"external runtime assets found: {parser.external_assets}")
        for required_id in {"app", "search", "quiz", "chapters"}:
            if required_id not in parser.ids:
                errors.append(f"HTML is missing required id: {required_id}")
    if errors:
        fail("\n- " + "\n- ".join(errors))
    print("validation=passed")
    print(f"evidence_references={len(collect_evidence_ids(study))}")
    print(f"unique_cues_used={len(set(collect_evidence_ids(study)))}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest", help="Acquire YouTube captions and metadata")
    ingest.add_argument("url")
    ingest.add_argument("--work-dir", default=".build/source")
    ingest.add_argument("--language", default="en")
    ingest.set_defaults(func=run_ingest)
    normalize = sub.add_parser("normalize", help="Normalize VTT cues into stable evidence IDs")
    normalize.add_argument("--vtt", required=True)
    normalize.add_argument("--metadata")
    normalize.add_argument("--language", default="en")
    normalize.add_argument("--out", required=True)
    normalize.set_defaults(func=run_normalize)
    render = sub.add_parser("render", help="Render a self-contained HTML artifact")
    render.add_argument("--study", required=True)
    render.add_argument("--evidence", required=True)
    render.add_argument("--out", required=True)
    render.set_defaults(func=run_render)
    validate = sub.add_parser("validate", help="Validate evidence grounding and HTML portability")
    validate.add_argument("--study", required=True)
    validate.add_argument("--evidence", required=True)
    validate.add_argument("--html", required=True)
    validate.set_defaults(func=run_validate)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
