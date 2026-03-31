---
name: say
description: Say a Japanese word or phrase aloud using macOS TTS. Use when the user asks to hear, pronounce, or say a word.
disable-model-invocation: false
argument-hint: [word or phrase]
allowed-tools: Bash(say *)
---

Use macOS `say` with the Kyoko voice to speak a Japanese word or phrase aloud.

# Steps

1. If the argument is in Spanish, translate it to Japanese first

1. Show the translation in the format:

```
   **kanji**
   hiragana
```

1. Run `say -v Kyoko "<japanese text>"` using the Japanese text

1. If no argument is provided, ask the user what they want to hear

# Completion

The word or phrase was shown and spoken aloud via the system speaker.
