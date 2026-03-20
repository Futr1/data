# EHR Schema

The manuscript-facing model input is a combination of a panoramic radiograph and structured EHR fields.

## Required Structured Fields

| Field | Type | Description | Public release status |
| --- | --- | --- | --- |
| `patient_id` | string | De-identified internal identifier | Example only |
| `sex` | categorical | Biological sex recorded in chart | Example only |
| `age` | integer | Age at encounter | Example only |
| `chief_complaint` | text | Primary complaint at presentation | Example only |
| `history_of_present_illness` | text | Current symptom course and triggers | Example only |
| `past_history` | text | Relevant medical and dental history | Example only |
| `smoking_status` | categorical | Tobacco exposure | Example only |
| `diabetes_status` | categorical | Diabetes or glycemic control summary | Example only |
| `specialized_periodontal_examination` | object/text | Pocket depth, bleeding, mobility, furcation, recession, and related exam details | Example only |
| `adjudication_notes` | text | Specialist review summary when applicable | Not public |

## Auxiliary Materials

The following materials may support verification and expert adjudication but are not direct public model inputs in this release:

- intraoral photographs
- probing results
- supplementary chart attachments

## Public Sample Caveat

The current public sample JSON files are simplified de-identified examples. They demonstrate repository structure, not the full controlled clinical release.
