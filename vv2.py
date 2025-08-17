import subprocess
import sys

def restart_script():
    print("[알림] 필수 패키지 설치 후 스크립트를 재실행합니다...")
    python_exe = sys.executable
    script = sys.argv[0]
    args = sys.argv[1:]
    # 새 프로세스로 재실행
    subprocess.Popen([python_exe, script] + args)
    sys.exit(0)

def install_and_restart_if_needed(package, import_name=None):
    import_name = import_name or package
    try:
        __import__(import_name)
    except ImportError:
        print(f"[설치 중] {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        restart_script()


# 필수 패키지 리스트
packages = [
    ("numpy", None),
    ("sd", None),
    ("sounddevice", None),
    ("pyperclip", None),
    ("requests", None),
    ("webrtcvad", None),
    ("pywin32", None),
    ("pyautogui", None)
]

for pkg, name in packages:
    install_and_import(pkg, name)


import win32gui

def list_all_windows():
    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # 빈 문자열 제외
                result.append((hwnd, title))
    windows = []
    win32gui.EnumWindows(enum_handler, windows)
    return windows

# 실행 시 모든 윈도우 출력
for hwnd, title in list_all_windows():
    print(f"HWND: {hwnd}, Title: {title}")

    
import os
import json
import tkinter as tk
import pyperclip
import sounddevice as sd
import numpy as np
import wave
import requests
import threading
import time
import subprocess
from datetime import datetime
from collections import deque
from threading import Lock

import tempfile
import webrtcvad
import contextlib
import struct

import win32gui
import pyautogui
import re

# ---------------- 윈도우 제어 ----------------
def find_window(title_substring):
    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if title_substring in window_text:
                result.append(hwnd)
    windows = []
    win32gui.EnumWindows(enum_handler, windows)
    return windows

def activate_window(window_title_substring):
    windows = find_window(window_title_substring)
    if not windows:
        print(f'"{window_title_substring}" 창을 찾을 수 없습니다.')
        return None
    hwnd = windows[0]
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.2)
    return hwnd

def send_key_to_window(window_title_substring, key):
    hwnd = activate_window(window_title_substring)
    if hwnd is None:
        return False
    time.sleep(0.1)
    pyautogui.press(key.lower())
    return True

def send_text_to_window(window_title_substring, text):
    hwnd = activate_window(window_title_substring)
    if hwnd is None:
        return False
    pyperclip.copy(text)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    return True


# ---------------- config 읽기 ----------------
CONFIG_PATH = "config.json"

default_config = {
    "SAMPLE_RATE": 16000,
    "CHANNELS": 1,
    "BLOCK_SEC": 0.1,
    "CHUNK_SEC": 30,
    "CHUNK_RESET_SEC": 10,
    "LOUD_RMS_THRESHOLD": 0.005,
    "LOUD_REQUIRED_SEC": 5.0,
    "RMS_SMOOTHING": 0.9,
    "FFMPEG_PATH": "c:\\ffmpeg\\bin\\ffmpeg.exe",
    "WHISPER_SERVER_URL": "https://t1.modelderm.com/whisper",
    "SPEECH_SERVER_URL": "https://t1.modelderm.com/20b",
    "SPEECH_SERVER2_URL": "https://t1.modelderm.com/120b",
    "LANG": 'ko',
    "PROMPT": "피부과 진료 녹음을 듣고 차팅용으로 1~4줄, 단답식, 매우 짧게 요약. 예를 들면 '3MA 허리의 약한 가려움증','기간을 모르는 전신의 발진', 'r/o 대상포진','타병원에서 약복용', '3일후 다시 내원 필요' 같은 식으로 요약해줘. :",
    "PROMPT2": "피부과 진료 녹음을 듣고 의료 차팅을 해줘. 되도록이면 짧게 단답식으로 문장을 구성해줘. 예를 들면 '3MA 허리의 약한 가려움증','기간을 모르는 전신의 발진', 'r/o 대상포진','타병원에서 약복용', '3일후 다시 내원 필요' 같은 식으로 차팅해줘. 여러가지 문제로 내원하였다면 각각의 문제별로 나눠서 기술하고 대화에 있는 사실만 기록해줘. :",
}

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = default_config
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(f"[오류] 설정 파일 읽기 실패: {e}")
    config = default_config

