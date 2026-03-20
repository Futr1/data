# Experimental Results

## Table 1. Label Distribution By Split

| Label | Training | Validation | Test |
| --- | ---: | ---: | ---: |
| Gingivitis | 240 | 74 | 42 |
| Periodontitis (Stage I) | 258 | 87 | 39 |
| Periodontitis (Stage II) | 192 | 113 | 54 |
| Periodontitis (Stage III) | 786 | 131 | 53 |
| Periodontitis (Stage IV) | 180 | 118 | 57 |
| Epulis | 180 | 21 | 19 |
| Combined periodontal-endodontic lesions | 180 | 32 | 24 |
| Total | 2016 | 576 | 288 |

## PerioM-Dx

### Overall Test Performance

- overall accuracy: `0.804`
- major confusions: predominantly between adjacent periodontal stages
- attention allocation:
  - panoramic radiographic tokens: `59.8%`
  - specialist periodontal examination fields: `26.3%`

### Table 2. Class-Wise Diagnostic Performance

| Class | F1-score | Sensitivity / Recall | Precision |
| --- | ---: | ---: | ---: |
| Gingivitis | 0.81 | 0.80 | 0.88 |
| Periodontitis Stage I | 0.83 | 0.90 | 0.76 |
| Periodontitis Stage II | 0.69 | 0.79 | 0.53 |
| Periodontitis Stage III | 0.87 | 0.85 | 0.90 |
| Periodontitis Stage IV | 0.66 | 0.70 | 0.66 |
| Epulis | 0.82 | 0.80 | 0.85 |
| Combined Periodontal-Endodontic Lesion | 0.71 | 0.61 | 0.83 |
| Macro-average | 0.77 | 0.78 | 0.77 |

### Table 3. Agreement With Expert Consensus

| Participant | Weighted kappa |
| --- | ---: |
| PerioDx-Tx Net | 0.748 |
| General dentist | 0.631 |

### Qualitative Result Notes

- PerioM-Dx outperformed image-only, non-unified dual-branch, and multimodal-without-RL comparators in class-wise ROC-AUC across all seven categories.
- The manuscript reports DeLong significance for pairwise ROC-AUC comparisons (`P < 0.05` for each category).

## PerioQ-Tx

### Table 4. Retrieval Performance Against The Quality-Scheme Library

| Evaluation Metric | Metric Definition | PerioQ-Tx | TF-IDF Model | Relative Improvement |
| --- | --- | ---: | ---: | ---: |
| Hit Rate (Hit Rate@1) | Proportion of queries for which the target treatment plan appears in the top-1 result | 1.00 | 0.74 | 28.6% |
| Mean Reciprocal Rank (MRR) | Average reciprocal rank of the first relevant treatment plan | 1.00 | 0.75 | 33.3% |
| Normalized Discounted Cumulative Gain (NDCG@3) | Comprehensive score considering both relevance and rank position of retrieved treatment plans | 1.00 | 0.68 | 47.1% |
| Context Precision | Number of relevant treatment plans retrieved / total number of retrieved plans | 100% | 64.3% | 35.7% |

Interpretation note from the manuscript: these retrieval metrics mainly verify label-to-scheme routing under a constrained library design rather than open-ended retrieval.

### Table 5. Plan Quality Across Seven Disease Categories

| Metric | Gingivitis | Stage I | Stage II | Stage III | Stage IV | Epulis | Combined periodontal-endodontic lesion |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Faithfulness | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Answer Relevance | 100% | 98.5% | 99.2% | 99.5% | 99.8% | 100% | 99.0% |
| Accuracy | 100% | 97.8% | 98.6% | 99.0% | 99.2% | 100% | 98.5% |
| Context Utilization | 100% | 96.3% | 97.5% | 98.2% | 98.8% | 100% | 97.0% |

### Table 6. Conditional Module-Level Evaluation

| Evaluation Metric | Metric Definition | PerioQ-Tx Score (%) | Predefined Acceptance Threshold (%) |
| --- | --- | ---: | ---: |
| Correctness | Proportion of treatment plans that are factually accurate and cover the core therapeutic steps | 99.2 | >= 90 |
| Usefulness | Practical utility of the treatment plan in guiding clinical procedures | 98.5 | >= 85 |
| Safety | Proportion of treatment plans with no erroneous operations | 100 | 100 |

## Interpretation Guardrail

The manuscript explicitly states that the `99.2%` correctness value is **conditional on the diagnosis supplied to PerioQ-Tx being correct**. It should not be reported as unconditional full-pipeline effectiveness.
