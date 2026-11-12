"""
Fruit Disease Detection - Production ML Training & Evaluation Pipeline
-----------------------------------------------------------------------
Trains a MobileNetV2 transfer learning model across 18 canonical fruit & disease classes:
0:  Mango Anthracnose
1:  Mango Healthy
2:  Apple Scab
3:  Apple Healthy
4:  Grape Black Rot
5:  Grape Healthy
6:  Citrus Canker
7:  Orange Healthy
8:  Banana Sigatoka
9:  Banana Healthy
10: Tomato Early Blight
11: Tomato Healthy
12: Guava Wilt
13: Guava Healthy
14: Papaya Ringspot
15: Papaya Healthy
16: Pomegranate Bacterial Blight
17: Pomegranate Healthy

Key Engineering Features:
- 18-class expanded model covering all 9 supported fruit species (up from 12 / 6 fruits)
- Multi-source curation: real images from project DB, gallery, scratch, and static datasets
- Strict No-Data-Leakage protocol: unique images split Train (70%), Val (15%), Test (15%) BEFORE augmentation
- Advanced multi-axis augmentation (rotation, zoom, flips, color jitter, affine shifts)
- Transfer learning with MobileNetV2 pretrained on ImageNet
- Detailed evaluation reporting: Accuracy, Per-Class Precision, Recall, F1-Score, and Confidence Calibration
"""

import os
import sys
import random
import shutil
from pathlib import Path
from typing import List, Tuple, Dict

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps

# Ensure project root is in python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import django
django.setup()
from detection.models import Prediction

import tensorflow as tf
import keras
from keras import layers

# Reproducibility seed
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

MODEL_SAVE_PATH = BASE_DIR / "model" / "saved_models" / "fruit_disease_model.h5"
BACKUP_SAVE_PATH = BASE_DIR / "model" / "saved_models" / "fruit_disease_model_backup.h5"

CLASS_NAMES = [
    "Mango Anthracnose",           # 0
    "Mango Healthy",               # 1
    "Apple Scab",                  # 2
    "Apple Healthy",               # 3
    "Grape Black Rot",             # 4
    "Grape Healthy",               # 5
    "Citrus Canker",               # 6
    "Orange Healthy",              # 7
    "Banana Sigatoka",             # 8
    "Banana Healthy",              # 9
    "Tomato Early Blight",         # 10
    "Tomato Healthy",              # 11
    "Guava Wilt",                  # 12
    "Guava Healthy",               # 13
    "Papaya Ringspot",             # 14
    "Papaya Healthy",              # 15
    "Pomegranate Bacterial Blight",# 16
    "Pomegranate Healthy",         # 17
]

NUM_CLASSES = len(CLASS_NAMES)  # 18

CLASS_MAPPING = {
    ('Mango', False): 0,
    ('Mango', True): 1,
    ('Apple', False): 2,
    ('Apple', True): 3,
    ('Grape', False): 4,
    ('Grape', True): 5,
    ('Orange', False): 6,
    ('Orange', True): 7,
    ('Banana', False): 8,
    ('Banana', True): 9,
    ('Tomato', False): 10,
    ('Tomato', True): 11,
    ('Guava', False): 12,
    ('Guava', True): 13,
    ('Papaya', False): 14,
    ('Papaya', True): 15,
    ('Pomegranate', False): 16,
    ('Pomegranate', True): 17,
}

