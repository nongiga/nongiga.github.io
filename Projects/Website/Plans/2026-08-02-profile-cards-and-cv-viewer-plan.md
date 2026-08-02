# Profile Cards and Embedded CV Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate the PhD position from fellowships, make all profile cards point-form, and show the current CV directly on the home page.

**Architecture:** Keep the single-file static-site structure and update the existing profile-card markup and styles in `index.html`. Add a semantic `#cv` section that embeds the already-published `resume.pdf?v=20260802`, with open and download fallbacks. Extend the existing content-contract test suite so the page hierarchy and shared PDF target cannot regress.

**Tech Stack:** Static HTML, CSS, Python `unittest`, browser-native PDF embedding

## Global Constraints

- Keep exactly three profile cards on desktop and stack them on mobile.
- Present every profile-card item in point form.
- Keep the PhD position out of the fellowships-and-recognition card.
- Use `resume.pdf?v=20260802` as the single current CV artifact.
- Do not alter the CV document or either published PDF.

---

### Task 1: Profile hierarchy and CV viewer

**Files:**
- Modify: `tests/test_profile_content.py`
- Modify: `index.html`

**Interfaces:**
- Consumes: the existing `resume.pdf?v=20260802` public artifact and `.bio-strip` card system
- Produces: three point-form profile cards, `#cv`, `.cv-viewer`, and open/download links

- [ ] **Step 1: Write the failing profile-card and CV-viewer tests**

Add a helper that extracts a profile card by heading and add these assertions:

```python
def profile_card(html: str, heading: str) -> str:
    match = re.search(
        rf'<div class="bio-card[^>]*>\s*<h3>{re.escape(heading)}</h3>(.*?)</div>',
        html,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"Missing profile card: {heading}")
    return match.group(1)

def test_profile_cards_are_point_form_and_separate_fellowships(self):
    research = profile_card(self.html, "Research focus")
    position = profile_card(self.html, "Academic position")
    recognition = profile_card(self.html, "Fellowships &amp; recognition")
    for card in (research, position, recognition):
        self.assertIn("<ul>", card)
        self.assertIn("<li>", card)
    self.assertIn("PhD Candidate in Systems Biology", position)
    self.assertNotIn("Pivotal Research", position)
    self.assertNotIn("MATS", position)
    self.assertNotIn("PhD Candidate", recognition)
    self.assertIn("Pivotal Research Frontier Biodefense Fellow", recognition)
    self.assertIn("ML Alignment &amp; Theory Scholars (MATS), Autumn 2026", recognition)

def test_current_cv_is_visible_and_downloadable(self):
    self.assertIn('<a href="#cv">CV</a>', self.html)
    cv = re.search(r'<section class="section" id="cv">(.*?)</section>', self.html, re.DOTALL)
    self.assertIsNotNone(cv)
    self.assertIn('data="resume.pdf?v=20260802"', cv.group(1))
    self.assertIn('href="resume.pdf?v=20260802" target="_blank"', cv.group(1))
    self.assertIn('href="resume.pdf?v=20260802" download', cv.group(1))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 tests/test_profile_content.py`

Expected: failures for the missing Academic position card, Fellowships & recognition card, `#cv` section, and CV navigation link.

- [ ] **Step 3: Implement the point-form cards**

Replace the current card bodies with three `<ul>` lists headed `Research focus`, `Academic position`, and `Fellowships &amp; recognition`. Keep the approved wording from the design. Add subtle bullet markers using `.bio-card li::before`, with left padding on list items.

- [ ] **Step 4: Implement the embedded CV section**

Add `CV` to the main navigation. Insert `#cv` after `#talks` and before `#writing`, containing:

```html
<object class="cv-viewer" data="resume.pdf?v=20260802" type="application/pdf">
  <p>Your browser cannot display the embedded CV. <a href="resume.pdf?v=20260802" target="_blank">Open the full CV</a>.</p>
</object>
```

Add separate `.cv-actions` links for **Open full CV** and **Download CV**. Style the viewer as a full-width, bordered, rounded surface with a desktop height of `850px` and a mobile height of `600px`.

- [ ] **Step 5: Run the complete content suite**

Run: `python3 tests/test_profile_content.py`

Expected: all tests pass, including the existing byte-equality check for the two public PDFs.

- [ ] **Step 6: Check markup and review the page**

Run: `git diff --check`

Confirm the embedded target, open target, download target, and hero CV target all use `resume.pdf?v=20260802`. Review the updated page in the existing local preview.

- [ ] **Step 7: Commit**

```bash
git add index.html tests/test_profile_content.py
git commit -m "feat: separate profile hierarchy and embed CV"
```
