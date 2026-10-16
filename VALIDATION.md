# Import validation

- Upstream snapshot: `a58c50aa6b5c4d650a3428c01c925ef9c792fe3b`.
- Converted: 177/177 queries (175 C#, 2 Visual Basic).
- Source bodies: exact byte preservation verified against the upstream Git tree.
- Reproducibility: `python3 tools/import_examples.py --verify` passed for all outputs and manifest.
- RunPad format: 177/177 files accepted by RpadParser from RunPad revision `fc3a61d`.
  Verification used an isolated .NET harness containing the format sources; no application
  build outputs or source files were modified. The harness parsed documents only.
- Original supporting files and MIT license: unchanged (3 files).
- 37 examples have dependency/API/header compatibility notes in IMPORT-MANIFEST.json.
- Script execution, package restore, compilation and external-service access: not performed.
- No claim that the unchanged examples all execute successfully in RunPad.
