# app/utils/add_timestamp.py
import subprocess
from app.utils.video_utils import FONT_PATH, FFMPEG_EXE


def add_timestamp_to_video(src: str, dst: str, epoch: int):
    vf = (
        f"drawtext="
        f"fontfile='{FONT_PATH}':"
        f"text='%{{pts\\:localtime\\:{epoch}}}':"
        "fontcolor=white:fontsize=36:"
        "x=10:y=main_h-text_h-10:box=1:boxcolor=black@0.5"
    )
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", src,
        "-vf", vf,
        "-codec:a", "copy",
        dst,
    ]
    subprocess.run(cmd, check=True)
