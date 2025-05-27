# app/gui/tk_main.py
import os
import tkinter as tk
from tkinter import filedialog
from app.utils.video_utils import extract_epoch
from app.utils.add_timestamp import add_timestamp_to_video

def main():
    root = tk.Tk()
    root.withdraw()
    fp = filedialog.askopenfilename(
        title="選擇 MP4",
        filetypes=[("MP4 files", "*.mp4;*.MP4")]
    )
    if not fp:
        print("未選擇檔案")
        return
    fname = os.path.basename(fp)
    parsed = extract_epoch(fname)
    if not parsed:
        print(f"檔名格式不符，略過: {fname}")
        return
    ts_str, epoch = parsed
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_fp = os.path.join(out_dir, f"timestamp_{fname}")
    print(f"處理 {fname}，加上動態時間戳: {ts_str}")
    add_timestamp_to_video(fp, out_fp, epoch)
    print("✅ 轉檔完成 →", out_fp)

if __name__ == "__main__":
    main()
