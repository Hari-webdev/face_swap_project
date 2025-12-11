from typing import Optional, Literal
from pydantic import BaseModel, HttpUrl


class FaceSwapJobRequest(BaseModel):
    base_image_url: HttpUrl
    selfie_url: HttpUrl


class FaceSwapJobResponse(BaseModel):
    reference_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    message: Optional[str] = None
    result_image_url: Optional[str] = None
    processing_ms: Optional[float] = None
    error: Optional[str] = None
