# VideoCraft agent guidance

- Use the repo-scoped `$videocraft` skill for video-to-guide requests.
- Keep downloaded captions, video, audio, and temporary frames under `.build/`; never commit them.
- Treat `study.json` as agent-authored content and `index.html` as deterministic generated output.
- Require timestamp evidence for every chapter, concept, and quiz answer.
- Run `python -m unittest discover -s tests -v` after pipeline changes.
- Run the skill validator and artifact validator before delivery.
- Do not claim a model or Codex surface in provenance unless it is known from the active session.
- Do not redistribute source frames, audio, or transcripts unless the user confirms reuse rights.

