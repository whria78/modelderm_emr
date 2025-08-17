## Requirements && Usage

- **Python 3.12** (install from Windows Store)
- Optional: **FFmpeg** (for audio trimming)

```bash
python vv2.py
# Install requirements manually if an error occurs as followings:
# pip install numpy sounddevice pyperclip requests pydub pyautogui pywin32
```

## Non-Korean Configuration

Please modify the following parts of the `config.json` generated after running `vv2.py`:

```
"LANG": "en",
"PROMPT": 
"Listen to the dermatology consultation recording and summarize it in 1-4 short lines for charting purposes. Use very brief, single-answer style. For example: '3MA mild itch on back', 'widespread rash of unknown duration', 'r/o shingles', 'medication from another hospital', 'return in 3 days'. :",
"PROMPT2": 
"Listen to the dermatology consultation recording and create a medical chart. Try to keep sentences brief and in single-answer style. For example: '3MA mild itch on back', 'widespread rash of unknown duration', 'r/o shingles', 'medication from another hospital', 'return in 3 days'. If the patient presents with multiple issues, separate them by issue and only record facts mentioned in the conversation. :"
```

```
"LANG": "es",
"PROMPT": 
"Escucha la grabación de la consulta dermatológica y resume en 1-4 líneas cortas para fines de registro. Usa un estilo muy breve y de respuesta única. Por ejemplo: '3MA picazón leve en la espalda', 'erupción generalizada de duración desconocida', 'r/o herpes zóster', 'medicación de otro hospital', 'volver en 3 días'. :",
"PROMPT2": 
"Escucha la grabación de la consulta dermatológica y crea un registro médico. Intenta mantener las frases breves y de respuesta única. Por ejemplo: '3MA picazón leve en la espalda', 'erupción generalizada de duración desconocida', 'r/o herpes zóster', 'medicación de otro hospital', 'volver en 3 días'. Si el paciente presenta varios problemas, sepáralos por cada problema y solo registra los hechos mencionados en la conversación. :"
```

## ⚠ Server Availability

The servers are currently publicly accessible until 2025-9-30, and will be closed.  
To run the servers locally, please refer to the following resources:

- [script for the whisper - https://github.com/whria78/modelderm_emr/tree/main/server](https://github.com/whria78/modelderm_emr/tree/main/server)  
- [llama-server.exe & cudart-llama-bin-win-cuda-12.4-x64.zip - https://github.com/ggml-org/llama.cpp/releases](https://github.com/ggml-org/llama.cpp/releases)  
- [cuda12.4 - https://developer.nvidia.com/cuda-12-4-0-download-archive](https://developer.nvidia.com/cuda-12-4-0-download-archive)
- [gpt-oss 120b - https://huggingface.co/ggml-org/gpt-oss-120b-GGUF](https://huggingface.co/ggml-org/gpt-oss-120b-GGUF)
- [gpt-oss 20b - https://huggingface.co/ggml-org/gpt-oss-20b-GGUF](https://huggingface.co/ggml-org/gpt-oss-20b-GGUF)

## Screenshot
![Screenshot](screenshot.png)
