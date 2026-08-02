from pathlib import Path
import re
import subprocess
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


def docx_body_blocks(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find(f"{W_NS}body")
    return ["".join(node.text or "" for node in block.iter(f"{W_NS}t")) for block in body]


def text_between(blocks: list[str], start: str, end: str) -> str:
    start_index = next(i for i, block in enumerate(blocks) if block.endswith(start))
    end_index = next(i for i, block in enumerate(blocks) if block.endswith(end))
    return "\n".join(blocks[start_index + 1 : end_index])


def profile_card(html: str, heading: str) -> str:
    match = re.search(
        rf'<div class="bio-card[^>]*>\s*<h3>{re.escape(heading)}</h3>(.*?)</div>',
        html,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"Missing profile card: {heading}")
    return match.group(1)


class ProfileContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML_PATH.read_text(encoding="utf-8")

    def test_research_first_profile_and_affiliations(self):
        self.assertIn("evaluating and applying genome language models", self.html)
        self.assertIn("ML Alignment &amp; Theory Scholars (MATS), Autumn 2026", self.html)
        self.assertIn("Biosecurity track", self.html)
        self.assertIn("Gary Abel at Fourth Eon Bio", self.html)
        self.assertIn("Pivotal Research Frontier Biodefense Fellow", self.html)
        self.assertNotIn("Incoming Fellow", self.html)
        for incorrect in ("Geoff Ralston", "Charlie Petty", "Bio Action Plan"):
            self.assertNotIn(incorrect, self.html)

    def test_public_contact_address_is_current(self):
        self.assertIn("contact@noga.science", self.html)
        self.assertIn('href="mailto:contact@noga.science"', self.html)
        self.assertNotIn("noga.aharony@columbia.edu", self.html)

        docx = docx_text(DOCX_PATH)
        self.assertIn("contact@noga.science", docx)
        self.assertNotIn("noga.aharony@columbia.edu", docx)

        pdf = subprocess.run(
            ["pdftotext", str(PDF_PATHS[0]), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertIn("contact@noga.science", pdf)
        self.assertNotIn("noga.aharony@columbia.edu", pdf)

    def test_iclr_workshop_paper_is_not_listed(self):
        removed_title = "ICLR 2022 Challenge for Computational Geometry"
        self.assertNotIn(removed_title, self.html)
        self.assertNotIn(removed_title, docx_text(DOCX_PATH))
        pdf = subprocess.run(
            ["pdftotext", str(PDF_PATHS[0]), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertNotIn(removed_title, pdf)

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
        self.assertIn(
            "ML Alignment &amp; Theory Scholars (MATS), Autumn 2026",
            recognition,
        )

    def test_research_focus_uses_three_broad_fields(self):
        research = profile_card(self.html, "Research focus")
        items = re.findall(r"<li>(.*?)</li>", research, re.DOTALL)
        self.assertEqual(
            items,
            [
                "Machine learning for biology",
                "Evaluation and interpretability",
                "Microbial genomics",
            ],
        )

    def test_fellowship_recognition_items_share_one_semantic_line(self):
        recognition = profile_card(self.html, "Fellowships &amp; recognition")
        items = re.findall(r"<li>(.*?)</li>", recognition, re.DOTALL)
        self.assertEqual(len(items), 5)
        for item in items:
            self.assertNotIn("<br>", item)
            self.assertRegex(
                item,
                r"^<strong>.+?</strong> <span class=\"muted\">&middot; .+?</span>$",
            )

    def test_current_cv_opens_as_its_own_page(self):
        self.assertNotIn('id="cv"', self.html)
        self.assertNotIn('class="cv-viewer', self.html)
        self.assertNotIn('<object', self.html)
        self.assertIn(
            '<a href="resume.pdf?v=20260802" target="_blank">CV</a>',
            self.html,
        )
        self.assertGreaterEqual(
            self.html.count('href="resume.pdf?v=20260802" target="_blank"'),
            2,
        )

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
            "Current fellowships",
            "ML Alignment & Theory Scholars (MATS), Autumn 2026",
            "Biosecurity track",
            "Gary Abel",
            "Fourth Eon Bio",
            "function-based DNA synthesis screening",
            "Pivotal Research Frontier Biodefense Fellow",
            "CIBB 2026",
            "ASM BIG 2026",
        ):
            self.assertIn(expected, text)
        for incorrect in ("Geoff Ralston", "Charlie Petty", "Bio Action Plan"):
            self.assertNotIn(incorrect, text)

    def test_cv_updates_are_in_their_intended_sections(self):
        blocks = docx_body_blocks(DOCX_PATH)
        fellowships = text_between(
            blocks,
            "Current fellowships",
            "Research experience",
        )
        presentations = text_between(blocks, "Posters and talks", "Awards and funding")
        awards = text_between(
            blocks,
            "Awards and funding",
            "Teaching, mentorship, and scientific service",
        )
        for expected in ("Pivotal Research", "ML Alignment & Theory Scholars"):
            self.assertIn(expected, fellowships)
            self.assertNotIn(expected, awards)
        for expected in ("CIBB 2026", "ASM BIG 2026"):
            self.assertIn(expected, presentations)

    def test_cv_footer_and_rows_are_publication_ready(self):
        with zipfile.ZipFile(DOCX_PATH) as archive:
            footer_names = [
                name for name in archive.namelist() if name.startswith("word/footer")
            ]
            footer_text = "".join(
                node.text or ""
                for name in footer_names
                for node in ET.fromstring(archive.read(name)).iter(f"{W_NS}t")
            )
            document = ET.fromstring(archive.read("word/document.xml"))
        self.assertIn("Noga Aharony · Curriculum Vitae · August 2026", footer_text)
        rows = list(document.iter(f"{W_NS}tr"))
        self.assertTrue(rows)
        for row in rows:
            properties = row.find(f"{W_NS}trPr")
            self.assertIsNotNone(properties)
            self.assertIsNotNone(properties.find(f"{W_NS}cantSplit"))

    def test_public_pdfs_match_and_cache_is_current(self):
        self.assertEqual(PDF_PATHS[0].read_bytes(), PDF_PATHS[1].read_bytes())
        self.assertIn('href="resume.pdf?v=20260802"', self.html)

    def test_public_pdf_contains_confirmed_updates(self):
        result = subprocess.run(
            ["pdftotext", str(PDF_PATHS[0]), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
        pdf_text = result.stdout
        for expected in (
            "ML Alignment & Theory Scholars (MATS), Autumn 2026",
            "Biosecurity track",
            "Gary Abel",
            "Fourth Eon Bio",
            "Pivotal Research Frontier Biodefense Fellow",
            "CIBB 2026",
            "ASM BIG 2026",
            "Noga Aharony · Curriculum Vitae · August 2026",
        ):
            self.assertIn(expected, pdf_text)
        for incorrect in ("Geoff Ralston", "Charlie Petty", "Bio Action Plan"):
            self.assertNotIn(incorrect, pdf_text)


if __name__ == "__main__":
    unittest.main()
