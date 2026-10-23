from pathlib import Path
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"
DOCX_PATH = ROOT / "Noga_Aharony_CV_Academic_October_2026_public.docx"
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
        self.assertIn(
            "evaluating biological language models for scientific capability and safety",
            self.html,
        )
        self.assertIn("ML Alignment &amp; Theory Scholars (MATS), Autumn 2026", self.html)
        self.assertIn("Biosecurity and field-building tracks", self.html)
        self.assertNotIn("Gary Abel", self.html)  # mentor changing (22 Oct 2026)
        self.assertNotIn("BiTS", self.html)  # BiTS asks for no public mention until its own announcement
        self.assertIn("Pivotal Research Frontier Biodefense Fellow", self.html)
        self.assertIn("biological AI model evaluation", self.html)
        self.assertNotIn("engineered-DNA detection", self.html)
        self.assertNotIn("Incoming Fellow", self.html)
        for incorrect in ("Geoff Ralston", "Charlie Petty", "Bio Action Plan", "Gary Abel", "BiTS"):
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
                "Biological AI model evaluation",
                "Generalization and interpretability",
                "Microbial genomics and biosurveillance",
            ],
        )

    def test_current_direction_uses_approved_public_language(self):
        for expected in (
            "Building an empirical agenda for biological AI safety",
            "we think we know surprisingly little about the capabilities of these models",
            "We are now pressure-testing the research agenda and organizational model.",
            "whether the right next step is a hosted program, an independent team, or no new capacity at all.",
        ):
            self.assertIn(expected, self.html)
        self.assertNotIn("wavebench-collab-2026-08-07-6343773", self.html)

    def test_substack_writing_is_current_and_complete(self):
        expected = (
            "https://microbia.substack.com/p/we-need-more-empirical-research-on",
            "As a researcher, I know we don't understand biological AI model capabilities at all.",
            "It's unclear what the best model in each category even is!",
            "This knowledge is also necessary from a risk evaluation and policy perspective.",
            "Without it, we can't make informed choices about how to develop these models safely.",
            "I write on Substack about all disparate topics surrounding my work",
            "from explaining proofs to biosecurity and how to have a more productive PhD.",
            "https://microbia.substack.com/",
            "https://microbia.substack.com/p/abs-always-be-submitting",
            "ABS: Always. Be. Submitting.",
            "Academia Is Like The Walking Dead: To Survive, You Have to Keep Moving",
            "https://microbia.substack.com/p/rusty-math-the-universal-approximation",
            "Rusty Math: The Universal Approximation Theorem",
            "Why am I here",
        )
        for item in expected:
            self.assertIn(item, self.html)

    def test_presentations_distinguish_current_from_upcoming(self):
        self.assertIn(
            "Current and upcoming presentations, followed by selected past work.",
            self.html,
        )
        self.assertIn("Current &amp; upcoming", self.html)

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
            '<a href="resume.pdf?v=20261022" target="_blank">CV</a>',
            self.html,
        )
        self.assertGreaterEqual(
            self.html.count('href="resume.pdf?v=20261022" target="_blank"'),
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
            "Fellowships and programs",
            "ML Alignment & Theory Scholars (MATS), Autumn 2026",
            "Biosecurity and field-building tracks",
            "SPAR",
            "BlueDot Impact",
            "Pivotal Research Frontier Biodefense Fellow",
            "CIBB 2026",
            "Professional experience",
            "Co-founder · MAGENTA",
            "Evaluation Collaborator · Radical Numerics",
            "Submitted to ICLR 2027.",
        ):
            self.assertIn(expected, text)
        for incorrect in ("Geoff Ralston", "Charlie Petty", "Bio Action Plan", "Gary Abel", "BiTS", "ASM BIG 2026"):
            self.assertNotIn(incorrect, text)

    def test_cv_updates_are_in_their_intended_sections(self):
        blocks = docx_body_blocks(DOCX_PATH)
        fellowships = text_between(
            blocks,
            "Fellowships and programs",
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
        self.assertIn("CIBB 2026", presentations)
        self.assertNotIn("ASM BIG 2026", presentations)

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
        self.assertIn("Noga Aharony · Curriculum Vitae · October 2026", footer_text)
        rows = list(document.iter(f"{W_NS}tr"))
        self.assertTrue(rows)
        for row in rows:
            properties = row.find(f"{W_NS}trPr")
            self.assertIsNotNone(properties)
            self.assertIsNotNone(properties.find(f"{W_NS}cantSplit"))

    def test_public_pdfs_match_and_cache_is_current(self):
        self.assertEqual(PDF_PATHS[0].read_bytes(), PDF_PATHS[1].read_bytes())
        self.assertIn('href="resume.pdf?v=20261022"', self.html)

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
            "Biosecurity and field-building tracks",
            "SPAR",
            "Pivotal Research Frontier Biodefense Fellow",
            "CIBB 2026",
            "MAGENTA",
            "Radical Numerics",
            "Submitted to ICLR",
            "Noga Aharony · Curriculum Vitae · October 2026",
        ):
            self.assertIn(expected, pdf_text)
        for incorrect in ("Geoff Ralston", "Charlie Petty", "Bio Action Plan", "Gary Abel", "BiTS", "ASM BIG"):
            self.assertNotIn(incorrect, pdf_text)


if __name__ == "__main__":
    unittest.main()
