import pytest
from flask import Flask
from app.routes import register_routes


def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app


def test_compress_invalid_crf():
    app = create_app()
    with app.test_client() as client:
        resp = client.post('/compress', json={'src': 'file.mp4', 'crf': 'abc'})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data['status'] == 'fail'
        assert 'Invalid crf' in data['message']

