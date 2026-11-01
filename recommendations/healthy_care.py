from typing import List

HEALTHY_CARE_TIPS = {
    "Apple": [
        "Store apples in a cool, dry place or refrigerator to prolong freshness.",
        "Wash apples before consumption to remove residues.",
        "Keep apples away from strong ethylene-producing fruits like bananas.",
        "Inspect regularly for bruises or soft spots and remove affected areas."
    ],
    "Banana": [
        "Store bananas at room temperature; avoid refrigeration until fully ripe.",
        "Separate bananas from other fruits to slow down ripening.",
        "Keep bananas away from direct sunlight and heat sources.",
        "Consume within a few days of ripening to prevent over‑softness."
    ],
    "Grape": [
        "Refrigerate grapes in a breathable container or perforated bag.",
        "Wash grapes gently before eating; avoid soaking.",
        "Remove any shriveled or moldy grapes to protect the bunch.",
        "Store away from strong‑smelling foods to maintain flavor."
    ],
    "Tomato": [
        "Store tomatoes at room temperature away from direct sunlight.",
        "Avoid refrigerating as it reduces flavor and texture.",
        "Keep stems intact and handle gently to prevent bruising.",
        "Consume within a week for best taste and nutritional value."
    ],
    "Orange": [
        "Store oranges in a cool, well‑ventilated area; refrigeration is optional.",
        "Wash the peel before consumption to remove surface contaminants.",
        "Handle gently to avoid skin punctures that lead to spoilage.",
        "Consume within 2‑3 weeks for optimal freshness."
    ],
    "Mango": [
        "Allow mangoes to ripen at room temperature; refrigerate after ripe.",
        "Store mangoes away from direct sunlight to prevent uneven ripening.",
        "Handle with care to avoid bruising the soft flesh.",
        "Consume before the skin turns overly wrinkled or mushy."
    ]
}

def get_healthy_care_tips(fruit_name: str) -> List[str]:
    """Return a short list of 3‑4 general care tips for a healthy fruit.
    If the fruit is not in the predefined map, a generic set of tips is returned.
    """
    return HEALTHY_CARE_TIPS.get(fruit_name, [
        "Store the fruit in appropriate conditions (cool, dry, well‑ventilated).",
        "Handle gently and wash before consumption.",
        "Inspect regularly and remove any spoiled portions.",
        "Consume within the typical freshness window for the fruit."
    ])
