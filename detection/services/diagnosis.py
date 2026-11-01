import logging
from typing import Dict, Any, Optional
from ontology_engine.reasoner import OntologyReasoner
from recommendations.treatment import get_categorized_treatments
from recommendations.prevention import get_prevention_guidelines
from fruits.models import Fruit
from diseases.models import Disease

logger = logging.getLogger(__name__)

class DiagnosisEngine:
    """
    Coordinates ML prediction output with the Semantic Ontology Reasoning Engine
    and relational knowledge base to produce an integrated, authoritative diagnosis.
    """

    def __init__(self):
        self.reasoner = OntologyReasoner()

    def generate_diagnosis(self, ml_prediction: Dict[str, Any], env_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Synthesizes ML prediction, ontology inference, and localized recommendations.
        """
        # Step 1: Execute ontology semantic reasoning
        ontology_results = self.reasoner.reason(ml_prediction, env_context=env_context)

        fruit_name = ml_prediction.get("fruit", "Fruit")
        disease_name = ml_prediction.get("disease", "Unknown Disease")
        is_mock = ml_prediction.get("is_mock", True)
        confidence = ml_prediction.get("confidence", 0.0)

        # Step 2: Resolve DB entities and adjust suggestions for healthy fruits
        fruit_obj = Fruit.objects.filter(fruit_name__iexact=fruit_name).first()
        if not fruit_obj and fruit_name.lower() in ['grape', 'grapes']:
            fruit_obj = Fruit.objects.filter(fruit_name__iexact='Grape').first()

        is_healthy = ml_prediction.get("is_healthy", False) or "healthy" in disease_name.lower() or "no disease" in disease_name.lower()

        if is_healthy:
            # Use healthy Disease entry if it exists
            disease_obj = Disease.objects.filter(affected_fruit=fruit_obj, is_healthy=True).first()
            # Healthy care tips instead of generic treatments
            from recommendations.healthy_care import get_healthy_care_tips
            treatment_strings = get_healthy_care_tips(fruit_name)
        else:
            disease_obj = Disease.objects.filter(disease_name__iexact=disease_name).first()
            if not disease_obj and fruit_obj:
                # Fallback search within that fruit
                disease_obj = Disease.objects.filter(affected_fruit=fruit_obj, disease_name__icontains=disease_name.replace(fruit_name, "").strip()).first()
            # Normal treatment extraction
            lookup_name = disease_name
            categorized_treatments = get_categorized_treatments(lookup_name)
            treatment_strings = []
            for cat, items in categorized_treatments.items():
                for item in items:
                    treatment_strings.append(f"[{cat.title()}] {item['title']}: {item['description']}")

        # Step 3: Extract structured symptoms from ontology + DB
        symptoms_list = ontology_results.get("symptoms", [])
        if disease_obj and disease_obj.symptoms.exists():
            for s in disease_obj.symptoms.all():
                if s.name not in symptoms_list:
                    symptoms_list.append(s.name)

        # Step 4: Merge ontology treatments (treatment_strings already set in Step 2)
        lookup_name = "Healthy" if is_healthy else disease_name
        categorized_treatments = get_categorized_treatments(lookup_name) if not is_healthy else {}

        # Merge ontology treatments
        for ot in ontology_results.get("treatments", []):
            if ot not in treatment_strings:
                treatment_strings.append(ot)

        # Step 5: Extract preventions
        prevention_items = get_prevention_guidelines(lookup_name, fruit_name=fruit_name)
        prevention_strings = [f"{p['practice']}: {p['action']}" for p in prevention_items]
        for op in ontology_results.get("prevention", []):
            if op not in prevention_strings:
                prevention_strings.append(op)

        # Step 6: Environmental factors
        env_list = ontology_results.get("environmental_factors", [])
        if env_context:
            if env_context.get("temperature"):
                env_list.append(f"Recorded Temperature: {env_context['temperature']}°C")
            if env_context.get("humidity"):
                env_list.append(f"Recorded Relative Humidity: {env_context['humidity']}%")

        severity = ontology_results.get("severity", "Moderate")
        pathogen = ontology_results.get("pathogen", "Plant Pathogen")
        explanation = ontology_results.get("explanation", "")

        return {
            "fruit_name": fruit_name,
            "disease_name": disease_name,
            "confidence": confidence,
            "is_mock": is_mock,
            "model_source": ml_prediction.get("model_source", "CNN Classifier"),
            "severity": severity,
            "pathogen": pathogen,
            "is_healthy": ontology_results.get("is_healthy", False),
            "symptoms": symptoms_list,
            "treatments": treatment_strings,
            "prevention": prevention_strings,
            "environmental_factors": env_list,
            "explanation": explanation,
            "categorized_treatments": categorized_treatments,
            "prevention_guidelines": prevention_items,
            "fruit_obj": fruit_obj,
            "disease_obj": disease_obj,
            "ontology_individual": ontology_results.get("ontology_individual", "")
        }
