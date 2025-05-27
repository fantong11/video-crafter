# app/services/video_service.py
from app.utils.video_utils import extract_epoch, cut_video, compress_video
from app.utils.add_timestamp import add_timestamp_to_video


class VideoService:
    @staticmethod
    def add_timestamp(input_path, output_path, filename):
        print(f"[DEBUG] filename: {filename}", flush=True)
        ts_epoch = extract_epoch(filename)
        if not ts_epoch:
            raise ValueError('Invalid filename format')
        _, epoch = ts_epoch
        add_timestamp_to_video(input_path, output_path, epoch)
        return output_path

    @staticmethod
    def cut(src, out_path, start, end):
        cut_video(src, out_path, start, end)
        return out_path

    @staticmethod
    def compress(src, out_path, crf=28):
        compress_video(src, out_path, crf)
        return out_path
