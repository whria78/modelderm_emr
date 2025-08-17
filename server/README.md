# Whisper & GPT-OSS Servers

This repository contains instructions to run Whisper and GPT-OSS models as services on specific ports.

## 1. Whisper

Run Whisper on port **12346**:

```bash
python voice.py
````

## 2. GPT-OSS 20B

Run GPT-OSS 20B on port **13000**:

```bash
llama-server -m ~/gpt-oss-20b.gguf \
  --n-gpu-layers 999 \
  -c 0 \
  -fa \
  --jinja \
  --reasoning-format none \
  --host 0.0.0.0 \
  --port 13000 \
  --temp 0.2 \
  --flash-attn
```

## 3. GPT-OSS 120B

Run GPT-OSS 120B on port **13001**:

```bash
llama-server -m ~/gpt-oss-120b-mxfp4-00001-of-00003.gguf \
  --n-cpu-moe 36 \
  --n-gpu-layers 999 \
  -c 0 \
  -fa \
  --jinja \
  --reasoning-format none \
  --host 0.0.0.0 \
  --port 13001 \
  --temp 0.2 \
  --flash-attn
```

## ⚠ Server URL Format

Make sure to use the following format for server URLs (replace IP with `127.0.0.1` if running locally):

```python
# WHISPER_SERVER_URL = "http://127.0.0.1:12346/api/upload"
# SPEECH_SERVER_URL = "http://127.0.0.1:13000/v1/chat/completions"  # 20B
# SPEECH_SERVER_URL = "http://127.0.0.1:13001/v1/chat/completions"  # 120B
```
