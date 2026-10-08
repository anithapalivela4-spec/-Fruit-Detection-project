import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from fruits.models import Fruit, Variety
from diseases.models import Disease, Symptom, EnvironmentalFactor, Treatment, Prevention, Pathogen
from detection.models import UploadedImage, Prediction, Diagnosis
from django.core.files.base import ContentFile
import io
from PIL import Image, ImageDraw

class Command(BaseCommand):
    help = "Seeds database with comprehensive academic project data for Fruit Disease Detection System"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Fruit Disease Detection System database..."))

        # 1. Create Default Users
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@fruitdisease.org",
                "first_name": "System",
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            admin_user.profile.role = "admin"
            admin_user.profile.farm_location = "Central Research Station, New Delhi"
            admin_user.profile.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        farmer_user, created = User.objects.get_or_create(
            username="farmer_ramesh",
            defaults={
                "email": "ramesh@kisanmail.in",
                "first_name": "Ramesh",
                "last_name": "Patil"
            }
        )
        if created:
            farmer_user.set_password("farmer123")
            farmer_user.save()
            farmer_user.profile.role = "farmer"
            farmer_user.profile.farm_location = "Nashik Horticultural Belt, Maharashtra"
            farmer_user.profile.phone = "+91 9822012345"
            farmer_user.profile.save()
            self.stdout.write(self.style.SUCCESS("Created farmer user: farmer_ramesh / farmer123"))

        expert_user, created = User.objects.get_or_create(
            username="expert_dr_sharma",
            defaults={
                "email": "dr.sharma@agri-univ.edu",
                "first_name": "Dr. Sunita",
                "last_name": "Sharma",
                "is_staff": True
            }
        )
        if created:
            expert_user.set_password("expert123")
            expert_user.save()
            expert_user.profile.role = "expert"
            expert_user.profile.farm_location = "Regional Agronomy Centre, Pune"
            expert_user.profile.bio = "Senior Plant Pathologist specializing in subtropical fruit orchard fungal diseases."
            expert_user.profile.save()
            self.stdout.write(self.style.SUCCESS("Created expert user: expert_dr_sharma / expert123"))

        # 2. Seed Pathogens
        pathogens_data = [
            ("Colletotrichum gloeosporioides", "fungal", "Colletotrichum gloeosporioides", "Hemibiotrophic ascomycete fungus forming dark acervuli on fruit and foliar surfaces."),
            ("Venturia inaequalis", "fungal", "Venturia inaequalis", "Ascomycete fungus responsible for scab on Malus species."),
            ("Xanthomonas citri", "bacterial", "Xanthomonas citri subsp. citri", "Gram-negative rod-shaped bacterium with single polar flagellum."),
            ("Guignardia bidwellii", "fungal", "Guignardia bidwellii", "Fungal pathogen producing pycnidia and black mummification of grape berries."),
            ("Pseudocercospora fijiensis", "fungal", "Pseudocercospora fijiensis", "Destructive airborne fungal pathogen affecting Musa species foliage."),
            ("Alternaria solani", "fungal", "Alternaria solani", "Soil-borne fungal pathogen generating target-like concentric rings."),
            ("Oidium mangiferae", "fungal", "Oidium mangiferae", "Obligate biotrophic fungus coating inflorescences and tender leaves with white talc-like mycelium."),
            ("Fusarium oxysporum", "fungal", "Fusarium oxysporum f. sp. cubense", "Vascular wilt fungus penetrating root xylem vessels."),
            ("Healthy Host Specimen", "none", "Non-pathogenic", "Normal vegetative physiological status without active pathogen attack.")
        ]
        pathogen_dict = {}
        for name, p_type, sci, chars in pathogens_data:
            p, _ = Pathogen.objects.get_or_create(
                name=name,
                defaults={"pathogen_type": p_type, "scientific_name": sci, "characteristics": chars}
            )
            pathogen_dict[name] = p

        # 3. Seed Symptoms
        symptoms_data = [
            ("Leaf Spot", "Circular to irregular necrotic lesions with distinct border.", "Spots on leaves reducing photosynthetic area.", "Leaves"),
            ("Yellow Leaves", "Generalized chlorosis or interveinal yellowing of leaf blade.", "Yellowing caused by chlorophyll degradation or vascular stress.", "Leaves"),
            ("Brown Spot", "Small circular brown spots expanding into irregular blotches.", "Necrotic browning on foliage and immature fruits.", "Leaves and Fruit"),
            ("Black Spot", "Dark circular sunken necrotic spots with raised borders.", "Common indicator of anthracnose and bacterial infections.", "Fruit and Leaves"),
            ("Powdery Surface", "White to grayish powdery coating resembling talcum powder.", "Superficial epiphytic fungal mycelium and conidiophores.", "Leaves, Stems, Flowers"),
            ("Fruit Rot", "Soft watery rotting tissues with dark sporulating centers.", "Decay leading to fruit drop and economic crop loss.", "Fruit"),
            ("Leaf Curl", "Upward or downward rolling and distortion of foliage.", "Thickened leaves with crinkled or distorted margins.", "Leaves and Shoots"),
            ("Lesion", "Depressed necrotic sores or blisters on plant epidermis.", "Breakdown of epidermis allowing secondary opportunists.", "Fruit, Stem, Leaves"),
            ("Mold", "Velvety or fluffy fungal growth with gray or black spore masses.", "Surface colonization in high relative humidity.", "Fruit and Twigs"),
            ("Wilting", "Drooping and loss of plant turgor despite soil moisture.", "Vascular xylem vessel occlusion causing moisture starvation.", "Vascular System"),
            ("Stem Lesion", "Elongated dark cankers and sunken cracks along branches.", "Weakens structural branch integrity and girdles twigs.", "Branches and Twigs"),
            ("Discoloration", "Mottling, mosaic patterns, or yellow halos around necrotic foci.", "Color shift away from normal healthy green tissue.", "Whole Plant"),
            ("Normal Leaf Morphology", "Uniform glossy cuticle with vibrant chlorophyll coloration.", "Absence of chlorosis, necrosis, or distortions.", "Whole Specimen")
        ]
        symptom_dict = {}
        for name, vis, desc, part in symptoms_data:
            s, _ = Symptom.objects.get_or_create(
                name=name,
                defaults={"visual_characteristics": vis, "description": desc, "affected_part": part}
            )
            symptom_dict[name] = s

        # 4. Seed Environmental Factors
        env_data = [
            ("High Relative Humidity (>80%)", "24°C - 32°C", ">80%", "Promotes free moisture on plant surfaces, facilitating spore germination and germ tube penetration."),
            ("Warm Temperatures (25°C - 32°C)", "25°C - 32°C", "60% - 90%", "Accelerates fungal mycelial growth rates and bacterial multiplication cycles."),
            ("Cool & Wet Weather (16°C - 24°C)", "16°C - 24°C", "75% - 95%", "Ideal conditions for Apple Scab ascospores and Phytophthora zoospores."),
            ("Dense Canopy & Poor Aeration", "Variable", ">70%", "Traps microclimatic humidity inside tree canopy, delaying evaporation after rain or dew."),
            ("Intermittent Wind-Driven Rainfall", "20°C - 30°C", "High", "Splashes bacterial exudate and fungal conidia across orchard rows.")
        ]
        env_dict = {}
        for name, temp, hum, desc in env_data:
            ef, _ = EnvironmentalFactor.objects.get_or_create(
                name=name,
                defaults={"temperature_range": temp, "humidity_range": hum, "description": desc}
            )
            env_dict[name] = ef

        # 5. Seed Treatments
        treatments_data = [
            ("Canopy Sanitation & Pruning", "cultural", "Prune diseased twigs 5 cm below infection margins. Collect fallen leaves and diseased fruit; bury or incinerate them.", "Sterilize pruning tools between cuts using 70% isopropyl alcohol."),
            ("Copper Oxychloride Protectant Spray", "chemical", "Apply Copper Oxychloride 50% WP at 2.5 g per liter of clean water during early flush initiation.", "Observe 14-day pre-harvest interval. Wear protective gloves and respirators."),
            ("Cold-Pressed Neem Seed Oil (0.5%)", "organic", "Spray 5 ml cold-pressed neem oil mixed with 1 ml horticultural surfactant per liter of water.", "Spray during dawn or late dusk to prevent sunlight scorch on tender leaves."),
            ("Trichoderma viride Bio-Fungicide", "biological", "Foliar mist and soil collar drench with Trichoderma viride at 5 g/L to outcompete phytopathogens.", "Do not tank-mix biological agents simultaneously with copper fungicides."),
            ("Bordeaux Mixture (1%) Spray", "organic", "Apply freshly formulated Bordeaux mixture (1:1:100 copper sulfate + slaked lime) immediately post-pruning.", "Use only wooden, earthen, or plastic vessels for preparation; avoid metallic drums."),
            ("Streptocycline Agricultural Bactericide", "chemical", "Spray Streptocycline at 100 ppm combined with copper oxychloride for bacterial canker control.", "Strictly adhere to national agricultural extension dosage limits."),
            ("Bacillus subtilis Suspension", "biological", "Bio-fungicidal application of Bacillus subtilis (Serenade) at 3 ml/L for powdery mildew suppression.", "Store bio-formulations in a cool, shaded environment below 25°C."),
            ("Balanced Macro & Micronutrient Drench", "cultural", "Supplement soil with potassium sulfate and micronutrient zinc-boron spray to strengthen epidermal cell walls.", "Avoid excess urea / synthetic nitrogen which produces tender susceptible flushes.")
        ]
        treatment_dict = {}
        for title, cat, desc, prec in treatments_data:
            t, _ = Treatment.objects.get_or_create(
                title=title,
                defaults={"category": cat, "description": desc, "precautions": prec}
            )
            treatment_dict[title] = t

        # 6. Seed Preventions
        prevention_data = [
            ("Micro-Drip Irrigation Implementation", "Irrigation Management", "Switch to micro-drip or root-zone emitters to keep foliage dry.", "All Seasons"),
            ("Canopy Spacing & Sun Penetration", "Canopy Management", "Thin inner upright water sprouts and cross branches to permit 360-degree sunlight and wind flow.", "Annual Post-Harvest"),
            ("Resistant Cultivar Selection", "Varietal Breeding", "Select regional agricultural university verified disease-tolerant or resistant cultivars.", "Planting Phase"),
            ("Weekly Field Scouting & Monitoring", "Early Warning Surveillance", "Routinely inspect lowermost leaf surfaces and fruit clusters twice weekly.", "Vegetative to Harvest"),
            ("Field Tool Hygiene & Disinfection", "Sanitation", "Disinfect pruning knives, shears, and grafting blades between each tree using 1% sodium hypochlorite.", "All Year")
        ]
        prevention_dict = {}
        for title, p_type, desc, season in prevention_data:
            pv, _ = Prevention.objects.get_or_create(
                title=title,
                defaults={"practice_type": p_type, "description": desc, "season": season}
            )
            prevention_dict[title] = pv

        # 7. Seed Fruits
        fruits_data = [
            ("Mango", "Mangifera indica", "Alphonso, Kesar, Dasheri, Banganapalli", "Green to Golden Yellow", "maturation", "King of fruits widely cultivated in tropical and subtropical regions. Prone to anthracnose and powdery mildew in humid periods.", "24°C - 30°C", "50% - 65%", "Well-drained alluvial soil"),
            ("Apple", "Malus domestica", "Red Delicious, Gala, Fuji, Granny Smith", "Green to Crisp Crimson Red", "development", "Temperate deciduous fruit tree. Highly susceptible to Venturia inaequalis (scab) during cool spring rainfalls.", "18°C - 24°C", "60% - 75%", "Deep rich loamy soil"),
            ("Grape", "Vitis vinifera", "Thompson Seedless, Cabernet, Concord, Bangalore Blue", "Green to Deep Purple", "fruit_set", "Woody deciduous perennial vine yielding berries in clusters. Sensitive to black rot and powdery mildew.", "20°C - 32°C", "50% - 70%", "Sandy loam with good drainage"),
            ("Orange", "Citrus sinensis", "Nagpur Mandarin, Valencia, Navel", "Bright Orange", "development", "Subtropical citrus species bearing nutritious hesperidium fruit. Vulnerable to citrus canker and greening.", "20°C - 28°C", "55% - 75%", "Light loamy soil"),
            ("Banana", "Musa acuminata", "Grand Naine (G9), Robusta, Dwarf Cavendish", "Vibrant Yellow to Green", "development", "Fast-growing giant herbaceous monocotyledonous perennial. Prone to Sigatoka leaf spot and Panama wilt.", "25°C - 35°C", "70% - 85%", "Fertile deep clay loam"),
            ("Guava", "Psidium guajava", "Allahabad Safeda, Lucknow 49 (Sardar)", "Pale Green to Light Yellow", "development", "Hardy tropical shrub and small tree rich in Vitamin C. Main challenge is fungal wilt complex.", "23°C - 30°C", "60% - 80%", "Well-drained sandy loam"),
            ("Papaya", "Carica papaya", "Red Lady, Pusa Delicious, Solo", "Yellowish Orange", "maturation", "Fast-growing herbaceous tropical tree known for digestive enzymes. Susceptible to papaya ringspot virus.", "25°C - 32°C", "60% - 75%", "Rich porous loam"),
            ("Tomato", "Solanum lycopersicum", "Roma, Pusa Ruby, Cherry Tomato", "Lustrous Scarlet Red", "maturation", "Widely grown culinary fruit/vegetable. Prone to early and late fungal blights.", "20°C - 26°C", "50% - 70%", "Loamy soil rich in organic matter"),
            ("Pomegranate", "Punica granatum", "Bhagwa, Arakta, Ganesh", "Deep Ruby Red", "maturation", "Drought-hardy fruit crop of high antioxidant value. Vulnerable to bacterial blight (Telya).", "25°C - 35°C", "40% - 60%", "Light sandy loam")
        ]
        fruit_dict = {}
        for f_name, sci, var, col, stage, desc, opt_t, opt_h, soil in fruits_data:
            f, _ = Fruit.objects.get_or_create(
                fruit_name=f_name,
                defaults={
                    "scientific_name": sci,
                    "variety": var,
                    "color": col,
                    "growth_stage": stage,
                    "description": desc,
                    "optimal_temperature": opt_t,
                    "optimal_humidity": opt_h,
                    "soil_type": soil
                }
            )
            fruit_dict[f_name] = f

        # 8. Seed Diseases
        diseases_catalog = [
            # Mango
            {
                "fruit": "Mango",
                "name": "Mango Anthracnose",
                "code": "Mango___Anthracnose",
                "pathogen": "Colletotrichum gloeosporioides",
                "severity": "high",
                "is_healthy": False,
                "env": "Warm temperatures (25-30°C) with prolonged relative humidity (>80%).",
                "desc": "Devastating fungal disease creating sunken black necrotic spots on leaves, blossoms, and developing fruits leading to blossom blight and tear-stain fruit streaks.",
                "symptoms": ["Black Spot", "Lesion", "Fruit Rot", "Leaf Spot"],
                "treatments": ["Canopy Sanitation & Pruning", "Copper Oxychloride Protectant Spray", "Cold-Pressed Neem Seed Oil (0.5%)", "Trichoderma viride Bio-Fungicide"],
                "preventions": ["Canopy Spacing & Sun Penetration", "Micro-Drip Irrigation Implementation", "Weekly Field Scouting & Monitoring"]
            },
            {
                "fruit": "Mango",
                "name": "Mango Powdery Mildew",
                "code": "Mango___Powdery_Mildew",
                "pathogen": "Oidium mangiferae",
                "severity": "moderate",
                "is_healthy": False,
                "env": "Cool nights and dry warm days during flowering season.",
                "desc": "Fungal infection coating the inflorescence panicles and tender leaves with white talc-like powdery fungal growth, causing blossom drop and unfertilized fruitlet loss.",
                "symptoms": ["Powdery Surface", "Leaf Curl", "Discoloration"],
                "treatments": ["Bacillus subtilis Suspension", "Canopy Sanitation & Pruning"],
                "preventions": ["Canopy Spacing & Sun Penetration", "Weekly Field Scouting & Monitoring"]
            },
            {
                "fruit": "Mango",
                "name": "Mango Healthy",
                "code": "Mango___Healthy",
                "pathogen": "Healthy Host Specimen",
                "severity": "healthy",
                "is_healthy": True,
                "env": "Optimum orchard management with balanced microclimate.",
                "desc": "Specimen exhibits healthy foliage and fruit tissue with intact epidermal cuticle and vigorous photosynthetic activity.",
                "symptoms": ["Normal Leaf Morphology"],
                "treatments": ["Balanced Macro & Micronutrient Drench"],
                "preventions": ["Weekly Field Scouting & Monitoring", "Canopy Spacing & Sun Penetration"]
            },

            # Apple
            {
                "fruit": "Apple",
                "name": "Apple Scab",
                "code": "Apple___Scab",
                "pathogen": "Venturia inaequalis",
                "severity": "moderate",
                "is_healthy": False,
                "env": "Cool, wet spring weather (16-24°C) with extended leaf wetness.",
                "desc": "Foliar and fruit disease manifesting as velvety olive-green spots which darken and become corky, causing cracked, distorted fruit.",
                "symptoms": ["Leaf Spot", "Lesion", "Discoloration"],
                "treatments": ["Canopy Sanitation & Pruning", "Copper Oxychloride Protectant Spray"],
                "preventions": ["Canopy Spacing & Sun Penetration", "Field Tool Hygiene & Disinfection"]
            },
            {
                "fruit": "Apple",
                "name": "Apple Black Rot",
                "code": "Apple___Black_Rot",
                "pathogen": "Guignardia bidwellii",
                "severity": "high",
                "is_healthy": False,
                "env": "Warm wet conditions following bloom.",
                "desc": "Forms circular brown lesions with concentric rings on leaves ('frog-eye leaf spot') and dark, rotting mummified fruit.",
                "symptoms": ["Brown Spot", "Fruit Rot", "Stem Lesion"],
                "treatments": ["Canopy Sanitation & Pruning", "Copper Oxychloride Protectant Spray"],
                "preventions": ["Canopy Spacing & Sun Penetration", "Weekly Field Scouting & Monitoring"]
            },
            {
                "fruit": "Apple",
                "name": "Apple Healthy",
                "code": "Apple___Healthy",
                "pathogen": "Healthy Host Specimen",
                "severity": "healthy",
                "is_healthy": True,
                "env": "Optimal temperate orchard condition.",
                "desc": "Firm, crisp leaf lamina with no visible chlorotic margins or pathogenic lesions.",
                "symptoms": ["Normal Leaf Morphology"],
                "treatments": ["Balanced Macro & Micronutrient Drench"],
                "preventions": ["Weekly Field Scouting & Monitoring"]
            },

            # Citrus / Orange
            {
                "fruit": "Orange",
                "name": "Citrus Canker",
                "code": "Orange___Citrus_Canker",
                "pathogen": "Xanthomonas citri",
                "severity": "high",
                "is_healthy": False,
                "env": "Wind-driven heavy rains and warm temperatures (20-30°C).",
                "desc": "Bacterial disease inducing raised, blister-like corky lesions surrounded by characteristic oily margins and yellow halos on leaves and rinds.",
                "symptoms": ["Lesion", "Yellow Leaves", "Discoloration"],
                "treatments": ["Bordeaux Mixture (1%) Spray", "Streptocycline Agricultural Bactericide"],
                "preventions": ["Micro-Drip Irrigation Implementation", "Field Tool Hygiene & Disinfection"]
            },
            {
                "fruit": "Orange",
                "name": "Orange Healthy",
                "code": "Orange___Healthy",
                "pathogen": "Healthy Host Specimen",
                "severity": "healthy",
                "is_healthy": True,
                "env": "Balanced irrigation and pest-controlled citrus grove.",
                "desc": "Glossy dark green leaves showing strong vein development and vibrant tissue structure.",
                "symptoms": ["Normal Leaf Morphology"],
                "treatments": ["Balanced Macro & Micronutrient Drench"],
                "preventions": ["Weekly Field Scouting & Monitoring"]
            },

            # Grape
            {
                "fruit": "Grape",
                "name": "Grape Black Rot",
                "code": "Grape___Black_Rot",
                "pathogen": "Guignardia bidwellii",
                "severity": "high",
                "is_healthy": False,
                "env": "Warm temperatures (24-30°C) with persistent humidity.",
                "desc": "Causes circular tan leaf spots with small black pycnidia, and transforms whole berries into shriveled, hard, black mummies.",
                "symptoms": ["Black Spot", "Fruit Rot", "Leaf Spot"],
                "treatments": ["Canopy Sanitation & Pruning", "Copper Oxychloride Protectant Spray"],
                "preventions": ["Canopy Spacing & Sun Penetration", "Micro-Drip Irrigation Implementation"]
            },
            {
                "fruit": "Grape",
                "name": "Grape Healthy",
                "code": "Grape___Healthy",
                "pathogen": "Healthy Host Specimen",
                "severity": "healthy",
                "is_healthy": True,
                "env": "Well-aerated trellis system with uniform solar exposure.",
                "desc": "Clean palmately lobed grape foliage with no spots, rust, or powdery growth.",
                "symptoms": ["Normal Leaf Morphology"],
                "treatments": ["Balanced Macro & Micronutrient Drench"],
                "preventions": ["Weekly Field Scouting & Monitoring"]
            },

            # Banana
            {
                "fruit": "Banana",
                "name": "Banana Sigatoka",
                "code": "Banana___Sigatoka",
                "pathogen": "Pseudocercospora fijiensis",
                "severity": "high",
                "is_healthy": False,
                "env": "High tropical humidity (>80%) and temperatures above 26°C.",
                "desc": "Yellow-brown foliar streaks that expand and coalesce into large necrotic dark bands, inducing premature leaf death and under-sized bunches.",
                "symptoms": ["Yellow Leaves", "Brown Spot", "Lesion"],
                "treatments": ["Canopy Sanitation & Pruning", "Cold-Pressed Neem Seed Oil (0.5%)"],
                "preventions": ["Micro-Drip Irrigation Implementation", "Canopy Spacing & Sun Penetration"]
            },
            {
                "fruit": "Banana",
                "name": "Banana Healthy",
                "code": "Banana___Healthy",
                "pathogen": "Healthy Host Specimen",
                "severity": "healthy",
                "is_healthy": True,
                "env": "Fertile plantation with proper drainage.",
                "desc": "Vigorous, broad green banana leaf blade with strong midrib and zero necrotic streaks.",
                "symptoms": ["Normal Leaf Morphology"],
                "treatments": ["Balanced Macro & Micronutrient Drench"],
                "preventions": ["Weekly Field Scouting & Monitoring"]
            },

            # Tomato
            {
                "fruit": "Tomato",
                "name": "Tomato Early Blight",
                "code": "Tomato___Early_Blight",
                "pathogen": "Alternaria solani",
                "severity": "moderate",
                "is_healthy": False,
                "env": "Warm humid conditions alternating with dry intervals.",
                "desc": "Produces characteristic target-board circular lesions with concentric rings primarily on older lower leaves.",
                "symptoms": ["Brown Spot", "Yellow Leaves", "Lesion"],
                "treatments": ["Canopy Sanitation & Pruning", "Trichoderma viride Bio-Fungicide"],
                "preventions": ["Micro-Drip Irrigation Implementation", "Canopy Spacing & Sun Penetration"]
            },
            {
                "fruit": "Tomato",
                "name": "Tomato Healthy",
                "code": "Tomato___Healthy",
                "pathogen": "Healthy Host Specimen",
                "severity": "healthy",
                "is_healthy": True,
                "env": "Polyhouse or well-staked field with drip irrigation.",
                "desc": "Vibrant compound leaves with uniform green turgid leaflets free from blights.",
                "symptoms": ["Normal Leaf Morphology"],
                "treatments": ["Balanced Macro & Micronutrient Drench"],
                "preventions": ["Weekly Field Scouting & Monitoring"]
            }
        ]

        for item in diseases_catalog:
            fruit_obj = fruit_dict.get(item["fruit"])
            pathogen_obj = pathogen_dict.get(item["pathogen"])
            d, _ = Disease.objects.get_or_create(
                code_name=item["code"],
                defaults={
                    "disease_name": item["name"],
                    "affected_fruit": fruit_obj,
                    "pathogen": pathogen_obj,
                    "pathogen_name": item["pathogen"],
                    "severity": item["severity"],
                    "is_healthy": item["is_healthy"],
                    "environmental_condition": item["env"],
                    "description": item["desc"]
                }
            )

            # Link symptoms
            for s_name in item["symptoms"]:
                if s_name in symptom_dict:
                    d.symptoms.add(symptom_dict[s_name])

            # Link treatments
            for t_name in item["treatments"]:
                if t_name in treatment_dict:
                    d.treatments.add(treatment_dict[t_name])

            # Link preventions
            for p_name in item["preventions"]:
                if p_name in prevention_dict:
                    d.preventions.add(prevention_dict[p_name])

            # Link high humidity and warm temp env factors
            if not item["is_healthy"]:
                if "High Relative Humidity (>80%)" in env_dict:
                    d.environmental_factors.add(env_dict["High Relative Humidity (>80%)"])
                if "Warm Temperatures (25°C - 32°C)" in env_dict:
                    d.environmental_factors.add(env_dict["Warm Temperatures (25°C - 32°C)"])

        # 9. Create Sample Synthetic Images and Sample Predictions for Demonstration
        self.stdout.write("Generating sample demo images and prediction records...")
        
        sample_scenarios = [
            {
                "user": farmer_user,
                "fruit": "Mango",
                "disease": "Mango Anthracnose",
                "confidence": 94.6,
                "color_fill": (90, 140, 45),
                "spots": True,
                "filename": "sample_mango_anthracnose.jpg",
                "notes": "Observed on mature Dasheri mango trees during humid monsoon spell."
            },
            {
                "user": farmer_user,
                "fruit": "Apple",
                "disease": "Apple Scab",
                "confidence": 91.2,
                "color_fill": (80, 150, 60),
                "spots": True,
                "filename": "sample_apple_scab.jpg",
                "notes": "Collected from lower orchard canopy after continuous spring rainfall."
            },
            {
                "user": expert_user,
                "fruit": "Orange",
                "disease": "Citrus Canker",
                "confidence": 96.8,
                "color_fill": (210, 130, 30),
                "spots": True,
                "filename": "sample_citrus_canker.jpg",
                "notes": "Specimen sent for university pathology lab validation."
            },
            {
                "user": farmer_user,
                "fruit": "Mango",
                "disease": "Mango Healthy",
                "confidence": 98.4,
                "color_fill": (45, 170, 55),
                "spots": False,
                "filename": "sample_mango_healthy.jpg",
                "notes": "Post-sanitation healthy vegetative check on new Alphonso flush."
            }
        ]

        for sc in sample_scenarios:
            # Generate a 224x224 synthetic test image in memory
            img = Image.new('RGB', (224, 224), color=sc["color_fill"])
            draw = ImageDraw.Draw(img)
            
            # Draw leaf shape
            draw.ellipse([30, 20, 194, 204], fill=sc["color_fill"], outline=(30, 80, 20), width=3)
            # Draw midrib vein
            draw.line([(112, 20), (112, 204)], fill=(120, 200, 70), width=3)

            if sc["spots"]:
                # Draw dark necrotic spots
                draw.ellipse([70, 70, 95, 95], fill=(40, 25, 15))
                draw.ellipse([130, 110, 155, 135], fill=(35, 20, 10))
                draw.ellipse([90, 140, 115, 165], fill=(50, 30, 20))
            
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=90)
            img_content = ContentFile(buf.getvalue(), name=sc["filename"])

            up_img = UploadedImage.objects.create(
                user=sc["user"],
                image=img_content,
                original_filename=sc["filename"],
                file_size_bytes=len(buf.getvalue()),
                width=224,
                height=224
            )

            fruit_obj = fruit_dict.get(sc["fruit"])
            disease_obj = Disease.objects.filter(disease_name=sc["disease"]).first()

            pred = Prediction.objects.create(
                uploaded_image=up_img,
                user=sc["user"],
                fruit_name=sc["fruit"],
                disease_name=sc["disease"],
                confidence=sc["confidence"],
                is_mock=True,
                model_source="Demonstration Mock Prediction Engine (Awaiting fruit_disease_model.h5)",
                fruit_ref=fruit_obj,
                disease_ref=disease_obj,
                temperature_input="28",
                humidity_input="78",
                user_notes=sc["notes"]
            )

            # Build diagnosis
            is_healthy = "healthy" in sc["disease"].lower()
            severity = "Healthy" if is_healthy else ("High" if "anthracnose" in sc["disease"].lower() or "canker" in sc["disease"].lower() else "Moderate")
            pathogen_name = "None (Healthy Tissue)" if is_healthy else ("Colletotrichum gloeosporioides (Fungus)" if "anthracnose" in sc["disease"].lower() else "Xanthomonas citri (Bacterium)")

            symptoms = ["Normal Leaf Morphology"] if is_healthy else ["Black Spot", "Lesion", "Tissue Chlorosis"]
            treatments = ["Maintain standard irrigation and nutrient balance."] if is_healthy else [
                "[Cultural] Pruning & Sanitation: Cut dead twigs 5 cm below infection.",
                "[Chemical] Copper Oxychloride 50% WP at 2.5 g/L.",
                "[Organic] Cold-Pressed Neem Seed Oil 0.5%."
            ]
            preventions = [
                "Micro-Drip Irrigation: Avoid overhead sprinklers.",
                "Canopy Management: Thin branches to maximize sun drying.",
                "Field Sanitation: Disinfect shears with 70% alcohol."
            ]
            explanation = (
                f"Ontology Rule Verification: The ML pipeline classified the specimen as '{sc['disease']}' "
                f"with {sc['confidence']}% confidence. The semantic knowledge graph mapped this to severity class '{severity}'. "
                f"Agronomic remediation protocols were inferred through Protégé-compatible OWL axioms."
            )

            Diagnosis.objects.create(
                prediction=pred,
                severity=severity,
                pathogen=pathogen_name,
                symptoms_summary="; ".join(symptoms),
                treatments_summary="; ".join(treatments),
                prevention_summary="; ".join(preventions),
                environmental_factors_summary="High Humidity (>80%); Warm Temperatures (25-30°C)",
                explanation=explanation,
                ontology_individual=f"Disease_{sc['disease'].replace(' ', '_')}"
            )

        self.stdout.write(self.style.SUCCESS("[SUCCESS] Seed data completed successfully!"))
        self.stdout.write(self.style.SUCCESS("  - 3 User accounts created (admin / farmer_ramesh / expert_dr_sharma)"))
        self.stdout.write(self.style.SUCCESS(f"  - {len(fruits_data)} Fruits, {len(diseases_catalog)} Diseases seeded"))
        self.stdout.write(self.style.SUCCESS("  - Symptoms, Pathogens, Treatments, and Preventions interconnected"))
        self.stdout.write(self.style.SUCCESS("  - Sample test predictions generated with real images for immediate viva demo"))
