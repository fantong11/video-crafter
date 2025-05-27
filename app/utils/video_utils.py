# app/utils/video_utils.py
import os
import re
import time

FONT_PATH = r"C\:/Windows/Fonts/arial.ttf"
FFMPEG_EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "bin", "ffmpeg.exe")

def extract_epoch(filename: str):
    m = re.search(r"DJI_(\d{14})_", filename)
    if not m:
        return None
    dt = m.group(1)
    ts_str = f"{dt[:4]}-{dt[4:6]}-{dt[6:8]} {dt[8:10]}:{dt[10:12]}:{dt[12:14]}"
    epoch = int(time.mktime(time.strptime(ts_str, "%Y-%m-%d %H:%M:%S")))
    return ts_str, epoch

def cut_video(src: str, dst: str, start: str, end: str):
    import subprocess
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-ss", start,
        "-to", end,
        "-i", src,
        "-c:v", "libx264",
        "-c:a", "aac",
        dst,
    ]
    subprocess.run(cmd, check=True)

def compress_video(src: str, dst: str, crf: int = 28):
    import subprocess
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", src,
        "-vcodec", "libx264",
        "-crf", str(crf),
        "-preset", "medium",
        "-acodec", "aac",
        dst,
    ]
    subprocess.run(cmd, check=True)
