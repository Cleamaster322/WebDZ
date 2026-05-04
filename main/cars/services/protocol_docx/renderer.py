import re
from pathlib import Path

from docx import Document
from docx.shared import Inches


PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")


IMAGE_PLACEHOLDERS = {
    "photo_stand_test",
    "photo_gas_test",
    "photo_noise_test",
}


def iter_paragraphs(document):
    for paragraph in document.paragraphs:
        yield paragraph

    for table in document.tables:
        yield from iter_table_paragraphs(table)

    for section in document.sections:
        header = section.header
        footer = section.footer

        for paragraph in header.paragraphs:
            yield paragraph

        for table in header.tables:
            yield from iter_table_paragraphs(table)

        for paragraph in footer.paragraphs:
            yield paragraph

        for table in footer.tables:
            yield from iter_table_paragraphs(table)


def iter_table_paragraphs(table):
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                yield paragraph

            for nested_table in cell.tables:
                yield from iter_table_paragraphs(nested_table)


def build_run_ranges(paragraph):
    ranges = []
    cursor = 0

    for run in paragraph.runs:
        start = cursor
        end = start + len(run.text)
        ranges.append((run, start, end))
        cursor = end

    return ranges


def find_run_index(ranges, char_index):
    for index, (_, start, end) in enumerate(ranges):
        if start <= char_index < end:
            return index

    if ranges and char_index == ranges[-1][2]:
        return len(ranges) - 1

    return None


def replace_placeholder_in_paragraph(paragraph, context):
    if not paragraph.runs:
        return

    full_text = "".join(run.text for run in paragraph.runs)

    if "{{" not in full_text:
        return

    matches = list(PLACEHOLDER_RE.finditer(full_text))

    if not matches:
        return

    # Идём с конца, чтобы позиции предыдущих matches не ломались.
    for match in reversed(matches):
        key = match.group(1)
        value = context.get(key, "")

        ranges = build_run_ranges(paragraph)

        start_index = find_run_index(ranges, match.start())
        end_index = find_run_index(ranges, match.end() - 1)

        if start_index is None or end_index is None:
            continue

        first_run, first_start, first_end = ranges[start_index]
        last_run, last_start, last_end = ranges[end_index]

        before = first_run.text[: match.start() - first_start]
        after = last_run.text[match.end() - last_start :]

        is_image = key in IMAGE_PLACEHOLDERS and value

        if start_index == end_index:
            if is_image:
                first_run.text = before + after
                try_add_picture(first_run, value)
            else:
                first_run.text = before + str(value) + after
        else:
            if is_image:
                first_run.text = before
                try_add_picture(first_run, value)
            else:
                first_run.text = before + str(value)

            for index in range(start_index + 1, end_index):
                paragraph.runs[index].text = ""

            last_run.text = after


def try_add_picture(run, image_path):
    path = Path(image_path)

    if not path.exists():
        return

    try:
        run.add_picture(str(path), width=Inches(3.2))
    except Exception:
        # Если картинка повреждена или неподдерживаемая — просто оставляем место пустым.
        return


def render_protocol_docx(template_path, output_path, context):
    document = Document(template_path)

    for paragraph in iter_paragraphs(document):
        replace_placeholder_in_paragraph(paragraph, context)

    document.save(output_path)

    return output_path