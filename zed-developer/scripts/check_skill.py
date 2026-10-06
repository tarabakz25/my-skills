#!/usr/bin/env python3
"""Validate Cursor skill metadata, layout, and relative Markdown links."""
from __future__ import annotations
import argparse,re,sys
from pathlib import Path
NAME=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$'); LINK=re.compile(r'\[[^\]]*\]\(([^)]+)\)')
def frontmatter(text):
    if not text.startswith('---\n'): raise ValueError('SKILL.md must start with YAML frontmatter')
    end=text.find('\n---\n',4)
    if end<0: raise ValueError('frontmatter closing delimiter missing')
    d={}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith((' ','\t')): continue
        if ':' in line:
            k,v=line.split(':',1); d[k.strip()]=v.strip().strip('"\'')
    return d,text[end+5:]
def check(root):
    errors=[]; warnings=[]; p=root/'SKILL.md'
    if not p.is_file(): return ['missing SKILL.md'],warnings
    text=p.read_text(encoding='utf-8')
    try: meta,_=frontmatter(text)
    except ValueError as e: return [str(e)],warnings
    name=meta.get('name',''); desc=meta.get('description','')
    if not NAME.fullmatch(name): errors.append('invalid skill name')
    if name!=root.name: errors.append(f'name {name!r} must match folder {root.name!r}')
    if not desc: errors.append('description is required')
    elif len(desc.encode())>1024: warnings.append('description exceeds 1024 bytes')
    if len(text.splitlines())>=500: warnings.append('SKILL.md should remain below 500 lines')
    refs=root/'references'; md_files=[p]+(sorted(refs.glob('*.md')) if refs.is_dir() else [])
    for md in md_files:
        for target in LINK.findall(md.read_text(encoding='utf-8')):
            clean=target.split('#',1)[0]
            if not clean or re.match(r'^[a-z]+://',clean) or clean.startswith(('mailto:','zed:')): continue
            dest=(md.parent/clean).resolve()
            try: dest.relative_to(root.resolve())
            except ValueError: warnings.append(f'{md.relative_to(root)} links outside skill: {target}'); continue
            if not dest.exists(): errors.append(f'{md.relative_to(root)} broken link: {target}')
    return errors,warnings
def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('skill_root',type=Path); a=ap.parse_args(argv)
    errs,warns=check(a.skill_root.resolve())
    for x in warns: print('WARN:',x)
    for x in errs: print('ERROR:',x,file=sys.stderr)
    print(f'Result: {len(errs)} error(s), {len(warns)} warning(s)'); return int(bool(errs))
if __name__=='__main__': raise SystemExit(main())
