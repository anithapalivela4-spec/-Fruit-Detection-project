import numpy as np
from PIL import Image, ImageOps

def resize_image(image_input, target_size=(224, 224)) -> Image.Image:
    """
    Resize input image (path, file object, or PIL Image) to target dimensions.
    Handles EXIF orientation and alpha/transparency safely.
    """
    if isinstance(image_input, (str, bytes)):
        img = Image.open(image_input)
    elif hasattr(image_input, 'read'):
        img = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        img = image_input
    elif isinstance(image_input, np.ndarray):
        img = Image.fromarray(image_input.astype('uint8'))
    else:
        raise ValueError("Unsupported image input type.")

    # Apply EXIF rotation for mobile / digital cameras
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # Handle transparency / alpha channels (composite onto white background)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        rgba = img.convert('RGBA')
        white_bg = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
        img = Image.alpha_composite(white_bg, rgba).convert('RGB')
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    return img.resize(target_size, Image.Resampling.BILINEAR)
