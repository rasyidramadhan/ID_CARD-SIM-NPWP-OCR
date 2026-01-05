from fastapi import FastAPI, HTTPException, UploadFile, File
from docs_ocr import ktp, sim, npwp
from file import PDF_IMAGES
import os, time, shutil, json



try:
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(use_angle_cls=True, lang='id', show_log=False, use_textline_orientation=True,
            # det_model_dir = Your detection model path,
            # rec_model_dir = Your recognition model path
            )
    
    app = FastAPI(title="OCR API - Rasyid 2026")
    file_extensions = [".jpg", ".jpeg", ".png", ".pdf"]

except Exception as e:
    print("Error initializing Module:", e)
    ModuleNotFoundError("Module is not found")

def file_initialize(upload_file: UploadFile, file_extensions):
    file_name = upload_file.filename
    name_part, extension = os.path.splitext(file_name)
    extension = extension.lower()

    if extension not in file_extensions:
        raise HTTPException(400, "Invalid file type")

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    file_path = os.path.join("uploads", file_name)
    final_name_part = os.path.splitext(os.path.basename(file_path))[0]
    json_path = os.path.join("results", f"{final_name_part}.json")

    with open(file_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

    if extension == ".pdf":
        image_path = PDF_IMAGES(file_path, "uploads")
        
        if not image_path:
            raise HTTPException(400, "Failed to convert PDF to images")
        
        image_path = image_path[0]
    else:
        image_path = file_path

    return image_path, json_path

@app.get("/")
def home():
    return {"message": "Welcome to OCR API"}

@app.post("/KTP")
def ktp_ocr(file: UploadFile = File(...)):
    image_path, json_path = file_initialize(file, file_extensions)
    start_time = time.time()
    result = ocr.ocr(image_path, cls=True)
    texts = [line[1][0] for line in result[0]]
    data = ktp(texts)
    processing_time = round(time.time() - start_time, 2)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f'| File name: {file.filename} | Time: {processing_time} s | save as: {json_path} |')

    return data

@app.post("/SIM")
def sim_ocr(file: UploadFile = File(...)):
    image_path, json_path = file_initialize(file, file_extensions)
    start_time = time.time()
    result = ocr.ocr(image_path, cls=True)
    texts = [line[1][0] for line in result[0]]
    data = sim(texts)
    processing_time = round(time.time() - start_time, 2)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f'File name: {file.filename} | Time: {processing_time} s | save as: {json_path}')

    return data

@app.post("/NPWP")
def npwp_ocr(file: UploadFile = File(...)):
    image_path, json_path = file_initialize(file, file_extensions)
    start_time = time.time()
    result = ocr.ocr(image_path, cls=True)
    texts = [line[1][0] for line in result[0]]
    data = npwp(texts)
    processing_time = round(time.time() - start_time, 2)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f'File name: {file.filename} | Time: {processing_time} s | save as: {json_path}')

    return data

@app.delete("/delete-file")
def delete_file(file_name: str):
    if not os.path.exists(f"uploads/{file_name}"):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        os.remove(f"uploads/{file_name}")
        return {"message": f"File '{file_name}' has been deleted."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error deleting file: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=2000, reload=True)