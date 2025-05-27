# app/routes.py
from flask import request, jsonify, send_from_directory, send_file
from app.services.video_service import VideoService
import tempfile
import os

class ApiResponse:
    @staticmethod
    def success(data=None, message=None):
        return jsonify({
            'status': 'success',
            'data': data if data is not None else None,
            'message': message
        })

    @staticmethod
    def fail(message=None, data=None):
        return jsonify({
            'status': 'fail',
            'data': data if data is not None else None,
            'message': message
        })

def register_routes(app):
    @app.route('/add_timestamp', methods=['POST'])
    def api_add_timestamp():
        """
        Add dynamic timestamp to video
        ---
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: file
            type: file
            required: true
            description: MP4 video file
        responses:
          200:
            description: Success
            schema:
              type: object
              properties:
                status:
                  type: string
                data:
                  type: object
                message:
                  type: string
        """
        file = request.files.get('file')
        if not file or not file.filename:
            return ApiResponse.fail('Missing file'), 400
        filename = file.filename or 'input.mp4'
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, filename)
        file.save(input_path)
        # 確保 output 有副檔名
        if not filename.lower().endswith('.mp4'):
            filename = filename + '.mp4'
        output_path = os.path.join(temp_dir, f"timestamp_{filename}")
        try:
            VideoService.add_timestamp(input_path, output_path, filename)
        except ValueError as e:
            return ApiResponse.fail(str(e)), 400
        # 回傳下載連結
        return ApiResponse.success({'output': output_path, 'download_url': f"/download?path={output_path}"})

    @app.route('/download')
    def download_file():
        """
        Download a processed video file
        ---
        parameters:
          - in: query
            name: path
            type: string
            required: true
            description: File path to download
        responses:
          200:
            description: File download
        """
        path = request.args.get('path')
        if not path or not os.path.exists(path):
            return ApiResponse.fail('File not found'), 404
        return send_file(path, as_attachment=True)

    @app.route('/cut', methods=['POST'])
    def api_cut():
        """
        Cut video
        ---
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                src:
                  type: string
                start:
                  type: string
                end:
                  type: string
        responses:
          200:
            description: Success
            schema:
              type: object
              properties:
                status:
                  type: string
                data:
                  type: object
                message:
                  type: string
        """
        data = request.get_json()
        src = data.get('src')
        start = data.get('start')
        end = data.get('end')
        if not src or not start or not end:
            return ApiResponse.fail('Missing parameters'), 400
        start_safe = start.replace(':', '_')
        end_safe = end.replace(':', '_')
        out_path = src.replace('.mp4', f'_cut_{start_safe}_{end_safe}.mp4')
        VideoService.cut(src, out_path, start, end)
        return ApiResponse.success({'output': out_path, 'download_url': f"/download?path={out_path}"})

    @app.route('/compress', methods=['POST'])
    def api_compress():
        """
        Compress video
        ---
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                src:
                  type: string
                crf:
                  type: integer
        responses:
          200:
            description: Success
            schema:
              type: object
              properties:
                status:
                  type: string
                data:
                  type: object
                message:
                  type: string
        """
        data = request.get_json()
        src = data.get('src')
        crf = int(data.get('crf', 28))
        if not src:
            return ApiResponse.fail('Missing src'), 400
        out_path = src.replace('.mp4', '_compressed.mp4')
        VideoService.compress(src, out_path, crf)
        return ApiResponse.success({'output': out_path, 'download_url': f"/download?path={out_path}"})

    @app.route('/docs')
    def swagger_ui():
        """
        Static Swagger UI (legacy)
        ---
        responses:
          200:
            description: Swagger UI HTML
        """
        return send_from_directory('static', 'swagger.html')
