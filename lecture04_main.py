import os
import datetime
import subprocess
from pathlib import Path
import speech_recognition as sr
import csv

# =====================================
# フォルダとファイルの設定
# =====================================
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# タイムスタンプ付き録音ファイル名
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
AUDIO_FILE = OUTPUT_DIR / f"recording_{timestamp}.wav"
TRANSCRIPT_FILE = OUTPUT_DIR / f"transcription_{timestamp}.txt"
CSV_FILE = OUTPUT_DIR / "transcription_list.csv"

# =====================================
# Step 1: 録音
# =====================================
print("=== Step 1: 録音開始 ===")
try:
    subprocess.run(
        [
            "ffmpeg",
            "-f", "avfoundation",  # macOS の場合。Windows: dshow, Linux: alsa
            "-i", ":0",
            "-t", "10",
            "-ac", "1",
            "-ar", "16000",
            str(AUDIO_FILE)
        ],
        check=True
    )
    print(f"録音完了: {AUDIO_FILE}")

except subprocess.CalledProcessError as e:
    print(f"recording.py の実行中にエラーが発生しました。")
    print(e)
    exit(1)

# =====================================
# Step 2: 文字起こし
# =====================================
print("=== Step 2: 文字起こし開始 ===")
recognizer = sr.Recognizer()
try:
    with sr.AudioFile(str(AUDIO_FILE)) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ja-JP")
        print(f"文字起こし結果:\n{text}")

except Exception as e:
    print("文字起こし中にエラーが発生しました。終了します。")
    print(e)
    exit(1)

# transcription.txt に保存
with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
    f.write(text + "\n")
print(f"文字起こしをファイルに保存しました: {TRANSCRIPT_FILE}")

# =====================================
# Step 3: CSV に保存
# =====================================
def save_transcription_to_csv(text: str, csv_path: Path):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    file_exists = csv_path.exists()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["日付", "時刻", "文字起こし内容"])
        writer.writerow([date_str, time_str, text])

save_transcription_to_csv(text, CSV_FILE)
print(f"CSVに保存しました: {CSV_FILE}")