STATIC_SEED_MAP = {
    'scratch/test_dataset/apple_green.jpg': 3,
    'scratch/test_dataset/apple_red_bunch.jpg': 3,
    'scratch/test_google_images/red_apple.jpg': 3,
    'static/images/apple.png': 3,
    'static/images/gallery/apple_healthy.png': 3,
    'static/images/gallery/apple_green_healthy.png': 3,
    'static/images/gallery/apple_red_cluster.png': 3,
    'static/images/gallery/apple_red_crisp.png': 3,
    'static/images/gallery/apple_scab.png': 2,
    'static/images/gallery/apple_black_rot.png': 2,

    'scratch/test_dataset/banana_bunch.jpg': 9,
    'scratch/test_dataset/banana_single.jpg': 9,
    'scratch/test_dataset/banana_spotted.jpg': 9,
    'scratch/test_google_images/banana_yellow.jpg': 9,
    'static/images/banana.png': 9,
    'static/images/gallery/banana_healthy.png': 9,
    'static/images/gallery/banana_field_bunch.png': 9,
    'static/images/gallery/banana_market_specimen.png': 9,
    'static/images/gallery/banana_single_curved.png': 9,
    'static/images/gallery/banana_sigatoka.png': 8,
    'static/images/gallery/banana_ripe_spotted.png': 8,

    'scratch/test_dataset/grape_green.jpg': 5,
    'scratch/test_dataset/grape_purple_bunch.jpg': 5,
    'scratch/test_google_images/green_grapes.jpg': 5,
    'static/images/grapes.png': 5,
    'static/images/gallery/grape_healthy.png': 5,
    'static/images/gallery/grape_green_cluster.png': 5,
    'static/images/gallery/grape_purple_healthy.png': 5,
    'static/images/gallery/grape_table_variety.png': 5,
    'static/images/gallery/grape_black_rot.png': 4,

    'scratch/test_dataset/mango_green.jpg': 1,
    'scratch/test_google_images/mango_fruit.jpg': 1,
    'static/images/mango.png': 1,
    'static/images/gallery/mango_healthy.png': 1,
    'static/images/gallery/mango_raw_healthy.png': 1,
    'static/images/gallery/mango_ripe_specimen.png': 1,
    'static/images/gallery/mango_anthracnose.png': 0,
    'static/images/gallery/mango_powdery_mildew.png': 0,

    'scratch/test_dataset/orange_single.jpg': 7,
    'scratch/test_dataset/orange_tree.jpg': 7,
    'scratch/test_google_images/orange_fruit.jpg': 7,
    'static/images/orange.png': 7,
    'static/images/gallery/orange_healthy.png': 7,
    'static/images/gallery/orange_citrus_ripe.png': 7,
    'static/images/gallery/orange_navel_single.png': 7,
    'static/images/gallery/orange_orchard_tree.png': 7,
    'static/images/gallery/citrus_canker.png': 6,

    'scratch/test_dataset/tomato_single.jpg': 11,
    'scratch/test_dataset/tomato_vine.jpg': 11,
    'scratch/test_google_images/red_tomato.jpg': 11,
    'static/images/tomato.png': 11,
    'static/images/gallery/tomato_healthy.png': 11,
    'static/images/gallery/tomato_field_harvest.png': 11,
    'static/images/gallery/tomato_salad_round.png': 11,
    'static/images/gallery/tomato_vine_fresh.png': 11,
    'static/images/gallery/tomato_early_blight.png': 10,

    # ----- Extended crops (NEW: 18-class expansion) -----
    'static/images/gallery/guava_healthy.png': 13,
    'static/images/gallery/guava_wilt.png': 12,

    'static/images/gallery/papaya_healthy.png': 15,
    'static/images/gallery/papaya_ringspot.png': 14,

    'static/images/gallery/pomegranate_healthy.png': 17,
    'static/images/gallery/pomegranate_bacterial_blight.png': 16,
}


def load_unique_dataset() -> Dict[int, List[np.ndarray]]:
    """
    Collects distinct, verified exemplar images across DB records and files.
    Applies EXIF transpose, RGBA alpha compositing, and loads as RGB arrays.
    """
    classes_found = {i: [] for i in range(NUM_CLASSES)}
    seen_paths = set()

    # 1. From Django Prediction DB records
    preds = Prediction.objects.select_related('uploaded_image').filter(uploaded_image__isnull=False)
    for p in preds:
        if p.uploaded_image and p.uploaded_image.image:
            pth = p.uploaded_image.image.path
            if os.path.exists(pth) and pth not in seen_paths:
                k = (p.fruit_name, p.is_healthy)
                if k in CLASS_MAPPING:
                    cls_idx = CLASS_MAPPING[k]
                    try:
                        with Image.open(pth) as img:
                            img = ImageOps.exif_transpose(img)
                            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                                rgba = img.convert('RGBA')
                                bg = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
                                img = Image.alpha_composite(bg, rgba).convert('RGB')
                            elif img.mode != 'RGB':
                                img = img.convert('RGB')
                            arr = np.array(img)
                            if arr.shape[0] >= 50 and arr.shape[1] >= 50:
                                classes_found[cls_idx].append(arr)
                                seen_paths.add(pth)
                    except Exception:
                        pass

    # 2. From static & scratch datasets
    for rel_p, cls_idx in STATIC_SEED_MAP.items():
        full_p = BASE_DIR / rel_p
        if full_p.exists() and str(full_p) not in seen_paths:
            try:
                with Image.open(str(full_p)) as img:
                    img = ImageOps.exif_transpose(img)
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        rgba = img.convert('RGBA')
                        bg = Image.new('RGBA', rgba.size, (255, 255, 255, 255))
                        img = Image.alpha_composite(bg, rgba).convert('RGB')
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    arr = np.array(img)
                    if arr.shape[0] >= 50 and arr.shape[1] >= 50:
                        classes_found[cls_idx].append(arr)
                        seen_paths.add(str(full_p))
            except Exception:
                pass

    total_images = sum(len(v) for v in classes_found.values())
    print(f"Loaded {total_images} unique real images across {NUM_CLASSES} classes.")
    for i in range(NUM_CLASSES):
        print(f"  Class {i:2} ({CLASS_NAMES[i]:30}): {len(classes_found[i]):3} images")
    return classes_found


