# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in
this repository.

## Purpose

This is a Japanese language learning repository. Lesson content is written in Spanish.
The primary goal is learning Japanese -- any code here is incidental tooling.

## Working in this repo

Focus on Japanese language learning. When asked about Japanese, help with grammar,
vocabulary, kanji readings, and exercises. Respond in Spanish unless asked otherwise.

## Lessons

Markdown files (`00-gojuuon.md`, etc.) are the core content. To add a lesson, create a
new `.md` file and add its filename to the `lessons` array in `index.html`.

Special markdown syntax: `{text}` wraps Japanese text with an inline play button for
text-to-speech.

## Running

```
./server.sh    # opens browser and serves on localhost:9999
```
