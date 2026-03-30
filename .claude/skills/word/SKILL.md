---
name: word
description: Provide a new Japanese word with its meaning and usage examples
disable-model-invocation: true
---

Pick a new Japanese word at random. Choose common, useful vocabulary appropriate for a
learner. Avoid repeating words that already have files in `words/`.

# Steps

1. Check `words/` for existing files to avoid duplicates.
1. Pick a new word.
1. Create the file `words/<word>.md` (the filename is the romaji of the word).
1. Use the appropriate template:
   - Verbs: follow `template-verb.md`
   - i-adjectives: follow `template-adj-i.md`
   - na-adjectives: follow `template-adj-na.md`
   - Everything else: follow `template-other.md`
   - Example sentences must be very simple: short, with basic grammar only.
     Use only the target word plus common particles and basic verb forms.
     Avoid compound grammar, subordinate clauses, or advanced patterns.

# Completion

The file `words/<word>.md` exists with valid frontmatter and both sections filled in.
