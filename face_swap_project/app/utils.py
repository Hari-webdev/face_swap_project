"""URL and Image validation utilities"""
import requests
from urllib.parse import urlparse
from typing import Tuple
from app.constant import Constants


def is_valid_image_url(url: str) -> Tuple[bool, str]:
    """Validate if URL points to an accessible image"""
    try:
        if not url or not str(url).strip():
            return False, Constants.ValidationError.EMPTY_URL.value
        
        parsed = urlparse(str(url))
        if not parsed.scheme or not parsed.netloc:
            return False, Constants.ValidationError.INVALID_URL_FORMAT.value
        
        if parsed.scheme not in Constants.SUPPORTED_PROTOCOLS:
            return False, Constants.ValidationError.INVALID_PROTOCOL.value
        
        response = requests.head(
            str(url), 
            timeout=Constants.REQUEST_TIMEOUT, 
            allow_redirects=True
        )
        
        if response.status_code != 200:
            if response.status_code == 404:
                return False, Constants.ValidationError.HTTP_404.value
            elif response.status_code == 403:
                return False, Constants.ValidationError.HTTP_403.value
            elif response.status_code >= 500:
                return False, Constants.ValidationError.HTTP_500.value.format(status_code=response.status_code)
            else:
                return False, Constants.ValidationError.HTTP_OTHER.value.format(status_code=response.status_code)
        
        content_type = response.headers.get('Content-Type', '').lower()
        if not any(t in content_type for t in Constants.IMAGE_CONTENT_TYPES):
            return False, Constants.ValidationError.UNSUPPORTED_IMAGE.value
        
        content_length = response.headers.get('Content-Length')
        if content_length:
            size_mb = int(content_length) / (1024 * 1024)
            max_size_mb = Constants.MAX_IMAGE_SIZE / (1024 * 1024)
            if size_mb > max_size_mb:
                return False, Constants.ValidationError.IMAGE_TOO_LARGE.value.format(size_mb=size_mb)
        
        return True, ""
        
    except requests.exceptions.Timeout:
        return False, Constants.ValidationError.TIMEOUT.value
    except requests.exceptions.ConnectionError:
        return False, Constants.ValidationError.CONNECTION_ERROR.value
    except Exception as e:
        return False, Constants.ValidationError.VALIDATION_ERROR.value.format(error=str(e))


def validate_face_swap_images(base_image_url: str, selfie_url: str) -> Tuple[bool, str]:
    """Validate both image URLs"""
    if not base_image_url:
        return False, Constants.ValidationError.BASE_IMAGE_URL_REQUIRED.value
    
    if not selfie_url:
        return False, Constants.ValidationError.SELFIE_URL_REQUIRED.value
    
    valid, error = is_valid_image_url(base_image_url)
    if not valid:
        return False, Constants.ValidationError.BASE_IMAGE_URL_INVALID.value.format(error=error)
    
    valid, error = is_valid_image_url(selfie_url)
    if not valid:
        return False, Constants.ValidationError.SELFIE_URL_INVALID.value.format(error=error)
    
    return True, ""
    
