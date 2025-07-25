from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re
import io

app = FastAPI()

# Carica il modello solo una volta
model = ocr_predictor(pretrained=True)

# Parole chiave comuni in vari paesi
KEYWORDS = ["TOTAL", "TOTALE", "MONTANT", "BETRAG", "IMPORTO", "TOTALTTC", "AMOUNT", "TOTAL:", "TOT"]

def estrai_totale(image_bytes):
    doc = DocumentFile.from_images(image_bytes)
    result = model(doc)
    text = result.render().upper()

    # 1. Cerca keyword seguita da un numero
    for kw in KEYWORDS:
        pattern = rf"{kw}[^0-9]*([0-9]+[,.][0-9]{{2}})"
        match = re.search(pattern, text)
        if match:
            return match.group(1).replace(",", ".")

    # 2. Fallback: prendi il numero più alto
    numeri = re.findall(r"([0-9]+[,.][0-9]{2})", text)
    if numeri:
        numeri_float = [float(n.replace(",", ".")) for n in numeri]
        return str(max(numeri_float))

    return None

totale = estrai_totale("scontrino.jpeg")
if totale:
    print("✅ Totale trovato:", totale)
else:
    print("❌ Nessun totale rilevato")

@app.post("/ocr/")
async def ocr_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File non valido. Atteso un file immagine.")

    image_bytes = await file.read()

    try:
        totale = estrai_totale(image_bytes)
        if totale:
            return JSONResponse({"totale": totale})
        else:
            return JSONResponse({"totale": None, "message": "Nessun totale rilevato"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'elaborazione: {str(e)}")
