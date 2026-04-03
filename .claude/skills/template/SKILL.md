---
name: template
description: Generate a printable HTML practice grid for Japanese writing. Use when the user wants to practice writing kana, kanji, or sentences by hand.
argument-hint: [name] [characters or sentences to practice]
allowed-tools: Bash(python3 *)
---

Generate a printable practice sheet by running the generate script.

# Usage

```
python3 .claude/skills/template/generate.py --grid <8|10|15> [--sentences] [--two-columns] <name> "<content>"
```

- `--grid`: cell size in mm (required)
- `--sentences`: flag for sentence mode (1 ref row + 3 practice rows per sentence)
- `--two-columns`: split sentences into two columns per page (requires `--sentences --no-wrap`)
- `--no-wrap`: one sentence per row (default is to auto-pack short sentences together)
- `name`: filename for the output (becomes `practice-<name>.html`)
- `content`: the Japanese text to practice

# Grid limits

Paper: US Letter with 10mm margins. Usable area: 196mm x 259mm.

| grid | columns | rows | use |
|------|---------|------|-----|
| 8mm  | 24      | 32   | kana |
| 10mm | 19      | 25   | kanji + kana mixed |
| 15mm | 13      | 17   | kanji, sentences |

Sentences: 4 rows per sentence (1 ref + 3 practice).

The script auto-paginates: content that exceeds one page generates multiple pages. Each
sentence must fit within the column count (the script errors if a sentence is too long).

# How to choose grid and flags

- Pure kana practice: `--grid 8`
- Kanji characters: `--grid 15`
- Mixed kanji + kana: `--grid 10`
- Sentences (any): add `--sentences`, use `--grid 15` or `--grid 10`
- Short sentences with fixed layout: add `--no-wrap --two-columns` for 2-column split
- Wrap is on by default: short sentences auto-pack together in a row

IMPORTANT: In `--sentences` mode, every sentence MUST end with punctuation (。？！).
The script splits sentences on these markers. Missing punctuation will cause sentences to
merge.

# Steps

1. Run the generate script with the appropriate arguments
2. Tell the user the generated file path so they can open and print it (Cmd+P)

# Completion

Report the generated file path.
