#!/usr/bin/env python3
"""Adobe Fonts (Typekit) helpers for the typography skill.

Auth: ADOBE_API_KEY env var → X-Typekit-Token header.
Never prints the token. Docs: https://fonts.adobe.com/docs/api
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://typekit.com/api/v1/json"


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def token() -> str:
    value = os.environ.get("ADOBE_API_KEY", "").strip()
    if not value:
        die(
            "ADOBE_API_KEY is unset. Export your Adobe Fonts / Typekit API token "
            "(e.g. in ~/.zshrc) before verifying Adobe faces."
        )
    return value


def request(path: str, *, follow_redirects: bool = True) -> dict:
    url = f"{API}/{path.lstrip('/')}"
    req = urllib.request.Request(
        url,
        headers={
            "X-Typekit-Token": token(),
            "Accept": "application/json",
            "User-Agent": "typography-skill/1.0",
        },
        method="GET",
    )
    opener = urllib.request.build_opener(
        urllib.request.HTTPRedirectHandler()
        if follow_redirects
        else urllib.request.HTTPHandler()
    )
    try:
        with opener.open(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        die(f"HTTP {exc.code} for {path}: {detail[:300]}")
    except urllib.error.URLError as exc:
        die(f"network error for {path}: {exc.reason}")


def cmd_ping(_: argparse.Namespace) -> None:
    data = request("kits")
    kits = data.get("kits") or []
    print(f"ok: authenticated ({len(kits)} kit(s))")


def cmd_kits(_: argparse.Namespace) -> None:
    data = request("kits")
    for kit in data.get("kits") or []:
        print(kit.get("id", "?"))


def cmd_kit(args: argparse.Namespace) -> None:
    data = request(f"kits/{args.kit_id}")
    kit = data.get("kit") or {}
    if args.json:
        json.dump(kit, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return
    print(f"id: {kit.get('id')}")
    print(f"name: {kit.get('name')}")
    print(f"domains: {', '.join(kit.get('domains') or [])}")
    print(f"embed: https://use.typekit.net/{kit.get('id')}.css")
    for fam in kit.get("families") or []:
        css = ", ".join(fam.get("css_names") or [])
        variations = ", ".join(fam.get("variations") or [])
        print(f"- {fam.get('name')} | css: {css} | variations: {variations}")


def cmd_family(args: argparse.Namespace) -> None:
    slug = args.slug.strip().lower().replace(" ", "-")
    data = request(f"families/{slug}")
    family = data.get("family") or {}
    if not family.get("name") and family.get("id"):
        data = request(f"families/{family['id']}")
        family = data.get("family") or {}
    if args.json:
        json.dump(family, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return
    if not family.get("name"):
        die(f"family not found for slug/id: {args.slug}")
    variations = [v.get("fvd") for v in (family.get("variations") or []) if v.get("fvd")]
    libraries = [lib.get("id") for lib in (family.get("libraries") or [])]
    print(f"name: {family.get('name')}")
    print(f"id: {family.get('id')}")
    print(f"slug: {family.get('slug')}")
    print(f"css_stack: {family.get('css_stack')}")
    print(f"libraries: {', '.join(libraries)}")
    print(f"variations: {', '.join(variations)}")
    web = family.get("web_link")
    if web:
        print(f"web: {web}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify Adobe Fonts via Typekit API (ADOBE_API_KEY)."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ping = sub.add_parser("ping", help="Confirm ADOBE_API_KEY works")
    p_ping.set_defaults(func=cmd_ping)

    p_kits = sub.add_parser("kits", help="List kit IDs")
    p_kits.set_defaults(func=cmd_kits)

    p_kit = sub.add_parser("kit", help="Show kit families + CSS names + embed URL")
    p_kit.add_argument("kit_id")
    p_kit.add_argument("--json", action="store_true")
    p_kit.set_defaults(func=cmd_kit)

    p_family = sub.add_parser("family", help="Lookup family by slug or id")
    p_family.add_argument("slug", help="e.g. source-serif-4 or pcpv")
    p_family.add_argument("--json", action="store_true")
    p_family.set_defaults(func=cmd_family)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
