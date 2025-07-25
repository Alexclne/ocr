from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re


app = FastAPI()
templates = Jinja2Templates(directory="templates")
model = ocr_predictor(pretrained=True)

KEYWORDS = ["TOTAL", "TOTALE", "MONTANT", "BETRAG", "IMPORTO", "TOTALTTC", "AMOUNT", "TOTAL:", "TOT"]

def extract_total(image_bytes):
    try:
        doc = DocumentFile.from_images(image_bytes)
    except Exception as e:
        raise ValueError(f"Errore nel caricamento dell'immagine: {e}")
    
    doc = DocumentFile.from_images(image_bytes)
    result = model(doc)
    text = result.render().upper()

    for kw in KEYWORDS:
        pattern = rf"{kw}[^0-9]*([0-9]+[,.][0-9]{{2}})"
        match = re.search(pattern, text)
        if match:
            return match.group(1).replace(",", ".")

    numeri = re.findall(r"([0-9]+[,.][0-9]{2})", text)
    if numeri:
        numeri_float = [float(n.replace(",", ".")) for n in numeri]
        return str(max(numeri_float))

    return None

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "totale": None})

@app.post("/", response_class=HTMLResponse)
async def submit(request: Request, file: UploadFile = File(...)):
    image_bytes = await file.read()
    totale = extract_total(image_bytes)
    return templates.TemplateResponse("index.html", {"request": request, "totale": totale})

@app.post("/ocr/")
async def ocr_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File non valido. Atteso un file immagine.")

    image_bytes = await file.read()

    try:
        totale = extract_total(image_bytes)
        if totale:
            return JSONResponse({"totale": totale})
        else:
            return JSONResponse({"totale": None, "message": "Nessun totale rilevato"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'elaborazione: {str(e)}")
