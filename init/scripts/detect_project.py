#!/usr/bin/env python3
"""Detect project metadata from the current directory for README/CLAUDE generation."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".next",
    ".nuxt",
    ".svelte-kit",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "__pycache__",
    ".venv",
    "venv",
}


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def run_git(args: list[str], cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None
    except OSError:
        return None


def top_level_dirs(root: Path, limit: int = 20) -> list[str]:
    dirs: list[str] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name in IGNORE_DIRS or child.name.startswith("."):
            continue
        dirs.append(child.name + "/")
        if len(dirs) >= limit:
            break
    return dirs


def scripts_from_package(pkg: dict) -> dict[str, str]:
    scripts = pkg.get("scripts") or {}
    if not isinstance(scripts, dict):
        return {}
    return {str(k): str(v) for k, v in scripts.items()}


def detect_stack_from_deps(deps: list[str]) -> list[str]:
    mapping = {
        "next": "Next.js",
        "react": "React",
        "vue": "Vue",
        "nuxt": "Nuxt",
        "svelte": "Svelte",
        "express": "Express",
        "fastify": "Fastify",
        "hono": "Hono",
        "@nestjs/core": "NestJS",
        "typescript": "TypeScript",
        "prisma": "Prisma",
        "drizzle-orm": "Drizzle",
        "tailwindcss": "Tailwind CSS",
        "vite": "Vite",
        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",
    }
    found: list[str] = []
    for dep, label in mapping.items():
        if dep in deps and label not in found:
            found.append(label)
    return found


def detect_entry_points(root: Path) -> list[str]:
    candidates = [
        "src/main.ts",
        "src/main.tsx",
        "src/main.js",
        "src/index.ts",
        "src/index.tsx",
        "src/app/main.ts",
        "main.py",
        "app/main.py",
        "cmd/main.go",
        "src/main.rs",
    ]
    return [c for c in candidates if (root / c).is_file()]


def detect_test_patterns(root: Path) -> list[str]:
    patterns = ["**/*.test.ts", "**/*.spec.ts", "**/*_test.go", "**/test_*.py"]
    hits: list[str] = []
    for pattern in patterns:
        for path in root.glob(pattern):
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            hits.append(str(path.relative_to(root)))
            if len(hits) >= 5:
                return hits
    return hits


def detect_project(root: Path) -> dict:
    output: dict = {
        "path": str(root.resolve()),
        "name": root.name,
        "description": None,
        "stack": [],
        "scripts": {},
        "entry_points": [],
        "top_level_dirs": top_level_dirs(root),
        "test_files_sample": [],
        "repo_url": None,
        "recent_commits": [],
        "has_readme": (root / "README.md").is_file(),
        "has_claude_md": (root / "CLAUDE.md").is_file(),
        "manifests": [],
    }

    pkg_text = read_text(root / "package.json")
    if pkg_text:
        output["manifests"].append("package.json")
        try:
            pkg = json.loads(pkg_text)
            if isinstance(pkg.get("name"), str):
                output["name"] = pkg["name"]
            if isinstance(pkg.get("description"), str):
                output["description"] = pkg["description"]
            deps = list((pkg.get("dependencies") or {}).keys()) + list((pkg.get("devDependencies") or {}).keys())
            output["stack"].extend(detect_stack_from_deps(deps))
            output["scripts"] = scripts_from_package(pkg)
        except json.JSONDecodeError:
            pass

    if (root / "tsconfig.json").is_file() and "TypeScript" not in output["stack"]:
        output["stack"].append("TypeScript")
        output["manifests"].append("tsconfig.json")

    for manifest, label in [
        ("go.mod", "Go"),
        ("Cargo.toml", "Rust"),
        ("pyproject.toml", "Python"),
        ("Gemfile", "Ruby"),
        ("composer.json", "PHP"),
    ]:
        if (root / manifest).is_file():
            output["manifests"].append(manifest)
            if label not in output["stack"]:
                output["stack"].append(label)

    for config, label in [
        ("next.config.ts", "Next.js"),
        ("next.config.js", "Next.js"),
        ("nuxt.config.ts", "Nuxt"),
        ("vite.config.ts", "Vite"),
        ("docker-compose.yml", "Docker Compose"),
        ("Dockerfile", "Docker"),
    ]:
        if (root / config).is_file() and label not in output["stack"]:
            output["stack"].append(label)
            output["manifests"].append(config)

    output["entry_points"] = detect_entry_points(root)
    output["test_files_sample"] = detect_test_patterns(root)

    repo_url = run_git(["remote", "get-url", "origin"], root)
    if repo_url:
        output["repo_url"] = repo_url

    log = run_git(["log", "-5", "--pretty=format:%s"], root)
    if log:
        output["recent_commits"] = log.splitlines()

    return output


def main() -> None:
    root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(detect_project(root), indent=2))


if __name__ == "__main__":
    main()
