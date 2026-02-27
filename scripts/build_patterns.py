#!/usr/bin/env python3
"""
Build script: Import patterns from pattern-engine into Hugo content.

Reads pattern markdown from the pattern-engine repo and generates:
- Individual pattern pages at content/patterns/<slug>.md
- Domain index pages (business, life, urban, ecology)
- Collection index pages (commons-blueprint, commons-engineer)
- Search index JSON for Fuse.js
"""

import os
import re
import json
import shutil
import yaml
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SITE_ROOT = SCRIPT_DIR.parent
PATTERN_ENGINE = Path(os.environ.get(
    "PATTERN_ENGINE_PATH",
    SITE_ROOT.parent / "pattern-engine"
))
CONTENT_PATTERNS = SITE_ROOT / "content" / "patterns"
STATIC_DIR = SITE_ROOT / "static" / "patterns"

# Map source folders to domain names
DOMAIN_MAP = {
    "life": "life",
    "urban": "urban",
    "business": "business",
    "ecology": "ecology",
}

COLLECTION_MAP = {
    "Commons Engineer Collection 01": "commons-engineer",
    "_core": "commons-engineer",  # core patterns are part of the engineer collection
}

# Domain metadata for index pages
DOMAIN_META = {
    "business": {
        "title": "Business Patterns",
        "icon": "building-2",
        "subtitle": "Tools for building organizations that thrive on change.",
        "sub_desc": "Organizations, enterprises, cooperatives, and ventures",
    },
    "life": {
        "title": "Life Patterns",
        "icon": "sprout",
        "subtitle": "The deep structures that underpin all living systems.",
        "sub_desc": "Core patterns of vitality, adaptation, and resilience",
    },
    "urban": {
        "title": "Urban Patterns",
        "icon": "landmark",
        "subtitle": "Patterns for cultivating resilient cities and civic infrastructure.",
        "sub_desc": "Cities, neighborhoods, public spaces, and urban systems",
    },
    "ecology": {
        "title": "Ecology Patterns",
        "icon": "trees",
        "subtitle": "Patterns for stewarding regenerative ecosystems.",
        "sub_desc": "Bioregional economies, natural commons, and regeneration",
    },
}


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None, text

    end = text.find("\n---", 3)
    if end == -1:
        return None, text

    fm_text = text[3:end]
    body = text[end + 4:]

    try:
        fm = yaml.safe_load(fm_text)
        if not isinstance(fm, dict):
            return None, text
        return fm, body
    except yaml.YAMLError:
        return None, text


def slug_from_filename(filepath):
    """Get slug from filename (without .md extension)."""
    return filepath.stem


def determine_domain(fm, source_folder):
    """Determine the commons domain from frontmatter or source folder."""
    # Check ontology.domain or ontology.commons_domain
    ontology = fm.get("ontology", {}) or {}
    domain = ontology.get("commons_domain", "")
    if not domain:
        domain = ontology.get("domain", "")

    # Normalize domain to string
    if isinstance(domain, list):
        domain = " ".join(str(d) for d in domain)
    domain = str(domain or "").lower()

    # Check classification
    classification = fm.get("classification", {}) or {}
    cd = classification.get("commons_domain", "")
    if isinstance(cd, list):
        cd = " ".join(str(d) for d in cd)
    cd = str(cd or "").lower()
    if not domain:
        domain = cd

    # Check top-level sector
    sector = str(fm.get("sector") or "").lower()

    # Check source folder
    folder = source_folder.lower()

    # Determine domain
    for key in DOMAIN_MAP:
        if key in domain or key in sector or key == folder:
            return key

    # Fallback: check cross_domains
    cross = ontology.get("cross_domains", []) or []
    for d in cross:
        if isinstance(d, str) and d.lower() in DOMAIN_MAP:
            return d.lower()

    return None


