import random
import numpy as np
from PIL import Image, ImageEnhance

def augment_image(image: Image.Image, rotate: bool = True, flip: bool = True, contrast: bool = True) -> Image.Image:
    """
    Applies data augmentation techniques to plant/fruit specimen images:
    - Random angle rotation
    - Horizontal flipping
    - Brightness and Contrast adjustments
    """
    augmented = image.copy()
    
    if flip and random.random() > 0.5:
        augmented = augmented.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
    if rotate:
        angle = random.choice([0, 90, 180, 270, random.randint(-25, 25)])
        if angle != 0:
            augmented = augmented.rotate(angle, expand=False)
            
    if contrast and random.random() > 0.5:
        factor = random.uniform(0.8, 1.2)
        enhancer = ImageEnhance.Contrast(augmented)
        augmented = enhancer.enhance(factor)
        
    return augmented
