from pathlib import Path
from docxtpl import DocxTemplate


def generate_protocol_docx(protocol):
    base_dir = Path(__file__).resolve().parent.parent
    template_path = base_dir / "templates" / "protocol_template.docx"
    output_dir = base_dir / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"protocol_{protocol.id}.docx"

    doc = DocxTemplate(str(template_path))

    context = {
        "protocol_number": protocol.protocol_number or "",
    }

    doc.render(context)
    doc.save(str(output_path))

    return output_path