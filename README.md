# Fruit Disease Detection System

**AI and Ontology-Based Fruit Disease Detection and Care Recommendation System**  
*A Final-Year Diploma Capstone Project in Computer Engineering / Information Technology & Agronomy.*

---

## 1. Project Overview

The **Fruit Disease Detection System** is a full-stack, responsive web application engineered to aid farmers, agricultural extension officers, and agronomists in rapid diagnosis and management of fruit crop pathologies. 

Traditional plant pathology tools either rely purely on computer vision (treating diagnostic classification as an unexplained black-box output) or rely on static advisory manuals. This project bridges that gap by uniting **Deep Learning Computer Vision** with **Semantic Web Knowledge Engineering (Protégé OWL 2, RDFLib, SPARQL, and SWRL rules)**.

### Academic Distinction: ML vs. Ontology

- **Machine Learning (CNN)**: Analyzes visual patterns on leaves and fruits to answer:  
  `"What disease is likely present in this specimen image?"`
- **Semantic Ontology (OWL / SPARQL / SWRL)**: Reasoners traverse formal logic knowledge graphs to answer:  
  `"What pathogen causes it, what are the clinical symptoms, what is its severity under current microclimate conditions, and what safe organic/cultural care measures must be taken?"`

---

## 2. Key Features

- **Specimen Image Upload**: Drag-and-drop file upload with live client-side image preview and validation (JPG, JPEG, PNG, WEBP, up to 10MB).
- **Deep Learning Pipeline**: Automated lanczos resizing to `(224, 224, 3)`, tensor rescaling/normalization, and inference.
- **Protégé-Compatible OWL Ontology**: Fully parsed knowledge graph with `:Fruit`, `:Disease`, `:Symptom`, `:Pathogen`, `:Severity`, `:Treatment`, `:Prevention`, and `:EnvironmentalFactor` classes.
- **Rule-Based Reasoning**: SWRL rule engine for environmental severity escalation (e.g., high humidity triggering elevated disease alerts).
- **Categorized Treatment Advice**: Multi-tiered remediation covering Organic barriers, Biological antagonists (Trichoderma, Bacillus), Cultural canopy sanitation, and safe chemical guidance.
- **Role-Based User Management**: Three distinct user roles (Farmer/User, Agricultural Expert, Administrator) built on Django's secure authentication.
- **Prediction History & Diagnostics**: Isolated history per user, with comprehensive administrative inspection mode and filterable tables.
- **Interactive Dashboards**: Visual charts powered by Chart.js displaying pathology frequency breakdowns.
- **RESTful APIs**: JSON endpoints for fruit catalogs, diseases, live predictions, history, and SPARQL ontology queries.
- **Exportable Reports**: One-click generation of text/printable diagnostic summaries for field documentation.

---

## 3. Technology Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5.3, FontAwesome 6, JavaScript (ES6+), Chart.js
- **Backend**: Python 3, Django 5/6, Django REST Framework (DRF)
- **Database**: SQLite3 (default for easy viva evaluation, easily configurable to MySQL)
- **Machine Learning & Image Processing**: TensorFlow / Keras, NumPy, OpenCV, Pillow
- **Ontology & Semantic Web**: W3C OWL 2, RDF/Turtle, RDFLib 7.x, SPARQL, SWRL

---

## 4. Project Directory Structure

