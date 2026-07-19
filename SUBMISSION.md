# Devpost draft

## One-line pitch

VideoCraft turns a technical video into a grounded, portable learning artifact directly inside Codex—without a custom app, backend, or API key.

## Inspiration

Technical video is difficult to revisit: the explanation, diagram, and critical caveat often live at different timestamps. Transcript-only summaries lose that relationship, while hosted notebook products make the reader depend on another interface.

## What it does

The user clones the repository, opens it in Codex Desktop or VS Code, and invokes a repo-scoped skill with a YouTube URL or caption file. Local Python acquires and normalizes evidence. Codex produces a structured, cited study model. A deterministic renderer checks every evidence reference and emits a single HTML file with chapter navigation, original diagrams, a cheatsheet, search, and an interactive quiz.

## How we built it

The project uses a Codex `SKILL.md` for the reusable workflow, Python standard-library scripts for evidence normalization/rendering/validation, `yt-dlp` for captions, and optional FFmpeg for local visual inspection. Playwright and Windows Computer Use validate the finished artifact from both an automated-browser and user-visible perspective.

## How Codex and GPT-5.6 were used

Codex designed and implemented the repository and is also the runtime interface. GPT-5.6 performed the core semantic work: evidence selection, cross-timestamp synthesis, concept explanations, quiz generation, and quality review. Deterministic scripts reject unsupported evidence IDs and render the final artifact. The final demo visibly shows the Codex completion report and the `GPT-5.6 Luna — Medium` model/reasoning label in the opening and closing chat footage; an extracted frame is included at `evidence/codex-luna-medium.png`.

Primary build Session ID: `019f7a8a-8de4-7482-a6a9-130b3fa43da5`. Verify this with `/feedback` in the primary Codex build thread before submission.

## Human decisions

We deliberately removed the custom frontend and API backend, required source-level provenance, separated agent judgment from deterministic code, kept downloaded media out of Git, and made the result portable outside Codex.

## Challenges

The central challenge was making an agentic result auditable. We solved it by normalizing captions into stable cue IDs and requiring every chapter, concept, and quiz answer to cite those IDs before rendering.

## Accomplishments

- One required runtime dependency.
- No API key or hosted service.
- A complete ready-to-open example.
- Reproducible hashes and offline tests.
- Interactive output that remains a normal file.

## Demo outline

1. **Evidence first:** show the real Codex Chat execution and the visible `GPT-5.6 Luna — Medium` evidence.
2. **Working result:** browse the portable `index.html`, show the original mechanism diagram, timestamp evidence, search, cheatsheet, and quiz.
3. **Completion:** show the Codex completion report with artifact path, evidence count, validation, tests, browser verification, and model visibility note.

The final demo is `demo-video-final.mp4`, a 140.2-second H.264/AAC video under the three-minute limit. It uses AI-assisted narration and does not include the source podcast audio, full transcript, or extracted source frames.
