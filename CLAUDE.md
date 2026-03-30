# CLAUDE.md

Este archivo guia a Claude Code (claude.ai/code) al trabajar con este repositorio.

## Proposito

Repositorio para aprender japones. El contenido de las lecciones esta escrito en
espanol. El objetivo principal es aprender japones -- el codigo aqui es solo
herramientas auxiliares.

## Trabajo en este repo

Enfocarse en el aprendizaje de japones. Cuando se pregunte sobre japones, ayudar con
gramatica, vocabulario, lecturas de kanji y ejercicios. Responder en espanol salvo que
se pida lo contrario.

Cada vez que uses kanji en una frase, acompañala de su equivalente en hiragana entre
paréntesis. Ej: 新しい (あたらしい)

## Lecciones

Los archivos markdown (`00-gojuuon.md`, etc.) son el contenido principal. Para agregar
una leccion, crear un nuevo archivo `.md` y agregar su nombre al array `lessons` en
`index.html`.

Sintaxis especial de markdown: `{texto}` envuelve texto japones con un boton inline de
text-to-speech.

## Ejecucion

```
./server.sh    # abre el navegador y sirve en localhost:9999
```