```text
Fruit/
│
├── manage.py                          # Django management runner
├── requirements.txt                   # Project dependency definitions
├── README.md                          # Comprehensive documentation
│
├── config/                            # Core Django settings and routing
│   ├── __init__.py
│   ├── settings.py                    # Project configuration (SQLite/MySQL)
│   ├── urls.py                        # Root URL dispatcher
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                          # Authentication and role management
│   ├── models.py                      # UserProfile (farmer, expert, admin)
│   ├── views.py                       # Login, Register, Profile, User List
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── fruits/                            # Horticultural host plant database
│   ├── models.py                      # Fruit and Variety models
│   ├── views.py                       # Fruit catalog and CRUD
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── diseases/                          # Phytopathology knowledge repository
│   ├── models.py                      # Disease, Symptom, Pathogen, Treatment, Prevention
│   ├── views.py                       # Disease catalog, filters, management
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── detection/                         # Core diagnostic orchestration
│   ├── models.py                      # UploadedImage, Prediction, Diagnosis
│   ├── views.py                       # Upload, Result, History, Dashboards
│   ├── api_views.py                   # REST API endpoints
│   ├── serializers.py                 # DRF serializers
│   ├── urls.py
│   ├── urls_dashboard.py
│   ├── urls_api.py
│   ├── forms.py                       # Specimen upload form
│   ├── context_processors.py          # Global template context status
│   └── services/
│       ├── image_processor.py         # Validation and dimension extraction
│       ├── predictor.py               # Interface to Keras prediction pipeline
│       └── diagnosis.py               # Fuses ML output with Ontology reasoning
│
├── ontology/                          # Semantic ontology knowledge base
│   ├── fruit_disease.owl              # Protégé 5.x OWL XML Ontology
│   ├── ontology_schema.ttl            # Turtle format schema
│   ├── classes/                       # Modular ontology class definitions
│   ├── instances/                     # Named individuals
│   └── rules/
│       └── disease_rules.swrl         # Semantic Web Rule Language definitions
│
├── ontology_engine/                   # Semantic reasoning layer
│   ├── __init__.py
│   ├── ontology_loader.py             # Singleton RDFLib graph loader
│   ├── sparql_queries.py              # Modular SPARQL query templates
│   └── reasoner.py                    # Symbolic reasoning engine
│
├── recommendations/                   # Advisory algorithms
│   ├── treatment.py                   # Categorized treatment engine
│   └── prevention.py                  # Agronomic prophylactic guidelines
│
├── reports/                           # Diagnostic summary generation
│   └── report_generator.py            # Formatted field text report builder
│
├── model/                             # Machine learning assets
│   ├── preprocessing/
│   │   ├── resize.py                  # Lanczos resizing to 224x224
│   │   ├── normalization.py           # Tensor normalization [0, 1]
│   │   └── augmentation.py            # Data augmentation utilities
│   ├── prediction/
│   │   └── predict.py                 # Keras model loader with mock fallback
│   └── saved_models/
│       └── fruit_disease_model.h5     # Trained Keras neural network weights
│
├── templates/                         # HTML5 Bootstrap templates
│   ├── base.html                      # Global master layout
│   ├── home.html                      # Project landing page
│   ├── about.html                     # Architecture & viva reference
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── dashboard.html                 # Farmer analytics dashboard
│   ├── admin_dashboard.html           # Administrator control center
│   ├── upload.html                    # Specimen upload and analysis
│   ├── result.html                    # Comprehensive diagnosis report
│   ├── history.html                   # Prediction history log
│   ├── fruits.html                    # Fruit species catalog
│   ├── fruit_detail.html
│   ├── fruit_form.html
│   ├── diseases.html                  # Pathology catalog
│   ├── disease_detail.html
│   ├── disease_form.html
│   ├── symptoms_list.html
│   ├── treatments_list.html
│   ├── preventions_list.html
│   ├── users_list.html
│   └── confirm_delete.html
│
├── static/
│   ├── css/style.css                  # Agricultural theme stylesheet
│   └── js/main.js                     # Drag-and-drop preview & UI logic
│
├── media/                             # Runtime image storage
│   └── uploads/                       # User-uploaded specimen photographs
│
└── tests/                             # Automated test suite
    ├── test_accounts.py               # User registration & auth tests
    ├── test_ontology.py               # RDFLib & SPARQL reasoning tests
    ├── test_prediction.py             # Preprocessing & prediction tests
    └── test_detection.py              # End-to-end detection flow tests
```

---