# 설정 변수
SAMPLE_RATE = config.get("SAMPLE_RATE", default_config["SAMPLE_RATE"])
CHANNELS = config.get("CHANNELS", default_config["CHANNELS"])
BLOCK_SEC = config.get("BLOCK_SEC", default_config["BLOCK_SEC"])
CHUNK_SEC = config.get("CHUNK_SEC", default_config["CHUNK_SEC"])
CHUNK_RESET_SEC = config.get("CHUNK_RESET_SEC", default_config["CHUNK_RESET_SEC"])
LOUD_RMS_THRESHOLD = config.get("LOUD_RMS_THRESHOLD", default_config["LOUD_RMS_THRESHOLD"])
LOUD_REQUIRED_SEC = config.get("LOUD_REQUIRED_SEC", default_config["LOUD_REQUIRED_SEC"])
RMS_SMOOTHING = config.get("RMS_SMOOTHING", default_config["RMS_SMOOTHING"])

FFMPEG_PATH = config.get("FFMPEG_PATH", default_config["FFMPEG_PATH"])
WHISPER_SERVER_URL = config.get("WHISPER_SERVER_URL", default_config["WHISPER_SERVER_URL"])
SPEECH_SERVER_URL = config.get("SPEECH_SERVER_URL", default_config["SPEECH_SERVER_URL"])
SPEECH_SERVER2_URL = config.get("SPEECH_SERVER2_URL", default_config["SPEECH_SERVER2_URL"])
PROMPT = config.get("PROMPT", default_config["PROMPT"])
PROMPT2 = config.get("PROMPT2", default_config["PROMPT2"])
LANG = config.get("LANG", default_config["LANG"])


# ---------------- 전역 상태 ----------------
frames = []
frames_lock = Lock()
recording = True
volume_rms = 0.0
MAX_SUM=6
summaries = deque(maxlen=MAX_SUM)
transcript_all =""
transcript_all_list=[]

chunk_start_time = time.time()
is_processing = False


# ---------------- 유틸 ----------------
def save_wav(filename, data_blocks, sample_rate):
    if not data_blocks:
        return
    data_np = np.concatenate(data_blocks, axis=0).astype(np.float32)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes((np.clip(data_np, -1.0, 1.0) * 32767).astype(np.int16).tobytes())

def convert_wav_to_mp3(wav_path):
    mp3_path = os.path.splitext(wav_path)[0] + ".mp3"
    try:
        subprocess.run(
            [FFMPEG_PATH, "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "320k", mp3_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
    except Exception as e:
        print("[FFmpeg 오류]", e)
    return mp3_path

def calc_loud_seconds(blocks, threshold_rms):
    total = 0.0
    for b in blocks:
        if b.size == 0:
            continue
        rms = float(np.sqrt(np.mean(np.square(b.astype(np.float32)))))
        if rms > threshold_rms:
            total += len(b) / SAMPLE_RATE
    return total

def format_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


# ---------------- 서버 통신 ----------------

def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        sample_rate = wf.getframerate()
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate, wf.getnchannels(), wf.getsampwidth()

def write_wave(path, pcm_data, sample_rate, n_channels=1, sampwidth=2):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)

def vad_trim(wav_path, aggressiveness=2):
    pcm_data, sample_rate, n_channels, sampwidth = read_wave(wav_path)
    if n_channels != 1 or sampwidth != 2:
        raise ValueError("webrtcvad requires mono PCM16 audio")

    vad = webrtcvad.Vad(aggressiveness)
    frame_duration = 30  # ms
    frame_size = int(sample_rate * frame_duration / 1000) * 2  # 2 bytes per sample

    # 프레임 단위로 분할
    frames = [pcm_data[i:i+frame_size] for i in range(0, len(pcm_data), frame_size)]
    voiced_frames = [f for f in frames if len(f) == frame_size and vad.is_speech(f, sample_rate)]

    if not voiced_frames:
        return wav_path  # 음성 없는 경우 원본 반환

    trimmed_pcm = b''.join(voiced_frames)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".wav")
    os.close(tmp_fd)
    write_wave(tmp_path, trimmed_pcm, sample_rate, n_channels, sampwidth)
    return tmp_path

