# RunPad examples — ormico collection

177 examples imported from [ormico/linqpad-queries](https://github.com/ormico/linqpad-queries)
into the RunPad `.rpad` Markdown format. Original examples: Zack Moore and upstream contributors.
The upstream MIT license and copyright notice are retained in [LICENSE](LICENSE).

## Import policy

- File/folder names and hierarchy are unchanged; `.linq` becomes `.rpad`.
- C#/VB source bodies are byte-for-byte preserved, including comments and line endings.
  Only a required final LF may be added before the closing Markdown fence.
- Query kind, namespaces, NuGet packages and assembly references are mapped to RunPad YAML.
- Upstream package versions were not pinned; they remain `latest`.
- Non-query assets are retained at their original relative paths.
- The exact original XML headers, source hashes and conversion notes are recorded in
  [IMPORT-MANIFEST.json](IMPORT-MANIFEST.json). Original files remain in upstream Git history.
- Snapshot: `a58c50aa6b5c4d650a3428c01c925ef9c792fe3b`.

## Open in RunPad

Open this directory as the queries folder, or open any `.rpad` file individually.
The collection contains 175 C# examples and 2 Visual Basic examples.

Conversion does **not** guarantee execution compatibility. Code has not been rewritten:
LINQPad APIs, old packages, machine-specific assembly paths, Windows-only APIs, local
files and external services may require adaptation. The one original RuntimeVersion
setting is preserved in the manifest but does not force an old runtime; imports use
`targetSdk: latest`, as the standard RunPad importer does. The scripts were not executed.

## Reproduce and verify

RunPad with a .NET 10 SDK and Git are required; no Python or extra NuGet packages.
Run these saved `.rpad` tools in this Git checkout, using RunPad or its CLI.

```sh
runpad tools/verify-examples.rpad
```

Verification reads original files from the pinned upstream Git commit and checks exact
reproduction of every converted file and the manifest. To regenerate the import:

```sh
runpad tools/import-examples.rpad
```

Both tools locate the checkout from the saved script path or current directory.
For another working directory, set `RUNPAD_EXAMPLES_ROOT` to the checkout path.
The verifier is read-only; the importer regenerates the converted examples.
Neither tool executes the imported queries.

The original repository is configured as the read-only source remote `upstream`.
The publishing remote `origin` is https://github.com/campforge/runpad-examples.
See [UPSTREAM-README.md](UPSTREAM-README.md) for the upstream README.

## GitHub Markdown preview

The `.rpad` extension is retained. Each generated document ends with an invisible
Markdown HTML comment:

```html
<!-- vim: set filetype=markdown: -->
```

This modeline lets GitHub Linguist detect Markdown from the document itself, including
when the markup renderer detects language independently of repository attributes.
`.gitattributes` still provides Markdown highlighting and diff configuration.
No `.md` mirrors or extra preview pages are generated; executable code is unchanged.
The modeline is outside the run block and does not affect execution.

Native GitHub preview was verified on AutoMapper.rpad: heading, highlighted code block
and no visible modeline text. All 177 outputs still pass import and RunPad parser checks.
