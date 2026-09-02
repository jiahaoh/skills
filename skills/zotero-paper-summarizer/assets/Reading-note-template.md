
> **Instructions for AI Agent:** Generate a markdown file named `<FirstAuthor et al. (Year) - ShortDescription>.md`. Classify the article type first, then complete all **Core Sections** and relevant **Conditional Sections** based on the classification.

---

## Article Classification

> **Instruction:** Select ONE primary type. If the article spans multiple types, choose the dominant focus. Make the selected article type one of the additional keywords. Do not include the "Article Classification" section in the final output, just for generation guidance. The final output should start with the YAML frontmatter block.

- [ ] **Biological Discovery** — Focus on novel biological findings, mechanisms, or disease insights
- [ ] **Technology Development** — Focus on new methods, tools, pipelines, or computational frameworks
- [ ] **Resource/Atlas** — Focus on generating reference datasets, atlases, or databases
- [ ] **Review** — Synthesis of existing literature, perspectives, or field overviews

---

## YAML Frontmatter

> **Instruction:** All article metadata goes into YAML frontmatter at the very top of the file. The frontmatter block is delimited by `---`. Use the following fields:

```yaml
---
title: "[Full article title]"
authors: "[First/co-first author(s); Corresponding author(s)]"
journal: "[Journal name only, e.g. Nature Methods; for preprints use bioRxiv, medRxiv, arXiv, etc.]"
doi: "[DOI string, e.g. 10.1038/s41586-023-05818-6]"
zotero_key: "[8-character Zotero item key, e.g. MXQZECW5]"
zotero_uri: "zotero://select/library/items/[Zotero item key]"
year: [Publication year as number]
status: "[published | preprint]"
summary: "[One sentence: WHAT the paper contributes — its main result or tool]"
motivation: "[One line: WHY the project exists — the field gap or problem it addresses]"
storyline: "[One line: HOW the paper closes that gap — method → key findings → model or conclusion]"
tags:
  - keyword-one
  - keyword-two
  - keyword-three
---
```

- Treat `summary`, `motivation`, and `storyline` as three distinct lenses; do not repeat the same sentence:
  - `summary` = what the paper delivers.
  - `motivation` = why the work was needed.
  - `storyline` = how the evidence and method build the paper's argument.
- `zotero_key` is the key of the source Zotero item. `zotero_uri` wraps the same key as `zotero://select/library/items/<key>`. Include both when the note corresponds to a Zotero item; otherwise omit both rather than inventing a key.
- Extract up to five tags. Format: `keyword-phrase` (use hyphens, avoid apostrophes, no `#` prefix)
- **Reuse the existing vocabulary — never coin a case / plural / spelling variant of a tag that already exists in `04.Reading/Notes/`.** Prefer an existing tag over a near-synonym. Use these canonical forms:

  | Dimension | Use these exact tags |
  |-----------|----------------------|
  | Article type (the one matching the classification above) | `biological-discovery`, `technology-development`, `resource-atlas`, `review` |
  | Sequencing assay (standard abbreviations) | `scRNA-seq`, `snRNA-seq` — never the spelled-out `single-cell-rna-seq` / `single-nucleus-rna-seq` variants |
  | Modality umbrella | `spatial-transcriptomics`, `single-cell-transcriptomics`, `proteomics`, `spatial-proteomics` |
  | Platform (keep as its own tag *alongside* the umbrella) | `Xenium`, `MERFISH`, `STARmap-PLUS`, `in-situ-sequencing`, `imaging-based-transcriptomics` |
  | Disease (s-form, no apostrophe) | `Alzheimers-disease`, `multiple-sclerosis`, `progressive-MS`, `Parkinsons-disease`, `Down-syndrome` |
  | Cell type (plural) | `microglia`, `astrocytes`, `oligodendrocytes`, `neurons`, `disease-associated-microglia`, `reactive-astrocytes` |
  | Common themes | `neuroinflammation`, `neurodegeneration`, `cell-cell-communication`, `deep-learning`, `foundation-model`, `multi-modal-integration`, `cell-segmentation`, `rna-localization`, `subcellular-localization`, `subcellular-mrna-localization` |

  Diseases take the `s`-form without apostrophe (`Alzheimers-disease`, not `Alzheimer` / `Alzheimer-disease`). Cell types are plural (`astrocytes`, not `astrocyte`). Spell out abbreviations only when no standard one exists (`disease-associated-microglia`, not `DAM`).
- The `summary` field should be a single sentence capturing the core contribution
- The `journal` field should contain the journal or preprint-server name only; do not append volume, issue, pages, dates, or citation text
- The `doi` field should be the raw DOI string without markdown link formatting
- The `status` field is `preprint` for non-peer-reviewed preprints (bioRxiv, medRxiv, arXiv, Research Square, etc.) and `published` otherwise
- The static table is a starting point. The live vocabulary in `04.Reading/Notes/` is authoritative; inspect it with `python3 <skill-dir>/scripts/note_tools.py tags` and validate proposed tags with `python3 <skill-dir>/scripts/note_tools.py check-tags <tag>...`

---

## Overview

> **Instruction:** Write 3–5 sentences summarizing the research question, approach, and main contribution.

[Summary paragraph]

**Dataset:** [Describe datasets used: species, tissue, sample size, platform/technology. Write "N/A" if no new data generated]

**Workflow:** [Using numbered list to briefly describe the analytical pipeline or experimental workflow. Write "N/A" for review articles]

---

## Key Takeaways

> **Instruction:** Extract 3–6 major conclusions. Prioritize novel findings over confirmatory results. For reviews, extract key synthesis points or emerging themes.

- [Finding 1]
- [Finding 2]
- [Finding 3]

---

## Contents

