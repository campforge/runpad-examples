# Import validation

- Upstream snapshot: `a58c50aa6b5c4d650a3428c01c925ef9c792fe3b`.
- Converted: 177/177 queries (175 C#, 2 Visual Basic).
- Source bodies: exact byte preservation verified against the upstream Git tree.
- Reproducibility: `tools/verify-examples.rpad` (C# body compiled and run in an isolated .NET 10 harness) passed for all outputs and manifest.
- RunPad format: 179/179 files accepted (177 examples and two C# tools) by RpadParser from RunPad revision `fc3a61d`.
  Verification used an isolated .NET harness containing the format sources; no application
  build outputs or source files were modified. The harness parsed documents only.
- Original supporting files and MIT license: unchanged (3 files).
- 37 examples have dependency/API/header compatibility notes in IMPORT-MANIFEST.json.
- Script execution, package restore, compilation and external-service access: not performed.
- No claim that the unchanged examples all execute successfully in RunPad.

## Native GitHub preview

- Added the hidden Markdown modeline after each run block; executable source bytes unchanged.
- Reproduction and RunPad parser checks passed again: 177/177.
- Live GitHub AutoMapper.rpad preview: one actual h1 heading, one pre/code block with
  syntax highlighting, and no visible modeline text. Verified after commit 7166d8c.
- No generated .md copies, extension changes or code rewrites.

## C# tooling

- Import and verification are self-contained `.rpad` C# programs with no NuGet dependencies.
- Both bodies compiled with warnings as errors: zero warnings and errors.
- Import followed by verification reproduced all 177 outputs and the manifest unchanged.
- The imported examples themselves were not executed.
