import pytest
from unittest.mock import patch
from app.utils import add_timestamp

def test_add_timestamp_to_video_calls_subprocess():
    src = "input.mp4"
    dst = "output.mp4"
    epoch = 1748412385
    with patch("subprocess.run") as mock_run:
        add_timestamp.add_timestamp_to_video(src, dst, epoch)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        # 檢查 ffmpeg 路徑、src、dst 是否在參數中
        assert src in args
        assert dst in args
        # 檢查 drawtext filter 是否正確
        vf_arg = args[args.index("-vf") + 1]
        assert f"localtime\\:{epoch}" in vf_arg
        assert "x=10:y=main_h-text_h-10" in vf_arg
        assert "fontfile" in vf_arg
