# Profile Cards and Embedded CV Design

## Goal

Make the home page hierarchy clearer by separating Noga's academic position from her fellowships, presenting the summary in point form, and showing the current CV directly on the website.

## Profile summary

The existing three-card strip remains a three-column layout on desktop and a single column on mobile. All three cards use concise bullet points.

1. **Research focus**
   - Genome language model evaluation
   - Microbial genomics and biosurveillance
   - Metagenomic binning
   - Detection across evolutionary distance
2. **Academic position**
   - PhD Candidate in Systems Biology
   - Columbia University
   - AlQuraishi Lab
3. **Fellowships & recognition**
   - Pivotal Research Frontier Biodefense Fellow
   - ML Alignment & Theory Scholars (MATS), Autumn 2026 — Biosecurity track, mentored by Gary Abel at Fourth Eon Bio
   - Open Philanthropy early-career funding
   - Miriam and Aaron Gutwirth Memorial Fellowship for Excellence in Research
   - NYC-PRI Innovative Tools and Solutions Award

The third card intentionally combines fellowships and recognition while keeping both separate from the PhD position.

## CV section

A dedicated `CV` navigation link points to a new section after Posters & Talks and before Writing. The section embeds `resume.pdf?v=20260802` in a full-width PDF viewer so visitors see the same file used by the existing CV link. Two controls remain available outside the viewer: **Open full CV** and **Download CV**.

On smaller screens, the embedded viewer remains available at a reduced height, while the external open/download controls provide a reliable fallback for browsers with limited inline PDF support. The embedded object includes fallback text linking to the full PDF.

## Verification

Automated checks will require:

- exactly three profile-card headings with the approved hierarchy;
- point-form lists in all three cards;
- no PhD text inside the fellowships-and-recognition card;
- a `CV` navigation link and a `#cv` section;
- the embedded viewer and both controls referencing the current `resume.pdf?v=20260802` artifact;
- the two published PDF copies remaining byte-identical.
