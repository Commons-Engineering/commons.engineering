#!/usr/bin/env python3
"""
Import curated pattern collections into Hugo content.
Fast script — only imports the small curated collections, not the full 16K.
"""
import os
import json
import yaml
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent
PATTERN_ENGINE = Path(os.environ.get(
    "PATTERN_ENGINE_PATH",
    SITE_ROOT.parent / "pattern-engine"
))
CONTENT = SITE_ROOT / "content" / "patterns"
STATIC = SITE_ROOT / "static" / "patterns"

SOURCES = {
    "commons-engineer": PATTERN_ENGINE / "_patterns" / "Commons Engineer Collection 01",
    "_core": PATTERN_ENGINE / "_patterns" / "_core",
}


def parse_fm(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    try:
        fm = yaml.safe_load(text[3:end])
        return (fm if isinstance(fm, dict) else None), text[end + 4:]
    except yaml.YAMLError:
        return None, text


def main():
    all_patterns = []
    seen_slugs = set()

    for source_name, source_dir in SOURCES.items():
        if not source_dir.exists():
            print(f"SKIP: {source_dir} not found")
            continue

        for md in sorted(source_dir.glob("*.md")):
            fm, body = parse_fm(md)
            if not fm:
                continue

            slug = fm.get("slug") or md.stem
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            title = fm.get("title", slug.replace("-", " ").title())
            summary = fm.get("summary", "")
            aliases = fm.get("aliases", [])

            # Determine domain from ontology
            ontology = fm.get("ontology", {}) or {}
            cross = ontology.get("cross_domains", []) or []
            domain_str = str(ontology.get("domain", ""))
            domain = None
            for d in ["life", "business", "urban", "ecology"]:
                if d in domain_str.lower() or d in [str(x).lower() for x in cross]:
                    domain = d
                    break

            # Universality
            universality = ""
            tags_data = fm.get("tags", {}) or {}
            if isinstance(tags_data, dict):
                universality = tags_data.get("universality", "")
            spec_layer = ontology.get("specification_layer", "")

            # Vitality
            commons = ontology.get("commons_assessment", {}) or {}
            vitality = commons.get("vitality")

            # Orbital
            orbital = fm.get("orbital_layer")

            # Build Hugo frontmatter
            hugo_fm = {
                "title": title,
                "slug": slug,
                "type": "pattern",
                "collection": "commons-engineer",
            }
            if summary:
                hugo_fm["summary"] = summary
            if aliases:
                hugo_fm["aliases_list"] = aliases
            if domain:
                hugo_fm["domain"] = domain
            if universality:
                hugo_fm["universality"] = universality
            if vitality:
                hugo_fm["vitality_score"] = vitality
            if orbital is not None:
                hugo_fm["orbital_layer"] = orbital

            tags = ["commons-engineer"]
            if domain:
                tags.append(domain)
            if universality:
                tags.append(universality)
            hugo_fm["tags"] = tags

            # Write
            dest = CONTENT / f"{slug}.md"
            fm_yaml = yaml.dump(hugo_fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
            dest.write_text(f"---\n{fm_yaml}---\n{body}", encoding="utf-8")

            all_patterns.append({
                "title": title,
                "slug": slug,
                "url": f"/patterns/{slug}/",
                "description": (summary or "")[:200],
                "aliases": aliases,
                "tags": tags,
                "domain": domain or "commons-engineering",
                "level": universality or spec_layer or "",
            })
            print(f"  {slug}")

    print(f"\nImported {len(all_patterns)} patterns")

    # Write search index
    STATIC.mkdir(parents=True, exist_ok=True)
    (STATIC / "search-index.json").write_text(
        json.dumps(all_patterns, indent=None), encoding="utf-8"
    )
    print(f"Search index: {len(all_patterns)} entries")


if __name__ == "__main__":
    main()
