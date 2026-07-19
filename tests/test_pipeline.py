import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PIPELINE_PATH = ROOT / ".agents/skills/videocraft/scripts/pipeline.py"
SPEC = importlib.util.spec_from_file_location("videocraft_pipeline", PIPELINE_PATH)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(pipeline)


def sample_study():
    cited = ["T0001"]
    return {
        "artifact": {"title": "Test guide", "eyebrow": "Evidence first", "subtitle": "Test", "audience": "Developers", "reading_minutes": 2},
        "source": {"video_id": "abcdefghijk", "url": "https://www.youtube.com/watch?v=abcdefghijk", "title": "Source", "channel": "Channel", "duration_seconds": 11, "caption_language": "en"},
        "summary": ["A compact test summary."],
        "learning_objectives": ["Trace a claim."],
        "chapters": [{"id": "problem", "title": "Problem", "start_seconds": 0, "end_seconds": 3, "lede": "Lede", "points": ["Point"], "evidence": cited}],
        "concepts": [{"term": "Tail", "definition": "Slow end", "why_it_matters": "Sets pace", "evidence": cited}],
        "cheatsheet": [{"signal": "Delay", "meaning": "Tail", "response": "Inspect"}],
        "quiz": [{"id": "q1", "question": "What sets pace?", "options": ["A", "B", "C", "D"], "answer_index": 0, "explanation": "The cited cue explains it.", "evidence": cited}],
        "takeaways": ["Keep evidence."],
        "method": "Local test.",
    }


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.cues = pipeline.parse_vtt(ROOT / "tests/fixtures/sample.vtt")
        self.evidence = {"schema_version": 1, "source": {"video_id": "abcdefghijk"}, "caption_file_sha256": "fixture", "cues": self.cues}

    def test_vtt_normalization_is_stable(self):
        self.assertEqual([cue["id"] for cue in self.cues], ["T0001", "T0002", "T0003"])
        self.assertEqual(self.cues[1]["start"], 3.0)

    def test_youtube_url_is_canonicalized(self):
        video_id, url = pipeline.canonical_youtube("https://youtu.be/abcdefghijk?t=12")
        self.assertEqual(video_id, "abcdefghijk")
        self.assertEqual(url, "https://www.youtube.com/watch?v=abcdefghijk")

    def test_invalid_host_is_rejected(self):
        with self.assertRaises(SystemExit):
            pipeline.canonical_youtube("https://example.com/watch?v=abcdefghijk")

    def test_missing_evidence_is_rejected(self):
        study = sample_study()
        study["concepts"][0]["evidence"] = ["T9999"]
        errors = pipeline.validate_study(study, self.evidence)
        self.assertTrue(any("invalid evidence" in error for error in errors))

    def test_render_is_deterministic_and_self_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            study_path = temp / "study.json"
            evidence_path = temp / "evidence.json"
            first = temp / "first.html"
            second = temp / "second.html"
            pipeline.write_json(study_path, sample_study())
            pipeline.write_json(evidence_path, self.evidence)
            for output in (first, second):
                args = type("Args", (), {"study": str(study_path), "evidence": str(evidence_path), "out": str(output)})
                pipeline.run_render(args)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            parser = pipeline.PortableHTMLParser()
            parser.feed(first.read_text(encoding="utf-8"))
            self.assertEqual(parser.external_assets, [])


if __name__ == "__main__":
    unittest.main()
