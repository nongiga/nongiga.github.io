"""Build the August 2026 Research Systems CV from a clean document model."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "Noga_Aharony_CV_Academic_August_2026_candidate.docx"

CHARCOAL = "1D2429"
COBALT = "24497F"
VERMILION = "D15339"
SECONDARY = "5C6871"
METADATA = "6D7982"
RULE = "D2D7DB"
WHITE = "FFFFFF"
DEEP_SLATE = "1D2C3B"
PRIMARY_FONT = "Arial"
METADATA_FONT = "Courier New"

USABLE_WIDTH = 10368
SECTION_INDEX_WIDTH = 548
SECTION_CONTENT_WIDTH = 9820
ENTRY_TEXT_WIDTH = 8524
ENTRY_DATE_WIDTH = 1296


@dataclass(frozen=True)
class Entry:
    date: str
    title: str
    context: str = ""


@dataclass(frozen=True)
class Publication:
    date: str
    authors: str
    title: str
    venue: str


EDUCATION = (
    Entry(
        "Current",
        "Doctor of Philosophy, Systems Biology · Columbia University",
        "Thesis: Systematic Evaluation Frameworks for Foundational Genome Language Models · Advisor: Mohammed AlQuraishi, PhD",
    ),
    Entry(
        "2021",
        "Master of Science, Biology · Technion — Israel Institute of Technology",
        "Thesis: Rapid Gene Content Alteration in Recurring Infections · Advisor: Roy Kishony, PhD",
    ),
    Entry(
        "2019",
        "Bachelor of Science, Honours Neuroscience · McGill University",
        "First Class Honours · Dean’s Honours List · Dean’s Multidisciplinary Research List",
    ),
)

CURRENT_FELLOWSHIPS = (
    Entry(
        "Aug–Oct 2026",
        "Pivotal Research Frontier Biodefense Fellow",
        "Developing reference-free methods to detect engineered DNA in metagenomic sequencing data.",
    ),
    Entry(
        "Sep–Dec 2026",
        "ML Alignment & Theory Scholars (MATS), Autumn 2026",
        "Biosecurity track, mentored by Gary Abel at Fourth Eon Bio; technical research including function-based DNA synthesis screening.",
    ),
)

RESEARCH_EXPERIENCE = (
    Entry(
        "2022–Current",
        "Mohammed AlQuraishi Lab · Columbia University · Program of Mathematical Genomics",
        "Developing evaluation frameworks and applications for genome language models across genomic context use, pathway-level reasoning, wastewater pathogen monitoring, and protein–protein interaction prediction. Co-developing GeneCtx and WAVEBench to test model behavior under realistic biological distribution shifts.",
    ),
    Entry(
        "2021–2023",
        "Tal Korem Lab · Columbia University · Program of Mathematical Genomics",
        "Created a model to detect small RNAs in bacterial genomes.",
    ),
    Entry(
        "2022",
        "Itsik Pe’er Lab · Columbia University · Department of Computer Science",
        "Developed a neural embedding model in hyperbolic spaces to improve small-protein prediction.",
    ),
    Entry(
        "2019–2021",
        "Roy Kishony Lab · Technion — Israel Institute of Technology · Department of Biology",
        "Built a computational pipeline to identify mobile genetic elements in recurring infections and designed experiments on eco-evolutionary dynamics in microbial communities.",
    ),
    Entry(
        "2018–2019",
        "Amine Kamen Lab · McGill University · Department of Bioengineering",
        "Designed and manufactured adeno-associated viruses carrying Cas9 for improved CAR-T cell engineering.",
    ),
    Entry(
        "2018",
        "Center for Health Security · Johns Hopkins Bloomberg School of Public Health",
        "Surveyed DNA-synthesis providers’ sequence- and customer-screening practices, informing Strengthening Security for Gene Synthesis; studied safety, innovation, and community norms in DIY biology.",
    ),
    Entry(
        "2017–2018",
        "Jonathan Kimmelman Lab · McGill University · Biomedical Ethics Unit",
        "Applied machine learning to analyze clinical-trial design factors that influence outcome forecasts; contributed to a meta-analysis.",
    ),
    Entry(
        "2017",
        "Edward Ruthazer Lab · McGill University · Montreal Neurological Institute",
        "Electroporated and imaged tadpoles to study structural plasticity in the developing visual system.",
    ),
    Entry(
        "2016–2017",
        "Rafael Najmanovich Lab · Université de Montréal · Pharmacology and Physiology",
        "Developed protein-interface software based on surrounding force fields and modeled C. difficile germination protease to identify candidate inhibitory ligands.",
    ),
)

PUBLICATIONS = (
    Publication(
        "2026",
        "Le Lievre T*, Aharony N*, Wang S, Adams E, AlQuraishi M.",
        "GeneCtx: An Evaluation Framework for Dissecting Genomic Context Use in Genome Language Models.",
        "Submitted to NeurIPS 2026 Evaluations & Datasets track.",
    ),
    Publication(
        "2023",
        "Liang C, Wagstaff J, Aharony N, Schmit V, Manheim D.",
        "Managing the Transition to Widespread Metagenomic Monitoring: Policy Considerations for Future Biosurveillance.",
        "Health Security, 21(1), 34–45.",
    ),
    Publication(
        "2022",
        "Myers A, Utpala S, Talbar S, Sanborn S, Shewmake C, Donnat C, Mathe J, Lupo U, Sonthalia R, Cui X, Szwagier T, Pignet A, Bergsson A, Hauberg S, Nielson D, Sommer S, Klindt D, Hermansen E, Vaupel M, Dunn B, Xiong J, Aharony N, Pe’er I, Ambellan F, Hanik M, Nava-Yazdani E, von Tycowicz C, Miolane N.",
        "ICLR 2022 Challenge for Computational Geometry & Topology: Design and Results.",
        "arXiv.",
    ),
    Publication(
        "2021",
        "Milman O*, Yelin I*, Aharony N, Katz R, Herzel E, Ben-Tov A, Kuint J, Gazit S, Chodick G, Patalon T, Kishony R.",
        "Community-level evidence for SARS-CoV-2 vaccine protection of unvaccinated individuals.",
        "Nature Medicine.",
    ),
    Publication(
        "2020",
        "Yelin I*, Aharony N*, Shaer-Tamar E*, Argoetti A*, Messer E, Berenbaum D, Shafran E, Kuzil A, Gandali N, Hashimshony T, Mandel-Gutfreund Y, Halberthal M, Geffen Y, Szwarcwort-Cohen M, Kishony R.",
        "Evaluation of COVID-19 RT-qPCR test in multi-sample pools.",
        "Clinical Infectious Diseases.",
    ),
    Publication(
        "2019",
        "Moco PD, Aharony N, Kamen A.",
        "Adeno-Associated Viral Vectors for Homology-Directed Generation of CAR-T cells.",
        "Biotechnology Journal.",
    ),
)

PRESENTATIONS = (
    Entry("2026", "Aharony N, AlQuraishi M. Evaluating Genome Language Model Embeddings as Transferable Priors for Metagenomic Binning.", "Accepted poster · CIBB 2026 · Rome, Italy · Sep 2–4, 2026."),
    Entry("2026", "Aharony N, Wang S, Neiswanger W. Benchmarking Genome Language Models for Novel Virus Detection in Wastewater Across Evolutionary Distance.", "Selected oral presentation · ASM BIG 2026 · Washington, DC · Oct 11–14, 2026 · Talk Oct 13."),
    Entry("2026", "Le Lievre T*, Aharony N*, AlQuraishi M. PRIME-Bench: A Benchmark for Pathway-Level Reasoning in Genome Language Models.", "Poster · ISMB 2026."),
    Entry("2026", "Aharony N. Who Holds the Reins in Agent-Assisted Systems Biology?", "Accepted poster and extended abstract · NE AI Agents Day 2026."),
    Entry("2026", "Aharony N, AlQuraishi M. Evaluating Genome Language Models for Metagenomic Binning.", "Accepted poster · Pioneering Israeli Science Conference / ScienceAbroad 2026."),
    Entry("2026", "Aharony N. Rapid Talks and Panel: 2024 Innovative Tools & Solutions Award Recipients.", "Flash talk and panelist · Pandemic Response Institute."),
    Entry("2025", "Aharony N. Genome Language Models Reading the Future of Pandemics in Wastewater.", "Flash talk · Pandemic Response Institute Innovation Showcase."),
    Entry("2022", "Aharony N. Computational Methods for Pandemic Pathogen Detection.", "Flash talk · Singer Symposium."),
    Entry("2021", "Aharony N, Kishony R. Rapid Alteration in Genetic Content Upon Recurring Infection.", "Poster · EMBL Symposium: New Approaches and Concepts in Microbiology."),
    Entry("2020", "Aharony N. Careers in Biosecurity.", "Flash talk · EAGx Virtual."),
    Entry("2018", "Aharony N, Gronvall G. How Secure is the Gene Synthesis Industry?", "Poster · Biological Weapons Convention: Meeting of Experts."),
)

AWARDS = (
    Entry("2024", "NYC Pandemic Response Institute Innovative Tools and Solutions Award", "Public-health emergency preparedness research funding."),
    Entry("2022", "EA Funds PhD Support Scholarship"),
    Entry("2021", "Open Philanthropy Early-Career Funding"),
    Entry("2020", "Miriam and Aaron Gutwirth Memorial Fellowship for Excellence in Research"),
    Entry("2019", "Leonard and Diane Sherman Interdisciplinary Graduate School Fellowship"),
    Entry("2018", "Open Philanthropy Early-Career Funding for Global Biological Risks"),
    Entry("2017, 2018", "McGill University Faculty of Science Scholarship"),
    Entry("2017", "CIHR Undergraduate Research Award in Computational Biology"),
    Entry("2016", "NSERC Undergraduate Student Research Award · FRQNT Top-Up to NSERC Undergraduate Student Research Award"),
)

TEACHING_SERVICE = (
    Entry("2016–2018", "Teaching Assistant · McGill University", "Created problem sets, held office hours, and led review sessions for biochemistry, molecular biology, neuroscience, and introductory physics."),
    Entry("2018–2023", "Research and career mentorship", "Mentored students and early-career professionals pursuing biosecurity and computational-biology projects through Effective Thesis and 80,000 Hours referrals."),
    Entry("2019", "Volunteer Consultant · Battelle Memorial Institute / ThreatSEQ", "Advised a ThreatSEQ–FBI initiative assessing whether gene-synthesis companies would detect orders containing genes from the Select Agents list."),
)

METHODS = (
    Entry("Computational", "Python · R · MATLAB · C/C++ · Java", "Biological language-model evaluation · sequence modeling · metagenomic analysis · hyperbolic embeddings · genomic pipeline development"),
    Entry("Experimental", "Microbial evolution experiments · AAV vector production · CRISPR/Cas9 delivery", "Molecular-biology workflows"),
)

LANGUAGES = (
    Entry("", "Hebrew", "Native"),
    Entry("", "English", "Near-native"),
    Entry("", "French", "Novice"),
)


def set_cell_width(cell, width: int) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.first_child_found_in("w:tcW")
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(width))
    tc_w.set(qn("w:type"), "dxa")


def set_table_geometry(table, widths: Iterable[int], indent: int = 0) -> None:
    widths = list(widths)
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table_pr = table._tbl.tblPr
    layout = table_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        table_pr.append(layout)
    layout.set(qn("w:type"), "fixed")
    table_width = table_pr.find(qn("w:tblW"))
    table_width.set(qn("w:w"), str(sum(widths)))
    table_width.set(qn("w:type"), "dxa")
    table_indent = table_pr.find(qn("w:tblInd"))
    if table_indent is None:
        table_indent = OxmlElement("w:tblInd")
        table_pr.append(table_indent)
    table_indent.set(qn("w:w"), str(indent))
    table_indent.set(qn("w:type"), "dxa")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        column = OxmlElement("w:gridCol")
        column.set(qn("w:w"), str(width))
        grid.append(column)
    for row in table.rows:
        for cell, width in zip(row.cells, widths):
            set_cell_width(cell, width)


def set_cell_margins(cell, *, top=70, start=80, bottom=70, end=80) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def shade_cell(cell, color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = tc_pr.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        tc_pr.append(shading)
    shading.set(qn("w:fill"), color)


def set_table_borders(table, *, top=RULE, bottom=RULE, inside_v=None, size="4") -> None:
    table_pr = table._tbl.tblPr
    borders = table_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        table_pr.append(borders)
    definitions = {"top": top, "bottom": bottom}
    if inside_v:
        definitions["insideV"] = inside_v
    for edge, color in definitions.items():
        node = borders.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:color"), color)


def prevent_row_split(row) -> None:
    properties = row._tr.get_or_add_trPr()
    if properties.find(qn("w:cantSplit")) is None:
        properties.append(OxmlElement("w:cantSplit"))


def set_run_font(run, font: str, size: float, color: str, *, bold=False, italic=False) -> None:
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    run.bold = bold
    run.italic = italic
    fonts = run._r.get_or_add_rPr().rFonts
    fonts.set(qn("w:ascii"), font)
    fonts.set(qn("w:hAnsi"), font)
    fonts.set(qn("w:cs"), font)


def define_style(document, name: str, size: float, color: str, *, font=PRIMARY_FONT, bold=False):
    style = document.styles.add_style(name, 1)
    style.font.name = font
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.color.rgb = RGBColor.from_string(color)
    style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), font)
    style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), font)
    style._element.get_or_add_rPr().rFonts.set(qn("w:cs"), font)
    fmt = style.paragraph_format
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(2.5)
    fmt.line_spacing_rule = WD_LINE_SPACING.SINGLE
    fmt.line_spacing = 1.1
    return style


def configure_styles(document: Document) -> None:
    normal = document.styles["Normal"]
    normal.font.name = PRIMARY_FONT
    normal.font.size = Pt(9.75)
    normal.font.color.rgb = RGBColor.from_string(CHARCOAL)
    normal.paragraph_format.space_after = Pt(2.5)
    normal.paragraph_format.line_spacing = 1.1
    # Word stores style sizes in half-point units, so approved quarter-point
    # values are rounded upward to preserve the minimum readable size.
    define_style(document, "CV Body", 10, CHARCOAL)
    define_style(document, "CV Name", 26, CHARCOAL, bold=True)
    define_style(document, "CV Role", 9, SECONDARY)
    define_style(document, "CV Contact", 8, SECONDARY)
    define_style(document, "CV Section Title", 11, CHARCOAL, bold=True)
    define_style(document, "CV Section Index", 7.5, VERMILION, font=METADATA_FONT, bold=True)
    define_style(document, "CV Entry Title", 10, CHARCOAL, bold=True)
    define_style(document, "CV Entry Context", 8.75, SECONDARY)
    define_style(document, "CV Entry Description", 9.5, CHARCOAL)
    define_style(document, "CV Date", 8, METADATA, font=METADATA_FONT)
    define_style(document, "CV Output ID", 7.5, COBALT, font=METADATA_FONT, bold=True)
    define_style(document, "CV Publication", 9.5, CHARCOAL)
    define_style(document, "CV Footer", 7.5, METADATA, font=METADATA_FONT)


def remove_default_paragraph(cell) -> None:
    paragraph = cell.paragraphs[0]
    paragraph.clear()
    paragraph.paragraph_format.space_after = Pt(0)


def add_hyperlink(paragraph, label: str, url: str):
    relationship = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), COBALT)
    properties.append(color)
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), PRIMARY_FONT)
    fonts.set(qn("w:hAnsi"), PRIMARY_FONT)
    properties.append(fonts)
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "16")
    properties.append(size)
    run.append(properties)
    text = OxmlElement("w:t")
    text.text = label
    run.append(text)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def add_field(paragraph, instruction: str) -> None:
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    value = OxmlElement("w:t")
    value.text = "2"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instr, separate, value, end):
        run = OxmlElement("w:r")
        run.append(node)
        paragraph._p.append(run)


def add_identity(document: Document) -> None:
    table = document.add_table(rows=1, cols=2)
    set_table_geometry(table, [6500, 3868])
    prevent_row_split(table.rows[0])
    for cell in table.rows[0].cells:
        set_cell_margins(cell, top=0, start=0, bottom=70, end=0)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        remove_default_paragraph(cell)

    left, right = table.rows[0].cells
    name = left.paragraphs[0]
    name.style = "CV Name"
    name.paragraph_format.space_after = Pt(1)
    run = name.add_run("Noga Aharony")
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:val"), "-6")
    run._r.get_or_add_rPr().append(spacing)
    role = left.add_paragraph(style="CV Role")
    role.add_run("Computational Biology · Systems Biology · Columbia University")

    contact = right.paragraphs[0]
    contact.style = "CV Contact"
    contact.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    contact.paragraph_format.space_before = Pt(4)
    contact.paragraph_format.space_after = Pt(2)
    top_border = OxmlElement("w:pBdr")
    border = OxmlElement("w:top")
    border.set(qn("w:val"), "single")
    border.set(qn("w:sz"), "16")
    border.set(qn("w:color"), COBALT)
    top_border.append(border)
    contact._p.get_or_add_pPr().append(top_border)
    add_hyperlink(contact, "contact@noga.science", "mailto:contact@noga.science")
    contact.add_run("  ·  ")
    add_hyperlink(contact, "website", "https://noga.science")
    contact2 = right.add_paragraph(style="CV Contact")
    contact2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_hyperlink(contact2, "GitHub", "https://github.com/nongiga")
    contact2.add_run("  ·  ")
    add_hyperlink(contact2, "Google Scholar", "https://scholar.google.com/citations?user=nVw6rmsAAAAJ")


def add_research_band(document: Document) -> None:
    table = document.add_table(rows=1, cols=4)
    set_table_geometry(table, [1656, 2904, 2904, 2904])
    set_table_borders(table, top=RULE, bottom=RULE, inside_v=RULE)
    prevent_row_split(table.rows[0])
    cells = table.rows[0].cells
    for cell in cells:
        set_cell_margins(cell, top=100, start=120, bottom=100, end=120)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        remove_default_paragraph(cell)
    shade_cell(cells[0], DEEP_SLATE)
    label = cells[0].paragraphs[0]
    label.paragraph_format.space_after = Pt(0)
    run = label.add_run("RESEARCH\nSYSTEMS")
    set_run_font(run, METADATA_FONT, 7.5, WHITE, bold=True)
    threads = (
        ("Evaluate", "Model behavior", "What do genome language models learn, use, and fail to capture?"),
        ("Transfer", "Microbial genomics", "When do representations remain useful under realistic distribution shifts?"),
        ("Detect", "Biosurveillance", "How can sequence models support detection across evolutionary distance?"),
    )
    for cell, (action, domain, question) in zip(cells[1:], threads):
        paragraph = cell.paragraphs[0]
        paragraph.paragraph_format.space_after = Pt(1)
        run = paragraph.add_run(action)
        set_run_font(run, METADATA_FONT, 7.5, VERMILION, bold=True)
        domain_p = cell.add_paragraph(style="CV Entry Context")
        domain_p.paragraph_format.space_after = Pt(2)
        domain_run = domain_p.add_run(domain)
        domain_run.bold = True
        question_p = cell.add_paragraph(style="CV Entry Description")
        question_p.paragraph_format.space_after = Pt(0)
        question_p.add_run(question)


def add_section_heading(document: Document, index: int, title: str) -> None:
    table = document.add_table(rows=1, cols=2)
    set_table_geometry(table, [SECTION_INDEX_WIDTH, SECTION_CONTENT_WIDTH])
    prevent_row_split(table.rows[0])
    for cell in table.rows[0].cells:
        set_cell_margins(cell, top=105, start=0, bottom=35, end=0)
        remove_default_paragraph(cell)
    index_p, title_p = (cell.paragraphs[0] for cell in table.rows[0].cells)
    index_p.style = "CV Section Index"
    index_p.add_run(f"{index:02d}")
    title_p.style = "CV Section Title"
    title_p.paragraph_format.keep_with_next = True
    title_p.add_run(title)
    p_pr = title_p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), RULE)
    borders.append(bottom)
    p_pr.append(borders)


def add_entry(document: Document, entry: Entry, *, compact=False) -> None:
    table = document.add_table(rows=1, cols=2)
    set_table_geometry(table, [ENTRY_TEXT_WIDTH, ENTRY_DATE_WIDTH], indent=SECTION_INDEX_WIDTH)
    prevent_row_split(table.rows[0])
    text_cell, date_cell = table.rows[0].cells
    for cell in (text_cell, date_cell):
        set_cell_margins(cell, top=18, start=0, bottom=45 if compact else 68, end=0)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        remove_default_paragraph(cell)
    title = text_cell.paragraphs[0]
    title.style = "CV Entry Title"
    title.paragraph_format.space_after = Pt(0.5 if entry.context else 0)
    title.add_run(entry.title)
    if entry.context:
        context = text_cell.add_paragraph(style="CV Entry Description")
        context.paragraph_format.space_after = Pt(0)
        context.add_run(entry.context)
    date = date_cell.paragraphs[0]
    date.style = "CV Date"
    date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    date.add_run(entry.date)


def add_publication(document: Document, number: int, publication: Publication) -> None:
    table = document.add_table(rows=1, cols=2)
    set_table_geometry(table, [ENTRY_TEXT_WIDTH, ENTRY_DATE_WIDTH], indent=SECTION_INDEX_WIDTH)
    prevent_row_split(table.rows[0])
    text_cell, date_cell = table.rows[0].cells
    for cell in (text_cell, date_cell):
        set_cell_margins(cell, top=20, start=0, bottom=75, end=0)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        remove_default_paragraph(cell)
    paragraph = text_cell.paragraphs[0]
    paragraph.style = "CV Publication"
    paragraph.paragraph_format.space_after = Pt(0)
    identifier = paragraph.add_run(f"P{number:02d}  ")
    set_run_font(identifier, METADATA_FONT, 7.5, COBALT, bold=True)
    remaining = publication.authors
    while "Aharony N" in remaining:
        before, remaining = remaining.split("Aharony N", 1)
        paragraph.add_run(before)
        own_name = paragraph.add_run("Aharony N")
        own_name.bold = True
    paragraph.add_run(remaining + " ")
    title = paragraph.add_run(publication.title + " ")
    title.italic = True
    paragraph.add_run(publication.venue)
    date = date_cell.paragraphs[0]
    date.style = "CV Date"
    date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    date.add_run(publication.date)


def add_page_break(document: Document) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.add_run().add_break(WD_BREAK.PAGE)


def configure_page_geometry(section) -> None:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)
    section.header_distance = Inches(0.30)
    section.footer_distance = Inches(0.30)


def configure_first_page_footer(section) -> None:
    section.different_first_page_header_footer = False
    footer = section.footer
    footer.is_linked_to_previous = False
    add_footer_table(footer, page_text="01 / 03")


def add_footer_table(footer, *, page_text: str | None = None, page_field=False) -> None:
    spacer = footer.paragraphs[0]
    spacer.clear()
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.line_spacing = 0.1
    table = footer.add_table(rows=1, cols=2, width=Inches(7.2))
    # Keep footer furniture slightly inside the body width; LibreOffice can
    # otherwise clip the final glyphs on a densely filled page.
    set_table_geometry(table, [8000, 2000])
    prevent_row_split(table.rows[0])
    for cell in table.rows[0].cells:
        set_cell_margins(cell, top=0, start=0, bottom=0, end=0)
        remove_default_paragraph(cell)
    left, right = (cell.paragraphs[0] for cell in table.rows[0].cells)
    left.style = "CV Footer"
    left.add_run("Noga Aharony · Curriculum Vitae · August 2026")
    right.style = "CV Footer"
    right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if page_field:
        add_field(right, "PAGE")
        right.add_run(" / 03")
    else:
        right.add_run(page_text or "")


def configure_running_section(section, page_text: str) -> None:
    section.different_first_page_header_footer = False
    header = section.header
    header.is_linked_to_previous = False
    running_header = header.paragraphs[0]
    running_header.clear()
    running_header.style = "CV Footer"
    running_header.paragraph_format.tab_stops.add_tab_stop(Inches(7.2), WD_ALIGN_PARAGRAPH.RIGHT)
    running_header.add_run("Noga Aharony")
    running_header.add_run("\tCurriculum Vitae · August 2026")

    footer = section.footer
    footer.is_linked_to_previous = False
    add_footer_table(footer, page_text=page_text)


def build_document(output_path: Path) -> Path:
    document = Document()
    section = document.sections[0]
    section.start_type = WD_SECTION.NEW_PAGE
    configure_page_geometry(section)
    configure_styles(document)
    configure_first_page_footer(section)

    add_identity(document)
    add_research_band(document)
    add_section_heading(document, 1, "Education")
    for entry in EDUCATION:
        add_entry(document, entry, compact=True)
    add_section_heading(document, 2, "Current fellowships")
    for entry in CURRENT_FELLOWSHIPS:
        add_entry(document, entry, compact=True)
    add_section_heading(document, 3, "Research experience")
    for entry in RESEARCH_EXPERIENCE[:6]:
        add_entry(document, entry, compact=True)

    continuation = document.add_section(WD_SECTION.NEW_PAGE)
    configure_page_geometry(continuation)
    configure_running_section(continuation, "02 / 03")
    add_section_heading(document, 3, "Research experience · continued")
    for entry in RESEARCH_EXPERIENCE[6:]:
        add_entry(document, entry, compact=True)

    add_section_heading(document, 4, "Publications and manuscripts")
    for number, publication in enumerate(PUBLICATIONS, 1):
        add_publication(document, number, publication)
    note = document.add_paragraph("* Equal contribution.", style="CV Entry Context")
    note.paragraph_format.left_indent = Inches(0.38)
    add_section_heading(document, 5, "Posters and talks")
    for entry in PRESENTATIONS[:7]:
        add_entry(document, entry, compact=True)

    final_page = document.add_section(WD_SECTION.NEW_PAGE)
    configure_page_geometry(final_page)
    configure_running_section(final_page, "03 / 03")
    add_section_heading(document, 5, "Posters and talks · continued")
    for entry in PRESENTATIONS[7:]:
        add_entry(document, entry, compact=True)

    add_section_heading(document, 6, "Awards and funding")
    for entry in AWARDS:
        add_entry(document, entry, compact=True)
    add_section_heading(document, 7, "Teaching, mentorship, and scientific service")
    for entry in TEACHING_SERVICE:
        add_entry(document, entry, compact=True)
    add_section_heading(document, 8, "Technical and experimental methods")
    for entry in METHODS:
        add_entry(document, entry, compact=True)
    add_section_heading(document, 9, "Languages")
    for entry in LANGUAGES:
        add_entry(document, entry, compact=True)

    core_properties = document.core_properties
    core_properties.title = "Noga Aharony — Curriculum Vitae"
    core_properties.subject = "Computational biology, systems biology, and biosurveillance research"
    core_properties.author = "Noga Aharony"
    core_properties.keywords = "computational biology; systems biology; genome language models; biosurveillance"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = build_document(args.output)
    print(f"Created {output}")


if __name__ == "__main__":
    main()
