import ffmpeg

# 録音時間（秒）
duration = 10
# 出力ファイル名
output_file = 'output/recording.wav'

try:
    print(f"{duration}秒間、マイクからの録音を開始します...")
    # FFmpegコマンドを実行
    # -f <デバイス入力形式>: OSに応じたデバイス入力形式を指定
    #   - Windows: 'dshow' または 'gdigrab'
    #   - macOS: 'avfoundation'
    #   - Linux: 'alsa'
    # -i <入力デバイス名>: デバイス名を指定
    (
        ffmpeg
        .input(':0', format='avfoundation', t=duration) # macOSの例
        .output(output_file, acodec='pcm_s16le', ar='44100', ac=1)
        .run(overwrite_output=True)
    )
    print(f"録音が完了しました。{output_file}に保存されました。")

except ffmpeg.Error as e:
    print(f"エラーが発生しました: {e.stderr.decode()}")
except Exception as e:
    print(f"予期せぬエラー: {e}")