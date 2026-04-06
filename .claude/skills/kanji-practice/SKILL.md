---
name: kanji-practice
description: Generate a printable kanji practice grid with reference kanji, onyomi, kunyomi, examples, and repetition cells. Use when the user wants to practice writing individual kanji.
argument-hint: [name] [kanji with readings or --json path]
allowed-tools: Bash(python3 *)
---

Generate a kanji practice sheet by running the generate script.

# Usage

```
python3 .claude/skills/kanji-practice/generate.py --json <path.json> <name>
python3 .claude/skills/kanji-practice/generate.py <name> "<content>"
```

- `--json`: path to a JSON file with kanji data (see schema below)
- `name`: filename for the output (becomes `practice-<name>.html`)
- `content`: kanji with furigana notation, e.g. `名 (な) 前 (まえ) 学 (がく)`

## JSON schema

```json
[{"kanji": "火", "strokes": 4, "on": ["カ"], "kun": ["ひ"], "examples": ["火曜日"]}]
```

Fields: `kanji` (required), `strokes`, `on`, `kun`, `examples`. Missing readings/strokes
are filled from kanjidic2 data. See `kanji/n5.json` for reference.

When using text input, compound words (multi-char) are added as examples to their
component kanji (max 2 per kanji). Only single-char entries create practice blocks.
Kanji are sorted by stroke count.

# Layout

Each block is two columns side by side (90mm x 30mm total):

Left column (18mm wide):
- Onyomi (6mm, katakana, max 2 readings)
- Kunyomi (6mm, hiragana, max 2 readings)
- Reference kanji (18mm, with cross-hairs and stroke count)

Right column (72mm wide):
- Top row: meaning (24mm, empty for user) + examples (48mm)
- Practice grid: 6 cols x 2 rows of 12mm square cells (12 cells total)

~12 blocks per page (2 across, 6 down). Font: Klee (thin strokes).

# Steps

1. Run the generate script with `--json` or inline kanji content
2. Tell the user the generated file path so they can open and print it (Cmd+P)

# Completion

Report the generated file path.