def send_to_whisper_server(wav_path, lang=LANG):
    start_time = time.time()
    
    try:
        # 음성 구간만 trim
        trimmed_path = vad_trim(wav_path)

        with open(trimmed_path, 'rb') as f:
            files = {'file': (os.path.basename(trimmed_path), f, 'audio/wav')}
            data = {'lang': lang}  # POST 데이터로 language 전달
            response = requests.post(WHISPER_SERVER_URL, files=files, data=data, timeout=60)
            response.raise_for_status()
            data = response.json()
            transcript = data.get('transcript') or data.get('text') or ''
        
        elapsed = time.time() - start_time
        print(f"[Whisper server processing time] {elapsed:.2f}초")
        os.remove(trimmed_path)
        return transcript

    except Exception as e:
        print("Error sending to Whisper server:", e)
        return ""

def send_to_speech_server(text):
    global PROMPT
    return send_to_speech_server_ex(PROMPT,text,SPEECH_SERVER_URL)

def send_to_speech_server2(text):
    global PROMPT2
    return send_to_speech_server_ex(PROMPT2,text,SPEECH_SERVER2_URL)

def send_to_speech_server_ex(PROMPT,text,url):
    try:
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": PROMPT + text}
            ]
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, json=payload, headers=headers, timeout=300)
        r.raise_for_status()
        data = r.json()
        response_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        match = re.search(r"<\|channel\|>final<\|message\|>(.*)", response_text, re.S)
        if match:
            return match.group(1).strip()
        return response_text.strip()
    except Exception as e:
        print("[요약 오류]", e)
        return ""


# ---------------- 처리 파이프라인 ----------------
def process_chunk(data_blocks):
    global is_processing
    global transcript_all
    
    if not data_blocks:
        is_processing = False
        return

    loud_sec = calc_loud_seconds(data_blocks, LOUD_RMS_THRESHOLD)
    print(f"[분석] 큰 소리 누적 {loud_sec:.2f}s / 임계 {LOUD_REQUIRED_SEC:.2f}s")

    if loud_sec < LOUD_REQUIRED_SEC:
        is_processing = False
        return

    ts = datetime.now().strftime("record_%Y_%m_%d_%H_%M_%S")
    wav_path = f"{ts}.wav"
    save_wav(wav_path, data_blocks, SAMPLE_RATE)
    convert_wav_to_mp3(wav_path)

    transcript = send_to_whisper_server(wav_path)
    if transcript:
        transcript_all += '\n' + transcript
        summary = send_to_speech_server(transcript)
        if summary:
            summaries.appendleft(summary)
            try:
                root.after(0, update_summary_buttons)
            except:
                pass
    is_processing = False


# ---------------- 오디오 콜백 ----------------
def audio_callback(indata, frames_count, time_info, status):
    global volume_rms
    x = indata[:, 0] if indata.ndim > 1 else indata
    x = x.astype(np.float32)
    rms = float(np.sqrt(np.mean(np.square(x)))) if x.size else 0.0
    volume_rms = RMS_SMOOTHING * volume_rms + (1.0 - RMS_SMOOTHING) * rms
    with frames_lock:
        frames.append(x.copy().reshape(-1, 1))

def create_tooltip(widget, text):
    tooltip = None

    def on_enter(event):
        nonlocal tooltip
        x = event.x_root + 10
        y = event.y_root + 10
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)  # 창 장식 제거
        tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tooltip, text=text, justify="left",
            background="#ffffe0", relief="solid", borderwidth=1,
            font=("Arial", 9), wraplength=400
        )
        label.pack(ipadx=1)

    def on_leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def on_patient_process(text):
    """버튼 클릭 시 실행"""
    root.title("Please Wait ...")
    result_text = send_to_speech_server2(text)
    if result_text.strip():
        pyperclip.copy(result_text)
        root.title("📋 text copied")
        print(result_text)
        
