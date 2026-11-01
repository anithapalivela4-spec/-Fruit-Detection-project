"""
Treatment Recommendation Service.
Provides categorized treatment advice across:
- Organic Treatment
- Biological Treatment
- Cultural Management
- Safe Agricultural Chemical Guidance
"""

from typing import Dict, List, Any

TREATMENT_CATEGORIES = {
    'organic': 'Organic Treatment',
    'biological': 'Biological Control',
    'cultural': 'Cultural & Field Management',
    'chemical': 'Chemical Protectant Guidance'
}

def get_categorized_treatments(disease_name: str) -> Dict[str, List[Dict[str, str]]]:
    """Return categorized treatment recommendations based on disease."""
    d_lower = disease_name.lower()
    
    if "healthy" in d_lower or "no disease" in d_lower:
        return {
            'cultural': [{
                'title': 'Canopy Aeration & Pruning',
                'description': 'Keep inner canopy open to ensure uniform sunlight penetration and prevent moisture buildup.',
                'precautions': 'Sanitize pruning shears between trees.'
            }],
            'organic': [{
                'title': 'Balanced Organic Nutrition',
                'description': 'Apply decomposed farmyard manure (FYM) or vermicompost to bolster natural systemic acquired resistance (SAR).',
                'precautions': 'Avoid excessive nitrogen fertilization which makes young flush susceptible to sucking pests.'
            }]
        }

    # Common treatments for anthracnose, rot, scab, canker, sigatoka
    results = {
        'organic': [],
        'biological': [],
        'cultural': [],
        'chemical': []
    }

    results['cultural'].append({
        'title': 'Sanitation & Debris Destruction',
        'description': 'Prune out mummified fruits, infected twigs 5 cm below the margin of infection, and collect fallen fallen foliage for immediate burial or composting away from orchard.',
        'precautions': 'Do not prune during humid, rainy, or overcast days to avoid spreading conidia.'
    })

    if "anthracnose" in d_lower or "scab" in d_lower or "rot" in d_lower:
        results['organic'].append({
            'title': 'Cold-Pressed Neem Seed Oil (0.5%)',
            'description': 'Spray 5 ml pure neem oil emulsified with 1 ml liquid soap per liter of water as a protective bio-fungal barrier on new flushes.',
            'precautions': 'Spray during early morning or evening hours to avoid phytotoxicity from direct sun.'
        })
        results['biological'].append({
            'title': 'Trichoderma viride / harzianum Formulation',
            'description': 'Apply bio-agent Trichoderma at 5g/liter as a foliar mist and tree collar drench to outcompete fungal mycelium.',
            'precautions': 'Do not mix biological agents simultaneously with chemical copper or sulphur fungicides.'
        })
        results['chemical'].append({
            'title': 'Copper Oxychloride (COC 50% WP)',
            'description': 'Foliar application of copper oxychloride at 2.5 g per liter of clean water during early pre-monsoon flush initiation.',
            'precautions': 'Follow recommended pre-harvest interval (PHI). Wear protective mask and gloves. Avoid water drift into bee hives.'
        })
    elif "canker" in d_lower or "bacterial" in d_lower:
        results['organic'].append({
            'title': 'Bordeaux Mixture (1%) Spray',
            'description': 'Freshly prepared 1:1:100 Bordeaux mixture (copper sulfate + slaked lime + water) applied after post-pruning.',
            'precautions': 'Use plastic, wooden, or earthen vessels for preparation; do not use metal.'
        })
        results['biological'].append({
            'title': 'Pseudomonas fluorescens Bio-Protection',
            'description': 'Spray microbial suspension of Pseudomonas fluorescens at 10g/L to colonize plant phyllosphere and suppress bacterial blight.',
            'precautions': 'Store bio-inoculants in a cool, shaded environment.'
        })
        results['chemical'].append({
            'title': 'Streptocycline + Copper Protectant',
            'description': 'Agricultural-grade bactericide (Streptocycline 100 ppm) combined with Copper Oxychloride (0.2%) during vegetative flush.',
            'precautions': 'Follow strict label dilution guidelines; observe 15-day pre-harvest interval.'
        })
    else:
        results['organic'].append({
            'title': 'Sulfur Dust / Liquid Wettable Sulfur (80% WDG)',
            'description': 'Spray at 2g/L for broad-spectrum powdery mildew and fungal spot prevention.',
            'precautions': 'Do not spray when temperatures exceed 32°C.'
        })
        results['biological'].append({
            'title': 'Bacillus subtilis (Serenade / Bio-agent)',
            'description': 'Apply beneficial bacterial antagonist at 3ml/L to inhibit spore germination.',
            'precautions': 'Keep away from direct heat.'
        })
        results['chemical'].append({
            'title': 'Broad-Spectrum Protective Fungicide',
            'description': 'Consult local certified agricultural extension officer for approved target fungicides.',
            'precautions': 'Always wear PPE and adhere to manufacturer safety data sheet.'
        })

    return results
