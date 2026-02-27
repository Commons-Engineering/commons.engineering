#!/usr/bin/env python3
"""
Import child patterns for Commons Engineer and Commons Blueprint meta patterns
from the Commons-OS/patterns GitHub repository.
"""

import os
import re
import json
import urllib.request
import urllib.error
import yaml
import time

REPO_RAW = "https://raw.githubusercontent.com/Commons-OS/patterns/main/_patterns"
CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "patterns")
SEARCH_INDEX_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "patterns", "search-index.json")

COMMONS_ENGINEER_CHILDREN = [
    "systems-seeing", "purpose-articulation", "context-diagnosis",
    "leverage-point-identification", "mental-model-externalization", "engineering-attitude",
    "learning-in-public", "body-of-work-cultivation", "failure-disclosure",
    "method-documentation", "consistent-presence", "evidence-based-practice",
    "knowledge-productization", "intellectual-asset-design", "relationship-as-capital",
    "reputation-compounding", "offering-design", "value-capture-ethics",
    "observer-to-participant", "holding-a-view", "authentic-visibility",
    "integrity-under-pressure", "vulnerability-as-leadership", "narrative-courage",
    "relationship-engineering", "reciprocity-design", "collaborative-governance",
    "boundary-negotiation", "complementary-capability-matching", "conflict-as-signal",
    "community-of-practice-design", "collective-sensing", "pattern-sharing-practice",
    "mutual-accountability", "community-as-resilience", "stewardship-rotation",
    "living-system-design", "commons-as-practice", "blueprint-application",
    "lighthouse-initiation", "vitality-diagnosis", "generative-exit",
]

COMMONS_BLUEPRINT_CHILDREN = [
    "adaptive-learning", "alignment-monitoring", "anomaly-response",
    "capability-specification", "commons-boundary-definition",
    "community-and-participation-model", "compliance-and-regulatory-specification",
    "conflict-resolution-mechanism", "coordination-protocol",
    "culture-and-workforce-specification", "ecosystem-partnership-design",
    "environment-sensing", "feedback-escalation", "feedback-loop-governance",
    "gap-analysis", "governance-design", "graduated-sanctions",
    "human-agent-handoff", "journey-design", "justice-and-inclusion-specification",
    "legitimacy-and-consent", "market-environment-specification",
    "multi-speed-feedback", "nested-systems-architecture", "operational-cadence",
    "organization-design", "pattern-lifecycle", "performance-sensing",
    "purpose-definition", "resource-orchestration", "scenario-specification",
    "self-organization-and-subsidiarity", "solution-architecture",
    "stakeholder-architecture", "structural-integrity-audit",
    "time-sliced-specification", "transformation-sequencing",
    "transparency-and-openness-protocol", "transparent-operations",
    "value-proposition-design", "value-stream-specification",
]

def fetch_pattern(slug):
    """Download a pattern from Commons-OS/patterns repo."""
    url = f"{REPO_RAW}/{slug}.md"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "commons-engineering-import/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"  [SKIP] {slug}: HTTP {e.code}")
        return None
    except Exception as e:
        print(f"  [ERROR] {slug}: {e}")
        return None

def parse_frontmatter(content):
    """Parse YAML frontmatter from a pattern file."""
    # Handle frontmatter with or without leading ---
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
        else:
            fm_text = parts[1]
            body = ""
    else:
        # Some files start with comments before ---
        idx = content.find("---")
        if idx >= 0:
            rest = content[idx+3:]
            idx2 = rest.find("---")
            if idx2 >= 0:
                fm_text = rest[:idx2]
                body = rest[idx2+3:].strip()
            else:
                fm_text = rest
                body = ""
        else:
            # Try parsing the whole thing as YAML (no --- delimiters, just yaml then markdown)
            # Find where the body starts (first markdown heading or blank line after yaml)
            fm_text = content
            body = ""

    try:
        fm = yaml.safe_load(fm_text)
        if not isinstance(fm, dict):
            return None, content
        return fm, body
    except yaml.YAMLError:
        return None, content

def slug_to_title(slug):
    """Convert a slug to a title."""
    return slug.replace("-", " ").title()

def determine_domain(fm):
    """Extract domain from frontmatter."""
    ontology = fm.get("ontology", {})
    if isinstance(ontology, dict):
        domain = ontology.get("domain", "")
        if isinstance(domain, list):
            domain = domain[0] if domain else ""
        return str(domain).lower()
    return ""

def determine_collection(slug):
    """Determine which collection a pattern belongs to."""
    collections = []
    if slug in COMMONS_ENGINEER_CHILDREN:
        collections.append("commons-engineer")
    if slug in COMMONS_BLUEPRINT_CHILDREN:
        collections.append("commons-blueprint")
    return collections

