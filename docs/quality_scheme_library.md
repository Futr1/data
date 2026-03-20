# Quality-Scheme Library

PerioQ-Tx is intentionally framed as **diagnosis-conditioned constrained drafting**, not open-domain free generation.

## Library Role

The quality-scheme library stores curated treatment pathways keyed by diagnosis labels. Each entry should contain:

- `scheme_id`
- `diagnosis_label`
- title or pathway summary
- retrieval keywords
- evidence or source note
- recommended steps
- contraindications
- follow-up items

## Cue-Memory Positioning

The manuscript describes the library as a constrained drafting substrate built from periodontal clinical guidelines and quality-control standards, including material derived from the American Academy of Periodontology and the European Federation of Periodontology.

The repository keeps the original cue-memory and H-framework reference code in the historical source tree, while the public wrappers under [`src/perioq_tx/`](/d:/文件/论文/华西论文-多模态/code/src/perioq_tx) expose a stable repository interface:

1. build index
2. retrieve candidates
3. filter unsafe or out-of-scope entries
4. generate a constrained draft
5. evaluate routing and draft quality

## Retrieval Configuration Reported In The Manuscript

- backend: Elasticsearch
- query: diagnosis label
- initial beam width: `k = 40`
- redundancy filter: BLEU-based semantic overlap threshold `> 0.4`
- cue-memory during evaluation: frozen, with no test-set write-back

## Evaluation Rule

High reported drafting performance should be interpreted as:

- diagnosis-conditioned routing inside a curated library
- constrained draft quality within the retrieved scheme space

It should **not** be interpreted as unrestricted autonomous treatment planning.
