from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import io
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key="AIzaSyAp2G0EQDjvzdazNTT78qyceLSFZRUmGJM")
model = genai.GenerativeModel("gemini-2.5-flash")
@app.get("/")
def get_root():
    return {"message": "Bienvenue dans l'API de traduction du darija marocain vers le français."}
@app.post("/translate/")
async def translate_file(file: UploadFile = File(...)):
    contents = await file.read()
    lignes = contents.decode().splitlines()

    output = io.StringIO()

    
    prompt = f"Traduire ce texte du darija marocain vers le français et c'est un time code tu le laisse comment il est  n'ajoute rien de ta téte juste traduit le texte qu on il s'agit d une ligne texte ne me dit pas aucune chose  :\n{li}"
    response = model.generate_content(prompt)
    traduction = response.text.strip()
    output.write(traduction + "\n")

    return StreamingResponse(output, media_type="text/plain", headers={
        "Content-Disposition": f"attachment; filename=traduit.txt"
    })
