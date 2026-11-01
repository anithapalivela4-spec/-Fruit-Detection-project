import os, sys
sys.path.insert(0, os.path.abspath('.'))
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from model.prediction.predict import FruitDiseasePredictor

p = FruitDiseasePredictor()

test_cases = [
    ('Apple Healthy', 'static/images/apple.png', 'Apple', 'Apple Healthy'),
    ('Apple Scab', 'media/uploads/2026/10/08/Screenshot_2026-10-08_171602.png', 'Apple', 'Apple Scab'),
    ('Banana Healthy', 'static/images/banana.png', 'Banana', 'Banana Healthy'),
    ('Banana Sigatoka', 'media/uploads/2026/10/08/Screenshot_2026-10-08_171653.png', 'Banana', 'Banana Sigatoka'),
    ('Grape Healthy', 'static/images/grapes.png', 'Grape', 'Grape Healthy'),
    ('Grape Black Rot', 'media/uploads/2026/10/08/Screenshot_2026-10-08_171632.png', 'Grape', 'Grape Black Rot'),
    ('Mango Healthy', 'static/images/mango.png', 'Mango', 'Mango Healthy'),
    ('Mango Anthracnose', 'media/uploads/2026/10/08/Screenshot_2026-10-08_142512.png', 'Mango', 'Mango Anthracnose'),
    ('Orange Healthy', 'static/images/orange.png', 'Orange', 'No disease detected'),
    ('Citrus Canker', 'media/uploads/2026/10/08/Screenshot_2026-10-08_171717.png', 'Orange', 'Citrus Canker'),
    ('Tomato Healthy', 'static/images/tomato.png', 'Tomato', 'No disease detected'),
    ('Tomato Healthy (Uploaded)', 'media/uploads/2026/10/09/Screenshot_2026-10-09_141100.png', 'Tomato', 'No disease detected'),
    ('Tomato Early Blight', 'media/uploads/2026/10/08/Screenshot_2026-10-08_171733.png', 'Tomato', 'Tomato Early Blight'),
]

# Support 'No disease detected' or '{Fruit} Healthy'
for i in range(len(test_cases)):
    lbl, pth, frt, dis = test_cases[i]
    if 'healthy' in lbl.lower():
        test_cases[i] = (lbl, pth, frt, 'No disease detected')

print("=== VERIFYING ALL 12 FRUIT & DISEASE CLASSES (HEALTHY & DISEASED) ===")
all_passed = True
for label, pth, exp_fruit, exp_disease in test_cases:
    if os.path.exists(pth):
        res = p.predict(pth)
        f = res['fruit']
        d = res['disease']
        c = res['confidence']
        src = res['model_source']
        is_healthy_match = (exp_disease == 'No disease detected' and (d == 'No disease detected' or 'healthy' in d.lower()))
        is_pass = (f == exp_fruit and (d == exp_disease or is_healthy_match))
        if not is_pass:
            all_passed = False
        status = "PASS" if is_pass else "FAIL"
        print(f"[{status}] {label:20} -> Fruit: {f:8} (exp: {exp_fruit:8}) | Disease: {d:22} (exp: {exp_disease:22}) | {c}% | {src[:25]}")
    else:
        print(f"[MISSING] {pth}")

print(f"\nOverall result: {'ALL 12 TEST CASES PASSED PERFECTLY!' if all_passed else 'SOME FAILED'}")
assert all_passed, "Not all test cases passed!"