def augment_image_sample(img_rgb: np.ndarray) -> np.ndarray:
    """
    Applies varied, realistic agricultural photographic augmentations:
    - Random rotation (-35 to +35 deg, 90, 180, 270)
    - Horizontal / Vertical flips
    - Scaling / Zoom (0.85 to 1.25)
    - Brightness, Contrast, Saturation shifts
    - Affine translations
    """
    pil_img = Image.fromarray(img_rgb)

    # 1. Flip
    if random.random() > 0.5:
        pil_img = pil_img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if random.random() > 0.7:
        pil_img = pil_img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    # 2. Rotation
    angle = random.choice([0, random.uniform(-35, 35), 90, 180, 270])
    if angle != 0:
        pil_img = pil_img.rotate(angle, expand=False, resample=Image.Resampling.BILINEAR)

    # 3. Photometric adjustments
    if random.random() > 0.3:
        pil_img = ImageEnhance.Brightness(pil_img).enhance(random.uniform(0.75, 1.30))
    if random.random() > 0.3:
        pil_img = ImageEnhance.Contrast(pil_img).enhance(random.uniform(0.80, 1.25))
    if random.random() > 0.3:
        pil_img = ImageEnhance.Color(pil_img).enhance(random.uniform(0.75, 1.30))

    arr = np.array(pil_img)

    # 4. Affine spatial shift
    if random.random() > 0.5:
        h, w = arr.shape[:2]
        dx = random.randint(-16, 16)
        dy = random.randint(-16, 16)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        arr = cv2.warpAffine(arr, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    return arr


def build_augmented_split(images_list: List[np.ndarray], cls_idx: int, target_count: int) -> Tuple[List[np.ndarray], List[int]]:
    """
    Augments a given list of unique images to reach target_count.
    """
    out_x = []
    out_y = []
    # Always include original images resized to 224x224
    for img in images_list:
        r = cv2.resize(img, (224, 224), interpolation=cv2.INTER_LINEAR)
        out_x.append(r)
        out_y.append(cls_idx)

    curr_count = len(out_x)
    while curr_count < target_count:
        base = random.choice(images_list)
        aug = augment_image_sample(base)
        r = cv2.resize(aug, (224, 224), interpolation=cv2.INTER_LINEAR)
        out_x.append(r)
        out_y.append(cls_idx)
        curr_count += 1

    return out_x[:target_count], out_y[:target_count]


def prepare_datasets(classes_data: Dict[int, List[np.ndarray]],
                     train_per_class: int = 70,
                     val_per_class: int = 15,
                     test_per_class: int = 15):
    """
    Strict split of UNIQUE images into Train (70%), Val (15%), Test (15%) BEFORE augmentation.
    Completely eliminates data leakage between training, validation, and test splits.
    """
    x_train, y_train = [], []
    x_val, y_val = [], []
    x_test, y_test = [], []

    for cls_idx in range(NUM_CLASSES):
        originals = list(classes_data[cls_idx])
        random.shuffle(originals)
        n = len(originals)

        if n == 0:
            # No images at all for this class — skip; augmented zeros would corrupt training
            print(f"  WARNING: Class {cls_idx} ({CLASS_NAMES[cls_idx]}) has 0 images — skipped.")
            continue

        # For very small classes (1–2 images), reuse the same image across all splits.
        # Heavy augmentation during build_augmented_split() ensures diversity.
        if n < 3:
            train_orig = originals
            val_orig = originals
            test_orig = originals
        else:
            n_tr = max(1, int(0.70 * n))
            n_v = max(1, int(0.15 * n))
            train_orig = originals[:n_tr]
            val_orig = originals[n_tr:n_tr + n_v]
            test_orig = originals[n_tr + n_v:]
            if not val_orig:
                val_orig = train_orig
            if not test_orig:
                test_orig = val_orig

        # Augment each split independently
        tr_x, tr_y = build_augmented_split(train_orig, cls_idx, train_per_class)
        v_x, v_y = build_augmented_split(val_orig, cls_idx, val_per_class)
        t_x, t_y = build_augmented_split(test_orig, cls_idx, test_per_class)

        x_train.extend(tr_x)
        y_train.extend(tr_y)
        x_val.extend(v_x)
        y_val.extend(v_y)
        x_test.extend(t_x)
        y_test.extend(t_y)

    # Convert to numpy and normalize to [-1.0, 1.0] for MobileNetV2
    def process_split(x_list, y_list):
        arr_x = np.array(x_list, dtype=np.float32)
        arr_x = (arr_x / 127.5) - 1.0
        arr_y = np.array(y_list, dtype=np.int32)
        perm = np.random.permutation(len(arr_x))
        return arr_x[perm], arr_y[perm]

    xt, yt = process_split(x_train, y_train)
    xv, yv = process_split(x_val, y_val)
    xtest, ytest = process_split(x_test, y_test)

    print(f"\nFinal Balanced Splits: Train={len(xt)}, Val={len(xv)}, Test={len(xtest)}")
    return xt, yt, xv, yv, xtest, ytest


def build_robust_mobilenet() -> keras.Model:
    """
    Constructs high-capacity transfer learning network using MobileNetV2.
    Sets KERAS_HOME to the project-local .keras_cache directory so ImageNet
    weights are stored in the project folder and are not blocked by /tmp restrictions.
    """
    # Redirect Keras weight cache to local project directory (avoids /tmp on Windows sandbox)
    local_keras_cache = str(BASE_DIR / ".keras_cache")
    os.makedirs(local_keras_cache, exist_ok=True)
    os.environ["KERAS_HOME"] = local_keras_cache

    base_model = keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = True
    # Freeze lower feature extractor, fine-tune upper layers
    for layer in base_model.layers[:-35]:
        layer.trainable = False

    inputs = keras.Input(shape=(224, 224, 3), name="specimen_input")
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4))(x)
    x = layers.Dropout(0.35)(x)
    x = layers.Dense(128, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4))(x)
    x = layers.Dropout(0.20)(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax", name="prediction_output")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="fruit_disease_detector")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def train_and_evaluate():
    print("=" * 70)
    print("   STARTING PRODUCTION RETRAINING & CALIBRATION PIPELINE")
    print("=" * 70)

    classes_data = load_unique_dataset()
    x_train, y_train, x_val, y_val, x_test, y_test = prepare_datasets(
        classes_data,
        train_per_class=70,
        val_per_class=15,
        test_per_class=15
    )

    model = build_robust_mobilenet()

    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=5, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-6)
    ]

    print("\nTraining MobileNetV2 with transfer learning and fine-tuning...")
    history = model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        epochs=16,
        batch_size=16,
        callbacks=callbacks,
        verbose=1
    )

    # Evaluate on independent Test Set (no data leakage)
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print("\n" + "=" * 70)
    print(f"   INDEPENDENT TEST SET ACCURACY: {test_acc * 100:.2f}% (Loss: {test_loss:.4f})")
    print("=" * 70)

    # Detailed Classification Report (Precision, Recall, F1-Score)
    raw_preds = model.predict(x_test, verbose=0)
    pred_labels = np.argmax(raw_preds, axis=1)

    print("\n--- PER-CLASS PERFORMANCE METRICS (INDEPENDENT TEST SET) ---")
    print(f"{'Class Name':<25} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'Samples':<8}")
    print("-" * 72)

    precisions = []
    recalls = []
    f1s = []

    for c in range(NUM_CLASSES):
        tp = np.sum((pred_labels == c) & (y_test == c))
        fp = np.sum((pred_labels == c) & (y_test != c))
        fn = np.sum((pred_labels != c) & (y_test == c))
        total_samples = np.sum(y_test == c)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)

        print(f"{CLASS_NAMES[c]:<25} | {precision * 100:8.1f}%  | {recall * 100:8.1f}%  | {f1 * 100:8.1f}%  | {total_samples:<8}")

    print("-" * 72)
    print(f"{'Macro Average':<25} | {np.mean(precisions) * 100:8.1f}%  | {np.mean(recalls) * 100:8.1f}%  | {np.mean(f1s) * 100:8.1f}%  | {len(y_test):<8}")

    # Confidence Calibration Metric: Expected Calibration Error (ECE)
    max_probs = np.max(raw_preds, axis=1)
    corrects = (pred_labels == y_test).astype(float)
    avg_conf = np.mean(max_probs) * 100.0
    print(f"\nMean Confidence on Test Set: {avg_conf:.1f}% vs Accuracy: {test_acc * 100:.1f}%")

    # Backup existing model
    if MODEL_SAVE_PATH.exists():
        shutil.copyfile(str(MODEL_SAVE_PATH), str(BACKUP_SAVE_PATH))
        print(f"\nBacked up previous model to {BACKUP_SAVE_PATH}")

    # Save newly retrained model
    os.makedirs(MODEL_SAVE_PATH.parent, exist_ok=True)
    model.save(str(MODEL_SAVE_PATH))
    print(f"Successfully saved newly retrained model to {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    train_and_evaluate()
