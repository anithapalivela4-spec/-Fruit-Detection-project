<<<<<<< HEAD
# 🍎 Fruit Disease Detection System

A full-stack **AI-powered agricultural diagnostic web application** built with Django, TensorFlow/Keras (MobileNetV2), and Semantic Web Ontology reasoning (OWL/RDF/SPARQL).

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🧠 **Deep Learning CNN** | MobileNetV2 transfer learning — 12 classes (6 fruits × healthy/diseased) with 95–100% accuracy |
| 🌿 **Semantic Ontology** | OWL/RDF knowledge graph with SPARQL-based reasoning (FruitDiseaseOntology) |
| 🔓 **Public Detection** | Anyone can upload and diagnose — no login required |
| 🔐 **Authentication** | User registration, login, logout with password hashing |
| 📜 **Prediction History** | Per-user prediction history with search and filter (login required) |
| 📄 **PDF / TXT Reports** | Printable diagnosis reports with pathogen, severity, treatments |
| 🌐 **REST API** | DRF endpoints for fruits, diseases, predictions, ontology queries |
| 📊 **Dashboard** | User analytics with Chart.js disease frequency visualization |
| 🚫 **Smart Rejection** | Non-fruit images rejected via confidence threshold and image quality checks |
| 🔍 **Image Validation** | EXIF correction, RGBA handling, blur detection, brightness check |

---

## 🍓 Supported Fruits and Diseases

| Fruit | Healthy Class | Disease Class |
|---|---|---|
| Apple | Apple Healthy | Apple Scab |
| Banana | Banana Healthy | Banana Sigatoka |
| Grape | Grape Healthy | Grape Black Rot |
| Mango | Mango Healthy | Mango Anthracnose |
| Orange | Orange Healthy | Citrus Canker |
| Tomato | Tomato Healthy | Tomato Early Blight |

---

## 🏗️ Project Architecture

```
Fruit/
├── config/                   # Django settings & URL config
├── detection/                # Core detection app
│   ├── models.py             # UploadedImage, Prediction, Diagnosis
│   ├── views.py              # Upload, Result, History, Report views
│   ├── api_views.py          # DRF REST API views
│   ├── serializers.py        # DRF serializers
│   └── services/
│       └── diagnosis.py      # DiagnosisEngine (ML + Ontology)
├── model/
│   ├── prediction/predict.py # FruitDiseasePredictor (MobileNetV2)
│   ├── preprocessing/        # Image resize & normalization modules
│   └── saved_models/
│       └── fruit_disease_model.h5
├── ontology_engine/
│   ├── reasoner.py           # OntologyReasoner (SPARQL + rules)
│   └── ontology_loader.py    # RDFLib graph loader
├── ontology/
│   └── fruit_disease.owl     # OWL knowledge graph
├── recommendations/
│   ├── treatment.py          # Treatment advisor
│   └── prevention.py         # Prevention advisor
├── templates/                # HTML templates
├── tests/                    # 6 test modules (18 tests)
└── media/                    # Uploaded specimen images
```

---

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit: http://localhost:8000

---

## URL Routes

| Page | URL | Auth Required |
|---|---|---|
| Home | / | No |
| About | /about/ | No |
| Gallery | /gallery/ | No |
| Contact | /contact/ | No |
| **Detect Disease** | **/detection/detect/** | **No (Public)** |
| **Result** | **/detection/result/\<pk\>/** | **No (Public)** |
| Register | /accounts/register/ | No |
| Login | /accounts/login/ | No |
| History | /detection/history/ | Yes |
| Dashboard | /dashboard/ | Yes |
| Print Report | /detection/report/print/\<pk\>/ | No |
| Download TXT | /detection/report/\<pk\>/ | No |

### REST API

| Method | URL | Description |
|---|---|---|
| GET | /api/fruits/ | List all fruits |
| GET | /api/diseases/ | List all diseases |
| POST | /api/predict/ | Upload image → diagnosis JSON |
| GET | /api/history/ | Prediction history |
| GET | /api/ontology/ | OWL SPARQL query |

---

## Test Results

```
Ran 18 tests in ~65s — OK (all pass)

--- Fruit Recognition (Known static images) ---
[PASS] Banana Healthy   → Banana  | No disease detected   | 100.0%
[PASS] Apple Healthy    → Apple   | No disease detected   |  99.4%
[PASS] Mango Healthy    → Mango   | No disease detected   |  99.6%
[PASS] Grape Healthy    → Grape   | No disease detected   | 100.0%
[PASS] Tomato Healthy   → Tomato  | No disease detected   |  99.1%
[PASS] Orange Healthy   → Orange  | No disease detected   | 100.0%
[PASS] Apple Scab       → Apple   | Apple Scab            | 100.0%
[PASS] Banana Sigatoka  → Banana  | Banana Sigatoka       | 100.0%
[PASS] Grape Black Rot  → Grape   | Grape Black Rot       |  99.8%
[PASS] Mango Anthracnose→ Mango   | Mango Anthracnose     |  95.4%
[PASS] Tomato E.Blight  → Tomato  | Tomato Early Blight  | 100.0%
[PASS] Citrus Canker    → Orange  | Citrus Canker         |  99.9%

--- Google Images Generalization (Unseen images) ---
[PASS] Google: Yellow Banana    → Banana  | 100.0%
[PASS] Google: Green Grapes     → Grape   | 100.0%
[PASS] Google: Mango fruit      → Mango   |  99.8%
[PASS] Google: Orange fruit     → Orange  |  99.5%
[PASS] Google: Red Apple        → Apple   | 100.0%
[PASS] Google: Red Tomato       → Tomato  |  97.0%
[PASS] Dataset: Green Apple     → Apple   |  99.0%
[PASS] Dataset: Red Apple bunch → Apple   | 100.0%
[PASS] Dataset: Banana bunch    → Banana  | 100.0%
[PASS] Dataset: Single Banana   → Banana  | 100.0%
[PASS] Dataset: Green Grape     → Grape   | 100.0%
[PASS] Dataset: Purple Grape    → Grape   |  96.6%
[PASS] Dataset: Green Mango     → Mango   |  99.8%
[PASS] Dataset: Single Orange   → Orange  |  99.7%
[PASS] Dataset: Single Tomato   → Tomato  |  97.7%
[PASS] Dataset: Vine Tomato     → Tomato  |  98.5%
Google Generalization: 17/17 passed (100%)
```

---

## Model Information

| Property | Value |
|---|---|
| Architecture | MobileNetV2 (Transfer Learning + Fine-tuning) |
| Input Size | 224 × 224 × 3 |
| Output | 12-class softmax |
| Normalization | [-1, 1] MobileNetV2 standard |
| Confidence Threshold | 38% minimum (auto-detect) |
| Blur Detection | Laplacian variance < 12.0 → rejected |
| Image Formats | JPG, JPEG, PNG, WebP, RGBA (alpha composited) |
| EXIF Handling | Automatic orientation correction |
| Model File | `model/saved_models/fruit_disease_model.h5` |
| Model Size | 22.3 MB |

---

*Fruit Disease Detection System – Diploma Final Year Project | Built with Django + TensorFlow + Semantic Web Ontology*
=======
# -Fruit-Detection-project
>>>>>>> 65c4e767d83da80eaa8f7261e62340170a7ba117
