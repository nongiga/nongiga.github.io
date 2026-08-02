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
