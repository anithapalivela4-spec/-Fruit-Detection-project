import os
from PIL import Image, ImageOps
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_uploaded_image(image_file):
    """
    Validates uploaded file:
    - Checks file extension (.jpg, .jpeg, .png, .webp, .jfif)
    - Checks file size against MAX_UPLOAD_SIZE (10MB)
    - Validates image integrity using PIL
    - Gives helpful error messages for unsupported or corrupted files
    """
    ext = os.path.splitext(image_file.name)[1].lower()
    allowed_exts = getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.webp', '.jfif'])
    if ext not in allowed_exts:
        raise ValidationError(
            f"Unsupported format '{ext}'. Please upload an image in JPG, JPEG, PNG, or WebP format."
        )

    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    if image_file.size > max_size:
        raise ValidationError(f"File size exceeds maximum limit of {max_size // (1024*1024)} MB.")

    try:
        # Verify image can be opened and decoded
        img = Image.open(image_file)
        img.verify()
        image_file.seek(0)
    except Exception as e:
        raise ValidationError(f"The uploaded file is corrupted or not a valid image: {e}")

    return True

def process_specimen_image(image_file):
    """
    Reads image dimensions and prepares metadata respecting EXIF orientation.
    """
    img = Image.open(image_file)
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    width, height = img.size
    if hasattr(image_file, 'seek'):
        image_file.seek(0)
    return {
        'width': width,
        'height': height,
        'format': img.format,
        'mode': img.mode
    }
