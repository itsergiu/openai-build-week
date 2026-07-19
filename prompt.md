Read AGENTS.md first, then invoke the repo skill $videocraft.

Process this YouTube video:

https://www.youtube.com/watch?v=TiW96H5HmAw

Create a fresh demonstration run under `.build/demo-run`; do not overwrite the committed example.

Use this workflow:

1. Acquire the English captions and metadata.
2. Normalize the captions into stable evidence cue IDs.
3. Inspect the evidence and author a new `study.json` using:
   `.agents/skills/videocraft/references/content-contract.md`
4. Render the result to:
   `.build/demo-run/index.html`
5. Validate all evidence references and HTML portability.
6. Run:
   `python -m unittest discover -s tests -v`
7. Report:
   - the generated artifact path;
   - the number of evidence references;
   - validation results;
   - any limitations;
   - the exact model and reasoning setting visible in this Codex session.

Use original paraphrases and diagrams. Do not commit the downloaded video, audio, full transcript, or extracted frames.
