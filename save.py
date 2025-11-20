"""
csv.py
文字起こし結果を履歴CSVに追記保存するモジュール
"""
import csv
from datetime import datetime
from pathlib import Path


def save_transcription_to_csv(text: str, csv_path: Path) -> None:
    """
    文字起こし結果をCSVファイルに追記保存する。
    
    Args:
        text (str): 文字起こし結果のテキスト
        csv_path (Path): CSVファイルのパス
    """
    # 現在の日時を取得
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # ファイルが存在しない場合はヘッダーを書き込む
    file_exists = csv_path.exists()
    
    # 追記モードでファイルを開く
    with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # ファイルが新規作成の場合はヘッダーを追加
        if not file_exists:
            writer.writerow(["日付", "時刻", "文字起こし内容"])
        
        # 追記行
        writer.writerow([date_str, time_str, text])


def read_transcription_txt(txt_path: Path) -> str:
    """
    transcription.txtファイルを読み取る。
    
    Args:
        txt_path (Path): txtファイルのパス
    
    Returns:
        str: ファイルの内容
    """
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


# 使用例
if __name__ == "__main__":
    # outputディレクトリのパス
    output_dir = Path("output")
    
    # 読み取るtxtファイルと保存先CSVファイルのパス
    txt_file = output_dir / "transcription.txt"
    csv_file = output_dir / "transcription_list.csv"
    
    # transcription.txtを読み取り
    if txt_file.exists():
        transcription_text = read_transcription_txt(txt_file)
        
        # デバッグ情報を表示
        print(f"ファイルパス: {txt_file}")
        print(f"読み取った文字数: {len(transcription_text)}")
        print(f"内容の先頭100文字: {transcription_text[:100]}")
        print("-" * 50)
        
        # CSVに保存
        save_transcription_to_csv(transcription_text, csv_file)
        print(f"✓ transcription.txtを読み取りました")
        print(f"✓ CSVファイルに保存しました: {csv_file}")
    else:
        print(f"✗ ファイルが見つかりません: {txt_file}")