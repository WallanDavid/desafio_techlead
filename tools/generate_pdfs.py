from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


@dataclass(frozen=True)
class MdToPdfInput:
    md_path: Path
    pdf_path: Path
    title: str


def _make_styles():
    base = getSampleStyleSheet()
    normal = ParagraphStyle(
        "VBLNormal",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        spaceAfter=4,
    )
    h1 = ParagraphStyle(
        "VBLH1",
        parent=base["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=10,
    )
    h2 = ParagraphStyle(
        "VBLH2",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceAfter=8,
    )
    h3 = ParagraphStyle(
        "VBLH3",
        parent=base["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        spaceAfter=6,
    )
    bullet = ParagraphStyle(
        "VBLBullet",
        parent=normal,
        leftIndent=12,
        bulletIndent=0,
        spaceBefore=1,
        spaceAfter=1,
    )
    code = ParagraphStyle(
        "VBLCode",
        parent=normal,
        fontName="Courier",
        fontSize=9,
        leading=11,
        leftIndent=6,
        spaceBefore=6,
        spaceAfter=8,
    )
    return {"normal": normal, "h1": h1, "h2": h2, "h3": h3, "bullet": bullet, "code": code}


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _md_to_story(md_text: str, title: str):
    styles = _make_styles()
    story = []
    story.append(Paragraph(_escape(title), styles["h1"]))
    story.append(Spacer(1, 3 * mm))

    in_code = False
    code_lines: list[str] = []

    def flush_code():
        nonlocal code_lines
        if not code_lines:
            return
        story.append(Preformatted("\n".join(code_lines).rstrip(), styles["code"]))
        code_lines = []

    for raw in md_text.splitlines():
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if line.strip() == "---":
            story.append(PageBreak())
            continue

        if not line.strip():
            story.append(Spacer(1, 2.5 * mm))
            continue

        if line.startswith("# "):
            story.append(Paragraph(_escape(line[2:].strip()), styles["h1"]))
            continue
        if line.startswith("## "):
            story.append(Paragraph(_escape(line[3:].strip()), styles["h2"]))
            continue
        if line.startswith("### "):
            story.append(Paragraph(_escape(line[4:].strip()), styles["h3"]))
            continue

        if line.lstrip().startswith(("- ", "* ")):
            content = line.lstrip()[2:].strip()
            story.append(Paragraph(_escape(content), styles["bullet"], bulletText="•"))
            continue

        story.append(Paragraph(_escape(line.strip()), styles["normal"]))

    if in_code:
        flush_code()

    return story


def render_pdf(inp: MdToPdfInput) -> None:
    md_text = inp.md_path.read_text(encoding="utf-8")
    doc = SimpleDocTemplate(
        str(inp.pdf_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=inp.title,
        author="VBL Energy Intelligence",
    )
    story = _md_to_story(md_text, inp.title)
    doc.build(story)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    targets = [
        MdToPdfInput(
            md_path=repo_root / "docs" / "architecture" / "PDF_A_Arquitetura_C4.md",
            pdf_path=repo_root / "docs" / "architecture" / "PDF_A_Arquitetura_C4.pdf",
            title="PDF A — Arquitetura e Modelagem (C4) — VBL Energy Intelligence",
        ),
        MdToPdfInput(
            md_path=repo_root / "docs" / "code-review" / "PDF_B_CodeReview_TelemetryService.md",
            pdf_path=repo_root / "docs" / "code-review" / "PDF_B_CodeReview_TelemetryService.pdf",
            title="PDF B — Avaliação Técnica do Legado — VBL Energy Intelligence",
        ),
        MdToPdfInput(
            md_path=repo_root / "docs" / "kickoff" / "PDF_C_Kickoff_4_Slides.md",
            pdf_path=repo_root / "docs" / "kickoff" / "PDF_C_Kickoff_4_Slides.pdf",
            title="PDF C — Estratégia, Liderança e Kickoff — VBL Energy Intelligence",
        ),
    ]

    for t in targets:
        t.pdf_path.parent.mkdir(parents=True, exist_ok=True)
        render_pdf(t)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