def build_hugo_frontmatter(fm, domain, collection, slug):
    """Build simplified Hugo-compatible frontmatter."""
    hugo_fm = {
        "title": fm.get("title", slug.replace("-", " ").title()),
        "slug": slug,
        "type": "pattern",
    }

    if fm.get("summary"):
        hugo_fm["summary"] = fm["summary"]

    if fm.get("aliases"):
        hugo_fm["aliases_list"] = fm["aliases"]

    # Tags for filtering
    tags = []
    if domain:
        tags.append(domain)
    if collection:
        tags.append(collection)

    # Universality level
    ontology = fm.get("ontology", {}) or {}
    tags_data = fm.get("tags", {}) or {}
    universality = tags_data.get("universality") or ontology.get("specification_layer", "")
    if universality:
        hugo_fm["universality"] = universality
        tags.append(universality)

    if tags:
        hugo_fm["tags"] = tags

    # Domain and collection
    if domain:
        hugo_fm["domain"] = domain
    if collection:
        hugo_fm["collection"] = collection

    # Commons assessment score
    commons = ontology.get("commons_assessment", {}) or {}
    vitality = commons.get("vitality")
    if vitality:
        hugo_fm["vitality_score"] = vitality

    # Orbital layer (v7 patterns)
    orbital = fm.get("orbital_layer")
    if orbital is not None:
        hugo_fm["orbital_layer"] = orbital

    return hugo_fm


