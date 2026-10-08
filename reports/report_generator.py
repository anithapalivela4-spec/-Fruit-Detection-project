"""
Diagnostic and Academic Project Report Generator.
Generates comprehensive printable and downloadable reports for viva/field use.
"""

from typing import Dict, Any

def generate_text_report(prediction_obj) -> str:
    """Generates a structured plain-text academic/field report."""
    diag = getattr(prediction_obj, 'diagnosis', None)
    
    report_lines = [
        "=" * 70,
        "   FRUIT DISEASE DETECTION SYSTEM - DIAGNOSTIC REPORT",
        "   AI & Semantic Web Ontology-Driven Decision Support",
        "=" * 70,
        f"Report ID: #{prediction_obj.id}",
        f"Date/Time: {prediction_obj.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"User: {prediction_obj.user.username} ({prediction_obj.user.email or 'N/A'})",
        "-" * 70,
        "1. SPECIMEN & ML PREDICTION",
        f"   Target Fruit        : {prediction_obj.fruit_name}",
        f"   Predicted Disease   : {prediction_obj.disease_name}",
        f"   Model Confidence    : {prediction_obj.confidence:.2f}%",
        f"   Inference Pipeline  : {prediction_obj.model_source}",
        f"   Mock Mode Active    : {'Yes (Demo Mode)' if prediction_obj.is_mock else 'No (Live Deep Learning Model)'}",
        "-" * 70,
    ]

    if diag:
        report_lines.extend([
            "2. ONTOLOGY REASONING & SEMANTIC INFERENCE",
            f"   Assigned Severity   : {diag.severity}",
            f"   Identified Pathogen : {diag.pathogen}",
            f"   Ontology Individual : {diag.ontology_individual or 'FruitDiseaseOntology Class'}",
            f"   Reasoning Statement :",
            f"     {diag.explanation}",
            "-" * 70,
            "3. ASSOCIATED CLINICAL SYMPTOMS",
        ])
        for sym in diag.get_symptoms_list():
            report_lines.append(f"   • {sym}")
            
        report_lines.extend([
            "-" * 70,
            "4. INTEGRATED TREATMENT & CARE GUIDANCE",
        ])
        for treat in diag.get_treatments_list():
            report_lines.append(f"   • {treat}")

        report_lines.extend([
            "-" * 70,
            "5. PREVENTATIVE AGRONOMIC MEASURES",
        ])
        for prev in diag.get_prevention_list():
            report_lines.append(f"   • {prev}")

    report_lines.extend([
        "=" * 70,
        "   DISCLAIMER: This diagnostic advisory is produced by an academic",
        "   deep learning and ontology system. Follow certified local agricultural",
        "   extension guidelines before applying commercial chemicals.",
        "=" * 70,
    ])

    return "\n".join(report_lines)
