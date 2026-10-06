#!/usr/bin/env python3
"""Static preflight checks for a Zed extension source directory."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
try: import tomllib
except ImportError: print('Python 3.11+ is required.',file=sys.stderr); raise SystemExit(2)
REQ={'id':str,'name':str,'version':str,'schema_version':int,'authors':list,'description':str,'repository':str}
SEMVER=re.compile(r'^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$')
def check(root: Path):
    errors=[]; warnings=[]; manifest=root/'extension.toml'
    if not manifest.is_file(): return ['missing extension.toml'],warnings
    try: data=tomllib.loads(manifest.read_text(encoding='utf-8'))
    except Exception as e: return [f'invalid extension.toml: {e}'],warnings
    for key,typ in REQ.items():
        if key not in data: errors.append(f'missing required manifest field: {key}')
        elif not isinstance(data[key],typ): errors.append(f'{key} must be {typ.__name__}')
        elif isinstance(data[key],(str,list)) and not data[key]: errors.append(f'{key} must not be empty')
    eid=data.get('id','')
    if isinstance(eid,str):
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',eid): warnings.append('id should use lowercase letters, digits, and hyphens')
        if re.search(r'zed|extension',eid,re.I): errors.append("published extension id must not contain 'zed' or 'extension'")
    name=data.get('name','')
    if isinstance(name,str) and re.search(r'\bzed\b|\bextension\b',name,re.I): errors.append("published extension name must not contain 'Zed' or 'extension'")
    ver=data.get('version')
    if isinstance(ver,str) and not SEMVER.fullmatch(ver): warnings.append('version is not conventional semver x.y.z')
    if data.get('schema_version') != 1: warnings.append('verify schema_version against current Zed docs (baseline is 1)')
    repo=data.get('repository','')
    if isinstance(repo,str) and repo and not repo.startswith('https://'): warnings.append('repository should normally be a public HTTPS URL')
    if not any(p.is_file() and p.name.upper().startswith(('LICENSE','LICENCE')) for p in root.iterdir()): errors.append('missing LICENSE/LICENCE at extension root')
    snippets=data.get('snippets',[])
    if isinstance(snippets,list):
        for rel in snippets:
            if Path(rel).is_absolute() or not (root/rel).is_file(): errors.append(f'missing/invalid snippet path: {rel}')
    grammars=data.get('grammars',{})
    if isinstance(grammars,dict):
        for gid,g in grammars.items():
            if not isinstance(g,dict): errors.append(f'grammar {gid} must be a table'); continue
            if not g.get('repository') or not g.get('rev'): errors.append(f'grammar {gid} needs repository and pinned rev')
            elif str(g['repository']).startswith('file://'): errors.append(f'grammar {gid} uses local file:// repository')
            elif len(str(g['rev']))<12: warnings.append(f'grammar {gid} rev does not look like a full commit')
    cargo=root/'Cargo.toml'; procedural=any(k in data for k in ('language_servers','language-servers','context_servers','debug_adapters','debug_locators'))
    if procedural and not cargo.is_file(): warnings.append('procedural capability likely requires Cargo.toml and Rust')
    if cargo.is_file():
        try:
            cd=tomllib.loads(cargo.read_text(encoding='utf-8')); dep=cd.get('dependencies',{}).get('zed_extension_api')
            if not dep: errors.append('Cargo.toml missing zed_extension_api')
            elif '<' in str(dep) or 'latest' in str(dep): errors.append('replace zed_extension_api placeholder with a published compatible version')
            cver=cd.get('package',{}).get('version')
            if ver and cver and ver!=cver: warnings.append('Cargo and extension.toml versions differ')
        except Exception as e: errors.append(f'invalid Cargo.toml: {e}')
    for folder in ('themes','icon_themes','snippets'):
        d=root/folder
        if d.is_dir():
            for p in d.glob('*.json'):
                try: json.loads(p.read_text(encoding='utf-8'))
                except Exception as e: errors.append(f'invalid JSON {p.relative_to(root)}: {e}')
    if (root/'themes').is_dir() and any((root/x).exists() for x in ('languages','icon_themes','snippets')): warnings.append('theme may need a separate marketplace extension')
    if (root/'icon_themes').is_dir() and any((root/x).exists() for x in ('languages','themes','snippets')): warnings.append('icon theme may need a separate marketplace extension')
    return errors,warnings

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('extension_root',type=Path); a=ap.parse_args(argv)
    if not a.extension_root.is_dir(): print('extension root is not a directory',file=sys.stderr); return 2
    errs,warns=check(a.extension_root.resolve())
    for x in warns: print('WARN:',x)
    for x in errs: print('ERROR:',x,file=sys.stderr)
    print(f'Result: {len(errs)} error(s), {len(warns)} warning(s)'); return int(bool(errs))
if __name__=='__main__': raise SystemExit(main())
