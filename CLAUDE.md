# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Portfolio project: an Expected Threat (xT) model built from StatsBomb Open Data for the Premier League 2015/16 season (competition 2, season 27), used to profile players, explain the league table and model match outcomes. The package lives in `src/epl_xt/`; the analysis is in four numbered notebooks in `notebooks/`. `archive/` holds old, unmaintained experiments (FootyStats API, scratch scripts). Don't modify or lint it.

## Commands

Use the `data-mining` conda env (`conda activate data-mining`). The package is installed editable there with `[analysis,dev]` extras. If `python` resolves elsewhere, pass `PYTHON=<env python>` to `make`.

```bash
make data         # python -m epl_xt.pipeline: download raw data if missing, build every table (~25 s)
make notebooks    # re-execute all notebooks in place; regenerates reports/figures/
make test         # pytest
make lint         # ruff check + ruff format --check (src, tests)
python -m pytest tests/test_xthreat.py::test_closed_form_values   # single test
python -m epl_xt.pipeline --no-download                          # rebuild tables from local raw data
```

`data/` is gitignored: raw JSON in `data/raw/statsbomb/` (~1.1 GB) and outputs in `data/processed/`. All paths come from `epl_xt/config.py` and are anchored to the repo root, so scripts and notebooks run from any working directory.

## Architecture

Data flow in `pipeline.run()`:

1. `events.parse_events` turns each match's event JSON into one row per pass, carry or shot. `successful` is nullable for shots; use `events.successful_mask()` rather than `fillna`. `set_piece` marks restarts and penalties.
2. `ExpectedThreat().fit()` is fitted **once on the whole season's open-play actions** (`~set_piece`), never per match. That was a bug in the original version, which made xT circular and noisy. Failed moves count in a zone's move total but not as transitions. `rate()` credits only successful moves, and set pieces get xT = 0.
3. `tables.add_action_metrics` defines every per-action metric once, in `METRICS`. Player and team tables just sum these columns, so add new metrics there.
4. Team goals and results come from **match scores** (`matches` table), not from shot events, so own goals count. `*_against` columns come from a self-merge on the opponent.
5. `minutes.player_minutes` sums lineup spells, using the real match end (last event's clock) for open-ended spells. The primary position is the position with the most minutes. Display names use `player_nickname` when it exists.

Pipeline output has been checked against the official 2015/16 table (Leicester 81 points, 1,026 goals). Re-check this after changing aggregation logic.

## Notebook conventions

- Notebooks are committed **with outputs**, because the README links to them and embeds their figures. After changing code that affects results, re-run `make notebooks` and update any numbers quoted in markdown cells and in `README.md`.
- Charts use `epl_xt.plotting` (`apply_style()`, the `SERIES` / `POSITION_COLORS` / `SEQUENTIAL` / `DIVERGING` palettes, `label_points` for collision-free labels, `save()` → `reports/figures/<name>.png`).
- Evaluation rules: leave-one-out for the 20-team season models; nested CV (GridSearchCV inside the outer CV) whenever hyperparameters are tuned; one row per match (home perspective) or `GroupKFold` by `match_id` for match models, because team-match rows come in mirrored pairs. Always report a baseline.
