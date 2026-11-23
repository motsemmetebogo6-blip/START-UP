# Closed FeCr SAF Scale-Up: 55 MW → 60 MW (65 MVA, optimised electrode geometry)

BEngTech Metallurgical Engineering design assignment, working repository.

| Path | Content | Status |
|---|---|---|
| `data/Ferrochrome_Data_Workbook.xlsx` | **Supervisor-confirmed plant data – governs over all earlier values** | Primary data |
| `docs/07_Data_Update_Notice.md` | One-page notice: what the workbook changes for each member | Issued |
| `report/Ch04_Design_Basis.md`, `Ch07_...`, `Ch12_...` | Tebogo's report chapters 4, 7, 12 (drafts, Word in `word/`) | Draft Rev A |
| `calcs/03_existing_condition_workbook.py` | Reads the workbook → `results/07_existing_condition.csv`, `results/12_alternatives_*` | Verified |
| `docs/00_SAF_Uprating_Design_Framework.md` | **Controlling document**: governing question, WP1–WP10, gates G0–G6, team allocation, interfaces, acceptance criteria, equipment classification, Power BI architecture | Rev 0 – for team approval (G0) |
| `docs/06_Work_Allocation.md`, `docs/06a_Work_Allocation_One_Page.md` | **Who does what** (Rev 6; no separate compiler, Tebogo assembles); one-page summary + detailed task cards | Rev 6 – proposed, for Tebogo to confirm |
| `docs/05_Literature_and_Evidence_Map.md` | Every source: link, what we took, where used, who checks it; gaps; download checklist | Rev 0 – issued |
| `references/papers/` | Shared folder for downloaded PDFs (R-xx_Author_Year.pdf) | Empty – awaiting downloads |
| `docs/04_Team_Work_Basis_and_Report_Structure.md` | **Team briefing**: what we work from, common numbers, rules, 20-chapter report structure with owners | Rev 0 – issued |
| `docs/03_Reference_Furnace_Specification.md` | WP1 draft: the frozen 'existing 55 MW furnace' (electrical, geometry, process, auxiliaries) | Rev A – for G1 |
| `calcs/01_reference_furnace.py` | RFS derivation and consistency checks → `results/01_rfs.csv` | Verified |
| `registers/` | Controlled common registers: assumptions, equipment classification (R/O/U/V), interfaces | Rev 0 |
| `powerbi/` + `calcs/export_powerbi.py` | Power BI star-schema dataset generated from calcs and registers | Rev 0 starter |
| `docs/01_Engineering_Design_Basis.md` | Brief interpretation, design basis, parameter and assumptions registers, case definitions, methodology, execution plan | Rev D – HP-1 cleared |
| `docs/02_Electrical_Design.md` | Baseline and 60 MW electrical operating points, R/X requirement, transformer requirements | Rev A – awaiting review (HP-2) |
| `calcs/parameters.py` | Single tagged input file | Live |
| `calcs/02_electrical_operating_points.py` | Phase 2 calculation → `results/02_*` | Verified |
| `calcs/00_screening_transformer_pf.py` | Screening check: PF needed for 60 MW within 65 MVA | Screening only |
| `word/01_Engineering_Design_Basis.docx`, `word/02_Electrical_Design.docx` | Word versions of docs 01 and 02 (generated from the Markdown; the .md files remain the master copy) | Rev D / Rev A |
| `references/REFERENCES.md` | Traceable reference register | Ongoing |
| `START` | Original file (untouched) | — |

Tags: [S] specified · [A] assumption · [L] literature · [C] calculated · [M] missing. No plant data has been invented.
