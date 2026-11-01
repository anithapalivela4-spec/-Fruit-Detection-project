"""
Prevention Recommendation Service.
Provides agricultural prevention strategies including:
- Proper irrigation
- Field sanitation
- Pruning
- Resistant varieties
- Crop rotation
- Proper spacing
- Regular monitoring
"""

from typing import List, Dict

def get_prevention_guidelines(disease_name: str, fruit_name: str = "") -> List[Dict[str, str]]:
    """Return categorized prevention measures for the diagnosed disease."""
    is_healthy = "healthy" in disease_name.lower() or "no disease" in disease_name.lower()
    
    guidelines = [
        {
            'practice': 'Sanitation & Orchard Hygiene',
            'season': 'Year-Round / Post-Harvest',
            'action': 'Rake and burn/bury all fallen leaf litter and diseased mummified fruits. Disinfect shears and pruning saws with 70% isopropyl alcohol or 1% bleach solution.'
        },
        {
            'practice': 'Irrigation Management',
            'season': 'Dry Seasons & Growth Cycles',
            'action': 'Use micro-drip or sub-surface irrigation. Avoid overhead sprinklers that keep leaf and canopy wet for prolonged hours, triggering spore germ tube penetration.'
        },
        {
            'practice': 'Canopy Aeration & Spacing',
            'season': 'Pre-monsoon / Annual Pruning',
            'action': 'Maintain adequate planting distances (e.g., 6x6m to 8x8m for tree crops) and thin crossing branches to promote air movement and rapid sun-drying of foliage.'
        },
        {
            'practice': 'Cultivar Selection & Resistant Varieties',
            'season': 'Planting Phase',
            'action': f'Plant verified disease-tolerant or resistant cultivars recommended by regional agricultural universities for {fruit_name or "orchard crops"}.'
        },
        {
            'practice': 'Field Scouting & Early Monitoring',
            'season': 'Weekly Scouting',
            'action': 'Inspect lower canopy, undersides of young leaves, and developing fruit clusters twice weekly, especially after warm spells or intermittent rains.'
        }
    ]

    if not is_healthy:
        guidelines.append({
            'practice': 'Nutritional Balance & Soil Health',
            'season': 'Pre-Flowering',
            'action': 'Conduct soil testing. Avoid excess nitrogenous fertilizers which promote lush succulent tissues that are highly vulnerable to fungal penetration. Supplement potassium and calcium to strengthen cell walls.'
        })

    return guidelines
