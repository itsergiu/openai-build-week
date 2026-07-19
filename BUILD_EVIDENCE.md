# Build evidence

This file records how VideoCraft was built with Codex and GPT‑5.6. It is an index to verifiable evidence, not a substitute for the original Codex session.

## Model and session record

| Role | Model / setting | Contribution | Independent proof |
|---|---|---|---|
| Primary implementation session | GPT‑5.6 Luna, Medium reasoning[^luna-proof] | Product architecture, Python pipeline, repo skill, deterministic renderer, tests, browser/desktop validation, and judging documentation | Add `/feedback` Session ID and `evidence/codex-luna-medium.png` |
| Independent content-authoring pass | `gpt-5.6-sol`, High reasoning | Authored `examples/openai-supercomputer-network/study.json` from the normalized 755-cue evidence set | `study.json` generation fields, `provenance.json` hashes, and this Codex thread |

[^luna-proof]: The “GPT‑5.6 Luna, Medium reasoning” label must be captured from the actual Codex model selector or session details. Repository text is self-reported provenance; the `/feedback` Session ID and an unedited UI screenshot are the jury-verifiable evidence. If the visible session label differs, replace this label everywhere before submission rather than overstating model use.

## Required attachments before submission

1. Run `/feedback` in the primary Codex build thread.
2. Copy the returned Session ID here: **`019f7a8a-8de4-7482-a6a9-130b3fa43da5`**.
3. Capture an unedited screenshot containing the VideoCraft workspace, visible GPT‑5.6 Luna model label, Medium reasoning setting, and enough Codex UI to establish the session.
4. Save it as `evidence/codex-luna-medium.png`.
5. Record the final commit hash below after the build is committed.
6. In the demo, show this evidence for approximately five seconds and show the working artifact for most of the video.

Final build commit: **`638c91d3c82fec6debdf6de0efc2ea2a419a0d70`**

## Machine-readable chain

```text
source caption file
  └─ SHA-256 in .build/evidence.json (local, not committed)
       └─ stable cue IDs cited by study.json
            └─ study SHA-256 in provenance.json
                 └─ rendered index.html SHA-256 in provenance.json
```

The committed [`provenance.json`](examples/openai-supercomputer-network/provenance.json) identifies the authoring model and hashes the structured input and final artifact. The validator rejects nonexistent cue references and reports citation coverage.

## Reproduction transcript

```powershell
python .agents/skills/videocraft/scripts/pipeline.py ingest "https://www.youtube.com/watch?v=TiW96H5HmAw" --work-dir .build/source
python .agents/skills/videocraft/scripts/pipeline.py normalize --vtt .build/source/source.en.vtt --metadata .build/source/source.info.json --out .build/evidence.json
python .agents/skills/videocraft/scripts/pipeline.py render --study examples/openai-supercomputer-network/study.json --evidence .build/evidence.json --out examples/openai-supercomputer-network/index.html
python .agents/skills/videocraft/scripts/pipeline.py validate --study examples/openai-supercomputer-network/study.json --evidence .build/evidence.json --html examples/openai-supercomputer-network/index.html
python -m unittest discover -s tests -v
```

## What this proves

- The Codex session produced and tested a non-trivial Python project.
- GPT‑5.6 performed core semantic work, not merely copy editing.
- The final artifact corresponds byte-for-byte to the recorded output hash.
- The repository alone does not prove the UI-selected primary model; the Session ID and screenshot are mandatory.

