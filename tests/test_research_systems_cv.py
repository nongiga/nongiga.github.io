from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/update_cv.py"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def load_builder():
    spec = spec_from_file_location("cv_builder", SCRIPT)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def all_text(element) -> str:
    return "".join(node.text or "" for node in element.iter(f"{W}t"))


def grid_widths(table) -> list[int]:
    grid = table.find(f"{W}tblGrid")
    return [int(column.attrib[f"{W}w"]) for column in grid.findall(f"{W}gridCol")]


class ResearchSystemsCVTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp_dir.name) / "candidate.docx"
        cls.builder = load_builder()
        cls.builder.build_document(cls.output)
        cls.document = Document(cls.output)
        with zipfile.ZipFile(cls.output) as archive:
            cls.document_root = ET.fromstring(archive.read("word/document.xml"))
            cls.document_xml = archive.read("word/document.xml").decode("utf-8")
            cls.styles_root = ET.fromstring(archive.read("word/styles.xml"))
            cls.footer_xml = "".join(
                archive.read(name).decode("utf-8")
                for name in archive.namelist()
                if name.startswith("word/footer")
            )

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_content_architecture_and_research_program(self):
        text = all_text(self.document_root)
        required = (
            "Evaluate",
            "What do genome language models learn, use, and fail to capture?",
            "Transfer",
            "When do representations remain useful under realistic distribution shifts?",
            "Detect",
            "How can sequence models support detection across evolutionary distance?",
            "Pivotal Research Frontier Biodefense Fellow",
            "ML Alignment & Theory Scholars (MATS), Autumn 2026",
            "Biosecurity track, mentored by Gary Abel at Fourth Eon Bio",
            "CIBB 2026",
            "ASM BIG 2026",
        )
        for item in required:
            self.assertIn(item, text)
        for prohibited in ("Geoff Ralston", "Charlie Petty", "Bio Action Plan"):
            self.assertNotIn(prohibited, text)

        headings = [
            "Education",
            "Current fellowships",
            "Research experience",
            "Publications and manuscripts",
            "Posters and talks",
            "Awards and funding",
            "Teaching, mentorship, and scientific service",
            "Technical and experimental methods",
            "Languages",
        ]
        positions = [text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))

    def test_fellowships_are_not_duplicated_as_awards(self):
        blocks = [all_text(block) for block in self.document_root.find(f"{W}body")]
        start = next(i for i, block in enumerate(blocks) if block.endswith("Current fellowships"))
        research = next(i for i, block in enumerate(blocks) if block.endswith("Research experience"))
        awards = next(i for i, block in enumerate(blocks) if block.endswith("Awards and funding"))
        teaching = next(i for i, block in enumerate(blocks) if block.endswith("Teaching, mentorship, and scientific service"))
        fellowship_text = "\n".join(blocks[start + 1 : research])
        awards_text = "\n".join(blocks[awards + 1 : teaching])
        for distinction in ("Pivotal Research", "ML Alignment & Theory Scholars"):
            self.assertIn(distinction, fellowship_text)
            self.assertNotIn(distinction, awards_text)

    def test_exact_table_geometry_and_non_splitting_rows(self):
        tables = list(self.document_root.iter(f"{W}tbl"))
        grids = [grid_widths(table) for table in tables]
        self.assertIn([1656, 2904, 2904, 2904], grids)
        self.assertIn([548, 9820], grids)
        self.assertIn([8524, 1296], grids)
        for row in self.document_root.iter(f"{W}tr"):
            properties = row.find(f"{W}trPr")
            self.assertIsNotNone(properties)
            self.assertIsNotNone(properties.find(f"{W}cantSplit"))

    def test_named_styles_and_color_tokens(self):
        style_sizes = {}
        for style in self.styles_root.findall(f"{W}style"):
            name = style.find(f"{W}name")
            size = style.find(f"{W}rPr/{W}sz")
            if name is not None and size is not None:
                style_sizes[name.attrib[f"{W}val"]] = int(size.attrib[f"{W}val"]) / 2
        expected = {
            "CV Body": 10,
            "CV Entry Title": 10,
            "CV Entry Description": 9.5,
            "CV Publication": 9.5,
        }
        for name, size in expected.items():
            self.assertEqual(style_sizes.get(name), size)
            self.assertGreaterEqual(size, 9.25)
        self.assertIn("24497F", self.document_xml)
        self.assertIn("D15339", self.document_xml)

    def test_page_geometry_and_footer(self):
        section = self.document_root.find(f"{W}body/{W}sectPr")
        page_size = section.find(f"{W}pgSz")
        margins = section.find(f"{W}pgMar")
        self.assertEqual(page_size.attrib[f"{W}w"], "12240")
        self.assertEqual(page_size.attrib[f"{W}h"], "15840")
        self.assertEqual(margins.attrib[f"{W}top"], "792")
        self.assertEqual(margins.attrib[f"{W}bottom"], "792")
        self.assertEqual(margins.attrib[f"{W}left"], "936")
        self.assertEqual(margins.attrib[f"{W}right"], "936")
        self.assertIn("Noga Aharony · Curriculum Vitae · August 2026", self.footer_xml)


if __name__ == "__main__":
    unittest.main()
