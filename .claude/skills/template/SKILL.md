---
name: template
description: Generate a printable HTML practice grid for Japanese writing. Use when the user wants to practice writing kana, kanji, or sentences by hand.
argument-hint: [name] [characters or sentences to practice]
allowed-tools: Bash(python3 *)
---

Generate a printable practice sheet by running the generate script.

# Usage

```
python3 .claude/skills/template/generate.py --grid <8|10|15> [--sentences] [--reps N] [--line-block] [--two-columns] <name> "<content>"
python3 .claude/skills/template/generate.py --grid <8|10|15> --file <path.md> --kanji [--furigana] [--reps N] <name>
python3 .claude/skills/template/generate.py --grid <8|10|15> --file <path.md> --kana [--reps N] <name>
```

- `--grid`: cell size in mm (required)
- `--file`: read sentences from a markdown file (```sentence and ```sentence-n fences)
- `--kanji`: extract kanji version (strip furigana readings). Mutually exclusive with `--kana`
- `--kana`: extract kana version (replace kanji with readings). Mutually exclusive with `--kanji`
- `--furigana`: with `--kanji`, also output the kana version after each sentence (interleaved)
- `--sentences`: flag for sentence mode (1 ref row + practice rows per sentence)
- `--reps N`: number of practice rows per sentence (default 3)
- `--line-block`: one sentence per block; if it exceeds the column width, ref text wraps to next rows (requires `--sentences`, incompatible with `--no-wrap`/`--two-columns`)
- `--two-columns`: split sentences into two columns per page (requires `--sentences --no-wrap`)
- `--no-wrap`: one sentence per row (default is to auto-pack short sentences together)
- `name`: filename for the output (becomes `practice-<name>.html`)
- `content`: the Japanese text to practice (not used with `--file`)

# Grid limits

Paper: US Letter with 10mm margins. Usable area: 196mm x 259mm.

| grid | columns | rows | use |
|------|---------|------|-----|
| 8mm  | 24      | 32   | kana |
| 9mm  | 21      | 28   | kana + kanji mixed |
| 10mm | 19      | 25   | kanji + kana mixed |
| 15mm | 13      | 17   | kanji, sentences |

Sentences: 1 ref + N practice rows (default 3). From the 2nd sentence onward, an extra
blank row is added above for annotations.

The script auto-paginates: content that exceeds one page generates multiple pages. In
default and `--no-wrap` modes, each sentence must fit within the column count. In
`--line-block` mode, sentences can exceed the column width and wrap to the next row(s).

# How to choose grid and flags

- Pure kana practice: `--grid 8`
- Kanji characters: `--grid 15`
- Mixed kanji + kana: `--grid 10`
- Sentences (any): add `--sentences`, use `--grid 15` or `--grid 10`
- Long sentences that may wrap: add `--line-block` (each sentence gets its own block, wraps if needed)
- Short sentences with fixed layout: add `--no-wrap --two-columns` for 2-column split
- Wrap is on by default: short sentences auto-pack together in a row

IMPORTANT: In `--sentences` mode (without `--file`), every sentence MUST end with
punctuation (。？！). The script splits on these markers. Missing punctuation will cause
sentences to merge. With `--file`, each ```sentence fence is one entry (no splitting).

## File input

`--file` reads ```sentence and ```sentence-n fences from a markdown file. Only the first
line of each fence is used. Furigana notation `漢字 (かな)` is parsed automatically.
`--file` implies `--sentences --line-block`. For ```sentence-n fences, a number label
appears to the left of the grid.

# Steps

1. Run the generate script with the appropriate arguments
2. Tell the user the generated file path so they can open and print it (Cmd+P)

# Completion

Report the generated file path.
