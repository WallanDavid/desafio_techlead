# Desafio Tech Lead — VBL Energy Intelligence

Este repositório contém os **3 documentos em PDF** solicitados no desafio (Arquitetura C4, Code Review do legado e Kickoff).

## Entregáveis (PDFs)

- **PDF A — Arquitetura e Modelagem (C4 Nível 1 e 2)**  
  `docs/architecture/PDF_A_Arquitetura_C4.pdf`
- **PDF B — Avaliação Técnica do Legado (TelemetryService.cs)**  
  `docs/code-review/PDF_B_CodeReview_TelemetryService.pdf`
- **PDF C — Estratégia, Liderança e Kickoff (4 slides)**  
  `docs/kickoff/PDF_C_Kickoff_4_Slides.pdf`

## Fontes (Markdown)

Os PDFs acima são gerados a partir dos arquivos `.md` no mesmo diretório:
- `docs/architecture/PDF_A_Arquitetura_C4.md`
- `docs/code-review/PDF_B_CodeReview_TelemetryService.md`
- `docs/kickoff/PDF_C_Kickoff_4_Slides.md`

## Como regerar os PDFs (opcional)

Pré-requisito: Python 3.x com `reportlab`.

```bash
python tools/generate_pdfs.py
```

## Estrutura

```text
docs/
  architecture/
  code-review/
  kickoff/
tools/
```

