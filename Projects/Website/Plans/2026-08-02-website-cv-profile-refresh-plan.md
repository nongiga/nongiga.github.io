# Website and CV Profile Refresh Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Publish a research-first website and expanded academic CV that consistently present Noga's confirmed Pivotal and MATS affiliations and her accepted upcoming CIBB and ASM BIG presentations.

**Architecture:** Keep `index.html` as the static website source and create a dated DOCX as the canonical editable CV. Add a lightweight content-contract test that reads the HTML and DOCX OOXML directly, then render the DOCX to a PDF, copy that verified PDF to both public locations, and validate byte-for-byte agreement.

**Tech Stack:** Static HTML/CSS, Python standard library, OOXML/DOCX, bundled `python-docx`, LibreOffice-based DOCX renderer, PDF text extraction, Git.

---

### Task 1: Add the profile content contract

**Files:**
- Create: `tests/test_profile_content.py`
- Inspect: `index.html`
- Inspect: `Noga_Aharony_CV_Academic_May_2026.docx`

**Step 1: Write the failing content tests**

Create a standard-library `unittest` suite that:

- reads `index.html`;
- extracts all visible DOCX text from `word/document.xml` with `zipfile` and `xml.etree.ElementTree`;
- asserts the new research-first metadata and hero text;
- asserts the website contains `Current affiliations`, `MATS Autumn 2026`, and `Pivotal Research Frontier Biodefense Fellow`;
- asserts `Incoming Fellow` is absent;
- asserts the presentations section contains separate `Upcoming` and `Selected past` headings;
- asserts the upcoming region contains CIBB, ASM BIG, Rome, Washington, DC, and their dates;
- asserts the upcoming region does not contain NeurIPS;
- asserts `Noga_Aharony_CV_Academic_August_2026.docx` contains MATS, Pivotal, CIBB, and ASM BIG;
- asserts both public PDF files are byte-identical;
- asserts the CV URL cache version is `20260802`.

Use this test skeleton:

```python
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"
DOCX_PATH = ROOT / "Noga_Aharony_CV_Academic_August_2026.docx"
PDF_PATHS = [
    ROOT / "resume.pdf",
    ROOT / "academic-site/static/uploads/resume.pdf",
]
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    return "\n".join(node.text or "" for node in root.iter(f"{W_NS}t"))


class ProfileContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML_PATH.read_text(encoding="utf-8")

    def test_research_first_profile_and_affiliations(self):
        self.assertIn("evaluating and applying genome language models", self.html)
        self.assertIn("Current affiliations", self.html)
        self.assertIn("MATS Autumn 2026", self.html)
        self.assertIn("Pivotal Research Frontier Biodefense Fellow", self.html)
        self.assertNotIn("Incoming Fellow", self.html)

    def test_upcoming_presentations_are_confirmed_only(self):
        upcoming = re.search(
            r'<div class="presentation-group" id="upcoming-presentations">(.*?)'
            r'<div class="presentation-group" id="selected-past-presentations">',
            self.html,
            re.DOTALL,
        )
        self.assertIsNotNone(upcoming)
        text = upcoming.group(1)
        for expected in (
            "CIBB 2026",
            "September 2&ndash;4, 2026",
            "Rome, Italy",
            "ASM BIG 2026",
            "October 11&ndash;14, 2026",
            "Washington, DC",
        ):
            self.assertIn(expected, text)
        self.assertNotIn("NeurIPS", text)

    def test_cv_source_contains_confirmed_updates(self):
        text = docx_text(DOCX_PATH)
        for expected in (
            "CURRENT FELLOWSHIPS AND AFFILIATIONS",
            "MATS Autumn 2026",
            "Pivotal Research Frontier Biodefense Fellowship",
            "CIBB 2026",
            "ASM BIG 2026",
        ):
            self.assertIn(expected, text)

    def test_public_pdfs_match_and_cache_is_current(self):
        self.assertEqual(PDF_PATHS[0].read_bytes(), PDF_PATHS[1].read_bytes())
        self.assertIn('href="resume.pdf?v=20260802"', self.html)


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run the tests to verify they fail**

Run:

```bash
/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_profile_content.py -v
```

Expected: failures for missing affiliations/presentation groups and an error because the August DOCX does not yet exist.

**Step 3: Commit the failing contract**

```bash
git add tests/test_profile_content.py
git commit -m "test: define website and CV profile contract"
```

### Task 2: Rewrite the website profile and presentation hierarchy

**Files:**
- Modify: `index.html:7`
- Modify: `index.html:631`
- Modify: `index.html:658-675`
- Modify: `index.html:838-897`
- Modify: `index.html:645`
- Test: `tests/test_profile_content.py`

**Step 1: Update the metadata and hero**

Set the metadata description to:

```html
<meta name="description" content="Noga Aharony is a PhD candidate in Systems Biology at Columbia University, evaluating and applying genome language models in microbial genomics and biosurveillance.">
```

Set the hero tagline to:

```html
<p class="hero-tagline">PhD candidate in Systems Biology at Columbia, evaluating and applying genome language models in microbial genomics and biosurveillance.</p>
```

**Step 2: Replace the profile cards**

Use three cards titled `Research focus`, `Current affiliations`, and `Selected recognition`.

Research copy:

```html
<p>I study what genome language models learn, where they fail, and how they can be used in microbial genomics and biosurveillance. My work spans genomic context, pathway-level reasoning, metagenomic binning, and detection across evolutionary distance.</p>
```

Current affiliations list:

```html
<ul>
  <li><strong>PhD candidate, Systems Biology</strong> <span class="muted">Columbia University</span></li>
  <li><strong>Pivotal Research Frontier Biodefense Fellow</strong> <span class="muted">Aug&ndash;Oct 2026</span></li>
  <li><strong>MATS Autumn 2026</strong> <span class="muted">Sep&ndash;Dec 2026</span></li>
