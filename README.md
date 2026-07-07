# mdforge — reusable, reproducible GROMACS MD analysis

[![CI](https://github.com/SamDozer/molecular-dynamics-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/SamDozer/molecular-dynamics-forge/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**mdforge** turns a GROMACS simulation directory into a complete, publication-quality,
fully reproducible analysis — with minimal input. Point it at a folder; it discovers
the files, **detects the system** (protein / ligand / DNA / RNA / membrane / ions /
multi-chain / …), **auto-selects the right analyses**, runs them with streaming-friendly
performance, and produces figures, tables, a provenance manifest, and a report.

> This repository began as a project-specific pipeline for an α-zein simulation
> (now preserved in [`legacy/`](legacy) and [`examples/`](examples)) and was
> refactored into this general toolkit.

---

## Highlights

- **Zero-config detection** — recursively finds `*.xtc/.trr/.tpr/.gro/.edr/.ndx/.top`,
  validates them (clear messages for anything missing), and classifies the system.
- **Automatic module selection** — each analysis declares the system types and files
  it supports; the pipeline runs exactly what applies (`--plan` shows *why*).
- **Extensible via plugins** — drop a `BaseAnalysis` subclass into
  `mdforge/analysis/plugins/` (or a `--plugin-dir`) and it is auto-discovered.
- **Config-driven** — describe a whole run in `config.yaml` and re-run with one command
  (ideal for HPC/batch).
- **Reproducible by construction** — every run writes `manifest.json/yaml` with library
  versions, git commit, input-file fingerprints, seeds, parameters and runtimes.
- **Publication-quality output** — 300-dpi PNG **and** vector PDF, consistent
  Nature-like style, plus Markdown + self-contained HTML (+ optional PDF) reports.
- **Scales** — streams frame-by-frame and caches a solute-only trajectory, so large
  (100 GB+) explicit-solvent runs stay tractable.

## Supported systems

protein-only · protein–protein · protein–peptide · protein–ligand · protein–DNA ·
protein–RNA · protein–membrane · multi-chain · ions · cofactors · mixed biomolecular
systems (detected automatically; override with `--system-type`).

## Install

```bash
git clone https://github.com/SamDozer/molecular-dynamics-forge
cd molecular-dynamics-forge
python -m pip install -e ".[all]"      # or ".[dev]" for tests
```

## Usage

```bash
mdforge detect  --input /path/to/sim_dir            # what's in my system?
mdforge analyze --input /path/to/sim_dir --plan     # what would run, and why?
mdforge analyze --input /path/to/sim_dir -o results # run everything applicable
mdforge analyze --config examples/alpha_zein_A8HNE1/config.yaml   # reproducible
mdforge list-analyses                                # registered analyses (incl. plugins)
```

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for all options and the plugin template.

## Architecture

```
mdforge/
  core/       system.py (detection) · base.py (BaseAnalysis) · registry.py (+plugins)
              context.py · config.py (YAML+CLI) · provenance.py · pipeline.py
  io/         discovery.py · validation.py
  statistics/ descriptive · timeseries · correlation · bootstrap
  plotting/   style · figures (PNG+PDF, 300 dpi)
  analysis/   rmsd · rmsf · rog · sasa · … + plugins/ (auto-discovered)
  report/     generator (Markdown + HTML + PDF)
  cli/        main (analyze/detect/list) · interactive
tests/  ·  examples/  ·  docs/  ·  legacy/  ·  Dockerfile  ·  .github/workflows/
```

Every analysis subclasses `BaseAnalysis`, declaring `required_files`,
`supported_systems`, `outputs` and `default_params`; subclasses auto-register, so
**detection → selection → run → report** is entirely data-driven.

## Analyses

Structure/dynamics analyses ship built-in and more are being ported from the
reference pipeline: **RMSD, RMSF, radius of gyration, SASA** (built-in now);
**H-bonds, PCA + free-energy landscape, DCCM, contact maps, clustering, DSSP,
salt bridges, native contacts, energies, convergence, RIN, ProLIF, MM/PBSA
workflow, interface & buried-surface analyses** (from [`legacy/`](legacy),
porting incrementally — each is a drop-in `BaseAnalysis`).

## Reproducibility

```bash
cat results/manifest.json     # versions, git commit, seeds, params, input hashes, runtimes
```

## Container

```bash
docker build -t mdforge .
docker run --rm -v /data/sim:/sim mdforge analyze --input /sim --output /sim/results
```

## License

MIT — see [LICENSE](LICENSE).
