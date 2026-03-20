# Label Schema

PerioM-Dx is documented as a **single seven-class diagnosis task**.

| Label | Brief definition | Mutually exclusive | Figure/Table abbreviation |
| --- | --- | --- | --- |
| `gingivitis` | Gingival inflammation without staging as periodontitis | Yes | G |
| `periodontitis_stage_i` | Early-stage periodontitis meeting Stage I criteria | Yes | P1 |
| `periodontitis_stage_ii` | Moderate periodontitis meeting Stage II criteria | Yes | P2 |
| `periodontitis_stage_iii` | Severe periodontitis meeting Stage III criteria | Yes | P3 |
| `periodontitis_stage_iv` | Advanced periodontitis meeting Stage IV criteria | Yes | P4 |
| `epulis` | Epulis lesion requiring separate label-level routing | Yes | EP |
| `combined_periodontal_endodontic_lesion` | Combined periodontal-endodontic lesion | Yes | CPEL |

## Notes

- This schema replaces the earlier public split between a five-class staging task and a separate lesion-judgment task.
- Quantitative reporting should use this unified label space.
- The wording of individual guideline rules should follow the manuscript-approved source references.
