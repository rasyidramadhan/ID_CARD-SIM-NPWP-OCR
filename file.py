from pdf2image import convert_from_path
import os

def PDF_IMAGES(pdf_path, out_dir):
    pages = convert_from_path(pdf_path, dpi=500)
    image_paths = []

    for i, page in enumerate(pages):
        if page.mode != "RGB":
            page = page.convert("RGB")

        img_path = os.path.join(out_dir, f"page_{i}.jpg")
        page.save(img_path)
        image_paths.append(img_path)

    return image_paths