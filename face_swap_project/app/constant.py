import enum


class Constants:
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    IMAGE_CONTENT_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"]
    SUPPORTED_PROTOCOLS = ['http', 'https']
    REQUEST_TIMEOUT = 10

    class JobStatus(enum.Enum):
        PENDING = "pending"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"

    class JobError(enum.Enum):
        INVALID_IMAGE_URL = "invalid_image_url"
        IMAGE_TOO_LARGE = "image_too_large"

    
    class JobMessage(enum.Enum):
        JOB_CREATED = "Face-swap job accepted"
        JOB_COMPLETED = "Face-swap job completed "
        JOB_FAILED = "Face-swap job failed"
        JOB_PROCESSING = "Face-swap job processing"
        JOB_VALIDATED = "Face-swap job validated"

    class ValidationError(enum.Enum):
        
        HTTP_404 = "Image not found. Please provide a valid and accessible image URL (Error: 404)"
        HTTP_403 = "Image access forbidden. Please use a publicly accessible image URL (Error: 403)"
        HTTP_500 = "Image server error. The image host is currently unavailable (Error: {status_code})"
        HTTP_OTHER = "Cannot access image URL. Server returned error {status_code}. Please check the URL"
        
        
        EMPTY_URL = "Image URL is required and cannot be empty"
        INVALID_URL_FORMAT = "Invalid URL format. Please provide a complete URL including http:// or https://"
        INVALID_PROTOCOL = "Invalid URL protocol. Only http:// and https:// URLs are supported"
        
        
        UNSUPPORTED_IMAGE = "Unsupported image format. Please provide JPG, PNG, WEBP, or GIF images only"
        IMAGE_TOO_LARGE = "Image file is too large ({size_mb:.1f}MB). Maximum allowed size is 10MB"
        
        
        TIMEOUT = "Request timeout. Cannot reach the image URL. Please check your internet connection"
        CONNECTION_ERROR = "Connection failed. Cannot access the image URL. Please verify the URL is correct"
        
        
        BASE_IMAGE_URL_REQUIRED = "base_image_url field is required"
        SELFIE_URL_REQUIRED = "selfie_url field is required"
        BASE_IMAGE_URL_INVALID = "base_image_url error: {error}"
        SELFIE_URL_INVALID = "selfie_url error: {error}"
        
        
        VALIDATION_ERROR = "Validation error: {error}"
        CREDITS_EXHAUSTED = "Insufficient credits. Please add credits to your Replicate account"