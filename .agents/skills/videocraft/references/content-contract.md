# Content contract

Author one UTF-8 JSON object with these required keys:

- `artifact`: `title`, `eyebrow`, `subtitle`, `audience`, `reading_minutes`.
- `source`: `video_id`, `url`, `title`, `channel`, `duration_seconds`, `caption_language`.
- `summary`: two to four original paragraphs.
- `learning_objectives`: three to six strings.
- `chapters`: objects containing `id`, `title`, `start_seconds`, `end_seconds`, `lede`, `points`, and `evidence`.
- `concepts`: objects containing `term`, `definition`, `why_it_matters`, and `evidence`.
- `cheatsheet`: objects containing `signal`, `meaning`, and `response`.
- `quiz`: objects containing `id`, `question`, four `options`, zero-based `answer_index`, `explanation`, and `evidence`.
- `takeaways`: three to six strings.
- `method`: original explanation of what was processed locally and what required Codex judgment.

Every `evidence` value is a non-empty list of normalized cue IDs such as `T0042`. Evidence IDs must exist in the supplied `evidence.json`.

## Grounding

- Paraphrase. Do not copy caption sentences into the artifact.
- Use the narrowest timestamp that supports a claim.
- Attribute opinions and forecasts to the speakers.
- Label agent-created diagrams as interpretations.
- Do not imply that processing a public URL grants redistribution rights.

## Quality target

The artifact must help an intermediate technical learner explain:

1. the problem;
2. the mechanism;
3. the tradeoffs;
4. the operational consequences;
5. the limits of the source.

