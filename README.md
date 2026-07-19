# VideoCraft submission package

This folder is a self-contained, Codex-ready project. Copy it locally and open the folder as the project root in Codex Chat.

## Contents

- `demo-video-final.mp4` — 125-second evidence-first demo: real Codex Chat execution footage with adjusted AI narration, followed by the interactive artifact demo.
- `demo-video-v2.mp4` — the artifact-focused source recording.
- `index.html` — portable, self-contained interactive study guide.
- `study.json` and `provenance.json` — authored study and renderer provenance.
- `.agents/skills/videocraft/` — the repo-scoped Codex skill, Python pipeline, content contract, and HTML template.
- `AGENTS.md`, tests, requirements, and project documentation.

## Use with Codex Chat

Open this folder as the working project. `AGENTS.md` points Codex to the repo-scoped `videocraft` skill. The skill can process a new YouTube URL or local caption file, normalize evidence, author a study, render a portable HTML artifact, and validate it.

## Run locally

```powershell
python -m unittest discover -s tests -v
python .agents/skills/videocraft/scripts/pipeline.py --help
```

For a new video, follow `.agents/skills/videocraft/SKILL.md` and keep acquisition data in an ignored `.build/` directory.

## Verification

- Evidence and HTML portability validation: passed.
- Evidence references: 55 across 39 unique cues.
- Unit tests: 5 passed.
- Final video: H.264/AAC, 125.2 seconds, under the three-minute limit.
- No source video, audio, full captions, extracted frames, browser profile, or intermediate recording files are included in the submission folder.
