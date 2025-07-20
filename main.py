from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
import re

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read image from the uploaded file
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Use OCR to extract text from image
        text = pytesseract.image_to_string(image)
        print("Extracted text:", text)

        # Use regex to find two 8-digit numbers and multiply them
        match = re.search(r"(\d{8})\s*\*\s*(\d{8})", text)
        if not match:
            return JSONResponse(status_code=400, content={"error": "Could not detect a valid multiplication problem"})

        num1 = int(match.group(1))
        num2 = int(match.group(2))
        result = num1 * num2

        return {
            "answer": result,
            "email": "24ds2000059@ds.study.iitm.ac.in"
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
