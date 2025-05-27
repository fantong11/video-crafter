import pytest
from unittest.mock import patch
from app.services import video_service


def test_add_timestamp_success(monkeypatch):
    called = {}

    def fake_extract_epoch(filename):
        return ("2025-05-27 08:06:25", 1748412385)

    def fake_add_timestamp_to_video(src, dst, epoch):
        called['ok'] = (src, dst, epoch)

    monkeypatch.setattr(video_service, "extract_epoch", fake_extract_epoch)
    monkeypatch.setattr(video_service, "add_timestamp_to_video", fake_add_timestamp_to_video)
    out = video_service.VideoService.add_timestamp(
        "in.mp4", "out.mp4", "DJI_20250527080625_0180_D.MP4"
    )
    assert out == "out.mp4"
    assert called['ok'][0] == "in.mp4"
    assert called['ok'][1] == "out.mp4"
    assert called['ok'][2] == 1748412385


def test_add_timestamp_invalid(monkeypatch):
    def fake_extract_epoch(filename):
        return None

    monkeypatch.setattr(video_service, "extract_epoch", fake_extract_epoch)
    with pytest.raises(ValueError):
        video_service.VideoService.add_timestamp("in.mp4", "out.mp4", "bad.mp4")


@patch("app.services.video_service.cut_video")
def test_cut_calls_cut_video(mock_cut):
    out = video_service.VideoService.cut(
        "in.mp4", "out.mp4", "00:00:01", "00:00:10"
    )
    mock_cut.assert_called_once_with(
        "in.mp4", "out.mp4", "00:00:01", "00:00:10"
    )
    assert out == "out.mp4"


@patch("app.services.video_service.compress_video")
def test_compress_calls_compress_video(mock_compress):
    out = video_service.VideoService.compress("in.mp4", "out.mp4", 27)
    mock_compress.assert_called_once_with(
        "in.mp4", "out.mp4", 27
    )
    assert out == "out.mp4"
