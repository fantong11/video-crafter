# Video Crafter API

A Dockerized Flask API for video processing (add timestamp, cut, compress) with auto-generated Swagger UI and download support.

## Features
- **Add Timestamp**: Add dynamic timestamp overlay to DJI video files (auto-detects from filename).
- **Cut Video**: Cut a segment from a video by start/end time.
- **Compress Video**: Compress video with configurable CRF.
- **Download Output**: All processed files can be downloaded via API.
- **Swagger UI**: Auto-generated API docs and testing at `/apidocs`.
- **Cross-platform**: Works on Windows and Linux (Docker recommended).

## Quick Start

### 1. Build and Run with Docker
```sh
docker build -t video-crafter .
docker run --rm -p 5000:5000 video-crafter
```

### 2. API Documentation & Testing
- Open [http://localhost:5000/apidocs](http://localhost:5000/apidocs) for Swagger UI.

### 3. Example API Usage
#### Add Timestamp
```sh
curl -F "file=@DJI_20250527080625_0180_D.MP4" http://localhost:5000/add_timestamp
```
- Response will include `download_url` for the processed file.

#### Download Output
```sh
curl -O "http://localhost:5000/download?path=/tmp/tmpxxxx/timestamp_DJI_20250527080625_0180_D.MP4"
```
- Use the `output` path from the API response as the `path` parameter.

#### Cut Video
```sh
curl -X POST -H "Content-Type: application/json" \
  -d '{"src": "/tmp/tmpxxxx/timestamp_DJI_20250527080625_0180_D.MP4", "start": "00:00:01", "end": "00:00:10"}' \
  http://localhost:5000/cut
```

#### Compress Video
```sh
curl -X POST -H "Content-Type: application/json" \
  -d '{"src": "/tmp/tmpxxxx/timestamp_DJI_20250527080625_0180_D.MP4", "crf": 28}' \
  http://localhost:5000/compress
```

## Development
- Python 3.10+
- Flask, flasgger, ffmpeg
- All dependencies in `requirements.txt`

## Folder Structure
- `app/` - Main application code
- `app/utils/` - Video processing utilities
- `app/services/` - Service layer
- `app/routes.py` - API endpoints
- `tests/` - Unit tests
- `output/` - (gitignored) Output files

## Notes
- For Windows, ffmpeg binary is expected in `bin/`.
- For Linux, ffmpeg is installed via apt in Docker.
- Temporary files are stored in system temp folder.
- Use the API's `download_url` to fetch processed files.

## License
MIT
