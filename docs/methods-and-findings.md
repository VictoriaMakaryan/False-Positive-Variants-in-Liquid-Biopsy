# Methods and findings

## Research question

Can sequencing evidence and read-position artifacts help prioritize cfDNA variants for manual review after LDT filtering?

The brief proposes preserving high clinical accuracy while reducing IGV review. Its ≥95% accuracy target is a **goal**, not a demonstrated result. The notebook does not include independently labeled holdout evaluation, IGV adjudication records, or a timing study.

## Implemented analysis

1. Inspect missingness; drop the sparsely populated population-frequency field and patient identifier from the working table.
2. Impute selected numerical fields with medians; remove duplicate working rows.
3. Inspect distributions, boxplots, pairwise correlations, and raw feature variance.
4. Standardize numerical features, apply the submitted clipped `log1p` transformations, and cap outliers using 1.5×IQR limits.
5. Fit PCA retaining at least 95% of processed variance; compare UMAP and t-SNE visualizations.
6. Compare K-Means with 4, 5, and 6 clusters; interpret a five-cluster UMAP solution using original evidence groups.
7. Explore original-scale differences with Mann–Whitney U tests. Visualize logistic-regression and RBF-SVM boundaries fitted to interpreted cluster labels.
8. Propose quality/read-support and read-edge-distance thresholds for three review actions.

HDBSCAN was imported but unused in the source. The public edition omits that dependency and commented-out alternatives; active PCA-based methods remain.

## Historical evidence from the submission

| Item | Recorded output | Interpretation |
| --- | --- | --- |
| Working data before duplicate removal | 1,944 rows, 22 columns | Historical output; source data not distributed |
| PCA | Four components; variance ratios 0.6531, 0.1985, 0.0836, 0.0282 | About 96.3% of processed variance |
| Clustering | Comparisons for k = 4, 5, 6 | Visual exploration, not a validated optimum |
| Cluster interpretation after group exclusion | 1,288 `GOOD`, 454 `BAD` | Manual cluster interpretations, not ground truth |
| Final rule outputs | 927 pass, 246 reject, 591 manual review | Original merge expanded rows; not validated unique-variant counts or workload savings |

The original interpreted table totals **1,742 rows**, whereas the final rule table totals **1,764**. The source merges on `Order_ID_cfDNA`, `HGVSc`, and `HGVSp_Short` without checking key uniqueness, which can expand records. The public notebook joins by original row index with a one-to-one check. The raw dataset is unavailable, so key multiplicities and corrected real-data counts have not been independently rerun.

The [correlation figure](figures/feature-correlation.png) is extracted unchanged from the submission. It records a positive association between `Tumor_VAF` and `t_alt_count` (approximately 0.70), and a negative association between `Avg_Min_Distance_ALT_reads` and `ALT_≤3_Distance_Percent` (approximately −0.70). Neither measures classification accuracy.

## Candidate rules

The module reproduces the executable thresholds: quality **>380** and alternate count **>31** for pass; otherwise alternate-read edge distance **<20** for reject; otherwise manual review. A source comment said 750, but the executable code used 380. The public notebook corrects that comment.

## Limitations and next validation steps

- **Independent evaluation is absent.** `GOOD`/`BAD` are interpreted clusters. Classifiers fitted to these labels illustrate their separation, not independently verified TP/FP prediction.
- **Cluster IDs are not portable.** The historical mapping of clusters 0, 1, and 3 to `GOOD` can change with data, preprocessing, or dependency versions. Reusing it requires explicit opt-in in the public notebook.
- **Preprocessing needs further study.** Scaling before clipped `log1p` can collapse distinct observations below −1. This edition preserves the submitted order for transparency. Compare suitable original-scale transformations followed by scaling, with stability analyses, in follow-up work.
- **Variance is not predictive importance.** Raw variance reflects feature units; PCA variance retention does not demonstrate biological discrimination.
- **Tests are exploratory.** Cluster-derived comparisons do not establish causality. Multiple testing and dependence between observations need appropriate treatment. The source conclusion mentions global group comparisons whose complete computations are absent; this edition does not claim to reproduce them.
- **Workload savings are unverified.** Preserve row identity before calculating action proportions. Actual time savings require representative review times and adjudicated outcomes.
- **Generalization is untested.** Use held-out, preferably patient-separated and external data with a defined labeling procedure. Report sensitivity and precision with uncertainty before operational use.

## Software validation

Tests cover threshold boundaries, missing evidence, pass precedence, row preservation, malformed inputs, and CLI overwrite protection. Notebook checks validate structure, parse code, and require cleared outputs. The public synthetic demo verifies software behavior; these checks do not validate clinical performance or reproduce the private-data study.

The preparation environment passed **26 tests**, `pip check`, and the seven-row CLI example. All **33 notebook code cells** also executed without errors against a separate 160-row invented dataset, with the historical-mapping opt-in enabled only in the in-memory test copy. The checked-in notebook remains output-free and retains its default mapping guard. This full-notebook smoke test is separate from the lightweight checks in GitHub Actions.
