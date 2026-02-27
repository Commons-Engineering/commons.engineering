#!/usr/bin/env python3
"""
Build script: Import patterns from pattern-engine into Hugo content.

Reads pattern markdown from the pattern-engine repo and generates:
- Individual pattern pages for collections and featured patterns (Hugo content)
- Domain JSON indexes for virtual-scrolling filter pages
- Domain-chunked search indexes for lazy-loading Fuse.js
- R2-ready pattern files for Cloudflare Worker rendering
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
R2_STAGING = SITE_ROOT / "r2-staging"  # Patterns staged for R2 upload

# Map source folders to domain names
DOMAIN_MAP = {
    "life": "life",
    "urban": "urban",
    "business": "business",
    "ecology": "ecology",
}

COLLECTION_MAP = {
    "Commons Engineer Collection 01": "commons-engineer",
    "_core": "commons-engineer",
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

# Urban-specific dimension labels
URBAN_DIMENSIONS = {
    "Purpose": {"icon": "compass", "color": "#8b5cf6"},
    "Agents": {"icon": "users", "color": "#f59e0b"},
    "Offers": {"icon": "package", "color": "#3b82f6"},
    "Operations": {"icon": "settings", "color": "#10b981"},
    "Governance": {"icon": "shield", "color": "#ef4444"},
    "CE-Specific": {"icon": "star", "color": "#6366f1"},
}

# Layer labels
LAYER_LABELS = {
    "L1": "Universal",
    "L2": "Cross-Domain",
    "L3": "Domain-Specific",
    "L4": "Context-Specific",
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
    ontology = fm.get("ontology", {}) or {}
    domain = ontology.get("commons_domain", "")
    if not domain:
        domain = ontology.get("domain", "")

    if isinstance(domain, list):
        domain = " ".join(str(d) for d in domain)
    domain = str(domain or "").lower()

    classification = fm.get("classification", {}) or {}
    cd = classification.get("commons_domain", "")
    if isinstance(cd, list):
        cd = " ".join(str(d) for d in cd)
    cd = str(cd or "").lower()
    if not domain:
        domain = cd

    sector = str(fm.get("sector") or "").lower()
    folder = source_folder.lower()

    for key in DOMAIN_MAP:
        if key in domain or key in sector or key == folder:
            return key

    cross = ontology.get("cross_domains", []) or []
    for d in cross:
        if isinstance(d, str) and d.lower() in DOMAIN_MAP:
            return d.lower()

    return None


def extract_layer(fm):
    """Extract the layer code (L1, L2, L3, L4) from frontmatter."""
    ontology = fm.get("ontology", {}) or {}
    layer_str = str(ontology.get("layer", "") or "")
    for code in ["L1", "L2", "L3", "L4"]:
        if code in layer_str:
            return code
    # Fallback to specification_layer
    spec_layer = str(ontology.get("specification_layer", "") or "")
    for code in ["L0", "L1", "L2", "L3", "L4"]:
        if code in spec_layer:
            return code
    return "L1"


def extract_dimension(fm):
    """Extract the urban_dimension (or equivalent category) from frontmatter."""
    ontology = fm.get("ontology", {}) or {}
    dim = ontology.get("urban_dimension", "")
    if dim:
        return str(dim)
    # Fallback for non-urban domains
    return ""


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

    tags = []
    if domain:
        tags.append(domain)
    if collection:
        tags.append(collection)

    ontology = fm.get("ontology", {}) or {}
    tags_data = fm.get("tags", {}) or {}
    universality = tags_data.get("universality") or ontology.get("specification_layer", "")
    if universality:
        hugo_fm["universality"] = universality
        tags.append(universality)

    if tags:
        hugo_fm["tags"] = tags

    if domain:
        hugo_fm["domain"] = domain
    if collection:
        hugo_fm["collection"] = collection

    commons = ontology.get("commons_assessment", {}) or {}
    vitality = commons.get("vitality")
    if vitality:
        hugo_fm["vitality_score"] = vitality

    orbital = fm.get("orbital_layer")
    if orbital is not None:
        hugo_fm["orbital_layer"] = orbital

    return hugo_fm


def write_pattern(slug, hugo_fm, body, dest_dir):
    """Write a pattern markdown file with Hugo frontmatter."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slug}.md"
    fm_str = yaml.dump(hugo_fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    dest.write_text(f"---\n{fm_str}---\n{body}", encoding="utf-8")
    return dest


def build_domain_index(patterns_in_domain):
    """Generate a lightweight JSON index for the domain filter page.
    
    Each entry is minimal: slug, title, layer, dimension, summary snippet.
    Target: ~100 bytes per entry for fast loading.
    """
    index = []
    for p in sorted(patterns_in_domain, key=lambda x: x["title"]):
        entry = {
            "s": p["slug"],                                    # slug
            "t": p["title"],                                   # title
            "l": p.get("layer", "L1"),                         # layer code
            "d": p.get("dimension", ""),                       # dimension/category
        }
        # Add truncated summary if available (first 120 chars)
        summary = p.get("summary", "")
        if summary:
            entry["m"] = summary[:120]
        index.append(entry)
    return index


def build_search_index(patterns):
    """Generate a search index chunk for Fuse.js."""
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


def stage_for_r2(slug, raw_text, domain):
    """Stage a pattern's raw markdown for R2 upload."""
    domain_dir = R2_STAGING / (domain or "uncategorized")
    domain_dir.mkdir(parents=True, exist_ok=True)
    dest = domain_dir / f"{slug}.md"
    dest.write_text(raw_text, encoding="utf-8")


def generate_domain_filter_page(domain, count, dimensions_count, layers_count):
    """Generate a domain index page with dynamic filter loading from JSON."""
    meta = DOMAIN_META.get(domain, {
        "title": f"{domain.title()} Patterns",
        "icon": "hexagon",
        "subtitle": f"Patterns for the {domain} domain.",
        "sub_desc": "",
    })

    # Build dimension filter buttons (only for domains that have them)
    dimension_buttons = ""
    if dimensions_count:
        for dim_name, dim_count in sorted(dimensions_count.items(), key=lambda x: -x[1]):
            dim_info = URBAN_DIMENSIONS.get(dim_name, {"icon": "tag", "color": "#64748b"})
            dimension_buttons += f'    <button class="filter-chip" data-dimension="{dim_name}"><i data-lucide="{dim_info["icon"]}" style="width:14px;height:14px;"></i> {dim_name} <span class="chip-count">{dim_count:,}</span></button>\n'

    # Build layer filter buttons
    layer_buttons = ""
    for layer_code, layer_count in sorted(layers_count.items(), key=lambda x: x[0]):
        label = LAYER_LABELS.get(layer_code, layer_code)
        layer_buttons += f'    <button class="filter-chip" data-layer="{layer_code}">{label} <span class="chip-count">{layer_count:,}</span></button>\n'

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

  /* Filter Controls */
  .filter-controls {{
    max-width: 1100px;
    margin: 0 auto 24px;
    padding: 0 20px;
  }}
  .filter-search {{
    width: 100%;
    max-width: 500px;
    margin: 0 auto 16px;
    display: block;
    padding: 12px 16px 12px 42px;
    border: 1px solid #e6e9ed;
    border-radius: 8px;
    font-size: 1em;
    color: #2c3e50;
    background: white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%238899aa' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E") 14px center no-repeat;
    transition: border-color 0.2s;
  }}
  .filter-search:focus {{
    outline: none;
    border-color: #3AAADC;
    box-shadow: 0 0 0 3px rgba(58,170,220,0.1);
  }}
  .filter-groups {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 8px;
  }}
  .filter-group-label {{
    font-size: 0.8em;
    color: #8899aa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    width: 100%;
    text-align: center;
    margin: 8px 0 4px;
  }}
  .filter-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border: 1px solid #e6e9ed;
    border-radius: 20px;
    background: white;
    cursor: pointer;
    font-size: 0.85em;
    color: #5a738e;
    transition: all 0.2s ease;
  }}
  .filter-chip:hover {{
    border-color: #3AAADC;
    color: #3AAADC;
  }}
  .filter-chip.active {{
    border-color: #3AAADC;
    background: #f0f9ff;
    color: #3AAADC;
    font-weight: 500;
  }}
  .chip-count {{
    font-size: 0.85em;
    color: #aab;
    font-weight: 400;
  }}
  .filter-chip.active .chip-count {{
    color: #3AAADC;
  }}
  .filter-status {{
    text-align: center;
    color: #8899aa;
    font-size: 0.9em;
    margin: 12px 0;
  }}
  .filter-status strong {{
    color: #3AAADC;
  }}

  /* Virtual scroll container */
  .patterns-viewport {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 20px;
    height: 70vh;
    overflow-y: auto;
    position: relative;
  }}
  .patterns-spacer {{
    position: relative;
  }}
  .patterns-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
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
    margin: 0 0 6px 0;
    color: #2c3e50;
    font-size: 1em;
    font-weight: 500;
  }}
  .pattern-card .card-meta {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 6px;
  }}
  .pattern-card .tag {{
    background: #f1f5f9;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75em;
    color: #64748b;
  }}
  .pattern-card .tag-layer {{ background: #ede9fe; color: #7c3aed; }}
  .pattern-card .tag-dim {{ background: #e0f2fe; color: #0369a1; }}
  .pattern-card p {{
    color: #5a738e;
    font-size: 0.85em;
    line-height: 1.5;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
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
  .loading-indicator {{
    text-align: center;
    padding: 40px;
    color: #8899aa;
  }}
  .loading-indicator .spinner {{
    display: inline-block;
    width: 32px;
    height: 32px;
    border: 3px solid #e6e9ed;
    border-top-color: #3AAADC;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
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
    <div class="number" id="total-count">{count:,}</div>
    <div class="label">Patterns</div>
  </div>
</div>

<div class="filter-controls">
  <input type="text" class="filter-search" id="domain-search" placeholder="Search within {meta['title'].lower()}..." autocomplete="off">

  <div class="filter-groups" id="layer-filters">
    <div class="filter-group-label">Layer</div>
    <button class="filter-chip active" data-layer="all">All</button>
{layer_buttons}  </div>

  {"<div class='filter-groups' id='dimension-filters'><div class='filter-group-label'>Dimension</div><button class='filter-chip active' data-dimension='all'>All</button>" + dimension_buttons + "</div>" if dimension_buttons else ""}

  <div class="filter-status" id="filter-status">Showing <strong>{count:,}</strong> patterns</div>
</div>

<div class="patterns-viewport" id="viewport">
  <div class="loading-indicator" id="loading">
    <div class="spinner"></div>
    <p>Loading patterns...</p>
  </div>
  <div class="patterns-spacer" id="spacer" style="display:none;">
    <div class="patterns-grid" id="grid"></div>
  </div>
</div>

<script>
(function() {{
  const DOMAIN = "{domain}";
  const CARD_HEIGHT = 120;  // Estimated card height in px
  const COLS = 3;           // Will be recalculated
  const BUFFER = 5;         // Extra rows to render above/below viewport

  let allPatterns = [];
  let filtered = [];
  let activeLayer = "all";
  let activeDimension = "all";
  let searchQuery = "";

  // Load domain index
  fetch("/patterns/domain-index-" + DOMAIN + ".json")
    .then(r => r.json())
    .then(data => {{
      allPatterns = data;
      filtered = data;
      document.getElementById("loading").style.display = "none";
      document.getElementById("spacer").style.display = "block";
      renderVirtual();
    }})
    .catch(err => {{
      document.getElementById("loading").innerHTML =
        "<p>Failed to load patterns. Please try again later.</p>";
    }});

  // Filter logic
  function applyFilters() {{
    filtered = allPatterns.filter(p => {{
      if (activeLayer !== "all" && p.l !== activeLayer) return false;
      if (activeDimension !== "all" && p.d !== activeDimension) return false;
      if (searchQuery) {{
        const q = searchQuery.toLowerCase();
        const title = (p.t || "").toLowerCase();
        const summary = (p.m || "").toLowerCase();
        if (!title.includes(q) && !summary.includes(q)) return false;
      }}
      return true;
    }});
    document.getElementById("filter-status").innerHTML =
      "Showing <strong>" + filtered.length.toLocaleString() + "</strong> patterns";
    renderVirtual();
  }}

  // Layer filter clicks
  document.querySelectorAll("[data-layer]").forEach(btn => {{
    btn.addEventListener("click", function() {{
      document.querySelectorAll("[data-layer]").forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      activeLayer = this.dataset.layer;
      applyFilters();
    }});
  }});

  // Dimension filter clicks
  document.querySelectorAll("[data-dimension]").forEach(btn => {{
    btn.addEventListener("click", function() {{
      document.querySelectorAll("[data-dimension]").forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      activeDimension = this.dataset.dimension;
      applyFilters();
    }});
  }});

  // Search input
  let searchTimeout;
  document.getElementById("domain-search").addEventListener("input", function() {{
    clearTimeout(searchTimeout);
    const val = this.value.trim();
    searchTimeout = setTimeout(() => {{
      searchQuery = val;
      applyFilters();
    }}, 200);
  }});

  // Virtual scrolling
  const viewport = document.getElementById("viewport");
  const spacer = document.getElementById("spacer");
  const grid = document.getElementById("grid");

  function getColCount() {{
    const w = viewport.clientWidth - 40; // minus padding
    return Math.max(1, Math.floor(w / 296)); // 280 + 16 gap
  }}

  function renderVirtual() {{
    const cols = getColCount();
    const rowHeight = CARD_HEIGHT + 16; // card + gap
    const totalRows = Math.ceil(filtered.length / cols);
    const totalHeight = totalRows * rowHeight;
    spacer.style.height = totalHeight + "px";

    const scrollTop = viewport.scrollTop;
    const viewportHeight = viewport.clientHeight;

    const startRow = Math.max(0, Math.floor(scrollTop / rowHeight) - BUFFER);
    const endRow = Math.min(totalRows, Math.ceil((scrollTop + viewportHeight) / rowHeight) + BUFFER);

    const startIdx = startRow * cols;
    const endIdx = Math.min(filtered.length, endRow * cols);

    grid.style.top = (startRow * rowHeight) + "px";

    let html = "";
    for (let i = startIdx; i < endIdx; i++) {{
      const p = filtered[i];
      const layerLabel = {{"L1":"Universal","L2":"Cross-Domain","L3":"Domain-Specific","L4":"Context-Specific"}}[p.l] || p.l;
      html += '<a href="/patterns/' + p.s + '/" class="pattern-card">' +
        '<h3>' + escHtml(p.t) + '</h3>' +
        '<div class="card-meta">' +
          '<span class="tag tag-layer">' + layerLabel + '</span>' +
          (p.d ? '<span class="tag tag-dim">' + escHtml(p.d) + '</span>' : '') +
        '</div>' +
        (p.m ? '<p>' + escHtml(p.m) + '</p>' : '') +
        '</a>';
    }}
    grid.innerHTML = html;
  }}

  function escHtml(s) {{
    if (!s) return "";
    return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }}

  viewport.addEventListener("scroll", renderVirtual);
  window.addEventListener("resize", renderVirtual);

  // Re-init lucide icons after load
  setTimeout(() => {{ if (window.lucide) lucide.createIcons(); }}, 100);
}})();
</script>
'''


def generate_collection_page(collection_name, count, patterns_in):
    """Generate a collection index page with static cards (small collections)."""
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
    m = meta.get(collection_name, {
        "title": collection_name.replace("-", " ").title(),
        "icon": "hexagon",
        "subtitle": "",
        "sub_desc": "",
    })

    cards_html = ""
    for p in sorted(patterns_in, key=lambda x: x["title"]):
        universality = p.get("universality", "domain")
        cards_html += f'''        <a href="/patterns/{p["slug"]}/" class="pattern-card" data-universality="{universality}">
          <h3>{p["title"]}</h3>
          <div class="meta">
            <span class="tag">{universality.replace("_", "-").title() if universality else "Domain"}</span>
          </div>
        </a>
'''

    return f'''---
title: "{m["title"]} - Commons Engineering"
type: "raw"
---

<style>
  .domain-hero {{ text-align: center; padding: 60px 20px 40px; }}
  .domain-hero .hero-icon {{ color: #3AAADC; margin-bottom: 20px; }}
  .domain-hero .hero-icon [data-lucide] {{ width: 56px; height: 56px; }}
  .domain-hero h1 {{ font-size: 2.4em; color: #2c3e50; margin: 0 0 10px 0; font-weight: 600; border: none; }}
  .domain-hero .subtitle {{ color: #5a738e; font-size: 1.15em; max-width: 600px; margin: 0 auto 10px; line-height: 1.7; }}
  .domain-hero .sub-desc {{ color: #8899aa; font-size: 0.95em; margin: 0; }}
  .stats-row {{ display: flex; justify-content: center; gap: 50px; margin: 30px auto; flex-wrap: wrap; max-width: 600px; }}
  .stat-item {{ text-align: center; }}
  .stat-item .number {{ font-size: 2em; font-weight: 700; color: #3AAADC; }}
  .stat-item .label {{ color: #5a738e; font-size: 0.9em; }}
  .filter-bar {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 0 auto 30px; padding: 16px 20px; background: #f9fafb; border-radius: 10px; max-width: 900px; justify-content: center; }}
  .filter-btn {{ padding: 8px 16px; border: 1px solid #e6e9ed; border-radius: 6px; background: white; cursor: pointer; font-size: 0.9em; color: #5a738e; transition: all 0.2s ease; }}
  .filter-btn:hover, .filter-btn.active {{ border-color: #3AAADC; background: #f0f4f8; color: #3AAADC; }}
  .patterns-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; max-width: 1100px; margin: 0 auto; padding: 0 20px; }}
  .pattern-card {{ background: white; border-radius: 8px; padding: 20px; border: 1px solid #e6e9ed; transition: all 0.3s ease; text-decoration: none; color: inherit; border-left: 3px solid transparent; }}
  .pattern-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.06); border-left-color: #3AAADC; }}
  .pattern-card h3 {{ margin: 0 0 8px 0; color: #2c3e50; font-size: 1.05em; font-weight: 500; }}
  .pattern-card .meta {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .pattern-card .tag {{ background: #f1f5f9; padding: 3px 10px; border-radius: 4px; font-size: 0.75em; color: #3AAADC; }}
  .back-link {{ display: inline-flex; align-items: center; gap: 6px; padding: 10px 20px; color: #3AAADC; text-decoration: none; font-weight: 500; font-size: 0.95em; }}
  .back-link:hover {{ color: #1e4a70; }}
</style>

<a href="/patterns/" class="back-link">&larr; Back to Patterns</a>

<div class="domain-hero">
  <div class="hero-icon"><i data-lucide="{m["icon"]}"></i></div>
  <h1>{m["title"]}</h1>
  <p class="subtitle">{m["subtitle"]}</p>
  <p class="sub-desc">{m["sub_desc"]}</p>
</div>

<div class="stats-row">
  <div class="stat-item">
    <div class="number">{count}</div>
    <div class="label">Patterns</div>
  </div>
</div>

<div class="patterns-grid" id="patterns-container">
{cards_html}</div>
'''


def main():
    patterns_src = PATTERN_ENGINE / "_patterns"
    if not patterns_src.exists():
        print(f"ERROR: Pattern engine not found at {patterns_src}")
        return

    print(f"Source: {patterns_src}")
    print(f"Destination: {CONTENT_PATTERNS}")

    # Clean R2 staging
    if R2_STAGING.exists():
        shutil.rmtree(R2_STAGING)
    R2_STAGING.mkdir(parents=True)

    all_patterns = []
    domain_patterns = {}
    collection_patterns = {}
    domain_dimensions = {}  # domain -> {dimension: count}
    domain_layers = {}      # domain -> {layer: count}

    # Process each source folder
    for folder in sorted(patterns_src.iterdir()):
        if not folder.is_dir():
            continue

        folder_name = folder.name
        print(f"\nProcessing: {folder_name}/")

        is_collection = folder_name in COLLECTION_MAP
        collection_name = COLLECTION_MAP.get(folder_name)
        domain_name = DOMAIN_MAP.get(folder_name.lower())

        md_files = list(folder.glob("*.md"))
        print(f"  Found {len(md_files)} patterns")

        for md_file in md_files:
            raw_text = md_file.read_text(encoding="utf-8", errors="replace")
            fm, body = parse_frontmatter(md_file)
            if fm is None:
                print(f"  SKIP (no frontmatter): {md_file.name}")
                continue

            slug = fm.get("slug") or slug_from_filename(md_file)
            if not slug:
                continue

            domain = determine_domain(fm, folder_name) or domain_name
            layer = extract_layer(fm)
            dimension = extract_dimension(fm)

            # Build Hugo frontmatter
            hugo_fm = build_hugo_frontmatter(fm, domain, collection_name, slug)

            # For collections and core patterns: write as Hugo content pages
            if is_collection:
                write_pattern(slug, hugo_fm, body, CONTENT_PATTERNS)

            # Stage ALL patterns for R2 (including collections)
            stage_for_r2(slug, raw_text, domain)

            # Track for indexes
            pattern_data = {
                **hugo_fm,
                "layer": layer,
                "dimension": dimension,
            }
            all_patterns.append(pattern_data)

            if domain:
                domain_patterns.setdefault(domain, []).append(pattern_data)
                # Track dimensions and layers per domain
                if dimension:
                    domain_dimensions.setdefault(domain, {})
                    domain_dimensions[domain][dimension] = domain_dimensions[domain].get(dimension, 0) + 1
                domain_layers.setdefault(domain, {})
                domain_layers[domain][layer] = domain_layers[domain].get(layer, 0) + 1

            if collection_name:
                collection_patterns.setdefault(collection_name, []).append(pattern_data)

    print(f"\n{'='*60}")
    print(f"Total patterns processed: {len(all_patterns)}")
    for d, ps in domain_patterns.items():
        print(f"  {d}: {len(ps)}")
    for c, ps in collection_patterns.items():
        print(f"  {c} (collection): {len(ps)}")

    # Generate domain filter pages (with JSON index loading)
    print("\nGenerating domain filter pages...")
    for domain in ["business", "life", "urban", "ecology"]:
        domain_dir = CONTENT_PATTERNS / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        patterns_in = domain_patterns.get(domain, [])
        dims = domain_dimensions.get(domain, {})
        layers = domain_layers.get(domain, {})

        if len(patterns_in) > 500:
            # Large domain: use virtual-scrolling filter page
            index_content = generate_domain_filter_page(domain, len(patterns_in), dims, layers)
        else:
            # Small domain: use static cards (existing approach)
            DOMAIN_META_COPY = dict(DOMAIN_META)
            index_content = generate_collection_page(domain, len(patterns_in), patterns_in)

        (domain_dir / "_index.md").write_text(index_content, encoding="utf-8")
        print(f"  {domain}/_index.md ({len(patterns_in)} patterns, {'dynamic' if len(patterns_in) > 500 else 'static'})")

    # Generate collection index pages (always static, small)
    print("\nGenerating collection index pages...")
    for coll_name, patterns_in in collection_patterns.items():
        coll_dir = CONTENT_PATTERNS / coll_name
        coll_dir.mkdir(parents=True, exist_ok=True)
        index_content = generate_collection_page(coll_name, len(patterns_in), patterns_in)
        (coll_dir / "_index.md").write_text(index_content, encoding="utf-8")
        print(f"  {coll_name}/_index.md ({len(patterns_in)} patterns)")

    # Generate domain JSON indexes (for filter pages)
    print("\nGenerating domain JSON indexes...")
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    for domain, patterns_in in domain_patterns.items():
        domain_index = build_domain_index(patterns_in)
        index_path = STATIC_DIR / f"domain-index-{domain}.json"
        index_path.write_text(json.dumps(domain_index, separators=(",", ":")), encoding="utf-8")
        size_kb = index_path.stat().st_size / 1024
        print(f"  {index_path.name} ({len(domain_index)} entries, {size_kb:.0f} KB)")

    # Generate domain-chunked search indexes (for lazy Fuse.js)
    print("\nGenerating chunked search indexes...")
    # Core index: collections + featured patterns (always loaded)
    core_patterns = []
    for coll_patterns in collection_patterns.values():
        core_patterns.extend(coll_patterns)
    core_index = build_search_index(core_patterns)
    core_path = STATIC_DIR / "search-index.json"
    core_path.write_text(json.dumps(core_index, separators=(",", ":")), encoding="utf-8")
    print(f"  search-index.json (core: {len(core_index)} entries)")

    # Per-domain search indexes (loaded lazily)
    for domain, patterns_in in domain_patterns.items():
        domain_search = build_search_index(patterns_in)
        search_path = STATIC_DIR / f"search-index-{domain}.json"
        search_path.write_text(json.dumps(domain_search, separators=(",", ":")), encoding="utf-8")
        size_kb = search_path.stat().st_size / 1024
        print(f"  search-index-{domain}.json ({len(domain_search)} entries, {size_kb:.0f} KB)")

    # Summary
    print(f"\n{'='*60}")
    print(f"Done! {len(all_patterns)} patterns processed.")
    print(f"  Hugo content pages: {sum(len(v) for v in collection_patterns.values())}")
    print(f"  R2 staged files: {sum(1 for _ in R2_STAGING.rglob('*.md'))}")
    print(f"  Domain indexes: {len(domain_patterns)}")
    print(f"  Search indexes: {len(domain_patterns) + 1}")


if __name__ == "__main__":
    main()
