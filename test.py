from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

KEYWORDS = ["TOTAL", "TOTALE", "MONTANT", "BETRAG", "IMPORTO", "TOTALTTC", "AMOUNT", "TOTAL:", "TOT"]

def estrai_totale(path_img):
    doc = DocumentFile.from_images(path_img)
    model = ocr_predictor(pretrained=True)
    result = model(doc)
    text = result.render().upper()

    # 1. Cerca keyword + numero accanto
    for kw in KEYWORDS:
        pattern = rf"{kw}[^0-9]*([0-9]+[,.][0-9]{{2}})"
        match = re.search(pattern, text)
        if match:
            return match.group(1).replace(",", ".")

    # 2. Fallback: numero più alto
    numeri = re.findall(r"([0-9]+[,.][0-9]{2})", text)
    if numeri:
        numeri_float = [float(n.replace(",", ".")) for n in numeri]
        return str(max(numeri_float))

    return None

totale = estrai_totale("image.png")
if totale:
    print("✅ Totale trovato:", totale)
else:
    print("❌ Nessun totale rilevato")