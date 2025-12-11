import time
import os
import base64
import replicate
import requests

from app import settings
from app.job_store import job_store
from app.configs.logger import log_execution, handle_errors
from app.constant import Constants


os.makedirs(settings.RESULT_DIR, exist_ok=True)


def upload_to_imgbb(image_path: str) -> str:
    """Upload an image file to imgbb and return the public URL."""
    if not settings.IMGBB_API_KEY:
        return ""
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        resp = requests.post(
            "https://api.imgbb.com/1/upload",
            params={
                "expiration": settings.IMGBB_EXPIRATION,
                "key": settings.IMGBB_API_KEY,
            },
            data={"image": encoded},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", {}).get("url", "")
    except Exception:
        return ""


@log_execution
@handle_errors
def process_face_swap_job(reference_id: str):
    job = job_store[reference_id]
    job["status"] = Constants.JobStatus.PROCESSING.value
    job["message"] = Constants.JobMessage.JOB_PROCESSING.value
    job_store[reference_id] = job
    
    start = time.time()

    try:
        output = replicate.run(
            settings.FACE_SWAP_MODEL,
            input={
                "input_image": str(job["base_image_url"]),
                "swap_image": str(job["selfie_url"])
            }
        )

        final_path = f"{settings.RESULT_DIR}/{reference_id}.jpg"

        if output is None:
            raise Exception("Face Not Detected")
        
        if isinstance(output, str):
            response = requests.get(output, timeout=settings.DOWNLOAD_TIMEOUT)
            response.raise_for_status()
            with open(final_path, "wb") as file:
                file.write(response.content)
        elif hasattr(output, 'read'):
            with open(final_path, "wb") as file:
                file.write(output.read())
        else:
            raise Exception(f"Unexpected output type: {type(output)}")

        job["status"] = Constants.JobStatus.COMPLETED.value
        job["message"] = Constants.JobMessage.JOB_COMPLETED.value
        public_url = upload_to_imgbb(final_path)
        job["result_image_url"] = public_url or f"/static/results/{reference_id}.jpg"
        job["processing_ms"] = int((time.time() - start) * 1000)
        job_store[reference_id] = job

    except Exception as e:
        job["status"] = Constants.JobStatus.FAILED.value
        job["message"] = Constants.JobMessage.JOB_FAILED.value
        job["error"] = str(e)
        job_store[reference_id] = job