def record_loop():
    global chunk_start_time, next_chunk_time, is_processing, transcript_all,transcript_all_list
    try:
        blocksize = int(SAMPLE_RATE * BLOCK_SEC)
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='float32',
            blocksize=blocksize,
            callback=audio_callback,
            latency='low'
        ):
            chunk_start_time = time.time()
            next_chunk_time = chunk_start_time + CHUNK_SEC
            threshold_crossed = False

            while recording:
                time.sleep(0.05)
                now = time.time()

                if volume_rms > LOUD_RMS_THRESHOLD:
                    threshold_crossed = True

                elapsed = now - chunk_start_time


                if elapsed >= CHUNK_RESET_SEC and not threshold_crossed:
                    with frames_lock:
                        frames.clear()
                    if transcript_all != "":
                        print(transcript_all)

                        # 🔽 새로운 버튼 생성
                        col_idx = 0
                        # 최근 transcript 가 왼쪽이 되도록 insert
                        patient_buttons.insert(0, transcript_all)

                        # 기존 버튼 clear 후 다시 grid
                        for w in patient_frame.winfo_children():
                            w.destroy()
                        for idx, t_text in enumerate(patient_buttons):
                            btn = tk.Button(
                                patient_frame,
                                text="📄",  # 문서 아이콘
                                width=2, height=1,
                                command=lambda tt=t_text: on_patient_process(tt)
                            )
                            btn.grid(row=0, column=idx, padx=2, pady=2)
                            create_tooltip(btn, t_text)  # 마우스 오버 시 transcript 내용 표시

                        transcript_all_list.append(transcript_all)
                        transcript_all = ""


                    chunk_start_time = now
                    next_chunk_time = now + CHUNK_SEC
                    threshold_crossed = False
                    continue


                if now >= next_chunk_time:
                    with frames_lock:
                        data_chunk = frames.copy()
                        frames.clear()
                    is_processing = True
                    threading.Thread(
                        target=process_chunk,
                        args=(data_chunk,),
                        daemon=True
                    ).start()
                    chunk_start_time = now
                    next_chunk_time = now + CHUNK_SEC
                    threshold_crossed = False
    except Exception as e:
        print("[녹음 오류]", e)


# ---------------- GUI ----------------
# ---------------- 창 위치 저장 ----------------
POSITION_FILE = "window_position.json"
def load_window_position():
    if os.path.exists(POSITION_FILE):
        try:
            with open(POSITION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("geometry")
        except Exception as e:
            print("Fail to load geometry:", e)
    return None

def save_window_position():
    try:
        geometry = root.geometry()
        with open(POSITION_FILE, "w", encoding="utf-8") as f:
            json.dump({"geometry": geometry}, f)
    except Exception as e:
        print("Fail to save geometry:", e)


root = tk.Tk()
root.title("recode & summarize")
root.attributes("-topmost", True)
root.resizable(False, False)
root.attributes('-toolwindow', True)  # 윈도우 상단 버튼에서 최소/최대 제거

last_geometry = load_window_position()
if last_geometry:
    root.geometry(last_geometry)
root.geometry("250x180")

summary_frame = tk.Frame(root)
summary_frame.pack(fill="both", expand=True, padx=10, pady=6)

# 🔽 patient_frame 은 grid 배치를 위해 별도 row=0 사용
patient_frame = tk.Frame(root)
patient_frame.pack(fill="x", side="bottom", padx=5, pady=5)
patient_buttons = []  # 버튼 관리용

def update_window_title():
    if is_processing:
        root.title("📤 processing…")
    else:
        elapsed = time.time() - chunk_start_time
        remaining = max(0, int(CHUNK_SEC - elapsed))
        root.title(f"🎙 {volume_rms:.3f} | {remaining} secs")
    root.after(500, update_window_title)

def on_copy(text):
    pyperclip.copy(text)
    root.title("📋 copied")
    send_key_to_window("진료실", "F2")
    send_key_to_window("진료실", "enter")
    send_text_to_window("진료실", text)
    send_key_to_window("진료실", "enter")

def trim_special(s: str) -> str:
    # 앞쪽 특수문자 제거
    s = re.sub(r'^\W+', '', s, flags=re.UNICODE)
    # 뒤쪽 특수문자 제거
    s = re.sub(r'\W+$', '', s, flags=re.UNICODE)
    return s

def update_summary_buttons():
    for w in summary_frame.winfo_children():
        w.destroy()
    if not summaries:
        tk.Label(summary_frame, text="No summary", font=("Arial", 10), fg="#666").pack()
        return
    total_line=0
    for idx, text in enumerate(list(summaries)):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            line = trim_special(line)
            if len(line) < 5:continue
            if total_line>=MAX_SUM:continue
            display = line if len(line) <= 120 else line[:120] + "..."
            total_line+=1
            btn = tk.Button(
                summary_frame,
                text=display.strip() or "",
                anchor="w",
                justify="left",
                wraplength=450,
                width=90,
                height=1,
                padx=0,
                pady=0,
                bd=1,
                relief='flat',
                command=lambda t=line: on_copy(t)
            )
            btn.pack(fill="x", padx=0,pady=0)

# 녹음 시작
threading.Thread(target=record_loop, daemon=True).start()
root.after(500, update_window_title)


def on_close():
    save_window_position()
    global recording
    recording = False
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
