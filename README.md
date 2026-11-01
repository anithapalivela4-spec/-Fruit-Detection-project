# 🍎 Fruit Disease Detection System

A full-stack **AI-powered agricultural diagnostic web application** built with Django, TensorFlow/Keras (MobileNetV2), and Semantic Web Ontology reasoning (OWL/RDF/SPARQL).

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🧠 **Deep Learning CNN** | MobileNetV2 trained on 12 classes (6 fruits x healthy/diseased) |
| 🌿 **Semantic Ontology** | OWL/RDF knowledge graph with SPARQL-based reasoning (FruitDiseaseOntology) |
| 🔐 **Authentication** | User registration, login, logout with password hashing |
| 📜 **Prediction History** | Per-user prediction history with search and filter |
| 📄 **PDF / TXT Reports** | Printable diagnosis reports with pathogen, severity, treatments |
| 🌐 **REST API** | DRF endpoints for fruits, diseases, predictions, ontology queries |
| 📊 **Dashboard** | User analytics with Chart.js disease frequency visualization |
| 🚫 **Smart Rejection** | Non-fruit images rejected via botanical chromatic validation |

---

## 🍓 Supported Fruits and Diseases

| Fruit | Healthy | Disease |
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
├── templates/                # 25 HTML templates
├── tests/                    # 6 test modules (17 tests)
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

| Page | URL | Auth |
|---|---|---|
| Home | / | No |
| About | /about/ | No |
| Gallery | /gallery/ | No |
| Register | /accounts/register/ | No |
| Login | /accounts/login/ | No |
| Detect Disease | /detection/detect/ | Yes |
| Result | /detection/result/<pk>/ | Yes |
| History | /detection/history/ | Yes |
| Dashboard | /dashboard/ | Yes |
| Print Report | /detection/report/print/<pk>/ | Yes |
| Download TXT | /detection/report/<pk>/ | Yes |

### REST API

| Method | URL | Description |
|---|---|---|
| GET | /api/fruits/ | List all fruits |
| GET | /api/diseases/ | List all diseases |
| POST | /api/predict/ | Upload image -> diagnosis JSON |
| GET | /api/history/ | Prediction history |
| GET | /api/ontology/ | OWL SPARQL query |

---

## Test Results

```
Ran 17 tests in 68.627s -- OK

[PASS] Healthy Banana  -> Banana  | No disease detected | 99.8%
[PASS] Healthy Apple   -> Apple   | No disease detected | 99.4%
[PASS] Healthy Tomato  -> Tomato  | No disease detected | 99.1%
[PASS] Healthy Grape   -> Grape   | No disease detected | 99.8%
[PASS] Healthy Mango   -> Mango   | No disease detected | 99.6%
[PASS] Diseased Banana -> Banana  | Banana Sigatoka     | 99.8%
[PASS] Diseased Apple  -> Apple   | Apple Scab          | 99.9%
[PASS] Diseased Tomato -> Tomato  | Tomato Early Blight | 99.8%
[PASS] Diseased Grape  -> Grape   | Grape Black Rot     | 99.3%
[PASS] Diseased Mango  -> Mango   | Mango Anthracnose   | 99.9%
```

---

## Model Information

| Property | Value |
|---|---|
| Architecture | MobileNetV2 (Transfer Learning) |
| Input Size | 224 x 224 x 3 |
| Output | 12-class softmax |
| Normalization | [-1, 1] MobileNetV2 standard |
| Confidence Threshold | 65% minimum |
| Model File | model/saved_models/fruit_disease_model.h5 |

---

*Fruit Disease Detection System - Built with Django + TensorFlow + Semantic Web Ontology*
