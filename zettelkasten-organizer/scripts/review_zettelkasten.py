#!/usr/bin/env python3
"""
Zettelkasten Review Script

Performs deep analysis of a Zettelkasten vault including:
- Content quality assessment
- Link graph analysis
- Cluster identification
- Connection strength evaluation
- Recommendation generation
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
from datetime import datetime


class ZettelkastenReviewer:
    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path).resolve()
        self.notes: Dict[str, Dict] = {}
        self.link_graph: Dict[str, Set[str]] = defaultdict(set)
        self.backlink_graph: Dict[str, Set[str]] = defaultdict(set)

    def load_vault_data(self):
        """Load vault data using analyze_vault script."""
        # We'll reuse logic from analyze_vault but extend it
        from analyze_vault import VaultAnalyzer

        analyzer = VaultAnalyzer(str(self.vault_path))
        analyzer.analyze_vault()

        self.notes = analyzer.notes
        self.link_graph = analyzer.link_graph
        self.backlink_graph = analyzer.backlink_graph

    def assess_note_quality(self, note_id: str) -> Dict:
        """Assess the quality of a single note."""
        note = self.notes[note_id]

        # Calculate metrics
        word_count = note["word_count"]
        outgoing_links = len(self.link_graph.get(note_id, set()))
        incoming_links = len(self.backlink_graph.get(note_id, set()))
        total_links = outgoing_links + incoming_links

        has_frontmatter = note["has_frontmatter"]
        has_tags = len(note["tags"]) > 0

        # Link density (links per 100 words)
        link_density = (outgoing_links / word_count * 100) if word_count > 0 else 0

        # Quality score (0-100)
        score = 0

        # Word count score (max 30 points)
        if word_count >= 100:
            score += 30
        elif word_count >= 50:
            score += 20
        elif word_count >= 20:
            score += 10

        # Connection score (max 40 points)
        if total_links >= 5:
            score += 40
        elif total_links >= 3:
            score += 30
        elif total_links >= 1:
            score += 20

        # Metadata score (max 30 points)
        if has_frontmatter:
            score += 15
        if has_tags:
            score += 15

        # Determine quality level
        if score >= 80:
            quality = "Excellent"
        elif score >= 60:
            quality = "Good"
        elif score >= 40:
            quality = "Fair"
        else:
            quality = "Needs Improvement"

        issues = []
        if word_count < 20:
            issues.append("Very short note (consider expanding)")
        if total_links == 0:
            issues.append("No connections (orphaned note)")
        elif total_links < 2:
            issues.append("Weak connections (add more links)")
        if not has_frontmatter:
            issues.append("Missing frontmatter metadata")
        if not has_tags:
            issues.append("No tags")
        if link_density < 1 and word_count > 50:
            issues.append("Low link density (consider adding context links)")

        return {
            "note_id": note_id,
            "quality": quality,
            "score": score,
            "metrics": {
                "word_count": word_count,
                "outgoing_links": outgoing_links,
                "incoming_links": incoming_links,
                "total_links": total_links,
                "link_density": round(link_density, 2),
                "has_frontmatter": has_frontmatter,
                "tag_count": len(note["tags"]),
            },
            "issues": issues,
        }

    def find_clusters(self, min_cluster_size: int = 3) -> List[Set[str]]:
        """Identify clusters of related notes using simple connected components."""
        visited = set()
        clusters = []

        def dfs(note_id: str, cluster: Set[str]):
            """Depth-first search to find connected notes."""
            if note_id in visited:
                return
            visited.add(note_id)
            cluster.add(note_id)

            # Visit linked notes
            for linked_note in self.link_graph.get(note_id, set()):
                dfs(linked_note, cluster)

            # Visit backlinking notes
            for backlinking_note in self.backlink_graph.get(note_id, set()):
                dfs(backlinking_note, cluster)

        for note_id in self.notes.keys():
            if note_id not in visited:
                cluster = set()
                dfs(note_id, cluster)
                if len(cluster) >= min_cluster_size:
                    clusters.append(cluster)

        return sorted(clusters, key=len, reverse=True)

    def identify_hub_notes(self, threshold: int = 5) -> List[Tuple[str, int]]:
        """Identify hub notes (notes with many connections)."""
        hubs = []

        for note_id in self.notes.keys():
            total_connections = (len(self.link_graph.get(note_id, set())) +
                               len(self.backlink_graph.get(note_id, set())))

            if total_connections >= threshold:
                hubs.append((note_id, total_connections))

        return sorted(hubs, key=lambda x: x[1], reverse=True)

    def suggest_connections(self, note_id: str, max_suggestions: int = 5) -> List[Dict]:
        """Suggest potential connections based on shared tags and links."""
        suggestions = []
        note = self.notes[note_id]
        note_tags = set(note["tags"])

        # Find notes with similar tags
        candidates = []
        for other_id, other_note in self.notes.items():
            if other_id == note_id:
                continue

            # Skip if already connected
            if (other_id in self.link_graph.get(note_id, set()) or
                other_id in self.backlink_graph.get(note_id, set())):
                continue

            other_tags = set(other_note["tags"])
            shared_tags = note_tags & other_tags

            if shared_tags:
                # Calculate similarity score
                tag_similarity = len(shared_tags) / max(len(note_tags), len(other_tags))

                # Check for common neighbors
                note_neighbors = (self.link_graph.get(note_id, set()) |
                                self.backlink_graph.get(note_id, set()))
                other_neighbors = (self.link_graph.get(other_id, set()) |
                                 self.backlink_graph.get(other_id, set()))
                common_neighbors = note_neighbors & other_neighbors

                neighbor_score = len(common_neighbors) * 0.2

                total_score = tag_similarity + neighbor_score

                candidates.append({
                    "note_id": other_id,
                    "score": total_score,
                    "shared_tags": list(shared_tags),
                    "common_neighbors": len(common_neighbors),
                })

        # Sort by score and return top suggestions
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:max_suggestions]

    def generate_recommendations(self) -> List[Dict]:
        """Generate actionable recommendations for improving the vault."""
        recommendations = []

        # Check for orphaned notes
        orphaned = []
        for note_id in self.notes.keys():
            outgoing = len(self.link_graph.get(note_id, set()))
            incoming = len(self.backlink_graph.get(note_id, set()))

            if outgoing == 0 and incoming == 0:
                orphaned.append(note_id)

        if orphaned:
            recommendations.append({
                "priority": "high",
                "category": "connectivity",
                "issue": f"Found {len(orphaned)} orphaned notes with no connections",
                "action": "Add links to connect these notes to your knowledge graph",
                "affected_notes": orphaned[:10],
            })

        # Check for weakly connected notes
        weak_notes = []
        for note_id in self.notes.keys():
            total_conn = (len(self.link_graph.get(note_id, set())) +
                         len(self.backlink_graph.get(note_id, set())))
            if 0 < total_conn < 2:
                weak_notes.append(note_id)

        if weak_notes:
            recommendations.append({
                "priority": "medium",
                "category": "connectivity",
                "issue": f"Found {len(weak_notes)} weakly connected notes (1 connection)",
                "action": "Add at least one more connection to strengthen the network",
                "affected_notes": weak_notes[:10],
            })

        # Check for notes without frontmatter
        no_frontmatter = [nid for nid, note in self.notes.items()
                         if not note["has_frontmatter"]]

        if no_frontmatter:
            recommendations.append({
                "priority": "medium",
                "category": "metadata",
                "issue": f"Found {len(no_frontmatter)} notes without YAML frontmatter",
                "action": "Add frontmatter with at minimum: tags, created date, and type",
                "affected_notes": no_frontmatter[:10],
            })

        # Check for notes without tags
        no_tags = [nid for nid, note in self.notes.items()
                  if len(note["tags"]) == 0]

        if no_tags:
            recommendations.append({
                "priority": "low",
                "category": "metadata",
                "issue": f"Found {len(no_tags)} notes without tags",
                "action": "Add relevant tags to improve discoverability",
                "affected_notes": no_tags[:10],
            })

        # Check for very short notes
        short_notes = [nid for nid, note in self.notes.items()
                      if note["word_count"] < 20]

        if short_notes:
            recommendations.append({
                "priority": "low",
                "category": "content",
                "issue": f"Found {len(short_notes)} very short notes (<20 words)",
                "action": "Expand these notes or consider if they should be merged",
                "affected_notes": short_notes[:10],
            })

        # Identify potential hub notes that need creation
        clusters = self.find_clusters(min_cluster_size=5)
        for i, cluster in enumerate(clusters[:5]):
            cluster_tags = []
            for note_id in cluster:
                cluster_tags.extend(self.notes[note_id]["tags"])

            if cluster_tags:
                common_tags = Counter(cluster_tags).most_common(3)
                recommendations.append({
                    "priority": "medium",
                    "category": "structure",
                    "issue": f"Found cluster of {len(cluster)} related notes without clear hub",
                    "action": f"Consider creating index note for cluster around: {', '.join([t[0] for t in common_tags])}",
                    "affected_notes": list(cluster)[:10],
                })

        return recommendations

    def review_vault(self) -> Dict:
        """Perform comprehensive vault review."""
        print(f"Reviewing Zettelkasten vault: {self.vault_path}")

        # Load data
        self.load_vault_data()
        print(f"Loaded {len(self.notes)} notes")

        # Assess note quality
        print("Assessing note quality...")
        quality_assessments = []
        quality_distribution = defaultdict(int)

        for note_id in self.notes.keys():
            assessment = self.assess_note_quality(note_id)
            quality_assessments.append(assessment)
            quality_distribution[assessment["quality"]] += 1

        # Sort by score
        quality_assessments.sort(key=lambda x: x["score"])

        # Find clusters
        print("Identifying clusters...")
        clusters = self.find_clusters()

        # Identify hubs
        print("Identifying hub notes...")
        hubs = self.identify_hub_notes()

        # Generate recommendations
        print("Generating recommendations...")
        recommendations = self.generate_recommendations()

        return {
            "vault_path": str(self.vault_path),
            "review_date": datetime.now().isoformat(),
            "quality_summary": {
                "distribution": dict(quality_distribution),
                "top_quality_notes": [
                    {"note_id": a["note_id"], "score": a["score"]}
                    for a in quality_assessments[-10:]
                ],
                "needs_attention": [
                    {"note_id": a["note_id"], "score": a["score"], "issues": a["issues"]}
                    for a in quality_assessments[:10]
                ],
            },
            "structure": {
                "cluster_count": len(clusters),
                "largest_clusters": [
                    {"size": len(c), "sample_notes": list(c)[:5]}
                    for c in clusters[:5]
                ],
                "hub_notes": [
                    {"note_id": nid, "connections": conn}
                    for nid, conn in hubs[:10]
                ],
            },
            "recommendations": recommendations,
        }


def format_review_report(review: Dict) -> str:
    """Format review results as readable text report."""
    report = []
    report.append("=" * 70)
    report.append("ZETTELKASTEN REVIEW REPORT")
    report.append("=" * 70)
    report.append(f"Vault: {review['vault_path']}")
    report.append(f"Review Date: {review['review_date']}")
    report.append("")

    # Quality Summary
    report.append("QUALITY SUMMARY")
    report.append("-" * 70)
    dist = review["quality_summary"]["distribution"]
    for quality in ["Excellent", "Good", "Fair", "Needs Improvement"]:
        count = dist.get(quality, 0)
        report.append(f"  {quality}: {count}")
    report.append("")

    # Notes needing attention
    needs_attention = review["quality_summary"]["needs_attention"]
    if needs_attention:
        report.append("NOTES NEEDING ATTENTION (Lowest Quality)")
        report.append("-" * 70)
        for note in needs_attention:
            report.append(f"  {note['note_id']} (Score: {note['score']})")
            for issue in note["issues"]:
                report.append(f"    - {issue}")
        report.append("")

    # Top quality notes
    top_notes = review["quality_summary"]["top_quality_notes"]
    if top_notes:
        report.append("TOP QUALITY NOTES")
        report.append("-" * 70)
        for note in reversed(top_notes):
            report.append(f"  {note['note_id']} (Score: {note['score']})")
        report.append("")

    # Structure
    structure = review["structure"]
    report.append("VAULT STRUCTURE")
    report.append("-" * 70)
    report.append(f"Identified Clusters: {structure['cluster_count']}")
    report.append(f"Hub Notes: {len(structure['hub_notes'])}")
    report.append("")

    if structure["hub_notes"]:
        report.append("TOP HUB NOTES (Most Connected)")
        report.append("-" * 70)
        for hub in structure["hub_notes"]:
            report.append(f"  {hub['note_id']} ({hub['connections']} connections)")
        report.append("")

    if structure["largest_clusters"]:
        report.append("LARGEST CLUSTERS")
        report.append("-" * 70)
        for i, cluster in enumerate(structure["largest_clusters"], 1):
            report.append(f"  Cluster {i}: {cluster['size']} notes")
            report.append(f"    Sample: {', '.join(cluster['sample_notes'][:3])}")
        report.append("")

    # Recommendations
    recommendations = review["recommendations"]
    if recommendations:
        report.append("RECOMMENDATIONS")
        report.append("-" * 70)

        # Group by priority
        for priority in ["high", "medium", "low"]:
            priority_recs = [r for r in recommendations if r["priority"] == priority]
            if priority_recs:
                report.append(f"\n{priority.upper()} PRIORITY:")
                for rec in priority_recs:
                    report.append(f"  [{rec['category'].upper()}] {rec['issue']}")
                    report.append(f"  → {rec['action']}")
                    if rec.get("affected_notes"):
                        count = len(rec["affected_notes"])
                        sample = ", ".join(rec["affected_notes"][:3])
                        report.append(f"    Examples: {sample}")
                        if count > 3:
                            report.append(f"    ... and {count - 3} more")
                    report.append("")

    report.append("=" * 70)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Review Zettelkasten vault quality and structure"
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
        "--output",
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    # Review vault
    reviewer = ZettelkastenReviewer(args.vault_path)
    review = reviewer.review_vault()

    # Format output
    if args.format == "json":
        output = json.dumps(review, indent=2, ensure_ascii=False)
    else:
        output = format_review_report(review)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nReport written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
