#!/usr/bin/env python3
"""Reproduce the import from the pinned upstream Git tree without executing examples."""
import argparse
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = 'https://github.com/ormico/linqpad-queries'
REVISION = 'a58c50aa6b5c4d650a3428c01c925ef9c792fe3b'
KINDS = {k: ('csharp', k) for k in ('Statements', 'Program', 'Expression')}
KINDS.update({'VB' + k: ('vb', k) for k in ('Statements', 'Program', 'Expression')})

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def quote(text):
    return json.dumps(text, ensure_ascii=False)

def convert(path, source):
    # XML is UTF-8 in this collection; keep the source body bytes untouched, including CRLF.
    content = source.removeprefix(b'\xef\xbb\xbf')
    match = re.match(rb'\s*(<Query\b[^>]*(?:/>|>[\s\S]*?</Query>))', content)
    if not match:
        raise ValueError(f'Unrecognized Query header: {path}')
    query = ET.fromstring(match[1].decode('utf-8'))
    language, kind = KINDS[query.attrib['Kind']]
    code = content[match.end():]
    code.decode('utf-8')  # Fail explicitly rather than corrupt a different encoding.
    if re.search(rb'(?m)^`{3,}[ \t]*\r?$', code):
        raise ValueError(f'Code contains a run fence delimiter: {path}')
    yaml = ['---', 'version: "1.0"', f'language: {language}', 'targetSdk: latest', f'kind: {kind}']
    packages = [(e.text or '').strip() for e in query.findall('NuGetReference')]
    references = [(e.attrib.get('Relative') or e.text or '').strip() for e in query.findall('Reference')]
    namespaces = [(e.text or '').strip() for e in query.findall('Namespace')]
    packages, references, namespaces = ([x for x in values if x] for values in (packages, references, namespaces))
    if packages:
        yaml += ['packages:'] + [f'  {quote(name)}: latest' for name in dict.fromkeys(packages)]
    for key, values in [('references', references), ('namespaces', namespaces)]:
        if values:
            yaml += [key + ':'] + ['  - ' + quote(v) for v in values]
    title = Path(path).stem
    prefix = ('\n'.join(yaml + ['---', '', '# ' + title, '', '```' + language + ' run', ''])).encode('utf-8')
    added_newline = bool(code) and not code.endswith(b'\n')
    output = prefix + code + (b'\n' if added_newline else b'') + b'```\n\n<!-- vim: set filetype=markdown: -->\n'
    notes = []
    if references:
        notes.append('Original assembly paths/references retained; may be machine-specific.')
    if any(tag not in {'Reference', 'Namespace', 'NuGetReference'} for tag in [e.tag for e in query]):
        notes.append('Extra original header fields retained in this manifest, not translated into execution settings.')
    if re.search(rb'\b(?:LINQPad|Util|Hyperlinq|DumpContainer)\b', code):
        notes.append('Uses APIs that may require LINQPad-specific compatibility.')
    if packages:
        notes.append('Upstream does not pin package versions; latest retains that unpinned intent.')
    record = {'source': path, 'target': str(Path(path).with_suffix('.rpad')), 'language': language, 'kind': kind,
              'source_sha256': hashlib.sha256(source).hexdigest(), 'code_sha256': hashlib.sha256(code).hexdigest(),
              'code_bytes': len(code), 'added_terminal_newline': added_newline,
              'original_query_xml': match[1].decode('utf-8'), 'notes': notes}
    # Verify code byte preservation independently of Markdown/YAML serialization.
    assert output[len(prefix):len(prefix) + len(code)] == code
    return output, record

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='Read-only reproduction and byte comparison')
    args = parser.parse_args()
    paths = git('ls-tree', '-r', '--name-only', '-z', REVISION).decode().split('\0')
    records = []
    for path in sorted(p for p in paths if p.endswith('.linq')):
        output, record = convert(path, git('show', REVISION + ':' + path))
        target = ROOT / record['target']
        if args.verify:
            if target.read_bytes() != output:
                raise SystemExit('Conversion differs: ' + record['target'])
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(output)
        records.append(record)
    manifest = {'upstream_url': UPSTREAM, 'upstream_revision': REVISION, 'count': len(records),
                'conversion': 'Source body bytes preserved; only a required final LF may be appended.',
                'execution': 'Not executed or claimed runnable.', 'files': records}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    if args.verify:
        assert (ROOT / 'IMPORT-MANIFEST.json').read_bytes() == manifest_bytes
    else:
        (ROOT / 'IMPORT-MANIFEST.json').write_bytes(manifest_bytes)
        # Original bytes remain accessible in the pinned upstream Git history.
        for r in records:
            (ROOT / r['source']).unlink(missing_ok=True)
    print(f'{"Verified" if args.verify else "Converted"} {len(records)} examples; source code bytes preserved.')

if __name__ == '__main__':
    main()
