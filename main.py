from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

# Ensure the uploads directory exists
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    hobby: str = Form(...),
    hair: str = Form(...),
    singer: str = Form(...),
    body_count: int = Form(...),
    photo: UploadFile = File(...)
):
    try:
        # Save the uploaded photo
        photo_path = f"static/uploads/{photo.filename}"
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # Build response data
        response_data = {
            "request": request,
            "name": name,
            "age": age,
            "hobby": hobby,
            "hair": hair,
            "singer": singer,
            "body_count": body_count,
            "photo_path": f"/static/uploads/{photo.filename}",
        }
        
        # Check if user meets the criteria
        is_baddie = (body_count > 2 and 
                    hair.lower() == "red" and 
                    singer.lower() == "taylor swift")
        
        template = "success.html" if is_baddie else "failure.html"
        return templates.TemplateResponse(template, response_data)

    except Exception as e:
        return templates.TemplateResponse("failure.html", {
            "request": request,
            "error": str(e)
        })