## 5. Installation & Setup Guide

### 1. Prerequisites
- Python 3.10 to 3.14 installed on your computer.
- Git (optional, if cloning).

### 2. Virtual Environment (Recommended)
Open your terminal inside the project directory:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt):
venv\Scripts\activate.bat

# Activate on Linux / macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 6. Database Setup & Seeding

### 1. Apply Migrations
```bash
python manage.py makemigrations accounts fruits diseases detection
python manage.py migrate
```

### 2. Populate Sample Academic Data
Run our custom seed command to populate fruit species, diseases, symptoms, treatments, preventions, default user accounts, and test specimens:

```bash
python manage.py seed_data
```

### 3. Default Demo Accounts
| Role | Username | Password | Purpose |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full system governance, Django Admin access |
| **Farmer / User** | `farmer_ramesh` | `farmer123` | Specimen scanning, history, personal dashboard |
| **Agri Expert** | `expert_dr_sharma` | `expert123` | Phytopathology & symptom knowledge curation |

---

## 7. Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```

---

## 8. Switching to MySQL (Optional)

If your external examiner requires MySQL:
1. Ensure MySQL server is running (e.g., via XAMPP or MySQL Workbench).
2. Create database:
   ```sql
   CREATE DATABASE fruit_disease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. In `config/settings.py`, uncomment the MySQL database block:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'fruit_disease_db',
           'USER': 'root',
           'PASSWORD': 'your_mysql_password',
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   ```
4. Run `python manage.py migrate` followed by `python manage.py seed_data`.

---

## 9. Machine Learning Model Placement

The prediction engine automatically inspects the following directory:
```text
model/saved_models/fruit_disease_model.h5
```

- **When a real `.h5` file exists**: The system automatically executes live Keras deep learning inference on uploaded specimen images.
- **When `.h5` file is absent**: The application automatically activates a clearly marked **Mock Prediction Service** (`SYSTEM_MOCK_MODE = True`). The application will never crash during viva evaluation.

---

## 10. Semantic Ontology Usage (Protégé & SPARQL)

The file `ontology/fruit_disease.owl` is fully compatible with Stanford University's **Protégé 5.x**. You can open it directly in Protégé to inspect class hierarchies, object properties, and SWRL rules.

In Python, RDFLib loads the graph into memory. You can test live SPARQL queries through the included API:
```text
http://127.0.0.1:8000/api/ontology/?disease=Mango+Anthracnose
```

---

## 11. REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/fruits/` | List all supported fruit crop species |
| `GET` | `/api/diseases/` | List all diseases with linked symptoms & remedies |
| `POST` | `/api/predict/` | Upload multipart image and get immediate JSON diagnosis |
| `GET` | `/api/history/` | Retrieve user prediction history |
| `GET` | `/api/ontology/` | Query ontology knowledge graph for a pathology |

---

## 12. Automated Testing

To run the automated test suite verifying user authentication, model pipelines, ontology loaders, and detection flows:

```bash
python manage.py test tests
```

---

## 13. External Viva Demonstration Checklist

1. **Log in** as `farmer_ramesh` (password: `farmer123`).
2. Go to **Detect Disease** and upload any fruit leaf photograph.
3. Observe real-time image validation and preview.
4. Click **Detect Disease & Run Ontology**.
5. Examine the **Diagnosis Report**:
   - Neural classification confidence metric.
   - Protégé OWL ontology reasoning justification.
   - Identified causative pathogen.
   - Clinical symptom correlation.
   - Categorized care advice (Organic, Biological, Cultural, Chemical).
   - Prophylactic prevention guidelines.
6. Click **Download Printable Summary** to demonstrate documentation output.
7. Switch to `admin` (password: `admin123`) to show the **Admin Console**, where fruits, diseases, symptoms, treatments, and users can be managed.
8. Show the **Architecture / About** page to explain the theoretical foundation of combining Machine Learning with Semantic Web Ontologies.
