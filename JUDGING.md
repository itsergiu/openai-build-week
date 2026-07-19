# OpenAI Build Week evidence matrix

Source of truth: [OpenAI Build Week](https://openai.com/build-week/) and the [official Devpost rules](https://openai.devpost.com/rules). Verify the rules again immediately before submission.

| Criterion | What this project demonstrates | Repository evidence |
|---|---|---|
| Baseline viability | A working Codex skill and a ready-made artifact; no custom UI required | `.agents/skills/videocraft/`, example `index.html` |
| Technological implementation | Caption acquisition, deterministic normalization, stable evidence IDs, schema/ref validation, reproducible rendering, hashing, offline tests | `pipeline.py`, `tests/`, `provenance.json` |
| Design | Three-step judge path, chat-native operation, responsive offline artifact, keyboard-friendly controls, actionable errors | `README.md`, artifact, Playwright report/screenshots |
| Potential impact | Helps developers and students turn long technical video into a portable, source-linked learning object | Example guide, quiz, timestamp coverage |
| Quality of idea | The distributable product is a repo-native capability plus an evidence-bearing artifact, not another hosted summarizer | Skill contract, local-first architecture, original diagrams |

## Submission requirements checklist

- [ ] Select the Education or Work & Productivity track.
- [ ] Public YouTube demo is under three minutes, contains audio, and shows the project working.
- [ ] Demo explains how both Codex and GPT‑5.6 were used.
- [ ] Repository is public with license, or private access is granted to the addresses specified in the rules.
- [x] README explains Codex collaboration and human decisions.
- [x] Installation instructions and supported platform assumptions are documented.
- [x] Judges can inspect a finished artifact without rebuilding.
- [x] Tests and reproducibility commands are included.
- [ ] Add the `/feedback` Codex Session ID.
- [ ] Add an unedited Codex screenshot proving GPT‑5.6 Luna with Medium reasoning, and confirm the label matches the actual session.
- [ ] Record a dated commit after the challenge opens.
- [ ] Review all third-party material and demo footage for reuse rights.

## Honest limitations

- YouTube acquisition depends on platform availability and `yt-dlp` compatibility.
- Captions can contain errors; the artifact provides timestamp links for verification.
- Visual frame analysis is optional and local. The committed example does not redistribute extracted frames because no reuse license was established.
- This repository proves a complete workflow and artifact, but it does not guarantee a judging score.

