from pathlib import Path
from docxtpl import DocxTemplate


def generate_test_docx():
    base_dir = Path(__file__).resolve().parent
    template_path = base_dir / "templates" / "protocol_template.docx"
    output_path = base_dir / "templates" / "protocol_test_output.docx"

    print("TEMPLATE:", template_path)
    print("OUTPUT:", output_path)

    doc = DocxTemplate(str(template_path))

    context = {
        "protocol_number": "TMP-001"
    }

    doc.render(context)
    doc.save(str(output_path))

    return output_path