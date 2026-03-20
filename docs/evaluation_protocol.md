# Evaluation Protocol

## Diagnosis Module: PerioM-Dx

Reported diagnosis evaluation in the manuscript includes:

- ROC-AUC
- accuracy
- class-wise precision, sensitivity, specificity, and F1
- confusion matrix
- weighted Cohen's kappa in the 100-case reader comparison
- mean time per case in the 100-case reader comparison

## Answer-Only Scoring

PerioM-Dx may produce:

```text
<think> ... </think><answer> ... </answer>
```

For quantitative scoring, only the `<answer>` content should be evaluated. The reasoning trace is not part of the exact-match diagnosis metric.

## Drafting Module: PerioQ-Tx

Retrieval quality is reported with:

- Hit Rate@1
- MRR
- NDCG@3
- Context Precision

Draft quality is reported with:

- Faithfulness
- Answer Relevance
- Accuracy
- Context Utilization

Additional safety-oriented checks described in the manuscript include:

- schema adherence
- out-of-scope content detection
- contraindication screening

Conditional module-level evaluation is reported with:

- Correctness
- Usefulness
- Safety

## Conditional Correctness Statement

The reported `99.2% correctness` for the treatment module must be described as a **conditional module-level result** assuming an accurate upstream diagnosis. It is not an end-to-end autonomous treatment-planning accuracy claim.
