# Data guide

## Public example

`examples/synthetic_variants.csv` contains invented values, not de-identified clinical observations. Its seven rows demonstrate the extracted triage rules, not biological performance.

## Private research input

The submitted notebook reads `All_groups_in_one.csv`, a variant-level table described in the project brief as combining cfDNA, matched tissue evidence, reference controls, and curated false positives. That file was not provided for this release and is not redistributed.

Place authorized input at `data/private/All_groups_in_one.csv`, or use an absolute path:

```bash
export LIQUID_BIOPSY_DATA=/absolute/path/to/All_groups_in_one.csv
jupyter lab
```

The notebook resolves its default from the checkout root or `notebooks/`. Source tables may contain sample identifiers and clinical context. Keep them local. Input folders, generated outputs, and common genomic table formats are ignored by Git. Review executed notebook outputs before committing: `.gitignore` cannot remove information embedded in a notebook.

### Core evidence fields

| Field | Meaning / use |
| --- | --- |
| `Tumor_VAF` | Variant allele fraction; verify source units |
| `t_depth`, `t_alt_count` | Tumor/target depth and alternate-read count, using source naming |
| `n_depth`, `n_alt_count` | Normal/comparator depth and alternate-read count, using source naming |
| `variant_qual` | Variant quality, described as Phred quality in the brief |
| `Strand_Bias` | Source-specific strand-bias metric |
| `Avg_Min_Distance_ALT_reads` | Average minimum alternate-read distance to a read edge |
| `Avg_Min_Distance_REF_reads` | Corresponding reference-read distance |
| `ALT_≤3_Distance_Percent` | Fraction/percentage of alternate evidence near read ends, using the source definition |
| `group` | One of the eight predefined categories below |

The notebook also references `LDT_PASS_cfDNA`, `LDT_PASS_DNA`, `HGVSc`, `HGVSp_Short`, and `Order_ID_cfDNA` in cleaning/display cells. `Patient_ID`, `gnomADg_AF_popmax`, and `Unnamed: 0` are handled if present. Other source annotations can remain. Do not include identifiers as numerical modeling inputs. The public notebook attaches labels by original row index, not annotations.

### Original evidence groups

| Group | Description from the brief |
| --- | --- |
| `cfdna_LDT_only` | Detected only in cfDNA, passing its LDT filter |
| `TWIST_LDT_TP` | TWIST control variants supported by the reference |
| `TWIST_LDT_FP` | TWIST control variants without reference confirmation |
| `KNOWN_FP_CFDNA_LDT` | Curated false positives passing cfDNA LDT filtering |
| `WES_LDT_cfDNA_LDT` | Tissue and cfDNA evidence passing both filters |
| `WES_LDT_cfDNA_NO` | Tissue and cfDNA evidence, passing the tissue filter only |
| `WES_NO_cfDNA_LDT` | Tissue and cfDNA evidence, passing the cfDNA filter only |
| `WES_NO_cfDNA_NO` | Detected in both, passing neither filter |

Group membership does not establish independently adjudicated TP/FP labels for every row. The notebook excludes `WES_NO_cfDNA_NO` before cluster interpretation.

## CLI input contract

The rule module requires only `variant_qual`, `t_alt_count`, and `Avg_Min_Distance_ALT_reads`. Values must be numeric and nonnegative; non-missing values must be finite, and read counts must be whole numbers. Missing values cannot satisfy a threshold. Additional columns are preserved, so outputs can contain sensitive information when private inputs are used.

The module does not fit clusters or impute evidence. A row with incomplete evidence can still satisfy an independent rule: missing quality does not prevent rejection when read-edge distance is below 20. Pass takes precedence if both pass conditions and low distance occur, matching the supplied code.
