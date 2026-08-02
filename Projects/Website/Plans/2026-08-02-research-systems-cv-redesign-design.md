# Research Systems CV Redesign

## Goal

Rebuild Noga Aharony's CV as a distinctive 2026 research document optimized first for research-industry roles while retaining unmistakable academic rigor. The document should signal depth across machine learning, biology, and biosecurity through evidence and structure, not promotional language.

## Intended impression

The reader should see a late-stage PhD researcher who understands complex systems, works across disciplinary boundaries, and executes carefully. The CV should feel authored and current rather than templated, but never resemble a startup résumé, student portfolio, or EA-branded profile.

The visual direction is **E + signal** from the approved visual companion:

- a precise research-systems grid;
- one memorable research-program band near the top of page 1;
- deep cobalt and restrained burnt vermilion against charcoal and white;
- paper-style identifiers and functional metadata;
- disciplined chronology and full academic evidence below the designed opening.

## Design principle

The CV gets one designed moment: the research-program band. Everything else is quiet, regular, and easy to inspect. Distinction comes from revealing the intellectual architecture of the work, not from decorative graphics or claims about personal qualities.

The following are explicitly excluded:

- skill meters, icons, headshots, badges, keyword pills, and infographics;
- slogans such as “biosecurity leader,” “mission-driven,” or “impact-focused”;
- a sidebar résumé layout;
- bright electric blue, gradients, oversized blocks of color, or a branded-cover treatment;
- unexplained abbreviations or coded identity labels;
- duplicate fellowship entries in both the current-fellowships and awards sections.

## Content architecture

The CV remains a comprehensive three-page academic document. It will not be squeezed into two pages at the expense of readability.

### Page 1 opening

1. **Identity block**
   - Noga Aharony
   - Computational Biology · Systems Biology · Columbia University
   - email, website, GitHub, and Google Scholar using clean linked labels rather than raw long URLs
2. **Research-program band**
   - **Evaluate — Model behavior:** What do genome language models learn, use, and fail to capture?
   - **Transfer — Microbial genomics:** When do representations remain useful under realistic distribution shifts?
   - **Detect — Biosurveillance:** How can sequence models support detection across evolutionary distance?
3. **Education**
4. **Current fellowships**
   - Pivotal Research Frontier Biodefense Fellowship
   - ML Alignment & Theory Scholars (MATS), Biosecurity track, mentored by Gary Abel at Fourth Eon Bio
5. **Research experience**

The band summarizes research questions only. It does not repeat awards, metrics, or self-evaluative claims.

### Remaining sections

Sections continue in this order:

1. Publications and manuscripts
2. Posters and talks, with confirmed upcoming presentations first and formats stated explicitly
3. Awards and funding
4. Teaching, mentorship, and scientific service
5. Technical and experimental methods
6. Languages

Pivotal and MATS appear only under Current fellowships, not again under Awards and funding. Awards remain reverse chronological. Publications retain full author lists and consistently bold only Noga's name. Presentation entries consistently state poster, oral presentation, panel, or flash talk.

## Biosecurity treatment

Biosecurity is present only where substantiated:

- Pivotal's engineered-DNA detection project;
- the MATS Biosecurity track with Gary Abel at Fourth Eon Bio;
- biosurveillance and evolutionary-distance research;
- relevant presentations and prior gene-synthesis work.

The header and role line do not claim biosecurity as an identity. This keeps the signal serious, technical, and proportional to the evidence.

## Visual system

### Base preset and opening pattern

- Base document preset: `compact_reference_guide`
- First-page header pattern: `memo_masthead`
- Named override: `research_systems_cv`

The override is necessary because a CV is denser than the base reference-guide preset and uses an evidence grid rather than memo metadata. The override is applied consistently rather than through ad hoc direct formatting.

### Page geometry

- Page: US Letter, portrait
- Margins: 0.55 in top and bottom; 0.65 in left and right
- Usable width: 7.20 in / 10,368 DXA
- Header distance: 0.30 in
- Footer distance: 0.30 in
- Target length: 3 pages

### Typography

- Primary font: Helvetica Neue; Arial fallback for environments without Helvetica Neue
- Functional metadata font: Menlo; Courier New fallback
- Body: 9.75 pt, charcoal, 1.10 line spacing, 0 pt before, 2.5 pt after
- Name: 26 pt, bold, -0.3 pt character spacing, 0 pt before, 2 pt after
- Role line: 9 pt, regular, muted charcoal, 4 pt after
- Contact labels: 8 pt, regular, muted charcoal, 1.10 line spacing
- Section title: 11 pt, semibold, title case, charcoal
- Section index: 7.5 pt functional metadata font, vermilion
- Entry title: 9.75 pt, semibold
- Entry institution/context: 8.75 pt, muted charcoal
- Entry description: 9.25 pt, charcoal
- Dates: 8 pt functional metadata font, right aligned, muted blue-gray
- Publication/output identifiers: 7.5 pt functional metadata font, cobalt
- Footer: 7.5 pt functional metadata font, muted gray

