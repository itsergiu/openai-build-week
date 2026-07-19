---
name: videocraft
description: Convert a YouTube URL, local video, VTT, or SRT transcript into a grounded, self-contained HTML study guide with chapters, concepts, a cheatsheet, quiz, timestamp evidence, and provenance. Use for video-to-notes, lecture guides, technical-video cheatsheets, cited learning artifacts, or judge-ready demonstrations that should run locally from VS Code Codex or Codex Desktop without a custom application or OpenAI API backend.
---

# VideoCraft

Create a portable learning artifact while using Codex chat as the interface. Keep acquisition and rendering deterministic; use agent judgment only for synthesis, evidence selection, and explanation.

## Workflow

1. Confirm the input is a YouTube URL, local media file, or caption file.
2. Read [content-contract.md](references/content-contract.md).
3. For YouTube, acquire metadata and captions into an ignored working directory:

   `python .agents/skills/videocraft/scripts/pipeline.py ingest <url> --work-dir .build/source`

4. Normalize captions into stable cue IDs:

   `python .agents/skills/videocraft/scripts/pipeline.py normalize --vtt .build/source/source.en.vtt --metadata .build/source/source.info.json --out .build/evidence.json`

5. Inspect the normalized evidence. Use timestamp links as the primary evidence. Extract temporary frames with FFmpeg only when the spoken words are insufficient to explain a diagram, slide, or code sample. Never commit source media or frames without confirmed reuse rights.
6. Author `study.json` using the contract. Paraphrase source material; do not reproduce the transcript. Attach at least one valid cue ID to every chapter, concept, and quiz answer.
7. Render a single-file artifact:

   `python .agents/skills/videocraft/scripts/pipeline.py render --study <study.json> --evidence .build/evidence.json --out <index.html>`

8. Validate grounding and portability:

   `python .agents/skills/videocraft/scripts/pipeline.py validate --study <study.json> --evidence .build/evidence.json --html <index.html>`

9. Run repository tests and perform a browser smoke test. Report any unavailable live-source or visual-analysis step explicitly.

## Judgment rules

- Prefer concise explanations that teach a reusable mental model.
- Treat transcript claims as source claims, not universal facts.
- Distinguish direct source coverage from agent inference.
- Reject unsupported citations rather than inventing evidence.
- Keep the HTML usable offline; timestamp links may open the original source online.
- Use original CSS diagrams and prose in committed examples unless reuse rights for source imagery are documented.
- Preserve uncertainty around names, numbers, and protocol behavior when captions are ambiguous.

## Deliverables

- `study.json`: reviewable agent-authored content.
- `index.html`: deterministic, self-contained artifact.
- `provenance.json`: hashes and reproducibility metadata emitted by the renderer.
- Validation output showing evidence coverage and portability checks.

