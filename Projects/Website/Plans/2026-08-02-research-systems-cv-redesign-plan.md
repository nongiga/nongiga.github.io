# Research Systems CV Redesign Implementation Plan

> **Required subskill:** Use `superpowers:executing-plans` to implement this plan task by task. Use `superpowers:test-driven-development` for each behavior change and `superpowers:verification-before-completion` before reporting completion.

**Goal:** Rebuild the August 2026 CV from a clean document model as a distinctive, rigorous, three-page “Research Systems” CV, then publish the verified PDF to both website locations.

**Architecture:** Replace the source-template patcher with a deterministic DOCX builder whose content, styles, and table geometry are explicit in Python. Generate a separate candidate artifact first, verify its structure and rendered pages, and only then replace the public DOCX/PDF. Keep website assertions separate from document-builder assertions so failures identify the correct layer.

**Technology:** Python 3, `python-docx`, WordprocessingML helpers, LibreOffice-backed DOCX rendering, `pdftotext`, Python `unittest`.

---

## Task 1: Define the new document contract with failing tests

**Files:**
- Create: `tests/test_research_systems_cv.py`
- Modify: `tests/test_profile_content.py`
- Test: `tests/test_research_systems_cv.py`

### Step 1: Add a temporary-build test harness

Import `scripts/update_cv.py` through `importlib`, call `build_document(output_path)`, and open the result with `python-docx` and `zipfile`. The harness must build in `tempfile.TemporaryDirectory()` so no public artifact changes during TDD.

```python
@classmethod
def setUpClass(cls):
    cls.temp_dir = tempfile.TemporaryDirectory()
    cls.output = Path(cls.temp_dir.name) / "candidate.docx"
    cv_builder.build_document(cls.output)
    cls.document = Document(cls.output)
    with zipfile.ZipFile(cls.output) as archive:
        cls.document_xml = archive.read("word/document.xml").decode("utf-8")
        cls.styles_xml = archive.read("word/styles.xml").decode("utf-8")
```

### Step 2: Assert the approved content architecture

Add tests for:

- the three research-band statements and action labels;
- section order from Education through Languages;
- Current fellowships containing Pivotal and MATS;
- Awards and funding containing neither fellowship;
- exact MATS wording with Biosecurity track, Gary Abel, and Fourth Eon Bio;
- confirmed CIBB and ASM BIG items;
- absence of Ralston, Petty, and Bio Action Plan.

### Step 3: Assert the visual-system primitives

Inspect styles and XML to require:

- named styles with body text no smaller than 9.25 pt;
- color tokens `24497F` and `D15339`;
- a four-column table grid `[1656, 2904, 2904, 2904]`;
- section grids `[548, 9820]` and entry grids `[8524, 1296]`;
- `cantSplit` on research-band and entry rows;
- Letter page size and the approved margins;
- footer wording `Noga Aharony · Curriculum Vitae · August 2026`.

### Step 4: Update public-artifact expectations

Change the old footer assertion in `tests/test_profile_content.py` to the approved wording and change the awards test so it requires that Pivotal and MATS appear under Current fellowships but not under Awards and funding.

### Step 5: Run the new tests and confirm failure

Run:

```bash
python -m unittest tests.test_research_systems_cv -v
```

Expected: FAIL because `build_document` and the clean visual system do not exist yet.

### Step 6: Commit the contract

```bash
git add tests/test_research_systems_cv.py tests/test_profile_content.py
git commit -m "test: define research systems CV contract"
```

## Task 2: Replace the template patcher with a clean CV builder

**Files:**
- Replace: `scripts/update_cv.py`
- Test: `tests/test_research_systems_cv.py`

### Step 1: Define structured content constants

Represent education, fellowships, research experience, publications, presentations, awards, teaching/service, methods, and languages as ordered records. Keep dates and status wording in the data rather than embedding them in layout helpers.

```python
CURRENT_FELLOWSHIPS = [
    Entry(
        date="Aug–Oct 2026",
        title="Pivotal Research Frontier Biodefense Fellow",
        context="Developing reference-free methods to detect engineered DNA in metagenomic sequencing data.",
    ),
    Entry(
        date="Sep–Dec 2026",
        title="ML Alignment & Theory Scholars (MATS), Autumn 2026",
        context="Biosecurity track, mentored by Gary Abel at Fourth Eon Bio; technical research including function-based DNA synthesis screening.",
    ),
]
```

Transcribe the remaining approved content from the committed August CV, normalizing only the rules in the design specification.

### Step 2: Establish page geometry and named styles

Create `Document()` from scratch. Configure US Letter, 0.55-inch vertical margins, 0.65-inch horizontal margins, and 0.30-inch header/footer distances. Define named paragraph styles for identity, metadata, body, section title/index, entry title/context/description, date, output identifier, and footer. Use Helvetica Neue with Arial fallback and Menlo with Courier New fallback. Store point sizes and colors centrally.

### Step 3: Implement reusable WordprocessingML helpers

Implement focused helpers for:

- fixed table width and explicit `tblGrid` columns;
- cell margins, shading, and borders;
- `cantSplit`, `keep_with_next`, and paragraph spacing;
- hyperlinks with clean labels;
- page-number fields and distinct first-page header/footer;
- character spacing for the name;
- safe bolding of Noga's name only in publication author lists.

No component may apply an unexplained font size or color directly; component helpers must draw from named tokens.

### Step 4: Build the identity block and research-program band

