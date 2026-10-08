import numpy as np
from PIL import Image

def resize_image(image_input, target_size=(224, 224)) -> Image.Image:
    """
    Resize input image (path, file object, or PIL Image) to target dimensions.
    Preserves aspect ratio or performs high-quality bicubic/lanczos resampling.
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

    # Convert to RGB mode if RGBA or grayscale
    if img.mode != 'RGB':
        img = img.convert('RGB')

    return img.resize(target_size, Image.Resampling.LANCZOS)
