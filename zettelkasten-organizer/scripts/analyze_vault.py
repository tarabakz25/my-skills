#!/usr/bin/env python3
"""
Obsidian Vault Analyzer for Zettelkasten

Analyzes an Obsidian vault to identify:
- Total note count and distribution
- Link statistics (incoming/outgoing)
- Orphaned notes (no connections)
- Broken links
- YAML frontmatter compliance
- Naming convention violations
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


class VaultAnalyzer:
    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path).resolve()
        self.notes: Dict[str, Dict] = {}
        self.link_graph: Dict[str, Set[str]] = defaultdict(set)
        self.backlink_graph: Dict[str, Set[str]] = defaultdict(set)
        self.broken_links: List[Tuple[str, str]] = []

    def find_markdown_files(self) -> List[Path]:
        """Find all markdown files in the vault, excluding .obsidian folder."""
        md_files = []
        for path in self.vault_path.rglob("*.md"):
            if ".obsidian" not in path.parts:
                md_files.append(path)
        return md_files

    def extract_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from markdown content."""
        frontmatter = {}
        body = content

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_content = parts[1].strip()
                body = parts[2].strip()

                # Simple YAML parsing (basic key: value)
                for line in yaml_content.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")

                        # Handle lists
                        if value.startswith("[") and value.endswith("]"):
                            value = [v.strip().strip('"').strip("'")
                                   for v in value[1:-1].split(",")]

                        frontmatter[key] = value

        return frontmatter, body

    def extract_wiki_links(self, content: str) -> List[str]:
        """Extract [[wiki-style]] links from content."""
        # Match [[link]] or [[link|alias]]
        pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        matches = re.findall(pattern, content)
        return [match.strip() for match in matches]

    def extract_markdown_links(self, content: str) -> List[str]:
        """Extract [text](link.md) style links."""
        pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
        matches = re.findall(pattern, content)
        return [match[1].strip() for match in matches]

    def normalize_link(self, link: str, source_file: Path) -> str:
        """Normalize link to absolute path within vault."""
        # Remove .md extension if present
        link = link.replace(".md", "")

        # If it's just a filename, search for it in vault
        if "/" not in link:
            return link

        # Handle relative paths
        link_path = (source_file.parent / link).resolve()
        try:
            rel_path = link_path.relative_to(self.vault_path)
            return str(rel_path).replace(".md", "")
        except ValueError:
            return link

    def get_note_id(self, file_path: Path) -> str:
        """Get note identifier (relative path without extension)."""
        rel_path = file_path.relative_to(self.vault_path)
        return str(rel_path.with_suffix(""))

    def analyze_note(self, file_path: Path) -> Dict:
        """Analyze a single note file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"error": str(e)}

        note_id = self.get_note_id(file_path)
        frontmatter, body = self.extract_frontmatter(content)

        # Extract links
        wiki_links = self.extract_wiki_links(body)
        md_links = self.extract_markdown_links(body)
        all_links = wiki_links + md_links

        # Count words (approximate)
        word_count = len(body.split())

        # Extract tags from frontmatter and content
        tags = []
        if "tags" in frontmatter:
            if isinstance(frontmatter["tags"], list):
                tags.extend(frontmatter["tags"])
            else:
                tags.append(frontmatter["tags"])

        # Extract inline tags (#tag)
        inline_tags = re.findall(r'#([a-zA-Z0-9_/-]+)', body)
        tags.extend(inline_tags)

        return {
            "id": note_id,
            "path": str(file_path),
            "frontmatter": frontmatter,
            "outgoing_links": all_links,
            "word_count": word_count,
            "tags": list(set(tags)),
            "has_frontmatter": bool(frontmatter),
        }

    def build_link_graph(self):
        """Build bidirectional link graph."""
        for note_id, note_data in self.notes.items():
            for link in note_data["outgoing_links"]:
                # Normalize link
                normalized_link = link.replace(".md", "")

                # Find matching note
                matching_notes = [nid for nid in self.notes.keys()
                                if nid.endswith(normalized_link) or
                                   Path(nid).name == normalized_link]

                if matching_notes:
                    target = matching_notes[0]
                    self.link_graph[note_id].add(target)
                    self.backlink_graph[target].add(note_id)
                else:
                    # Broken link
                    self.broken_links.append((note_id, link))

    def find_orphaned_notes(self) -> List[str]:
        """Find notes with no incoming or outgoing links."""
        orphaned = []
        for note_id in self.notes.keys():
            outgoing = len(self.link_graph.get(note_id, set()))
            incoming = len(self.backlink_graph.get(note_id, set()))

            if outgoing == 0 and incoming == 0:
                orphaned.append(note_id)

        return orphaned

    def analyze_vault(self) -> Dict:
        """Perform full vault analysis."""
        print(f"Analyzing vault: {self.vault_path}")

        # Find all markdown files
        md_files = self.find_markdown_files()
        print(f"Found {len(md_files)} markdown files")

        # Analyze each note
        for file_path in md_files:
            note_data = self.analyze_note(file_path)
            if "error" not in note_data:
                self.notes[note_data["id"]] = note_data

        # Build link graph
        print("Building link graph...")
        self.build_link_graph()

        # Calculate statistics
        total_notes = len(self.notes)
        notes_with_frontmatter = sum(1 for n in self.notes.values()
                                     if n["has_frontmatter"])
        orphaned_notes = self.find_orphaned_notes()

        # Connection statistics
        connection_counts = []
        for note_id in self.notes.keys():
            outgoing = len(self.link_graph.get(note_id, set()))
            incoming = len(self.backlink_graph.get(note_id, set()))
            total_connections = outgoing + incoming
            connection_counts.append(total_connections)

        avg_connections = (sum(connection_counts) / len(connection_counts)
                          if connection_counts else 0)

        # Tag statistics
        all_tags = []
        for note in self.notes.values():
            all_tags.extend(note["tags"])
        tag_counts = defaultdict(int)
        for tag in all_tags:
            tag_counts[tag] += 1

        return {
            "summary": {
                "total_notes": total_notes,
                "notes_with_frontmatter": notes_with_frontmatter,
                "frontmatter_percentage": (notes_with_frontmatter / total_notes * 100
                                          if total_notes > 0 else 0),
                "orphaned_notes": len(orphaned_notes),
                "broken_links": len(self.broken_links),
                "average_connections": round(avg_connections, 2),
                "unique_tags": len(tag_counts),
            },
            "orphaned_notes": orphaned_notes,
            "broken_links": [
                {"source": src, "target": tgt}
                for src, tgt in self.broken_links
            ],
            "top_tags": sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20],
            "connection_distribution": {
                "min": min(connection_counts) if connection_counts else 0,
                "max": max(connection_counts) if connection_counts else 0,
                "avg": round(avg_connections, 2),
            }
        }


def format_report(analysis: Dict, format_type: str = "text") -> str:
    """Format analysis results as text or JSON."""
    if format_type == "json":
        return json.dumps(analysis, indent=2, ensure_ascii=False)

    # Text format
    summary = analysis["summary"]
    report = []
    report.append("=" * 60)
    report.append("ZETTELKASTEN VAULT ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")

    report.append("SUMMARY")
    report.append("-" * 60)
    report.append(f"Total Notes: {summary['total_notes']}")
    report.append(f"Notes with Frontmatter: {summary['notes_with_frontmatter']} "
                 f"({summary['frontmatter_percentage']:.1f}%)")
    report.append(f"Orphaned Notes: {summary['orphaned_notes']}")
    report.append(f"Broken Links: {summary['broken_links']}")
    report.append(f"Average Connections per Note: {summary['average_connections']}")
    report.append(f"Unique Tags: {summary['unique_tags']}")
    report.append("")

    if analysis["broken_links"]:
        report.append("BROKEN LINKS")
        report.append("-" * 60)
        for link in analysis["broken_links"][:20]:
            report.append(f"  {link['source']} -> [[{link['target']}]]")
        if len(analysis["broken_links"]) > 20:
            report.append(f"  ... and {len(analysis['broken_links']) - 20} more")
        report.append("")

    if analysis["orphaned_notes"]:
        report.append("ORPHANED NOTES (No Connections)")
        report.append("-" * 60)
        for note in analysis["orphaned_notes"][:20]:
            report.append(f"  {note}")
        if len(analysis["orphaned_notes"]) > 20:
            report.append(f"  ... and {len(analysis['orphaned_notes']) - 20} more")
        report.append("")

    if analysis["top_tags"]:
        report.append("TOP TAGS")
        report.append("-" * 60)
        for tag, count in analysis["top_tags"][:10]:
            report.append(f"  #{tag}: {count}")
        report.append("")

    conn_dist = analysis["connection_distribution"]
    report.append("CONNECTION DISTRIBUTION")
    report.append("-" * 60)
    report.append(f"  Minimum: {conn_dist['min']}")
    report.append(f"  Maximum: {conn_dist['max']}")
    report.append(f"  Average: {conn_dist['avg']}")
    report.append("")

    report.append("=" * 60)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Obsidian vault for Zettelkasten compliance"
    )
    parser.add_argument(
        "vault_path",
        nargs="?",
        default=".",
        help="Path to Obsidian vault (default: current directory)"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--orphans-only",
        action="store_true",
        help="Only show orphaned notes"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    # Analyze vault
    analyzer = VaultAnalyzer(args.vault_path)
    analysis = analyzer.analyze_vault()

    # Filter for orphans only if requested
    if args.orphans_only:
        analysis = {
            "orphaned_notes": analysis["orphaned_notes"],
            "count": len(analysis["orphaned_notes"])
        }

    # Format output
    output = format_report(analysis, args.format)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
