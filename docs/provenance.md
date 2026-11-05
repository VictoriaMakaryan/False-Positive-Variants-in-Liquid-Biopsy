# Provenance and public-edition changes

## Source materials

- **`FP_in_liquid_biopsy_FINAL (1).ipynb`** — supplied research notebook with code, narrative, tables, and figures.
- **`False Positive Variants in Liquid Biopsy_ Project for students 2026 (1).docx`** — supplied Russian-language brief describing the question, evidence groups, and intended validation. Its task instructions do not establish that each task was completed.
- **[Project presentation](https://docs.google.com/presentation/d/1VRVlxFJwOnT9711itlc5amiQRpV-2sJMkFSCQYh3cF0/edit)** — supplied link. The maintainer identifies its title slide as the source for team credits. Slides were inaccessible from the preparation environment; no slide-specific findings or unverified names have been transcribed.

The clinical dataset was not supplied. The raw document and original embedded tables are not redistributed. The repository contains a public notebook edition and one inspected aggregate correlation figure.

## Notebook changes

- Added an introduction, data-location instructions, section guide, and methodological notes.
- Cleared outputs, execution counts, and Colab metadata; removed inactive commented alternatives. The original attachment remains outside the checkout.
- Replaced the fixed CSV path with a local default and `LIQUID_BIOPSY_DATA` override.
- Updated pandas imputation assignments and t-SNE's `n_iter` argument to `max_iter`.
- Removed unused HDBSCAN imports; retained active PCA, UMAP, t-SNE, K-Means, statistical comparisons, and boundary visualizations.
- Stopped imputing annotation strings, which are not numerical modeling inputs.
- Replaced annotation-key merging with a one-to-one row-index join.
- Added explicit opt-in before reusing historical `GOOD`/`BAD` cluster interpretations.
- Corrected the quality-threshold comment to match the executed value, 380.
- Reworded conversational narrative and documented unsupported global-statistical conclusions as limitations.

The original numerical preprocessing order is retained, with its limitations documented. The private-data results have not been rerun.

## Extracted software and attribution

`src/liquid_biopsy` implements the final rule logic with numeric validation and safe CSV output handling. It is a public-edition addition, not a new trained model. The example data is entirely invented. Tests, dependency locking, and GitHub Actions support maintenance.

Victoria Makaryan maintains the repository. The analysis is team work; full team credits are on the linked presentation. The supplied brief names Artem Galoyan as project preparer and Daniil Nikitin and Artem Galoyan as supervisors. Individual contributions have not been inferred from file or repository ownership.

No open-source license has been assigned to supplied team materials. Agree on redistribution and licensing with contributors before granting reuse rights.
