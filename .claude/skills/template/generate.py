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
    9: (21, 28, "7.65mm"),
    10: (19, 25, "8.5mm"),
    15: (13, 17, "12.75mm"),
}

EMPTY = '<div class="cell"></div>'
SPACER = '<div class="spacer"></div>'
SENTENCE_END = re.compile(r"(?<=[。？！])")
FURIGANA = re.compile(r"(\S+)\s\(([^)]+)\)")
FOOTNOTE = re.compile(r"\[\d+\]")


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


def ref_cell_num(ch, num):
    return f'<div class="cell"><span class="num">{num}</span><span>{ch}</span></div>'


def to_kanji(line):
    line = FURIGANA.sub(r"\1", line)
    line = FOOTNOTE.sub("", line)
    return line.replace(" ", "")


def to_kana(line):
    line = FURIGANA.sub(r"\2", line)
    line = FOOTNOTE.sub("", line)
    return line.replace(" ", "")


def fill_page(cells, cols, rows, used_rows):
    remaining = (rows - used_rows) * cols
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


def sentence_row(chars, width, num=None):
    cells = []
    for i in range(width):
        if i < len(chars):
            if i == 0 and num is not None:
                cells.append(ref_cell_num(chars[i], num))
            else:
                cells.append(ref_cell(chars[i]))
        else:
            cells.append(EMPTY)
    return cells


def parse_markdown(path, kanji=False, kana=False, furigana=False):
    text = Path(path).read_text()
    result = []
    counter = 0
    in_fence = False
    fence_type = None
    got_first = False

    for line in text.split("\n"):
        stripped = line.strip()
        if not in_fence:
            if stripped.startswith("```sentence-n"):
                in_fence = True
                fence_type = "numbered"
                got_first = False
            elif stripped.startswith("```sentence"):
                in_fence = True
                fence_type = "plain"
                got_first = False
        elif stripped.startswith("```"):
            in_fence = False
        elif not got_first:
            got_first = True
            num = None
            if fence_type == "numbered":
                counter += 1
                num = counter
            if kanji:
                result.append((to_kanji(stripped), num))
                if furigana:
                    kana_ver = to_kana(stripped)
                    if kana_ver != result[-1][0]:
                        result.append((kana_ver, None))
            elif kana:
                result.append((to_kana(stripped), num))

    return result


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