def extract_summary(fm):
    """Extract summary from frontmatter."""
    return fm.get("summary", "")

def extract_aliases(fm):
    """Extract aliases from frontmatter."""
    aliases = fm.get("aliases", [])
    if isinstance(aliases, list):
        return [str(a) for a in aliases]
    return []

def extract_vitality(fm):
    """Extract vitality score from frontmatter."""
    ontology = fm.get("ontology", {})
    if isinstance(ontology, dict):
        ca = ontology.get("commons_assessment", {})
        if isinstance(ca, dict):
            return ca.get("vitality", ca.get("overall_score", 0))
        elif isinstance(ca, list):
            for item in ca:
                if isinstance(item, dict) and item.get("dimension") == "Vitality":
                    return item.get("score", 0)
    return 0

def create_hugo_pattern(slug, fm, body, collections):
    """Create a Hugo content file for a pattern."""
    title = fm.get("title", slug_to_title(slug))
    summary = extract_summary(fm)
    aliases = extract_aliases(fm)
    domain = determine_domain(fm)
    vitality = extract_vitality(fm)

    tags = list(collections)
    if domain and domain not in tags:
        tags.append(domain)

    # Build Hugo frontmatter
    hugo_fm = {
        "title": title,
        "slug": slug,
        "type": "pattern",
        "summary": summary,
    }
    if collections:
        hugo_fm["collection"] = collections[0]
    if aliases:
        hugo_fm["aliases_list"] = aliases
    if tags:
        hugo_fm["tags"] = tags
    if domain:
        hugo_fm["domain"] = domain
    if vitality:
        hugo_fm["vitality_score"] = vitality

    # Build the file content
    fm_yaml = yaml.dump(hugo_fm, default_flow_style=False, allow_unicode=True, sort_keys=False)

    output = f"---\n{fm_yaml}---\n\n{body}\n"

    # Write the file
    filepath = os.path.join(CONTENT_DIR, f"{slug}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output)

    return {"slug": slug, "title": title, "summary": summary, "collection": collections}

def main():
    os.makedirs(CONTENT_DIR, exist_ok=True)

    # Combine all unique slugs
    all_slugs = sorted(set(COMMONS_ENGINEER_CHILDREN + COMMONS_BLUEPRINT_CHILDREN))
    print(f"Total unique child patterns to import: {len(all_slugs)}")

    search_entries = []
    imported = 0
    skipped = 0

    for i, slug in enumerate(all_slugs):
        collections = determine_collection(slug)
        filepath = os.path.join(CONTENT_DIR, f"{slug}.md")

        # Check if already exists
        if os.path.exists(filepath):
            print(f"  [{i+1}/{len(all_slugs)}] {slug} — already exists, updating...")

        print(f"  [{i+1}/{len(all_slugs)}] Fetching {slug}...")
        raw = fetch_pattern(slug)

        if raw is None:
            skipped += 1
            continue

        fm, body = parse_frontmatter(raw)
        if fm is None:
            print(f"  [SKIP] {slug}: could not parse frontmatter")
            skipped += 1
            continue

        result = create_hugo_pattern(slug, fm, body, collections)
        imported += 1

        search_entries.append({
            "title": result["title"],
            "url": f"/patterns/{slug}/",
            "summary": result["summary"][:200] if result["summary"] else "",
            "collection": ", ".join(result["collection"]),
        })

        # Be nice to GitHub
        if i % 10 == 9:
            time.sleep(0.5)

    # Also add the existing local patterns to search index
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith(".md") and not filename.startswith("_"):
            slug = filename[:-3]
            if slug not in [e["slug"] for e in [{"slug": s} for s in all_slugs]]:
                filepath = os.path.join(CONTENT_DIR, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    fm, _ = parse_frontmatter(content)
                    if fm and isinstance(fm, dict):
                        title = fm.get("title", slug_to_title(slug))
                        summary = fm.get("summary", "")
                        collection = fm.get("collection", "")
                        search_entries.append({
                            "title": title,
                            "url": f"/patterns/{slug}/",
                            "summary": summary[:200] if summary else "",
                            "collection": collection,
                        })
                except:
                    pass

    # Write search index
    os.makedirs(os.path.dirname(SEARCH_INDEX_PATH), exist_ok=True)
    with open(SEARCH_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(search_entries, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Imported: {imported}, Skipped: {skipped}")
    print(f"Search index: {len(search_entries)} entries written to {SEARCH_INDEX_PATH}")

if __name__ == "__main__":
    main()