> **Instruction:** Summarize each major result section with subheadings. Reference supporting figures (e.g., Figure 3A). Focus on results, not methods repetition. For reviews, summarize major thematic sections.

### [Result Section 1 Title]
[Summary with figure references]

### [Result Section 2 Title]
[Summary with figure references]

---

## Conclusion / Future Directions

> **Instruction:** Summarize the authors' stated conclusions and proposed future work. Note any implications for the field. Also include connections to other work or questions for follow-up.

[Summary paragraph]

---

## Limitations

> **Instruction:** Extract 2–3 key limitations. Include both author-acknowledged limitations and any apparent gaps. For reviews, note scope limitations or biases in literature coverage.

- [Limitation 1]
- [Limitation 2]

---

# Conditional Sections

> **Instruction:** Complete the relevant section(s) based on Article Classification above.

---

## [If Technology Development] Technical Implementation

> **Instruction:** First, classify the method type, then complete the relevant subsections. Do not include the "Method Type" section in the final output, just for generation guidance.

### Method Type
- [ ] **Computational** — Software, algorithm, pipeline, or analytical method
- [ ] **Wet-lab** — Experimental protocol, assay, or laboratory technique
- [ ] **Hybrid** — Integrated wet-lab and computational workflow (complete both)

---

### [If Computational] Computational Framework
- **Programming language(s):** [e.g., Python 3.9, R 4.2]
- **Core dependencies/libraries:** [e.g., PyTorch, Scanpy, Squidpy]
- **Architecture type:** [e.g., graph neural network, variational autoencoder, transformer]
- **Input data format:** [Expected input structure]
- **Output:** [What the method produces]

### [If Computational] Key Hyperparameters
| Parameter | Value/Range | Notes |
|-----------|-------------|-------|
| [param 1] | [value]     | [context if relevant] |
| [param 2] | [value]     | [context if relevant] |

### [If Computational] Codebase
- **Repository:** [GitHub/GitLab URL or "Not available"]
- **Documentation quality:** [Brief assessment: well-documented / minimal / none]
- **Reproducibility:** [Note if demo data, tutorials, or Docker containers are provided]

---

### [If Wet-lab] Protocol Overview
- **Technology category:** [e.g., sequencing library prep, imaging, CRISPR screening, protein assay]
- **Key reagents/materials:** [Critical or novel reagents required]
- **Platform/instrument:** [e.g., 10x Genomics, Illumina, Visium, custom microscopy setup]
- **Throughput:** [Samples/cells per run, scalability notes]
- **Estimated time/cost:** [If reported]

### [If Wet-lab] Critical Protocol Steps
> **Instruction:** Identify 2–4 steps that are critical for success or represent novel modifications.

- [Step 1: brief description and why it matters]
- [Step 2: brief description and why it matters]

### [If Wet-lab] Validation & Benchmarking
- **Compared against:** [Existing methods used as benchmarks]
- **Key performance metrics:** [e.g., sensitivity, specificity, resolution, reproducibility]
- **Validation approach:** [How was the method validated?]

---

### Novel Methodological Ideas
> **Instruction:** Identify 1–3 conceptual innovations that distinguish this method from prior approaches. Applies to both computational and wet-lab methods.

- [Innovation 1: brief description of what's new and why it matters]
- [Innovation 2]

---

## [If Biological Discovery] Key Biological Insights

> **Instruction:** Elaborate on mechanistic findings, disease relevance, or translational implications.

### Mechanistic Findings
[Describe key molecular/cellular mechanisms uncovered]

### Disease/Translational Relevance
[Describe implications for disease understanding or therapeutic development. Write "N/A—basic biology focus" if not applicable]

---

## [If Resource/Atlas] Resource Description

> **Instruction:** Describe the resource's scope, accessibility, and utility.

### Resource Scope
- **Coverage:** [Species, tissues, conditions, cell types covered]
- **Scale:** [Number of cells, samples, donors, etc.]
- **Data modalities:** [e.g., scRNA-seq, spatial, ATAC, proteomics]

### Accessibility
- **Data portal:** [URL if available]
- **Raw data accession:** [GEO, ArrayExpress, etc.]
- **Processed data formats:** [h5ad, Seurat object, etc.]

### Recommended Use Cases
[Describe how other researchers might use this resource]

---

## [If Review] Review Structure

> **Instruction:** Capture the organizational logic and scholarly contribution of the review.

### Review Type
- [ ] **Narrative review** — Qualitative synthesis of a topic
- [ ] **Systematic review** — Structured search and analysis methodology
- [ ] **Perspective/Opinion** — Viewpoint piece with selective evidence
- [ ] **Meta-analysis** — Quantitative synthesis of published results

### Scope & Coverage
- **Time range of literature:** [e.g., 2015–2024]
- **Primary focus:** [Main topic/question addressed]
- **Sub-topics covered:** [List major themes or sections]

### Key Frameworks or Models
> **Instruction:** Identify any conceptual frameworks, models, or taxonomies proposed or synthesized by the authors.

- [Framework 1: brief description]
- [Framework 2: brief description]

### Knowledge Gaps Identified
> **Instruction:** Extract explicit gaps or open questions the authors highlight as needing future research.

- [Gap 1]
- [Gap 2]

### Key References to Follow Up
> **Instruction:** List 3–5 seminal or highly relevant papers cited that warrant deeper reading.

- [Reference 1: brief note on relevance]
- [Reference 2: brief note on relevance]

---

## Concept Clarification

> **Instruction:** Define 2–4 important concepts, terms, or techniques that are central to understanding this article. Use external sources if needed for complete explanations.

### [Concept 1]
[Definition and relevance to article]

### [Concept 2]
[Definition and relevance to article]
