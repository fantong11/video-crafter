# app/routes.py
from flask import request, jsonify
from app.services.video_service import VideoService
import tempfile
import os

def register_routes(app):
    @app.route('/add_timestamp', methods=['POST'])
    def api_add_timestamp():
        file = request.files.get('file')
        filename = request.form.get('filename')
        if not file or not filename:
            return jsonify({'error': 'Missing file or filename'}), 400
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, filename)
        file.save(input_path)
        output_path = os.path.join(temp_dir, f"timestamp_{filename}")
        try:
            VideoService.add_timestamp(input_path, output_path, filename)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify({'output': output_path})

    @app.route('/cut', methods=['POST'])
    def api_cut():
        data = request.get_json()
        src = data.get('src')
        start = data.get('start')
        end = data.get('end')
        if not src or not start or not end:
            return jsonify({'error': 'Missing parameters'}), 400
        start_safe = start.replace(':', '_')
        end_safe = end.replace(':', '_')
        out_path = src.replace('.mp4', '_cut_{}_{}.mp4'.format(start_safe, end_safe))
        VideoService.cut(src, out_path, start, end)
        return jsonify({'output': out_path})

    @app.route('/compress', methods=['POST'])
    def api_compress():
        data = request.get_json()
        src = data.get('src')
        crf = int(data.get('crf', 28))
        if not src:
            return jsonify({'error': 'Missing src'}), 400
        out_path = src.replace('.mp4', '_compressed.mp4')
        VideoService.compress(src, out_path, crf)
        return jsonify({'output': out_path})
