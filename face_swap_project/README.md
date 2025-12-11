# Face Swap API

AI-powered face swap service using Replicate's face-swap model.

**Live API:** https://face-swap-project.onrender.com/docs

**Deployment:** Render.com (Free Tier)

---

## 🚀 Quick Start

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and add your REPLICATE_API_TOKEN

# Run server
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

---

## 📡 API Endpoints

### 1. Create Face-Swap Job

**POST** `/api/v1/face-swap/jobs`

```bash
curl -X POST "https://face-swap-project.onrender.com/api/v1/face-swap/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "base_image_url": "https://i.ibb.co/YTb9mQwp/Hrithik-Roshan.jpg",
    "selfie_url": "https://i.ibb.co/3mr1Y4RR/celebs-that-comes-to-your-mind-when-classically-handsome-v0-lkbiduh5iavc1.webp"
  }'
```

**Response:**
```json
{
  "reference_id": "job_abc123...",
  "status": "pending",
  "message": "Face-swap job accepted"
}
```

### 2. Get Job Status

**GET** `/api/v1/face-swap/jobs/{reference_id}`

```bash
curl "https://face-swap-project.onrender.com/api/v1/face-swap/jobs/job_abc123..."
```

**Response (Completed):**
```json
{
  "reference_id": "job_abc123...",
  "status": "completed",
  "result_image_url": "https://i.ibb.co/xxx/result.jpg",
  "processing_ms": 13270
}
```

**Response (Failed):**
```json
{
  "reference_id": "job_abc123...",
  "status": "failed",
  "error": "Face Not Detected"
}
```

---

## Cost Per API Call

### Cost Breakdown (Per Face-Swap Job)

**Instance Type:** Render.com Free Tier (0.5 CPU, 512MB RAM)
- Equivalent paid tier: Starter ($7/month = ~$0.0097/hour)

**Average Processing Time:** 13 seconds (measured)
- Replicate API processing: ~11 seconds
- Image upload (imgBB): ~1.5 seconds
- API overhead: ~0.5 seconds

### Cost Formula

```
cost_per_job = (instance_cost_per_hour / 3600) × processing_seconds
```

### Detailed Calculation

| Component | Calculation | Cost |
|-----------|-------------|------|
| **Replicate API** | Face-swap model (per prediction) | $0.014 |
| **Server Compute** | ($0.0097 / 3600) × 13 | $0.000035 |
| **Network** | Data transfer (negligible) | $0.000001 |
| **Storage (imgBB)** | Free tier (10 min expiry) | $0.00 |
| **Total** | Sum of all components | **$0.014036** |

**Rounded Total: ~$0.014 per face-swap job**

**Note:** 
- Current deployment uses Render **Free Tier** ($0 hosting cost)
- Replicate API cost dominates (99.7% of total)
- Free tier has cold starts (~30s after 15min idle)

---

## Sample Images for Testing

Use these public image URLs to test the API:

| Image | URL |
|-------|-----|
| Base Image | `https://i.ibb.co/YTb9mQwp/Hrithik-Roshan.jpg` |
| Selfie Image | `https://i.ibb.co/3mr1Y4RR/celebs-that-comes-to-your-mind-when-classically-handsome-v0-lkbiduh5iavc1.webp` |

**Quick Test:**
```bash
curl -X POST "https://face-swap-project.onrender.com/api/v1/face-swap/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "base_image_url": "https://i.ibb.co/YTb9mQwp/Hrithik-Roshan.jpg",
    "selfie_url": "https://i.ibb.co/3mr1Y4RR/celebs-that-comes-to-your-mind-when-classically-handsome-v0-lkbiduh5iavc1.webp"
  }'
```

---

## Docker Deployment

```bash
# Build image
docker build -t face-swap-api .

# Run container
docker run -p 8000:8000 --env-file .env face-swap-api
```

---

## Live Demo

- **Swagger UI:** https://face-swap-project.onrender.com/docs
- **API Base URL:** https://face-swap-project.onrender.com

---

## Environment Variables

```bash
REPLICATE_API_TOKEN=your_token_here
IMGBB_API_KEY=your_key_here (optional)
FACE_SWAP_MODEL=cdingram/face-swap:latest
```

---

## Tech Stack

- FastAPI
- Replicate API (face-swap model)
- imgBB (image hosting)
- Docker
- Deployed on Render.com
