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

Cada vez que uses kanji, acompañalo de su lectura en hiragana entre parentesis. En
oraciones con multiples kanji, anotar cada palabra por separado.

Ej: {猫 (ねこ) は 動物 (どうぶつ) です。}

## Romaji

Usar romanizacion Hepburn para nombres de archivo y cualquier romaji en el contenido.
Ej: じ=ji, し=shi, ち=chi, つ=tsu, ふ=fu (no zi, si, ti, tu, hu).

## Lecciones, sesiones y palabras

Los archivos markdown dentro de `lessons`, `sessions` and `words` son el contenido
principal. Se descubren automaticamente del directorio raiz -- solo crear un nuevo
archivo `.md`.

### Sintaxis especial de markdown:

- `{texto}` envuelve texto japones con un boton inline de text-to-speech.

- `漢字 (かな)` se renderiza como ruby text con furigana encima del kanji.

  Ej: `言葉 (ことば)` muestra ことば sobre 言葉.

- Bloques `sentence` y `sentence-n` para oraciones junto a su traducción

  ```sentence-n
  ねこはどうぶつです
  el gato es un animal
  猫は動物です
  ```

  Estos bloques se muestra con la primera línea en primera jerarquía visual y las demás
  como accesorias. El sufijo `-n` sirve para que tengan numeración automática dentro de
  un documento.

### Ejecucion

```
./server.sh    # abre el navegador y sirve en localhost:9999
```
