#!/usr/bin/env python3
"""Validate JSON or conservative JSONC (comments and trailing commas), without editing."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

def strip_jsonc(text: str) -> str:
    out=[]; i=0; in_string=False; escape=False
    while i < len(text):
        c=text[i]
        if in_string:
            out.append(c)
            if escape: escape=False
            elif c=='\\': escape=True
            elif c=='"': in_string=False
            i+=1; continue
        if c=='"': in_string=True; out.append(c); i+=1; continue
        if c=='/' and i+1 < len(text) and text[i+1]=='/':
            out.extend('  '); i+=2
            while i < len(text) and text[i] not in '\r\n': out.append(' '); i+=1
            continue
        if c=='/' and i+1 < len(text) and text[i+1]=='*':
            out.extend('  '); i+=2
            while i+1 < len(text) and not (text[i]=='*' and text[i+1]=='/'):
                out.append('\n' if text[i]=='\n' else ' '); i+=1
            if i+1 >= len(text): raise ValueError('unterminated block comment')
            out.extend('  '); i+=2; continue
        out.append(c); i+=1
    chars=list(out); i=0; in_string=False; escape=False
    while i < len(chars):
        c=chars[i]
        if in_string:
            if escape: escape=False
            elif c=='\\': escape=True
            elif c=='"': in_string=False
        elif c=='"': in_string=True
        elif c==',':
            j=i+1
            while j < len(chars) and chars[j].isspace(): j+=1
            if j < len(chars) and chars[j] in '}]': chars[i]=' '
        i+=1
    return ''.join(chars)

def load(path: Path):
    raw=path.read_text(encoding='utf-8')
    if raw.startswith('\ufeff'): raw=raw[1:]
    return json.loads(strip_jsonc(raw))

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('files',nargs='+',type=Path); a=ap.parse_args(argv)
    failed=False
    for path in a.files:
        try: load(path); print(f'OK  {path}')
        except (OSError, UnicodeError, ValueError) as e:
            failed=True; print(f'ERR {path}: {e}',file=sys.stderr)
    return int(failed)
if __name__=='__main__': raise SystemExit(main())
