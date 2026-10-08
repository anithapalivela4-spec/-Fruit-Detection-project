import numpy as np
from PIL import Image

def normalize_image(image_input, method="rescaling") -> np.ndarray:
    """
    Normalize image pixels for neural network input tensor.
    Supported methods:
      - 'rescaling': Rescales pixel values from [0, 255] to [0.0, 1.0]
      - 'standardization': Zero-center and unit-variance (Z-score)
      - 'imagenet': Subtract ImageNet mean and divide by std
    """
    if isinstance(image_input, Image.Image):
        arr = np.array(image_input, dtype=np.float32)
    elif isinstance(image_input, np.ndarray):
        arr = image_input.astype(np.float32)
    else:
        raise ValueError("Input must be a PIL Image or NumPy array.")

    if method == "rescaling":
        arr = arr / 255.0
    elif method == "standardization":
        mean = np.mean(arr)
        std = np.std(arr) + 1e-7
        arr = (arr - mean) / std
    elif method == "imagenet":
        # ImageNet mean & std for RGB
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32) * 255.0
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32) * 255.0
        arr = (arr - mean) / std
    else:
        arr = arr / 255.0

    # Ensure shape has batch dimension (1, H, W, C)
    if len(arr.shape) == 3:
        arr = np.expand_dims(arr, axis=0)

    return arr
