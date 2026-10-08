import os
from PIL import Image
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_uploaded_image(image_file):
    """
    Validates uploaded file:
    - Checks file extension (.jpg, .jpeg, .png, .webp)
    - Checks file size against MAX_UPLOAD_SIZE (10MB)
    - Validates image integrity using PIL
    """
    ext = os.path.splitext(image_file.name)[1].lower()
    allowed_exts = getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.webp'])
    if ext not in allowed_exts:
        raise ValidationError(f"Unsupported format '{ext}'. Allowed formats: {', '.join(allowed_exts)}")

    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    if image_file.size > max_size:
        raise ValidationError(f"File size exceeds maximum limit of {max_size // (1024*1024)} MB.")

    try:
        # Verify image can be opened and parsed
        img = Image.open(image_file)
        img.verify()
        # Reset file pointer after verify()
        image_file.seek(0)
    except Exception as e:
        raise ValidationError(f"Invalid or corrupted image file: {e}")

    return True

def process_specimen_image(image_file):
    """
    Reads image dimensions and prepares it for processing.
    """
    img = Image.open(image_file)
    width, height = img.size
    image_file.seek(0)
    return {
        'width': width,
        'height': height,
        'format': img.format,
        'mode': img.mode
    }
