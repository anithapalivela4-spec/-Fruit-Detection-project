import os, sys
sys.path.insert(0, '.')

# ============================================================
# CHECK 1: predict.py class labels
# ============================================================
from model.prediction.predict import CLASS_LABELS, FRUIT_DISEASE_MAPPINGS
print("=== CHECK 1: CLASS LABELS (12 classes) ===")
for i, c in enumerate(CLASS_LABELS):
    print("  [{}] {:8} | {:30} | healthy={}".format(i, c["fruit"], c["disease"], c["healthy"]))

# ============================================================
# CHECK 2: Contact page phone/location
# ============================================================
print()
print("=== CHECK 2: CONTACT PAGE ===")
with open("templates/contact.html", encoding="utf-8") as f:
    ct = f.read()
print("  Phone 7995210970 present:", "7995210970" in ct)
print("  Rajahmundry present:", "Rajahmundry" in ct)
print("  Andhra Pradesh present:", "Andhra Pradesh" in ct)

# ============================================================
# CHECK 3: Gallery images variety
# ============================================================
print()
print("=== CHECK 3: GALLERY IMAGES ===")
with open("templates/gallery.html", encoding="utf-8") as f:
    gl = f.read()
fruits = ["apple", "banana", "mango", "tomato", "grape", "orange"]
for fr in fruits:
    print("  {} image referenced: {}".format(fr.capitalize(), fr.lower() in gl.lower()))

# ============================================================
# CHECK 4: Footer nav links removed
# ============================================================
print()
print("=== CHECK 4: FOOTER NAV LINKS ===")
with open("templates/base.html", encoding="utf-8") as f:
    base = f.read()

footer_start = base.lower().find("<footer")
footer_content = base[footer_start:] if footer_start != -1 else ""
nav_links = ["/detect", "/about", "/gallery", "/contact"]
all_removed = True
for link in nav_links:
    found = link.lower() in footer_content.lower()
    if found:
        all_removed = False
    print("  Nav link '{}' in footer: {}".format(link, "FOUND (not removed!)" if found else "Removed OK"))

home_links = ['href="/"', "href='/'"]
home_found = any(lk in footer_content for lk in home_links)
if home_found:
    all_removed = False
print("  Home link (href='/') in footer: {}".format("FOUND (not removed!)" if home_found else "Removed OK"))

print()
print("=== SUMMARY ===")
print("  Contact details: OK" if ("7995210970" in ct and "Rajahmundry" in ct) else "  Contact details: MISSING!")
print("  Gallery images: OK" if all(fr in gl.lower() for fr in fruits) else "  Gallery images: SOME MISSING")
print("  Footer nav links: {}".format("All removed OK" if all_removed else "Some links still present"))