Create a two-column identity block with name/role on the left and linked contact labels on the right. Add the fixed four-column research band using exact widths `[1656, 2904, 2904, 2904]`, charcoal label-cell fill, restrained vermilion action labels, light rules, and a non-splitting row.

### Step 5: Build sections and evidence entries

Use a 548/9820 section grid and an 8524/1296 entry grid. Render all sections in the approved order, with reverse chronology where appropriate. Use publication identifiers and hanging author/title/venue structure; use consistent presentation-format wording; do not duplicate current fellowships under Awards.

### Step 6: Add running furniture and deterministic output

Add the page-one footer, subsequent-page header, and `NN / 03` numbering fields. Expose:

```python
def build_document(output_path: Path) -> Path:
    ...
    document.save(output_path)
    return output_path
```

and a CLI `--output` option defaulting to `Noga_Aharony_CV_Academic_August_2026_candidate.docx`.

### Step 7: Run structural tests until green

Run:

```bash
python -m unittest tests.test_research_systems_cv -v
```

Expected: PASS.

### Step 8: Commit the clean builder

```bash
git add scripts/update_cv.py
git commit -m "feat: build research systems CV from clean model"
```

## Task 3: Generate and audit the candidate document

**Files:**
- Generate: `Noga_Aharony_CV_Academic_August_2026_candidate.docx`
- Modify as needed: `scripts/update_cv.py`
- Test: `tests/test_research_systems_cv.py`

### Step 1: Generate the candidate with bundled dependencies

Run the builder with the bundled Python runtime and repository dependency path. Keep the candidate separate from the public August DOCX.

### Step 2: Run document lint and preset audits

Use the Documents skill's style-lint and preset-audit helpers against the candidate. Confirm the intended named-style system, page geometry, minimum text size, and table widths. Fix deviations in the builder, not by patching the candidate file.

### Step 3: Render the candidate to PNG and PDF

Use the Documents skill render script to render every page to a fresh temporary directory. Confirm that output includes exactly three page images and one PDF.

### Step 4: Inspect every page at 100% zoom

Visually inspect all three rendered pages for:

- clipping, overlap, orphaned headings, or split rows;
- balanced page density and no unexplained blank areas;
- a mature, distinctive opening without student-portfolio styling;
- consistent entry alignment, date alignment, and wrapping;
- readable body text at or above 9.25 pt;
- restrained cobalt/vermilion use and grayscale legibility.

### Step 5: Iterate through the builder

For every visual defect, add or refine a regression assertion when practical, then adjust geometry, spacing, or prose in `scripts/update_cv.py`, regenerate, rerender, and reinspect all pages. Do not shrink primary body text below 9.25 pt.

### Step 6: Commit the visually approved implementation

```bash
git add scripts/update_cv.py tests/test_research_systems_cv.py
git commit -m "fix: refine three-page research systems layout"
```

## Task 4: Publish the verified CV artifacts

**Files:**
- Replace: `Noga_Aharony_CV_Academic_August_2026.docx`
- Replace: `resume.pdf`
- Replace: `academic-site/static/uploads/resume.pdf`
- Modify: `.gitignore`
- Test: `tests/test_profile_content.py`

### Step 1: Ignore the transient candidate

Add `Noga_Aharony_CV_Academic_August_2026_candidate.docx` and Python cache directories to `.gitignore`, preserving the untracked May provenance document.

### Step 2: Promote the candidate only after visual approval

Copy the verified candidate DOCX to the public August DOCX path. Copy the PDF created from that exact candidate to both public website PDF paths.

### Step 3: Verify public artifact identity and content

Require byte-identical PDF hashes, exactly three PDF pages, the approved footer, all current fellowships and confirmed presentations, and absence of prohibited names. Confirm the website embed, open link, and download link still target `resume.pdf?v=20260802`.

### Step 4: Run the complete test suite

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: all tests PASS.

### Step 5: Perform final rendered-page review

Render the promoted public DOCX and inspect all three pages again to ensure promotion introduced no change. Compare the promoted PDF hash to both public copies.

### Step 6: Commit the publication

```bash
git add .gitignore scripts/update_cv.py tests/test_research_systems_cv.py tests/test_profile_content.py Noga_Aharony_CV_Academic_August_2026.docx resume.pdf academic-site/static/uploads/resume.pdf
git commit -m "feat: publish research systems CV"
```

## Task 5: Reconcile the website presentation and hand off for review

**Files:**
- Modify if needed: `index.html`
- Modify if needed: `tests/test_profile_content.py`

### Step 1: Normalize Fellowship & recognition website lines

Keep the combined website card, but make each item use one semantic line:

`distinction title · date · essential context`

Use the same markup and visual order for Pivotal, MATS, NSF GRFP, and the Berrie Fellowship. Preserve point form and keep the PhD in the separate Academic position card.

### Step 2: Confirm the embedded viewer shows the new PDF

Reload the local website and verify that the embedded CV, Open CV control, and Download PDF control all expose the new three-page artifact.

### Step 3: Run final verification

Run the full tests, review `git diff --check`, inspect repository status for unrelated files, and confirm no source provenance document or cache file is staged.

### Step 4: Commit any website normalization separately

```bash
git add index.html tests/test_profile_content.py
git commit -m "fix: normalize fellowship recognition entries"
```

### Step 5: Present the result for user review

Provide direct links to the final DOCX and PDF, summarize the distinctive research-program treatment and evidence hierarchy, and request visual acceptance before branch convergence or deployment.
