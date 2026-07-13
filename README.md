# Raptor

**Raptor** — **R**apid **A**nalysis of **P**ower-grid **T**ransients via **O**rder **R**eduction.

**Fast, accurate transient power-grid (IR-drop) simulation for million-node designs.**

🔗 **Live page: [sheldonucr.github.io/raptor_io](https://sheldonucr.github.io/raptor_io/)**

Raptor computes full transient power-grid waveforms — dynamic IR-drop at every probe node — at a
fraction of the cost of a direct transient solver. It is powered by an **advanced Krylov subspace
reduction** engine: instead of re-solving a million-node mesh at every time step, Raptor builds a
compact reduced-order model that captures the grid's dominant dynamics, marches *that* small model
through time, and projects the result back onto the nodes you care about — validated throughout
against a direct back-Euler transient reference.

This repository hosts the **Raptor** promotion site (`index.html`), published at
**<https://sheldonucr.github.io/raptor_io/>**.

> **Naming.** The engine ships in two solver modes: **Raptor** — the advanced *rational* Krylov
> subspace solver (fastest, internally RA-IEKS) — and the standard **Krylov method** (most accurate,
> machine precision, internally IEKS). The internal names appear only in the result files; the site
> uses **Raptor** and **Krylov method** throughout.

---

## Why Raptor

Dynamic IR-drop is decided by the full time-domain response of a mesh with millions of nodes,
thousands of switching current sources, and thousands of time steps:

- **The grid is enormous.** Modern power grids reach millions of RC nodes across many metal layers.
- **Direct transient solves crawl.** Back-Euler with a sparse factorization re-solves the full mesh
  step after step — over three minutes for a single run on the largest IBM grid.
- **IR-drop must be in the loop.** Floorplanning, decap budgeting, and power delivery all need
  dynamic-IR feedback *per iteration*.

Raptor closes that gap: **essentially exact waveforms at up to 11.9× the speed.**

Beyond a single solve, Raptor also ships a **domain decomposition method**: the power grid is
partitioned into balanced subdomains, each subdomain is solved independently — in parallel across
multi-core CPUs and GPUs — and the solution is stitched back together at the shared boundary nodes,
so simulation scales out with the hardware you have.

---

## Headline results

Benchmarked against a **direct back-Euler transient** solve on the three IBM power-grid circuits,
reduction order 10, rational-Krylov shift time 1.0 s, error measured on 20 golden probe nodes/circuit
over 1,001 time points.

| Circuit  | Nodes     | Sources | Direct CPU (s) | Raptor CPU (s) | Raptor speedup | Raptor avg / max norm. err |
|----------|-----------|---------|---------------:|----------------:|----------------:|-----------------------------|
| ibmpg1t  | 54,265    | 25,082  | 2.267          | 0.407           | **5.57×**       | 7.08e-07 / 5.62e-06         |
| ibmpg2t  | 164,897   | 37,168  | 14.097         | 1.189           | **11.86×**      | 3.30e-08 / 7.39e-08         |
| ibmpg3t  | 1,043,444 | 202,009 | 203.929        | 32.642          | **6.25×**       | 1.43e-07 / 7.94e-07         |

Average Raptor speedup **7.89×**; maximum normalized error stays **< 6×10⁻⁶**. The standard Krylov
method reaches machine precision (~10⁻¹⁴) at 1.50× / 4.78× / 3.76× speedup on the same circuits.

---

## Repository layout

```
raptor_io/
├── index.html                     # the promotion page (self-contained)
├── README.md                      # this file
└── assets/
    └── figs/
        ├── accuracy_comparison.png # Raptor normalized error vs. direct, 3 circuits (log scale)
        └── speedup_comparison.png  # Raptor CPU-time speedup vs. direct, 3 circuits
```

## Regenerating the figures

The two result charts are generated directly from the numbers in
`ibm_ieks_raieks_shift1_results.md`. Regenerate them with:

```bash
python3 gen_plots.py     # requires matplotlib + numpy; writes into assets/figs/
```

(The generating script `gen_plots.py` was used to produce the current charts; edit the data arrays at
the top if the benchmark numbers change.)

## Previewing locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000/index.html
```

---

© 2026 Raptor · Developed at UC Riverside.
