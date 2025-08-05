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
    texte_a_traduire = ""

    for line in lignes:
        if line.strip() == "":
            texte_a_traduire += "\n"
        elif line.strip().replace(" ", "").isdigit() or \
             (":" in line and any(c.isdigit() for c in line)):
            texte_a_traduire += line + "\n"
        else:
            texte_a_traduire += line + "\n"

    prompt = (
        "Traduire ce texte du darija marocain vers le français.\n"
        "Garder intact les numéros et les timecodes.\n"
        "Ne rien ajouter ni modifier en dehors des traductions des textes en darija.\n"
        "Voici le texte à traduire :\n\n"
        f"{texte_a_traduire}"
    )

    # Création de l'objet StringIO
    output = io.StringIO()

    # Appel correct de la méthode generate_text
    response = model.generate_text(prompt)

    traduction = response.text.strip()
    output.write(traduction + "\n")
    output.seek(0)

    return StreamingResponse(output, media_type="text/plain", headers={
        "Content-Disposition": "attachment; filename=traduit.txt"
    })
