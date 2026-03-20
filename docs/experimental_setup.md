# Experimental Setup

## Study Design

PerioDx-Tx Net is a retrospective multimodal framework for periodontal diagnosis and diagnosis-conditioned care-pathway drafting. The system takes a panoramic radiograph and structured EHR fields as input and outputs:

1. a structured periodontal diagnosis
2. an internal audit rationale in `<think>` during model development
3. a diagnosis-conditioned draft treatment pathway aligned to a curated quality-scheme library

## Cohort And Split

- centers:
  - West China Hospital of Stomatology, Sichuan University
  - Stomatology Hospital of Zhejiang University
- initial cohort: `3,500`
- excluded incomplete or irreconcilable cases: `620`
- final analytic cohort: `2,880`
- train: `2,016`
- validation: `576`
- independent test: `288`
- split policy: patient-level, no overlap
- train/validation source: West China Hospital of Stomatology
- independent test source: prespecified two-center strategy
- IRB approvals:
  - `WCHSIRB-D-2024-430`
  - `2024-075 (Y)`

## Input Modalities

### Direct Model Inputs

- panoramic radiograph
- structured EHR fields:
  - sex
  - age
  - chief complaint
  - history of present illness
  - past history
  - specialized periodontal examination
  - other structured descriptors

### Auxiliary Adjudication Inputs

- intraoral photographs
- probing results

These auxiliary materials were used for integrity checks and expert adjudication rather than as direct model inputs in the reported pipeline.

## Task Definition

The diagnosis task is a unified seven-class classification problem:

- gingivitis
- periodontitis stage I
- periodontitis stage II
- periodontitis stage III
- periodontitis stage IV
- epulis
- combined periodontal-endodontic lesion

## Output Schema

The diagnostic module is formulated as conditional sequence generation with an XML-like structure:

```text
<think>
... auxiliary rationale summary for internal auditing ...
</think>
<answer>
... final diagnosis and structured management summary ...
</answer>
```

Only the `<answer>` block is used for quantitative evaluation.

## PerioM-Dx

### Architecture

- base model: `Qwen2-VL-2B-Instruct`
- vision encoder: ViT-style panoramic radiograph patch encoder
- text stream: serialized structured EHR
- fusion: cross-attention from text queries to visual keys/values

### Stage 1: Supervised Fine-Tuning

- method: LoRA-based supervised fine-tuning
- LoRA rank: `8`
- learning rate: `2e-5`
- batch size: `4`

### Stage 2: Reinforcement Learning

- algorithm: Group Relative Policy Optimization (GRPO)
- reward components:
  - format reward for valid `<answer>` structure and mandatory-field compliance
  - accuracy reward for exact-match diagnosis correctness

## PerioQ-Tx

### Library Construction

- source basis: periodontal clinical guidelines and quality-control standards
- representative sources named in manuscript:
  - American Academy of Periodontology
  - European Federation of Periodontology

### Retrieve-Filter-Generate-Feedback Pipeline

- retrieval backend: Elasticsearch
- retrieval query: diagnosis label
- initial beam width: `k = 40`
- overlap reduction: BLEU-based similarity threshold `> 0.4`
- feedback memory: cue-memory pool
- evaluation setting: cue-memory initialized from training corpus and frozen during test-time evaluation

## Evaluation Protocol

### Diagnosis

- one-vs-rest ROC per class
- macro-averaged ROC-AUC
- overall accuracy
- class-wise precision, sensitivity, specificity, F1
- confusion matrix

### Reader Study

- subset size: `100` test cases
- reference: expert consensus
- comparator: junior dentists
- metrics: weighted Cohen's kappa and mean time per case

### Drafting

- retrieval quality:
  - Hit Rate@1
  - MRR
  - NDCG@3
  - Context Precision
- draft quality:
  - Faithfulness
  - Answer Relevance
  - Accuracy
  - Context Utilization
- conditional module-level evaluation:
  - Correctness
  - Usefulness
  - Safety

## Important Interpretation Rule

The `99.2%` correctness of the treatment drafting module is explicitly a **conditional metric** under the diagnosis-conditioned evaluation protocol. It must not be interpreted as unconditional end-to-end clinical effectiveness.
