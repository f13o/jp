#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

KANA_RANGES = [(0x3040, 0x309F), (0x30A0, 0x30FF)]
KANJI_RANGE = (0x4E00, 0x9FFF)
TEMPLATES_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR = Path(__file__).resolve().parents[3]

GRIDS = {
    8: (24, 32, "6.8mm"),
    10: (19, 25, "8.5mm"),
    15: (13, 17, "12.75mm"),
}

EMPTY = '<div class="cell"></div>'
SENTENCE_END = re.compile(r"(?<=[。？！])")
ROWS_PER_SENTENCE = 4


def is_kana(ch):
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in KANA_RANGES)


def is_kanji(ch):
    lo, hi = KANJI_RANGE
    return lo <= ord(ch) <= hi


def is_japanese(ch):
    return is_kana(ch) or is_kanji(ch)


def ref_cell(ch):
    return f'<div class="cell"><span>{ch}</span></div>'


def fill_page(cells, cols, rows):
    remaining = (cols * rows) - len(cells)
    return cells + [EMPTY] * remaining


def make_page(cells):
    return '<div class="grid">\n' + "\n".join(cells) + "\n</div>"


def split_sentences(text):
    return [s.strip() for s in SENTENCE_END.split(text) if s.strip()]


def generate_characters(text, cols, rows):
    chars = []
    seen = set()
    for ch in text:
        if is_japanese(ch) and ch not in seen:
            chars.append(ch)
            seen.add(ch)

    pages = []
    for start in range(0, len(chars), cols):
        chunk = chars[start : start + cols]
        cells = [ref_cell(ch) for ch in chunk]
        cells += [EMPTY] * (cols - len(chunk))
        cells += [EMPTY] * ((rows - 1) * cols)
        pages.append(make_page(cells))
    return pages


def sentence_row(chars, width):
    cells = []
    for i in range(width):
        cells.append(ref_cell(chars[i]) if i < len(chars) else EMPTY)
    return cells


def pack_sentences(sentences, cols):
    groups = []
    current = []
    current_len = 0
    for s in sentences:
        if current and current_len + len(s) > cols:
            groups.append(current)
            current = [s]
            current_len = len(s)
        else:
            current.append(s)
            current_len += len(s)
    if current:
        groups.append(current)
    return groups


def generate_sentences(text, cols, rows, two_columns=False, wrap=False):
    sentences = split_sentences(text)
    sents_per_col = rows // ROWS_PER_SENTENCE

    if two_columns:
        half = (cols - 1) // 2
        max_len = half
        sents_per_page = sents_per_col * 2
    else:
        max_len = cols
        sents_per_page = sents_per_col

    for s in sentences:
        if len(s) > max_len:
            sys.exit(f"Error: oracion de {len(s)} caracteres, maximo {max_len}: {s}")

    if wrap:
        groups = pack_sentences(sentences, cols)
        blocks_per_page = rows // ROWS_PER_SENTENCE
        pages = []
        for page_start in range(0, len(groups), blocks_per_page):
            page_groups = groups[page_start : page_start + blocks_per_page]
            cells = []
            row = 0
            for group in page_groups:
                combined = list("".join(group))
                cells += sentence_row(combined, cols)
                row += 1
                practice_rows = min(3, rows - row)
                cells += [EMPTY] * (practice_rows * cols)
                row += practice_rows
            cells = fill_page(cells, cols, rows)
            pages.append(make_page(cells))
        return pages

    pages = []
    for page_start in range(0, len(sentences), sents_per_page):
        page_sents = sentences[page_start : page_start + sents_per_page]

        if two_columns:
            left = page_sents[:sents_per_col]
            right = page_sents[sents_per_col:]
            right_width = cols - half - 1
            cells = []
            for row_idx in range(rows):
                sent_idx = row_idx // ROWS_PER_SENTENCE
                is_ref = row_idx % ROWS_PER_SENTENCE == 0

                if is_ref and sent_idx < len(left):
                    cells += sentence_row(list(left[sent_idx]), half)
                else:
                    cells += [EMPTY] * half

                cells.append(EMPTY)

                if is_ref and sent_idx < len(right):
                    cells += sentence_row(list(right[sent_idx]), right_width)
                else:
                    cells += [EMPTY] * right_width
            pages.append(make_page(cells))
        else:
            cells = []
            row = 0
            for sentence in page_sents:
                cells += sentence_row(list(sentence), cols)
                row += 1
                practice_rows = min(3, rows - row)
                cells += [EMPTY] * (practice_rows * cols)
                row += practice_rows
            cells = fill_page(cells, cols, rows)
            pages.append(make_page(cells))
    return pages


def name_with_counter(name: str) -> Path:
    output = OUTPUT_DIR / f"practice-{name}.html"
    n = 1
    while output.exists():
        n += 1
        output = OUTPUT_DIR / f"practice-{name}-{n}.html"
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("content")
    parser.add_argument("--sentences", action="store_true")
    parser.add_argument("--two-columns", action="store_true")
    parser.add_argument("--no-wrap", action="store_true")
    parser.add_argument("--grid", type=int, choices=[8, 10, 15], required=True)
    args = parser.parse_args()

    if (args.two_columns or args.no_wrap) and not args.sentences:
        sys.exit("Error: --two-columns y --no-wrap solo funcionan con --sentences")
    if args.two_columns and not args.no_wrap:
        sys.exit("Error: --two-columns requiere --no-wrap")

    cols, rows, font_size = GRIDS[args.grid]
    wrap = args.sentences and not args.no_wrap

    if args.sentences:
        pages = generate_sentences(
            args.content, cols, rows, args.two_columns, wrap
        )
    else:
        pages = generate_characters(args.content, cols, rows)

    template = (TEMPLATES_DIR / "grid.html").read_text()
    html = (
        template
        .replace("{{COLS}}", str(cols))
        .replace("{{ROWS}}", str(rows))
        .replace("{{CELL_SIZE}}", str(args.grid))
        .replace("{{FONT_SIZE}}", font_size)
        .replace("{{PAGES}}", "\n".join(pages))
    )
    output = name_with_counter(args.name)
    output.write_text(html)
    print(f"Generated: {output} ({len(pages)} page(s))")


if __name__ == "__main__":
    main()
