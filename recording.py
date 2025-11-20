import ffmpeg
import os
from pathlib import Path

# 録音時間（秒）
duration = 10
# 出力フォルダとファイルパス
output_dir = Path("output")
output_file = output_dir / "recording.wav"

try:
    # ✅ 出力ディレクトリを必ず作成
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"{duration}秒間、マイクからの録音を開始します...")

    (
        ffmpeg
        .input(':0', format='avfoundation', t=duration)  # macOS用設定
        .output(str(output_file), acodec='pcm_s16le', ar='44100', ac=1)
        .run(overwrite_output=True)
    )

    print(f"録音が完了しました。{output_file} に保存されました。")

except ffmpeg.Error as e:
    # stderrがNoneの場合も安全に処理
    err_msg = e.stderr.decode() if e.stderr else str(e)
    print(f"エラーが発生しました: {err_msg}")

except Exception as e:
    print(f"予期せぬエラー: {e}")
