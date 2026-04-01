---
name: today
description: Guardar resumen de la conversacion de hoy en un archivo de sesion
disable-model-invocation: true
---

Guardar un resumen de la conversacion de hoy en `session/<fecha>.md` donde `<fecha>` es
la fecha de hoy en formato YYYY-MM-DD.

# Pasos

1. Revisar toda la conversacion de la sesion actual
2. Verificar que el directorio `session/` existe, crearlo si no
3. Escribir `session/<fecha>.md` resumiendo solo lo relativo al aprendizaje de japones:
   - Agrupar por tema (gramatica, vocabulario, etc.)
   - Incluir todos los terminos japoneses con kanji y lectura en hiragana
   - Incluir oraciones de ejemplo que se practicaron
   - Anotar correcciones o aclaraciones que se hicieron
   - NO incluir cambios al codigo ni al proyecto
4. Si el archivo ya existe, leer su contenido y agregar lo nuevo al final.
   No repetir temas que ya esten en el archivo, solo agregar lo que sea nuevo

# Completado

El archivo `session/<fecha>.md` existe con un resumen completo de la conversacion.