def generate_sentences(text, cols, rows, reps=3, two_columns=False, wrap=False):
    sentences = split_sentences(text)
    first_block = 1 + reps
    rest_block = 2 + reps
    sents_per_col = (
        max(0, 1 + (rows - first_block) // rest_block)
        if rows >= first_block
        else 0
    )

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
        pages = []
        for page_start in range(0, len(groups), sents_per_col):
            page_groups = groups[page_start : page_start + sents_per_col]
            cells = []
            row = 0
            for i, group in enumerate(page_groups):
                if i > 0:
                    cells.append(SPACER)
                    row += 1
                combined = list("".join(group))
                cells += sentence_row(combined, cols)
                row += 1
                practice_rows = min(reps, rows - row)
                cells += [EMPTY] * (practice_rows * cols)
                row += practice_rows
            cells = fill_page(cells, cols, rows, row)
            pages.append(make_page(cells))
        return pages

    pages = []
    for page_start in range(0, len(sentences), sents_per_page):
        page_sents = sentences[page_start : page_start + sents_per_page]

        if two_columns:
            left = page_sents[:sents_per_col]
            right = page_sents[sents_per_col:]
            right_width = cols - half - 1

            def ref_map(sents):
                refs = {}
                r = 0
                for i in range(len(sents)):
                    if i > 0:
                        r += 1
                    refs[r] = i
                    r += 1 + reps
                return refs

            left_refs = ref_map(left)
            right_refs = ref_map(right)

            cells = []
            for row_idx in range(rows):
                if row_idx in left_refs:
                    cells += sentence_row(list(left[left_refs[row_idx]]), half)
                else:
                    cells += [EMPTY] * half
                cells.append(EMPTY)
                if row_idx in right_refs:
                    cells += sentence_row(list(right[right_refs[row_idx]]), right_width)
                else:
                    cells += [EMPTY] * right_width
            pages.append(make_page(cells))
        else:
            cells = []
            row = 0
            for i, sentence in enumerate(page_sents):
                if i > 0:
                    cells.append(SPACER)
                    row += 1
                cells += sentence_row(list(sentence), cols)
                row += 1
                practice_rows = min(reps, rows - row)
                cells += [EMPTY] * (practice_rows * cols)
                row += practice_rows
            cells = fill_page(cells, cols, rows, row)
            pages.append(make_page(cells))
    return pages


def generate_line_blocks(sentences, cols, rows, reps=3):
    pages = []
    pending = list(sentences)

    while pending:
        cells = []
        row = 0
        used = 0
        for i, (s, num) in enumerate(pending):
            ref_rows = -(-len(s) // cols)
            annotation = 1 if (row > 0) else 0
            needed = annotation + (1 + reps) * ref_rows
            if row + needed > rows and row > 0:
                break
            if annotation:
                cells.append(SPACER)
                row += 1
            for r in range(ref_rows):
                chunk = list(s[r * cols : (r + 1) * cols])
                cells += sentence_row(chunk, cols, num if r == 0 else None)
                row += 1
                practice = min(reps, rows - row)
                cells += [EMPTY] * (practice * cols)
                row += practice
            used += 1
        pending = pending[used:]
        if pending:
            cells = fill_page(cells, cols, rows, row)
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
    parser.add_argument("content", nargs="?")
    parser.add_argument("--file", type=str)
    parser.add_argument("--kanji", action="store_true")
    parser.add_argument("--kana", action="store_true")
    parser.add_argument("--furigana", action="store_true")
    parser.add_argument("--sentences", action="store_true")
    parser.add_argument("--two-columns", action="store_true")
    parser.add_argument("--no-wrap", action="store_true")
    parser.add_argument("--line-block", action="store_true")
    parser.add_argument("--grid", type=int, choices=[8, 9, 10, 15], required=True)
    parser.add_argument("--reps", type=int, default=3)
    args = parser.parse_args()

    if args.file and args.content:
        sys.exit("Error: --file y content son mutuamente excluyentes")
    if not args.file and not args.content:
        sys.exit("Error: content o --file requerido")
    if args.file and not (args.kanji or args.kana):
        sys.exit("Error: --file requiere --kanji o --kana")
    if args.kanji and args.kana:
        sys.exit("Error: --kanji y --kana son mutuamente excluyentes")
    if args.furigana and not args.kanji:
        sys.exit("Error: --furigana requiere --kanji")
    if (args.two_columns or args.no_wrap) and not args.sentences:
        sys.exit("Error: --two-columns y --no-wrap solo funcionan con --sentences")
    if args.two_columns and not args.no_wrap:
        sys.exit("Error: --two-columns requiere --no-wrap")
    if args.line_block and not args.sentences:
        sys.exit("Error: --line-block requiere --sentences")
    if args.line_block and (args.two_columns or args.no_wrap):
        sys.exit("Error: --line-block no es compatible con --two-columns ni --no-wrap")

    cols, rows, font_size = GRIDS[args.grid]
    wrap = args.sentences and not args.no_wrap and not args.line_block

    if args.file:
        sentences = parse_markdown(
            args.file, args.kanji, args.kana, args.furigana
        )
        pages = generate_line_blocks(sentences, cols, rows, args.reps)
    elif args.line_block:
        sentences = [(s, None) for s in split_sentences(args.content)]
        pages = generate_line_blocks(sentences, cols, rows, args.reps)
    elif args.sentences:
        pages = generate_sentences(
            args.content, cols, rows, args.reps, args.two_columns, wrap
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
