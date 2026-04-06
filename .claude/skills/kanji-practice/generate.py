#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent / "template.html"
OUTPUT_DIR = Path(__file__).resolve().parents[3]
DATA_FILE = Path(__file__).parent / "kanji_data.json"

FURIGANA = re.compile(r"(\S+)\s\(([^)]+)\)")
DATA = json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else {}
BLOCKS_PER_PAGE = 12


def load_json(path):
    entries = json.loads(Path(path).read_text())
    result = []
    for e in entries:
        result.append({
            "kanji": e["kanji"],
            "on": e.get("on", []),
            "kun": e.get("kun", []),
            "examples": e.get("examples", []),
            "strokes": e.get("strokes", DATA.get(e["kanji"], {}).get("s", "?")),
        })
    return result


def expand_pairs(pairs):
    order = []
    info = {}
    for word, reading in pairs:
        if len(word) == 1:
            if word not in info:
                order.append(word)
                info[word] = []
            entry = (reading, None)
            if entry not in info[word]:
                info[word].append(entry)
        else:
            for ch in word:
                if ch in info:
                    examples = [w for _, w in info[ch] if w]
                    if word not in examples and len(examples) < 2:
                        info[ch].append((None, word))

    sorted_order = sorted(order, key=lambda ch: DATA.get(ch, {}).get("s", 99))

    result = []
    for ch in sorted_order:
        d = DATA.get(ch, {})
        examples = [ctx for _, ctx in info[ch] if ctx]
        result.append({
            "kanji": ch,
            "on": clean_readings(d.get("on", []))[:2],
            "kun": clean_readings(d.get("kun", []))[:2],
            "examples": examples,
            "strokes": d.get("s", "?"),
        })
    return result


def clean_readings(raw):
    result = []
    for r in raw:
        if r.startswith("-") or r.endswith("-"):
            continue
        result.append(r.replace(".", ""))
    return result


def render_block(entry):
    kanji = entry["kanji"]
    strokes = entry["strokes"]
    on = "<br>".join(entry["on"][:2])
    kun = "<br>".join(entry["kun"][:2])
    ex_html = "".join(f"<span>{e}</span>" for e in entry["examples"][:2])

    cells = '<div class="cell"></div>' * 12
    return (
        '<div class="block">'
        '<div class="left">'
        f'<div class="on">{on}</div>'
        f'<div class="kun">{kun}</div>'
        f'<div class="ref"><span>{kanji}</span><span class="strokes">{strokes}</span></div>'
        '</div>'
        '<div class="right">'
        '<div class="right-top">'
        '<div class="meaning"></div>'
        f'<div class="examples">{ex_html}</div>'
        '</div>'
        f'<div class="practice">{cells}</div>'
        '</div>'
        '</div>'
    )


def generate(entries):
    pages = []
    for start in range(0, len(entries), BLOCKS_PER_PAGE):
        page_entries = entries[start : start + BLOCKS_PER_PAGE]
        blocks = [render_block(e) for e in page_entries]
        pages.append('<div class="page">\n' + "\n".join(blocks) + "\n</div>")
    return pages


def name_with_counter(name):
    output = OUTPUT_DIR / f"practice-{name}.html"
    n = 1
    while output.exists():
        n += 1
        output = OUTPUT_DIR / f"practice-{name}-{n}.html"
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", type=str)
    group.add_argument("content", nargs="?")
    args = parser.parse_args()

    if args.json:
        entries = load_json(args.json)
    else:
        pairs = FURIGANA.findall(args.content)
        if not pairs:
            sys.exit("Error: no se encontraron pares kanji (lectura)")
        entries = expand_pairs(pairs)

    pages = generate(entries)
    template = TEMPLATE.read_text()
    html = template.replace("{{PAGES}}", "\n".join(pages))

    output = name_with_counter(args.name)
    output.write_text(html)
    print(f"Generated: {output} ({len(pages)} page(s), {len(entries)} kanji)")


if __name__ == "__main__":
    main()
