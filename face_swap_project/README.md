# Face Swap API

AI-powered face swap service using Replicate API.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and add your REPLICATE_API_TOKEN

# Run server
uvicorn app.main:app --reload
```

## API Endpoints

### Create Job
```bash
POST /api/v1/face-swap/jobs
Content-Type: application/json

{
  "base_image_url": "https://example.com/base.jpg",
  "selfie_url": "https://example.com/selfie.jpg"
}
```

### Get Job Status
```bash
GET /api/v1/face-swap/jobs/{reference_id}
```

## Docker

```bash
docker build -t face-swap-api .
docker run -p 8000:8000 --env-file .env face-swap-api
```
