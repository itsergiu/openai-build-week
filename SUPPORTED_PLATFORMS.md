# Supported platforms

The repository workflow is designed for:

- Windows 10/11 with Python 3.10+ and VS Code Codex or Codex Desktop.
- macOS and Linux with Python 3.10+ and a Codex surface that discovers repo skills.

Required Python package: `yt-dlp` for live YouTube acquisition. The core parser, validator, renderer, hashing, and test suite use only the Python standard library.

Optional: FFmpeg for private, local inspection of video frames when captions do not contain enough evidence. Frame extraction is not required to open, test, or inspect the committed example.

The generated HTML targets current Chromium, Firefox, and Safari. It remains readable with JavaScript disabled; search, theme switching, and quiz grading require JavaScript.

