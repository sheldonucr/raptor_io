# GridStack

**GridStack** (formerly **Raptor** — Rapid Analysis of Power-grid Transients via Order Reduction).

**Fast, accurate transient power-grid (IR-drop) simulation for million-node designs.**

🔗 **Live page: [sheldonucr.github.io/raptor_io](https://sheldonucr.github.io/raptor_io/)**

GridStack computes full transient power-grid waveforms — dynamic IR-drop at every probe node — at a
fraction of the cost of a direct transient solver. It is powered by an **advanced Krylov subspace
reduction** engine: instead of re-solving a million-node mesh at every time step, GridStack builds a
compact reduced-order model that captures the grid's dominant dynamics, marches *that* small model
through time, and projects the result back onto the nodes you care about — validated throughout
against a direct back-Euler transient reference.

This repository hosts the **GridStack** site and white paper series, published at
**<https://sheldonucr.github.io/raptor_io/>**.

> **Naming.** GridStack was previously called **Raptor**. The engine ships in two solver modes:
> **GridStack** — the advanced *rational* Krylov subspace solver (fastest, internally RA-IEKS) — and
> the standard **Krylov method** (most accurate, machine precision, internally IEKS). The internal
> names appear only in the result files; the site uses **GridStack** and **Krylov method** throughout.

---

## Why GridStack

Dynamic IR-drop is decided by the full time-domain response of a mesh with millions of nodes,
thousands of switching current sources, and thousands of time steps:

- **The grid is enormous.** Modern power grids reach millions of RC nodes across many metal layers.
- **Direct transient solves crawl.** Back-Euler with a sparse factorization re-solves the full mesh
  step after step — over three minutes for a single run on the largest IBM grid.
- **IR-drop must be in the loop.** Floorplanning, decap budgeting, and power delivery all need
  dynamic-IR feedback *per iteration*.

GridStack closes that gap: **essentially exact waveforms at up to 11.9× the speed.**

Beyond a single solve, GridStack also ships a **domain decomposition method**: the power grid is
partitioned into balanced subdomains, each subdomain is solved independently — in parallel across
multi-core CPUs and GPUs — and the solution is stitched back together at the shared boundary nodes,
so simulation scales out with the hardware you have.

---

## Headline results

Benchmarked against a **direct back-Euler transient** solve on the three IBM power-grid circuits
(54K / 165K / 1.04M nodes), reduction order 10, rational-Krylov shift time 1.0 s:

- **Up to 11.86×** faster than the direct solver (average **7.89×** across the three grids)
- **Maximum normalized waveform error < 6×10⁻⁶** — essentially exact
- The standard Krylov mode reaches **machine precision (~10⁻¹⁴)** at a moderate speedup

📄 Full per-circuit data, method, and figures: **[GS-WP-01 — Advanced Krylov Subspace
Reduction](whitepapers/wp01-krylov-reduction.html)**.

---

## Design

The site shares its design system with the sibling **ThermStack** site
(`/Volumes/joule/thermalcode/thermstack_io`): one editorial light palette
(`--ink #172b32`, `--green #087964`, `--blue #215fa4`, `--orange #ae521d`,
`--wash #f3f7f7`), Inter + JetBrains Mono, flat surfaces, hairline rules, and no
gradients or elevation. `assets/css/gridstack.css` mirrors that stylesheet; keep
the two in step when either changes.

## Site structure

The site is organized into three areas:

1. **Features & capabilities** (`index.html#capabilities`) — what GridStack does, kept short: the
   transient flow, the six capability cards, domain-decomposition scale-out, and agentic-flow
   integration.
2. **White papers** (`index.html#whitepapers`) — the technical record. All method detail, benchmark
   tables, and full-chip figures live here, one paper per topic, so nothing is repeated on the
   landing page.
3. **Contact** (`index.html#contact`) — demo requests.

### White paper series

| # | Title | Status |
|---|-------|--------|
| GS-WP-01 | [Advanced Krylov Subspace Reduction for Million-Node Transient Power-Grid Analysis](whitepapers/wp01-krylov-reduction.html) | Published |
| GS-WP-02 | [Full-Chip IR-Drop Visualization at Million-Node Scale](whitepapers/wp02-fullchip-visualization.html) | Published |
| GS-WP-03 | [GridStack vs. RedHawk-SC on Real Chip Designs](whitepapers/wp03-redhawk-correlation.html) | Published |
| GS-WP-04 | Domain Decomposition for Multi-Core and GPU Scale-Out | In preparation |
| GS-WP-05 | GridStack in Agentic EDA Sign-Off Flows | In preparation |

To add a paper: copy an existing file in `whitepapers/`, bump the `GS-WP-nn` number, and add a
`.capability` card to the `#whitepapers` section of `index.html` (replace the `In preparation` note
with a `.text-link` to the new file once it is published).

---

## Repository layout

```
gridstack_io/
├── index.html                          # landing page: features, white paper index, contact
├── whitepapers/
│   ├── wp01-krylov-reduction.html      # GS-WP-01 — method + full validation results
│   ├── wp02-fullchip-visualization.html# GS-WP-02 — full-chip structure / 2D / 3D drop views
│   └── wp03-redhawk-correlation.html   # GS-WP-03 — GridStack vs RedHawk-SC on RISC_CORE and LPU
├── gen_plots.py                        # regenerates the GS-WP-01 charts
├── README.md                           # this file
└── assets/
    ├── css/
    │   └── gridstack.css               # shared stylesheet for all pages
    ├── js/
    │   └── site.js                     # nav, figure lightbox, section tracking
    ├── img/
    │   └── gridstack.svg               # favicon / brand mark
    └── figs/
        ├── accuracy_comparison.png     # Figure 1 in GS-WP-01
        ├── speedup_comparison.png      # Figure 2 in GS-WP-01
        ├── views/                      # Figures 1a-c / 2a-c in GS-WP-02
        └── rhsc/                       # Figures 1-4 in GS-WP-03 (layouts, power grids, accuracy, wall time)
            ├── ibmpg2t_structure_2d.png
            ├── ibmpg2t_drop_2d.png
            ├── ibmpg2t_drop_3d.png
            ├── ibmpg3t_structure_2d.png
            ├── ibmpg3t_drop_2d.png
            └── ibmpg3t_drop_3d.png
```

## Regenerating the figures

The two result charts used in GS-WP-01 are generated from the benchmark numbers. Regenerate
them with:

```bash
python3 gen_plots.py     # requires matplotlib + numpy; writes into assets/figs/
```

(The generating script `gen_plots.py` was used to produce the current charts; edit the data arrays at
the top if the benchmark numbers change.)

## Previewing locally

```bash
python3 -m http.server 8788
# then open http://localhost:8788/index.html
```

---

© 2026 NoveetyAI, Inc. All rights reserved.
