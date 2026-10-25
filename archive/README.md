# Archive

Earlier experiments that are not part of the main xT analysis. They are kept for reference, are not maintained, and may not run as-is (paths and data locations predate the current layout).

| folder | what it was |
|---|---|
| `footystats_pipeline/` | Client for the [FootyStats API](https://footystats.org/api/) (2024/25 Premier League team stats). Needs a `FOOTYSTATS_API_KEY` in a `.env` file. |
| `footystats_eda/` | Exploratory analysis and feature-grouping helpers for the FootyStats data. |
| `json-playground/` | A standalone HTML page for testing [JMESPath](https://jmespath.org/tutorial.html) queries against API responses. |
| `scratch/` | One-off sanity-check scripts from the first version of the StatsBomb pipeline. |
| `project_action_items.md` | The original phase checklist for the course project. |

The first version of the StatsBomb pipeline and its notebooks (`statsbomb_pipeline/`, `PlayerModels-Statsbomb/`, `TeamModels-StatsBomb/`) were replaced by `src/epl_xt/` and `notebooks/`. They are still in the git history at commit `575f384`.
