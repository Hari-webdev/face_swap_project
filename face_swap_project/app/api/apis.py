import uuid
import time
from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.job_store import job_store
from app.face_swap import process_face_swap_job
from app.utils import validate_face_swap_images
from app.constant import Constants
from app.api.api_pandantic import FaceSwapJobRequest, FaceSwapJobResponse
from app.configs.logger import logger

router = APIRouter()


@router.post(
    "/api/v1/face-swap/jobs",
    response_model=FaceSwapJobResponse,
    response_model_exclude_none=True,
)
async def create_face_swap_job(request: FaceSwapJobRequest, background_tasks: BackgroundTasks):
    valid, error = validate_face_swap_images(str(request.base_image_url), str(request.selfie_url))
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    reference_id = f"job_{uuid.uuid4().hex}"
    
    job_store[reference_id] = {
        "reference_id": reference_id,
        "base_image_url": request.base_image_url,
        "selfie_url": request.selfie_url,
        "status": Constants.JobStatus.PENDING.value,
        "result_image_url": None,
        "message": Constants.JobMessage.JOB_CREATED.value,
        "error": None,
        "processing_ms": None,
        "created_at": time.time()
    }
    
    background_tasks.add_task(process_face_swap_job, reference_id)
    logger.info(f"Job {reference_id} created")
    
    return FaceSwapJobResponse(
        reference_id=reference_id,
        status=Constants.JobStatus.PENDING.value,
        message=Constants.JobMessage.JOB_CREATED.value,
    )


@router.get(
    "/api/v1/face-swap/jobs/{reference_id}",
    response_model=FaceSwapJobResponse,
    response_model_exclude_none=True,
)
async def get_face_swap_job(reference_id: str):
    if reference_id not in job_store:
        raise HTTPException(status_code=404, detail="Invalid reference_id")
    
    job = job_store[reference_id]
    
    if job["status"] == Constants.JobStatus.COMPLETED.value:
        return FaceSwapJobResponse(
            reference_id=job["reference_id"],
            status=job["status"],
            result_image_url=job["result_image_url"],
            processing_ms=job["processing_ms"]
        )
    elif job["status"] == Constants.JobStatus.FAILED.value:
        return FaceSwapJobResponse(
            reference_id=job["reference_id"],
            status=job["status"],
            error=job["error"]
        )
    
    return FaceSwapJobResponse(
        reference_id=job["reference_id"],
        status=job["status"],
        message=job.get("message")
    )


@router.get("/")
async def root():
    return {
        "service": "Face Swap API",
        "version": "1.0.0",
        "endpoints": {
            "create_job": "POST /api/v1/face-swap/jobs",
            "get_job": "GET /api/v1/face-swap/jobs/{reference_id}",
        }
    }