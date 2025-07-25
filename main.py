from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
model = ocr_predictor(pretrained=True)

KEYWORDS = ["TOTAL", "TOTALE", "MONTANT", "BETRAG", "IMPORTO", "TOTALTTC", "AMOUNT", "TOTAL:", "TOT"]

def extract_total(image_bytes):
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

@app.post("/ocr/", response_class=JSONResponse)
async def api_ocr(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Carica un file immagine valido.")

    image_bytes = await file.read()
    try:
        totale = extract_total(image_bytes)
        if totale:
            return {"totale": totale}
        else:
            return {"totale": None, "message": "Nessun totale rilevato"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore: {str(e)}")
