import os
from django.conf import settings
from model.prediction.predict import get_predictor

def system_status(request):
    """
    Supplies global template context on system mode:
    whether real ML model or Mock is loaded, ontology loaded, etc.
    """
    predictor = get_predictor()
    model_exists = os.path.exists(settings.SAVED_MODEL_PATH)
    owl_exists = os.path.exists(settings.OWL_FILE_PATH)
    
    return {
        'SYSTEM_MOCK_MODE': predictor.is_mock,
        'MODEL_FILE_EXISTS': model_exists,
        'ONTOLOGY_FILE_EXISTS': owl_exists,
        'MODEL_PATH_REL': 'model/saved_models/fruit_disease_model.h5',
        'ONTOLOGY_PATH_REL': 'ontology/fruit_disease.owl',
    }
