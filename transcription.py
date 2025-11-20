import whisper
import sys
import os

# === Step 2: 文字起こし開始 ===
print("=== Step 2: 文字起こし開始 ===")

# 録音したファイルのパス（recording.py で作成されたものを想定）
audio_file_path = "output/recording.wav"

# ファイル存在確認
if not os.path.exists(audio_file_path):
    print(f"音声ファイルが見つかりません: {audio_file_path}")
    sys.exit(1)

try:
    # Whisperモデルをロード（初回のみ自動ダウンロード）
    # 小さいモデルなら "tiny" や "small" も指定可
    model = whisper.load_model("base")

    # 文字起こしの実行
    result = model.transcribe(audio_file_path, language="ja")

    # 結果を保存
    text = result["text"]
    os.makedirs("output", exist_ok=True)
    with open("output/transcription.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("文字起こし完了！結果を output/transcription.txt に保存しました。")

except Exception as e:
    print(f"文字起こし中にエラーが発生しました。終了します。\n詳細: {e}")
    sys.exit(1)
