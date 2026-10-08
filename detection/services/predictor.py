from typing import Dict, Any, Optional
from model.prediction.predict import predict_fruit_disease

class DetectionPredictorService:
    @staticmethod
    def run_prediction(image_path_or_file, fruit_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes prediction on given image file/path.
        Returns:
            {
                "fruit": str,
                "disease": str,
                "confidence": float,
                "is_mock": bool,
                "model_source": str
            }
        """
        return predict_fruit_disease(image_path_or_file, fruit_hint=fruit_hint)
