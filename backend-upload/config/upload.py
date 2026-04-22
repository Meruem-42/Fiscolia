from fastapi import FastAPI, File, UploadFile


app = FastAPI()


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "message": "Fichier recu",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "status": "success",
    }