---
title: "Urban Patterns - Commons Engineering"
type: "raw"
---
<style>
  .domain-hero {
    text-align: center;
    padding: 60px 20px 40px;
  }
  .domain-hero .hero-icon {
    color: #3AAADC;
    margin-bottom: 20px;
  }
  .domain-hero .hero-icon [data-lucide] {
    width: 56px;
    height: 56px;
  }
  .domain-hero h1 {
    font-size: 2.4em;
    color: #2c3e50;
    margin: 0 0 10px 0;
    font-weight: 600;
    border: none;
  }
  .domain-hero .subtitle {
    color: #5a738e;
    font-size: 1.15em;
    max-width: 600px;
    margin: 0 auto 10px;
    line-height: 1.7;
  }
  .domain-hero .sub-desc {
    color: #8899aa;
    font-size: 0.95em;
    margin: 0;
  }
  .stats-row {
    display: flex;
    justify-content: center;
    gap: 50px;
    margin: 30px auto;
    flex-wrap: wrap;
    max-width: 600px;
  }
  .stat-item { text-align: center; }
  .stat-item .number {
    font-size: 2em;
    font-weight: 700;
    color: #3AAADC;
  }
  .stat-item .label {
    color: #5a738e;
    font-size: 0.9em;
  }
  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 20px;
    color: #3AAADC;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95em;
  }
  .back-link:hover { color: #1e4a70; }

  /* Filter Controls */
  .filter-controls {
    max-width: 1100px;
    margin: 0 auto 24px;
    padding: 0 20px;
  }
  .filter-search {
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
  }
  .filter-search:focus {
    outline: none;
    border-color: #3AAADC;
    box-shadow: 0 0 0 3px rgba(58,170,220,0.1);
  }
  .filter-groups {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 8px;
  }
  .filter-group-label {
    font-size: 0.8em;
    color: #8899aa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    width: 100%;
    text-align: center;
    margin: 8px 0 4px;
  }
  .filter-chip {
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
  }
  .filter-chip:hover {
    border-color: #3AAADC;
    color: #3AAADC;
  }
  .filter-chip.active {
    border-color: #3AAADC;
    background: #f0f9ff;
    color: #3AAADC;
    font-weight: 500;
  }
  .chip-count {
    font-size: 0.85em;
    color: #aab;
    font-weight: 400;
  }
  .filter-chip.active .chip-count {
    color: #3AAADC;
  }
  .filter-status {
    text-align: center;
    color: #8899aa;
    font-size: 0.9em;
    margin: 12px 0;
  }
  .filter-status strong {
    color: #3AAADC;
  }

  /* Virtual scroll container */
  .patterns-viewport {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 20px;
    height: 70vh;
    overflow-y: auto;
    position: relative;
  }
  .patterns-spacer {
    position: relative;
  }
  .patterns-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
  }
  .pattern-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #e6e9ed;
    transition: all 0.3s ease;
    text-decoration: none;
    color: inherit;
    border-left: 3px solid transparent;
  }
  .pattern-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    border-left-color: #3AAADC;
  }
  .pattern-card h3 {
    margin: 0 0 6px 0;
    color: #2c3e50;
    font-size: 1em;
    font-weight: 500;
  }
  .pattern-card .card-meta {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 6px;
  }
  .pattern-card .tag {
    background: #f1f5f9;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75em;
    color: #64748b;
  }
  .pattern-card .tag-layer { background: #ede9fe; color: #7c3aed; }
  .pattern-card .tag-dim { background: #e0f2fe; color: #0369a1; }
  .pattern-card p {
    color: #5a738e;
    font-size: 0.85em;
    line-height: 1.5;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .loading-indicator {
    text-align: center;
    padding: 40px;
    color: #8899aa;
  }
  .loading-indicator .spinner {
    display: inline-block;
    width: 32px;
    height: 32px;
    border: 3px solid #e6e9ed;
    border-top-color: #3AAADC;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>

<a href="/patterns/" class="back-link">&larr; Back to Patterns</a>

<div class="domain-hero">
  <div class="hero-icon"><i data-lucide="landmark"></i></div>
  <h1>Urban Patterns</h1>
  <p class="subtitle">Patterns for cultivating resilient cities and civic infrastructure.</p>
  <p class="sub-desc">Cities, neighborhoods, public spaces, and urban systems</p>
</div>

<div class="stats-row">
  <div class="stat-item">
    <div class="number" id="total-count">...</div>
    <div class="label">Patterns</div>
  </div>
</div>

<div class="filter-controls">
  <input type="text" class="filter-search" id="domain-search" placeholder="Search within urban patterns..." autocomplete="off">

  <div class="filter-groups" id="layer-filters">
    <div class="filter-group-label">Layer</div>
    <button class="filter-chip active" data-filter="layer" data-value="all">All</button>
  </div>

  <div class="filter-groups" id="dimension-filters">
    <div class="filter-group-label">Dimension</div>
    <button class="filter-chip active" data-filter="dimension" data-value="all">All</button>
  </div>

  <div class="filter-status" id="filter-status">Loading...</div>
</div>

<div class="patterns-viewport" id="viewport">
  <div class="loading-indicator" id="loading">
    <div class="spinner"></div>
    <p>Loading 14,000+ patterns...</p>
  </div>
  <div class="patterns-spacer" id="spacer" style="display:none;">
    <div class="patterns-grid" id="grid"></div>
  </div>
</div>

<script>
(function() {
  const DOMAIN = "urban";
  const CARD_HEIGHT = 120;
  const BUFFER = 5;

  let allPatterns = [];
  let filtered = [];
  let activeLayer = "all";
  let activeDimension = "all";
  let searchQuery = "";

  // Load domain index and dynamically build filter chips
  fetch("/patterns/domain-index-" + DOMAIN + ".json")
    .then(r => r.json())
    .then(data => {
      allPatterns = data;
      filtered = data;

      // Update total count
      document.getElementById("total-count").textContent = data.length.toLocaleString();

      // Build layer filter chips dynamically
      const layerCounts = {};
      const dimCounts = {};
      data.forEach(p => {
        if (p.l) layerCounts[p.l] = (layerCounts[p.l] || 0) + 1;
        if (p.d) dimCounts[p.d] = (dimCounts[p.d] || 0) + 1;
      });

      const layerContainer = document.getElementById("layer-filters");
      const layerLabels = {"L1":"Universal","L2":"Cross-Domain","L3":"Domain-Specific","L4":"Context-Specific"};
      let layerHtml = '<div class="filter-group-label">Layer</div>';
      layerHtml += '<button class="filter-chip active" data-filter="layer" data-value="all">All</button>';
      Object.keys(layerCounts).sort().forEach(l => {
        layerHtml += '<button class="filter-chip" data-filter="layer" data-value="' + l + '">' +
          (layerLabels[l] || l) + ' <span class="chip-count">' + layerCounts[l].toLocaleString() + '</span></button>';
      });
      layerContainer.innerHTML = layerHtml;

      const dimContainer = document.getElementById("dimension-filters");
      const dimIcons = {"Offers":"package","Operations":"settings","Agents":"users","Governance":"shield","Purpose":"compass","CE-Specific":"star"};
      let dimHtml = '<div class="filter-group-label">Dimension</div>';
      dimHtml += '<button class="filter-chip active" data-filter="dimension" data-value="all">All</button>';
      Object.keys(dimCounts).sort((a,b) => dimCounts[b] - dimCounts[a]).forEach(d => {
        const icon = dimIcons[d] ? '<i data-lucide="' + dimIcons[d] + '" style="width:14px;height:14px;"></i> ' : '';
        dimHtml += '<button class="filter-chip" data-filter="dimension" data-value="' + d + '">' +
          icon + escHtml(d) + ' <span class="chip-count">' + dimCounts[d].toLocaleString() + '</span></button>';
      });
      dimContainer.innerHTML = dimHtml;

      // Attach filter click handlers
      attachFilterHandlers();

      // Re-init lucide icons for the new chips
      if (window.lucide) lucide.createIcons();

      document.getElementById("loading").style.display = "none";
      document.getElementById("spacer").style.display = "block";
      updateStatus();
      renderVirtual();
    })
    .catch(err => {
      document.getElementById("loading").innerHTML =
        "<p>Failed to load patterns. Please try again later.</p>";
      console.error("Failed to load domain index:", err);
    });

  function attachFilterHandlers() {
    document.querySelectorAll('[data-filter="layer"]').forEach(btn => {
      btn.addEventListener("click", function() {
        document.querySelectorAll('[data-filter="layer"]').forEach(b => b.classList.remove("active"));
        this.classList.add("active");
        activeLayer = this.dataset.value;
        applyFilters();
      });
    });
    document.querySelectorAll('[data-filter="dimension"]').forEach(btn => {
      btn.addEventListener("click", function() {
        document.querySelectorAll('[data-filter="dimension"]').forEach(b => b.classList.remove("active"));
        this.classList.add("active");
        activeDimension = this.dataset.value;
        applyFilters();
      });
    });
  }

  function applyFilters() {
    filtered = allPatterns.filter(p => {
      if (activeLayer !== "all" && p.l !== activeLayer) return false;
      if (activeDimension !== "all" && p.d !== activeDimension) return false;
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        if (!(p.t || "").toLowerCase().includes(q) && !(p.m || "").toLowerCase().includes(q)) return false;
      }
      return true;
    });
    updateStatus();
    viewport.scrollTop = 0;
    renderVirtual();
  }

  function updateStatus() {
    document.getElementById("filter-status").innerHTML =
      "Showing <strong>" + filtered.length.toLocaleString() + "</strong> of " + allPatterns.length.toLocaleString() + " patterns";
  }

  // Search input with debounce
  let searchTimeout;
  document.getElementById("domain-search").addEventListener("input", function() {
    clearTimeout(searchTimeout);
    const val = this.value.trim();
    searchTimeout = setTimeout(() => {
      searchQuery = val;
      applyFilters();
    }, 200);
  });

  // Virtual scrolling
  const viewport = document.getElementById("viewport");
  const spacer = document.getElementById("spacer");
  const grid = document.getElementById("grid");

  function getColCount() {
    const w = viewport.clientWidth - 40;
    return Math.max(1, Math.floor(w / 296));
  }

  function renderVirtual() {
    const cols = getColCount();
    const rowHeight = CARD_HEIGHT + 16;
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
    for (let i = startIdx; i < endIdx; i++) {
      const p = filtered[i];
      const layerLabel = {"L1":"Universal","L2":"Cross-Domain","L3":"Domain-Specific","L4":"Context-Specific"}[p.l] || p.l || "";
      html += '<a href="/patterns/' + p.s + '/" class="pattern-card">' +
        '<h3>' + escHtml(p.t) + '</h3>' +
        '<div class="card-meta">' +
          (layerLabel ? '<span class="tag tag-layer">' + layerLabel + '</span>' : '') +
          (p.d ? '<span class="tag tag-dim">' + escHtml(p.d) + '</span>' : '') +
        '</div>' +
        (p.m ? '<p>' + escHtml(p.m) + '</p>' : '') +
        '</a>';
    }
    grid.innerHTML = html;
  }

  function escHtml(s) {
    if (!s) return "";
    return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }

  viewport.addEventListener("scroll", renderVirtual);
  window.addEventListener("resize", renderVirtual);
})();
</script>
