from flask import Flask, request, jsonify
import whisper
import os
import time

app = Flask(__name__)

# Whisper 모델 로드
whisper_model = whisper.load_model("turbo")  # "small", "medium", "large" 등 필요시 변경 가능

def format_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

@app.route('/api/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 요청에서 lang 읽기 (없으면 None → 자동 감지)
    lang = request.form.get("lang", None)
    print("Requested language: ",lang)

    os.makedirs('./temp', exist_ok=True)
    audio_path = f"./temp/{file.filename}"
    file.save(audio_path)

    # 처리 시간 측정
    start_time = time.time()
    result = whisper_model.transcribe(audio_path, language=lang, fp16=False, verbose=True)
    elapsed = time.time() - start_time
    print(f"[Whisper] file={file.filename}, lang={lang}, elapsed={elapsed:.2f} sec")

    segments = result.get('segments', [])
    lines = []
    for seg in segments:
        start_str = format_timestamp(seg['start'])
        end_str = format_timestamp(seg['end'])
        text = seg['text'].strip()
        lines.append(f"[{start_str} --> {end_str}]  {text}")

    output_text = "\n".join(lines)

    return jsonify({"transcript": output_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12346)