def write_pattern(slug, hugo_fm, body, dest_dir):
    """Write a pattern markdown file with Hugo frontmatter."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slug}.md"

    # Build clean YAML frontmatter
    fm_str = yaml.dump(hugo_fm, default_flow_style=False, allow_unicode=True, sort_keys=False)

    dest.write_text(f"---\n{fm_str}---\n{body}", encoding="utf-8")
    return dest


def build_search_index(patterns):
    """Generate search-index.json for Fuse.js."""
    index = []
    for p in patterns:
        entry = {
            "title": p["title"],
            "url": f"/patterns/{p['slug']}/",
            "slug": p["slug"],
        }
        if p.get("summary"):
            entry["description"] = p["summary"][:200]
        if p.get("aliases_list"):
            entry["aliases"] = p["aliases_list"]
        if p.get("tags"):
            entry["tags"] = p["tags"]
        if p.get("domain"):
            entry["domain"] = p["domain"]
        if p.get("universality"):
            entry["level"] = p["universality"]
        index.append(entry)
    return index


def generate_domain_index(domain, count, patterns_in_domain):
    """Generate a domain index page (e.g., business/_index.md)."""
    meta = DOMAIN_META.get(domain, {
        "title": f"{domain.title()} Patterns",
        "icon": "hexagon",
        "subtitle": f"Patterns for the {domain} domain.",
        "sub_desc": "",
    })

    # Build pattern cards HTML
    cards_html = ""
    for p in sorted(patterns_in_domain, key=lambda x: x["title"]):
        universality = p.get("universality", "domain")
        cards_html += f'''        <a href="/patterns/{p["slug"]}/" class="pattern-card" data-universality="{universality}">
          <h3>{p["title"]}</h3>
          <div class="meta">
            <span class="tag">{universality.replace("_", "-").title() if universality else "Domain"}</span>
          </div>
        </a>
'''

    return f'''---
title: "{meta["title"]} - Commons Engineering"
type: "raw"
---

<style>
  .domain-hero {{
    text-align: center;
    padding: 60px 20px 40px;
  }}
  .domain-hero .hero-icon {{
    color: #3AAADC;
    margin-bottom: 20px;
  }}
  .domain-hero .hero-icon [data-lucide] {{
    width: 56px;
    height: 56px;
  }}
  .domain-hero h1 {{
    font-size: 2.4em;
    color: #2c3e50;
    margin: 0 0 10px 0;
    font-weight: 600;
    border: none;
  }}
  .domain-hero .subtitle {{
    color: #5a738e;
    font-size: 1.15em;
    max-width: 600px;
    margin: 0 auto 10px;
    line-height: 1.7;
  }}
  .domain-hero .sub-desc {{
    color: #8899aa;
    font-size: 0.95em;
    margin: 0;
  }}
  .stats-row {{
    display: flex;
    justify-content: center;
    gap: 50px;
    margin: 30px auto;
    flex-wrap: wrap;
    max-width: 600px;
  }}
  .stat-item {{ text-align: center; }}
  .stat-item .number {{
    font-size: 2em;
    font-weight: 700;
    color: #3AAADC;
  }}
  .stat-item .label {{
    color: #5a738e;
    font-size: 0.9em;
  }}
  .filter-bar {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 0 auto 30px;
    padding: 16px 20px;
    background: #f9fafb;
    border-radius: 10px;
    max-width: 900px;
    justify-content: center;
  }}
  .filter-btn {{
    padding: 8px 16px;
    border: 1px solid #e6e9ed;
    border-radius: 6px;
    background: white;
    cursor: pointer;
    font-size: 0.9em;
    color: #5a738e;
    transition: all 0.2s ease;
  }}
  .filter-btn:hover, .filter-btn.active {{
    border-color: #3AAADC;
    background: #f0f4f8;
    color: #3AAADC;
  }}
  .patterns-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 20px;
  }}
  .pattern-card {{
    background: white;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #e6e9ed;
    transition: all 0.3s ease;
    text-decoration: none;
    color: inherit;
    border-left: 3px solid transparent;
  }}
  .pattern-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    border-left-color: #3AAADC;
  }}
  .pattern-card h3 {{
    margin: 0 0 8px 0;
    color: #2c3e50;
    font-size: 1.05em;
    font-weight: 500;
  }}
  .pattern-card .meta {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .pattern-card .tag {{
    background: #f0f4f8;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 0.75em;
    color: #3AAADC;
  }}
  .back-link {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 20px;
    color: #3AAADC;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95em;
  }}
  .back-link:hover {{ color: #1e4a70; }}
</style>

<a href="/patterns/" class="back-link">&larr; Back to Patterns</a>

<div class="domain-hero">
  <div class="hero-icon"><i data-lucide="{meta["icon"]}"></i></div>
  <h1>{meta["title"]}</h1>
  <p class="subtitle">{meta["subtitle"]}</p>
  <p class="sub-desc">{meta["sub_desc"]}</p>
</div>

<div class="stats-row">
  <div class="stat-item">
    <div class="number">{count}</div>
    <div class="label">{meta["title"]}</div>
  </div>
</div>

<div class="filter-bar">
  <button class="filter-btn active" data-filter="all">All Patterns</button>
  <button class="filter-btn" data-filter="universal">Universal</button>
  <button class="filter-btn" data-filter="human-universal">Human-Universal</button>
  <button class="filter-btn" data-filter="domain">Domain</button>
  <button class="filter-btn" data-filter="context-specific">Context-Specific</button>
  <button class="filter-btn" data-filter="implementation">Implementation</button>
</div>

<div class="patterns-grid" id="patterns-container">
{cards_html}</div>

<script>
document.querySelectorAll('.filter-btn').forEach(function(btn) {{
  btn.addEventListener('click', function() {{
    document.querySelectorAll('.filter-btn').forEach(function(b) {{ b.classList.remove('active'); }});
    btn.classList.add('active');
    var filter = btn.dataset.filter;
    document.querySelectorAll('.pattern-card').forEach(function(card) {{
      if (filter === 'all' || card.dataset.universality === filter) {{
        card.style.display = 'block';
      }} else {{
        card.style.display = 'none';
      }}
    }});
  }});
}});
</script>
'''


def main():
    patterns_src = PATTERN_ENGINE / "_patterns"
    if not patterns_src.exists():
        print(f"ERROR: Pattern engine not found at {patterns_src}")
        return

    # Clean existing pattern pages (but keep _index.md and domain folders)
    print(f"Source: {patterns_src}")
    print(f"Destination: {CONTENT_PATTERNS}")

    all_patterns = []
    domain_patterns = {}
    collection_patterns = {}

    # Process each source folder
    for folder in sorted(patterns_src.iterdir()):
        if not folder.is_dir():
            continue

        folder_name = folder.name
        print(f"\nProcessing: {folder_name}/")

        # Determine if this is a domain or collection folder
        is_collection = folder_name in COLLECTION_MAP
        collection_name = COLLECTION_MAP.get(folder_name)
        domain_name = DOMAIN_MAP.get(folder_name.lower())

        md_files = list(folder.glob("*.md"))
        print(f"  Found {len(md_files)} patterns")

        for md_file in md_files:
            fm, body = parse_frontmatter(md_file)
            if fm is None:
                print(f"  SKIP (no frontmatter): {md_file.name}")
                continue

            slug = fm.get("slug") or slug_from_filename(md_file)
            if not slug:
                continue

            # Determine domain from frontmatter or folder
            domain = determine_domain(fm, folder_name) or domain_name

            # Build Hugo frontmatter
            hugo_fm = build_hugo_frontmatter(fm, domain, collection_name, slug)

            # Write pattern file
            write_pattern(slug, hugo_fm, body, CONTENT_PATTERNS)

            # Track for indexes
            pattern_data = {**hugo_fm}
            all_patterns.append(pattern_data)

            if domain:
                domain_patterns.setdefault(domain, []).append(pattern_data)

            if collection_name:
                collection_patterns.setdefault(collection_name, []).append(pattern_data)

    print(f"\n{'='*60}")
    print(f"Total patterns imported: {len(all_patterns)}")
    for d, ps in domain_patterns.items():
        print(f"  {d}: {len(ps)}")
    for c, ps in collection_patterns.items():
        print(f"  {c} (collection): {len(ps)}")

    # Generate domain index pages
    print("\nGenerating domain index pages...")
    for domain in ["business", "life", "urban", "ecology"]:
        domain_dir = CONTENT_PATTERNS / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        patterns_in = domain_patterns.get(domain, [])
        index_content = generate_domain_index(domain, len(patterns_in), patterns_in)
        (domain_dir / "_index.md").write_text(index_content, encoding="utf-8")
        print(f"  {domain}/_index.md ({len(patterns_in)} patterns)")

    # Generate collection index pages
    print("\nGenerating collection index pages...")
    for collection_name, patterns_in in collection_patterns.items():
        coll_dir = CONTENT_PATTERNS / collection_name
        coll_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "commons-engineer": {
                "title": "The Commons Engineer",
                "icon": "compass",
                "subtitle": "Patterns for developing the capabilities to see, design, build, and steward living systems.",
                "sub_desc": "A curated collection of patterns for the practitioner",
            },
            "commons-blueprint": {
                "title": "The Commons Blueprint",
                "icon": "map",
                "subtitle": "Foundational patterns for designing resilient, self-governing organizations.",
                "sub_desc": "A guided path through the pattern library",
            },
        }
        m = meta.get(collection_name, {"title": collection_name, "icon": "hexagon", "subtitle": "", "sub_desc": ""})
        DOMAIN_META[collection_name] = m
        index_content = generate_domain_index(collection_name, len(patterns_in), patterns_in)
        (coll_dir / "_index.md").write_text(index_content, encoding="utf-8")
        print(f"  {collection_name}/_index.md ({len(patterns_in)} patterns)")

    # Generate search index
    print("\nGenerating search index...")
    search_index = build_search_index(all_patterns)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    search_path = STATIC_DIR / "search-index.json"
    search_path.write_text(json.dumps(search_index, indent=None), encoding="utf-8")
    print(f"  {search_path} ({len(search_index)} entries)")

    print(f"\nDone! {len(all_patterns)} patterns ready for Hugo.")


if __name__ == "__main__":
    main()
