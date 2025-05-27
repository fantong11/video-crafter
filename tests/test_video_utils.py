import pytest
from unittest.mock import patch
from app.utils import video_utils

def test_extract_epoch_valid():
    result = video_utils.extract_epoch("DJI_20250527080625_0180_D.MP4")
    assert result is not None, "extract_epoch returned None for a valid filename"
    ts, epoch = result
    assert ts == "2025-05-27 08:06:25"
    assert isinstance(epoch, int)

def test_extract_epoch_invalid():
    assert video_utils.extract_epoch("DJI_XXX.mp4") is None

@patch("subprocess.run")
def test_cut_video_calls_subprocess(mock_run):
    video_utils.cut_video("in.mp4", "out.mp4", "00:00:01", "00:00:10")
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert "-ss" in args and "-to" in args
    assert "in.mp4" in args and "out.mp4" in args

@patch("subprocess.run")
def test_compress_video_crf(mock_run):
    video_utils.compress_video("in.mp4", "out.mp4", crf=25)
    args = mock_run.call_args[0][0]
    assert "-crf" in args and "25" in args
    assert "-vcodec" in args and "libx264" in args
    assert "-acodec" in args and "aac" in args