</ul>
```

Recognition copy:

```html
<p>Recipient of Open Philanthropy early-career funding, the Miriam and Aaron Gutwirth Memorial Fellowship for Excellence in Research, and the NYC-PRI Innovative Tools and Solutions award.</p>
```

**Step 3: Split presentations into upcoming and selected past groups**

Add minimal group styling near the existing writing-list CSS:

```css
.presentation-group + .presentation-group { margin-top: 3rem; }
.presentation-group-title {
  margin-bottom: 0.75rem;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
```

Create `#upcoming-presentations` with exactly two entries:

- `Evaluating Genome Language Model Embeddings as Transferable Priors for Metagenomic Binning` — accepted poster, CIBB 2026, Rome, Italy, September 2–4, 2026.
- `Benchmarking Genome Language Models for Novel Virus Detection in Wastewater Across Evolutionary Distance` — selected oral presentation, ASM BIG 2026, Washington, DC, October 11–14, 2026; talk October 13.

Create `#selected-past-presentations` and retain ISMB 2026, NE AI Agents Day 2026, ScienceAbroad 2026, PRI 2026, and PRI Innovation Showcase 2025. Do not describe past entries as upcoming.

**Step 4: Update the CV cache version**

Change the CV link to `resume.pdf?v=20260802`.

**Step 5: Run the website-facing tests**

Run:

```bash
/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests.test_profile_content.ProfileContentTests.test_research_first_profile_and_affiliations tests.test_profile_content.ProfileContentTests.test_upcoming_presentations_are_confirmed_only -v
```

Expected: PASS.

**Step 6: Commit the website rewrite**

```bash
git add index.html
git commit -m "feat: restructure research profile and presentations"
```

### Task 3: Create the expanded canonical CV source

**Files:**
- Read: `Noga_Aharony_CV_Academic_May_2026.docx`
- Create: `Noga_Aharony_CV_Academic_August_2026.docx`
- Create: `scripts/update_cv.py`
- Test: `tests/test_profile_content.py`

**Step 1: Read the document-editing instructions**

Use `@documents:documents`, including `tasks/create_edit.md` and `tasks/verify_render.md`. Preserve the current type system, table geometry, margins, header, and section styling because this is an edit of an existing CV.

**Step 2: Implement the deterministic DOCX updater**

Create `scripts/update_cv.py` using bundled `python-docx`. It must:

1. copy the May source to the August destination;
2. replace the opening profile with:

   > Computational biology PhD candidate developing evaluation frameworks and applications for genome language models. My work asks what these models learn, where they fail, and how they can be used in microbial genomics and biosurveillance, spanning genomic context, pathway-level reasoning, metagenomic binning, and detection across evolutionary distance.

3. insert `CURRENT FELLOWSHIPS AND AFFILIATIONS` after Education, using a two-column table matching existing CV tables;
4. add:
   - `Aug–Oct 2026` — `Pivotal Research Frontier Biodefense Fellow` followed by a one-sentence description of the confirmed detection-focused project;
   - `Sep–Dec 2026` — `MATS Autumn 2026` followed by `Ralston/Petty Founding & Field-Building stream`;
5. prepend the two upcoming CIBB and ASM BIG entries to `POSTERS AND TALKS`, with conference dates, locations, and formats;
6. prepend Pivotal and MATS as 2026 entries to `AWARDS AND FUNDING`, while retaining every existing row;
7. use `keep_with_next` on section headings and avoid fixed row heights.

Use a helper that clones paragraph and table formatting from adjacent section elements instead of applying Word defaults. The script must be idempotent by always starting from the unchanged May input and overwriting only the August output.

**Step 3: Run the updater**

Run:

```bash
PYTHONPATH=/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python \
/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
scripts/update_cv.py
```

Expected: `Noga_Aharony_CV_Academic_August_2026.docx` is created without modifying the May source.

**Step 4: Run the DOCX-facing test**

Run:

```bash
/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests.test_profile_content.ProfileContentTests.test_cv_source_contains_confirmed_updates -v
```

Expected: PASS.

**Step 5: Commit the CV source and reproducible updater**

```bash
git add scripts/update_cv.py Noga_Aharony_CV_Academic_August_2026.docx
git commit -m "feat: expand CV with current fellowships and presentations"
```

### Task 4: Render and visually verify the CV

**Files:**
- Read: `Noga_Aharony_CV_Academic_August_2026.docx`
- Create for QA only: `/tmp/noga-cv-august-2026/page-*.png`
- Create for QA only: `/tmp/noga-cv-august-2026/Noga_Aharony_CV_Academic_August_2026.pdf`

**Step 1: Render every page**

Run:

```bash
PYTHONPATH=/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python \
/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
/Users/nogaaharony_1/.codex/plugins/cache/openai-primary-runtime/documents/26.801.11242/skills/documents/render_docx.py \
Noga_Aharony_CV_Academic_August_2026.docx \
--output_dir /tmp/noga-cv-august-2026 \
--emit_pdf
```

Expected: a PDF and one PNG for each page, likely three pages.

**Step 2: Inspect every page image**

Open every `page-*.png` at full size and check:

- no clipped or overlapping text;
- no stranded headings;
- dates remain aligned with their entries;
- the fellowships section is visually consistent with other sections;
- the presentations and awards tables do not create awkward page breaks;
- font sizes, line spacing, margins, and table geometry remain consistent.

**Step 3: Iterate until clean**

If any issue appears, adjust only `scripts/update_cv.py`, regenerate the DOCX, rerun the content test, rerender, and inspect every page again.

**Step 4: Check PDF text**

Run:

```bash
pdftotext /tmp/noga-cv-august-2026/Noga_Aharony_CV_Academic_August_2026.pdf -
```

Expected: all fellowship and presentation details appear once in the intended sections, with no missing glyphs.

### Task 5: Publish the verified CV PDF

**Files:**
- Modify: `resume.pdf`
- Modify: `academic-site/static/uploads/resume.pdf`
- Test: `tests/test_profile_content.py`

**Step 1: Copy the verified render to both public paths**

Copy `/tmp/noga-cv-august-2026/Noga_Aharony_CV_Academic_August_2026.pdf` to both public PDF paths.

**Step 2: Run the full content contract**

Run:

```bash
/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_profile_content.py -v
```

Expected: all tests PASS.

**Step 3: Verify the PDFs are identical and readable**

Run:

```bash
shasum -a 256 resume.pdf academic-site/static/uploads/resume.pdf
pdfinfo resume.pdf
```

Expected: identical SHA-256 hashes and a readable PDF with the visually verified page count.

**Step 4: Commit the published CVs**

```bash
git add resume.pdf academic-site/static/uploads/resume.pdf
git commit -m "chore: publish August 2026 academic CV"
```

### Task 6: Preview the website and run final consistency checks

**Files:**
- Verify: `index.html`
- Verify: `resume.pdf`
- Verify: `academic-site/static/uploads/resume.pdf`
- Verify: `Noga_Aharony_CV_Academic_August_2026.docx`
- Verify: `tests/test_profile_content.py`

**Step 1: Start the local site**

Use the repository's existing local preview command in `view.sh` or an equivalent local-only static server.

**Step 2: Inspect desktop and mobile layouts**

Check at approximately 1440 px and 390 px widths:

- hero copy wraps naturally;
- profile cards remain balanced;
- current-affiliation labels and dates are readable;
- upcoming and selected-past presentation groups are visually distinct;
- no horizontal overflow occurs;
- the CV link opens the new PDF.

**Step 3: Run final automated verification**

Run:

```bash
/Users/nogaaharony_1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_profile_content.py -v
git diff --check
git status --short
```

Expected: tests pass, `git diff --check` is silent, and only pre-existing unrelated untracked files remain.

**Step 4: Review the complete diff**

Confirm that the final diff contains only the approved profile, presentation, CV-source, test, and published-PDF changes. Confirm that no planned or conditional conference is presented as accepted.

**Step 5: Commit any final QA-only corrections**

```bash
git add index.html scripts/update_cv.py tests/test_profile_content.py Noga_Aharony_CV_Academic_August_2026.docx resume.pdf academic-site/static/uploads/resume.pdf
git commit -m "fix: polish website and CV profile refresh"
```

Skip this commit if no corrections were required.

