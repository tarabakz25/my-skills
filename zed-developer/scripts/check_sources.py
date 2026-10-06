#!/usr/bin/env python3
"""Best-effort HTTP check for official URLs embedded in Markdown."""
from __future__ import annotations
import argparse,re,sys,urllib.request
from pathlib import Path
URL=re.compile(r'https://[^\s)>\"\']+')
def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('skill_root',type=Path); ap.add_argument('--timeout',type=float,default=10); a=ap.parse_args(argv)
    urls=set()
    for p in a.skill_root.rglob('*.md'): urls.update(u.rstrip('.,;`') for u in URL.findall(p.read_text(encoding='utf-8')))
    bad=[]
    for u in sorted(urls):
        if any(x in u for x in ('OWNER/', 'example/')) or u == 'https://crates.io/crates/zed_extension_api':
            print('SKIP non-probe/placeholder',u); continue
        try:
            req=urllib.request.Request(u,headers={'User-Agent':'zed-developer-skill-source-check/1.0'})
            with urllib.request.urlopen(req,timeout=a.timeout) as r: print(r.status,u,'->',r.geturl())
        except Exception as e: bad.append((u,str(e))); print('ERR',u,e,file=sys.stderr)
    print(f'Checked {len(urls)} URL(s); {len(bad)} failure(s)'); return int(bool(bad))
if __name__=='__main__': raise SystemExit(main())
