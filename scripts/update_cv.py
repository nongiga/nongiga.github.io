"""Create the August 2026 academic CV from the unchanged May source."""

from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Noga_Aharony_CV_Academic_May_2026.docx"
DESTINATION = ROOT / "Noga_Aharony_CV_Academic_August_2026.docx"

PROFILE = (
    "Computational biology PhD candidate developing evaluation frameworks and "
    "applications for genome language models. My work asks what these models "
    "learn, where they fail, and how they can be used in microbial genomics and "
    "biosurveillance, spanning genomic context, pathway-level reasoning, "
    "metagenomic binning, and detection across evolutionary distance."
)


def paragraph_with_text(document: Document, text: str):
    return next(paragraph for paragraph in document.paragraphs if paragraph.text == text)


def table_after_heading(document: Document, heading: str):
    heading_xml = paragraph_with_text(document, heading)._p
    sibling = heading_xml.getnext()
    while sibling is not None and sibling.tag != qn("w:tbl"):
        sibling = sibling.getnext()
    if sibling is None:
        raise ValueError(f"No table follows heading: {heading}")
    return sibling


def first_paragraph(cell_xml):
    return cell_xml.find(qn("w:p"))


def run_properties(paragraph_xml, index: int = 0):
    runs = paragraph_xml.findall(qn("w:r"))
    if not runs:
        return None
    source = runs[min(index, len(runs) - 1)].find(qn("w:rPr"))
    return deepcopy(source) if source is not None else None


def clear_runs(paragraph_xml):
    for run in paragraph_xml.findall(qn("w:r")):
        paragraph_xml.remove(run)


def append_run(paragraph_xml, text: str, properties=None, break_before=False):
    run = OxmlElement("w:r")
    if properties is not None:
        run.append(deepcopy(properties))
    if break_before:
        run.append(OxmlElement("w:br"))
    text_node = OxmlElement("w:t")
    if text.startswith(" ") or text.endswith(" "):
        text_node.set(qn("xml:space"), "preserve")
    text_node.text = text
    run.append(text_node)
    paragraph_xml.append(run)


def fill_row(row_xml, date: str, runs):
    cells = row_xml.findall(qn("w:tc"))
    date_paragraph = first_paragraph(cells[0])
    body_paragraph = first_paragraph(cells[1])
    date_style = run_properties(date_paragraph, 0)
    body_styles = {
        "normal": run_properties(body_paragraph, 1),
        "bold": run_properties(body_paragraph, 0),
    }
    clear_runs(date_paragraph)
    append_run(date_paragraph, date, date_style)
    clear_runs(body_paragraph)
    for item in runs:
        append_run(
            body_paragraph,
            item[0],
            body_styles[item[1]],
            break_before=item[2] if len(item) > 2 else False,
        )


def clone_row(template_row, date: str, runs):
    row = deepcopy(template_row)
    fill_row(row, date, runs)
    return row


def insert_fellowships_section(document: Document):
    research_heading = paragraph_with_text(document, "RESEARCH EXPERIENCE")
    heading_xml = deepcopy(research_heading._p)
    heading_text = heading_xml.find(".//" + qn("w:t"))
    heading_text.text = "CURRENT FELLOWSHIPS AND AFFILIATIONS"
    heading_properties = heading_xml.find(qn("w:pPr"))
    if heading_properties is not None and heading_properties.find(qn("w:keepNext")) is None:
        heading_properties.append(OxmlElement("w:keepNext"))

    template_table = table_after_heading(document, "RESEARCH EXPERIENCE")
    table_xml = deepcopy(template_table)
    for row in table_xml.findall(qn("w:tr")):
        table_xml.remove(row)
    template_row = template_table.findall(qn("w:tr"))[0]
    table_xml.append(
        clone_row(
            template_row,
            "Aug–Oct 2026",
            [
                ("Pivotal Research Frontier Biodefense Fellow", "bold"),
                (
                    "Developing reference-free methods to detect engineered DNA "
                    "in metagenomic sequencing data.",
                    "normal",
                    True,
                ),
            ],
        )
    )
    table_xml.append(
        clone_row(
            template_row,
            "Sep–Dec 2026",
            [
                ("MATS Autumn 2026", "bold"),
                (
                    "Participant in the Ralston/Petty Founding & Field-Building stream.",
                    "normal",
                    True,
                ),
            ],
        )
    )

    research_heading._p.addprevious(heading_xml)
    research_heading._p.addprevious(table_xml)


def update_presentations(document: Document):
    table = table_after_heading(document, "POSTERS AND TALKS")
    template_row = table.findall(qn("w:tr"))[0]

    fill_row(
        template_row,
        "2026",
        [
            ("Le Lievre T*, ", "normal"),
            ("Aharony N*", "bold"),
            (
                ", AlQuraishi M. PRIME-Bench: A Benchmark for Pathway-Level "
                "Reasoning in Genome Language Models. Poster, ISMB 2026.",
                "normal",
            ),
        ],
    )

    asm = clone_row(
        template_row,
        "2026",
        [
            ("Aharony N", "bold"),
            (
                ", Wang S, Neiswanger W. Benchmarking Genome Language Models for "
                "Novel Virus Detection in Wastewater Across Evolutionary Distance. "
                "Selected oral presentation, ASM BIG 2026. Washington, DC, "
                "Oct 11–14, 2026; talk Oct 13.",
                "normal",
            ),
        ],
    )
    cibb = clone_row(
        template_row,
        "2026",
        [
            ("Aharony N", "bold"),
            (
                ", AlQuraishi M. Evaluating Genome Language Model Embeddings as "
                "Transferable Priors for Metagenomic Binning. Accepted poster, "
                "CIBB 2026. Rome, Italy, Sep 2–4, 2026.",
                "normal",
            ),
        ],
    )
    table.insert(0, asm)
    table.insert(0, cibb)


def update_awards(document: Document):
    table = table_after_heading(document, "AWARDS AND FUNDING")
    template_row = table.findall(qn("w:tr"))[0]
    mats = clone_row(
        template_row,
        "2026",
        [("MATS Autumn 2026.", "normal")],
    )
    pivotal = clone_row(
        template_row,
        "2026",
        [("Pivotal Research Frontier Biodefense Fellowship.", "normal")],
    )
    table.insert(0, mats)
    table.insert(0, pivotal)


def keep_headings_with_content(document: Document):
    for paragraph in document.paragraphs:
        if paragraph.style.name == "Heading 1":
            paragraph.paragraph_format.keep_with_next = True


def main():
    document = Document(SOURCE)
    document.paragraphs[3].text = PROFILE
    insert_fellowships_section(document)
    update_presentations(document)
    update_awards(document)
    keep_headings_with_content(document)
    document.save(DESTINATION)
    print(f"Created {DESTINATION.name}")


if __name__ == "__main__":
    main()