The final implementation must not reduce any primary body text below 9.25 pt to solve pagination. It should adjust spacing, table geometry, or prose length first.

### Color tokens

- Charcoal: `#1D2429`
- Deep cobalt: `#24497F`
- Burnt vermilion: `#D15339`
- Secondary text: `#5C6871`
- Metadata blue-gray: `#6D7982`
- Rules: `#D2D7DB`
- White: `#FFFFFF`

Deep cobalt carries the structure. Vermilion is limited to section indices and the research-band action labels. Body copy remains charcoal. The document must remain clear when printed in grayscale.

## Component geometry

### Identity block

The name and role occupy the left side. Contact labels occupy the right side and are anchored by one 2 pt cobalt rule above them. There is no rule beneath the name and no decorative line spanning the full page.

### Research-program band

The band is a fixed-width, four-column table because it contains repeated comparable records:

- total width: 10,368 DXA;
- label column: 1,656 DXA / 1.15 in;
- three research-thread columns: 2,904 DXA / 2.017 in each;
- table indent: 0 DXA;
- top and bottom border: 0.5 pt `#D2D7DB`;
- internal vertical borders: 0.5 pt `#D2D7DB`;
- label-cell fill: `#1D2C3B`;
- thread-cell fill: white;
- cell margins: 100 DXA top/bottom and 120 DXA start/end.

The band may wrap naturally but must not split across pages. Its three research questions use complete sentences and remain factual.

### Section and entry grid

Each section has a 548 DXA / 0.38 in index rail and a 9,820 DXA / 6.82 in content area. Entry records divide the content area into an 8,524 DXA text column and a 1,296 DXA / 0.90 in right-aligned date column. Tables use fixed DXA geometry, no visible cell borders, no fixed row heights, and `cantSplit` on each entry row.

There are no horizontal rules between every entry. A single light rule accompanies each section heading. Wrapped lines align under the entry text, never under the date or section index.

### Publications and presentations

Publications use a hanging structure with a small output identifier in cobalt. Author lists, titles, venues, and status are styled consistently. Noga's name alone is bolded; equal-contribution markers remain intact.

Presentations follow the same evidence-first system. Upcoming accepted items remain clearly distinguishable through wording and chronology, not colored badges.

### Running furniture

- Page 1 footer: `Noga Aharony · Curriculum Vitae · August 2026` at left; `01 / 03` at right
- Pages 2–3 header: `Noga Aharony` at left; `Curriculum Vitae · August 2026` at right
- Pages 2–3 footer: page number in the same `NN / 03` format
- No repeating decorative top border

## Content editing rules

- Preserve all confirmed academic content from the August 2026 CV unless this design explicitly removes duplication.
- Keep only confirmed and accepted upcoming presentations.
- Use en dashes consistently for ranges and em dashes only for syntactic breaks.
- Use `Current` for the PhD date rather than inventing an unconfirmed completion year.
- Use `Technion — Israel Institute of Technology` consistently.
- Use one capitalization system for degree titles, laboratories, fellowships, and section names.
- Describe unfamiliar fellowships in one factual line; do not add competitiveness claims without evidence.
- Keep the MATS wording factually exact: Biosecurity track, Gary Abel, Fourth Eon Bio.

## Implementation approach

The current DOCX should not be patched further. Its template contains conflicting table geometries and extensive direct formatting. The redesign will be generated from a clean document model using explicit paragraph styles, fixed table geometry, consistent row rules, and named helpers for each component.

The May 2026 source and current August 2026 CV remain untouched as provenance inputs. The new builder extracts and reconstructs the approved content into a separate candidate DOCX before replacing the public August 2026 artifact.

## Verification

The redesign is complete only when all of the following pass:

- every page is rendered to PNG and reviewed at 100% zoom;
- the page count is exactly 3;
- no clipping, overlap, orphaned headings, split entry rows, or unexplained blank space appears;
- body text is at least 9.25 pt;
- all section and entry grids share exact geometry;
- the research-program band is intact on page 1;
- only Noga's name is bolded in publication author lists;
- Pivotal and MATS are not duplicated under Awards and funding;
- confirmed CIBB and ASM BIG presentations remain present;
- Ralston, Petty, and Bio Action Plan are absent;
- both public PDF copies are byte-identical to the final rendered PDF;
- the website's embedded CV, open control, and download control continue to use that public PDF.
