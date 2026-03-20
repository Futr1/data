# Cohort Description

## Study Setting

PerioDx-Tx Net is documented as a retrospective two-center periodontal workflow spanning:

- West China Hospital of Stomatology, Sichuan University
- Stomatology Hospital of Zhejiang University

## Cohort Flow

- initial cohort: 3,500 cases
- excluded: 620 incomplete cases
- final analysis cohort: 2,880 cases
- train: 2,016
- validation: 576
- independent test: 288

## Incomplete Case Definition

Cases were excluded when one or more required elements for the manuscript-defined workflow were unavailable or unusable, including:

- panoramic radiograph unavailable or quality-insufficient
- missing key structured EHR fields
- incomplete specialist periodontal examination records
- imaging and record data that could not be reconciled during quality control

## Split Policy

- patient-level split
- no patient overlap across train, validation, and independent test
- training set (n = 2,016) and validation set (n = 576) derived from West China Hospital of Stomatology
- independent test set (n = 288) sampled from the two-center cohort under a prespecified strategy

## De-Identification And Adjudication

- all records were de-identified before analysis
- discrepancies in imaging-record consistency were adjudicated by senior periodontists with more than 10 years of clinical experience

## Ethics

- `WCHSIRB-D-2024-430`
- `2024-075 (Y)`

## Public Release Boundary

The public repository exposes only split summaries and de-identified examples. Patient-level ID lists are not released in this workspace.
