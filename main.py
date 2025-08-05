from fastapi import FastAPI , UploadFile, File
from fastapi.responses import StreamingResponse
import requests
import json
import sys 
import io
# ...existing code...
app = FastAPI()

@app.get("/github_user") 
def get_github_user():
 url = "https://api.github.com/users/octocat"
 response= requests.get(url)
 return (response.json())

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API FastAPI"}
@app.post("/translate/")
async def translate_file(file: UploadFile = File(...)):
    contents = await file.read()
    lignes = contents.decode().splitlines()

    output = io.StringIO()  # Pour construire le fichier texte en mémoire

    for line in lignes:
        if line.strip() :  # Ignore les lignes vides
            traduction = line.strip()
            output.write(traduction + "\n")
        else:
            output.write("\n")  # Garde les lignes vides

    output.seek(0)  # Revenir au début du fichier pour l’envoi

    return StreamingResponse(output, media_type="text/plain", headers={
        "Content-Disposition": f"attachment; filename=traduit.txt"
    })