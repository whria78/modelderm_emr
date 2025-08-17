## Requirements

- **Python 3.12** (install from Windows Store)
- Optional: **FFmpeg** (for audio trimming)

## Usage

```bash
python vv2.py
```

## Non-Korean Configuration

Please modify the following parts of the `config.json`:

```
"LANG": 'en',
"PROMPT": 
"Listen to the dermatology consultation recording and summarize it in 1-4 short lines for charting purposes. Use very brief, single-answer style. For example: '3MA mild itch on back', 'widespread rash of unknown duration', 'r/o shingles', 'medication from another hospital', 'return in 3 days'. :",
"PROMPT2": 
"Listen to the dermatology consultation recording and create a medical chart. Try to keep sentences brief and in single-answer style. For example: '3MA mild itch on back', 'widespread rash of unknown duration', 'r/o shingles', 'medication from another hospital', 'return in 3 days'. If the patient presents with multiple issues, separate them by issue and only record facts mentioned in the conversation. :"
```

```
"LANG": 'es',
"PROMPT": 
"Escucha la grabación de la consulta dermatológica y resume en 1-4 líneas cortas para fines de registro. Usa un estilo muy breve y de respuesta única. Por ejemplo: '3MA picazón leve en la espalda', 'erupción generalizada de duración desconocida', 'r/o herpes zóster', 'medicación de otro hospital', 'volver en 3 días'. :",
"PROMPT2": 
"Escucha la grabación de la consulta dermatológica y crea un registro médico. Intenta mantener las frases breves y de respuesta única. Por ejemplo: '3MA picazón leve en la espalda', 'erupción generalizada de duración desconocida', 'r/o herpes zóster', 'medicación de otro hospital', 'volver en 3 días'. Si el paciente presenta varios problemas, sepáralos por cada problema y solo registra los hechos mencionados en la conversación. :"
```

![Screenshot](screenshot.png)
