import fitz  # PyMuPDF
import os
import base64
from PIL import Image
import io
from src.utils.config import RAW_PAPERS_DIR, RAW_IMAGES_DIR

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from each page of a PDF.
    Returns a list of dicts with page number and text.
    """
    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()

        if text:
            pages.append({
                "page_num": page_num + 1,
                "text": text,
                "source": os.path.basename(pdf_path)
            })

    doc.close()
    return pages


def extract_images_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract images from a PDF and save them to data/raw/images/.
    Returns a list of dicts with image path and source info.
    """
    doc = fitz.open(pdf_path)
    images = []
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Skip tiny images (icons, logos)
            image = Image.open(io.BytesIO(image_bytes))
            width, height = image.size
            if width < 100 or height < 100:
                continue

            # Save image
            image_filename = f"{pdf_name}_page{page_num + 1}_img{img_index}.{image_ext}"
            image_path = os.path.join(RAW_IMAGES_DIR, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            images.append({
                "image_path": image_path,
                "page_num": page_num + 1,
                "source": os.path.basename(pdf_path)
            })

    doc.close()
    return images


def parse_pdf(pdf_path: str) -> dict:
    """
    Full pipeline: extract text and images from a PDF.
    Returns dict with pages and images.
    """
    print(f"Parsing: {os.path.basename(pdf_path)}")
    pages = extract_text_from_pdf(pdf_path)
    images = extract_images_from_pdf(pdf_path)

    print(f"  Pages extracted: {len(pages)}")
    print(f"  Images extracted: {len(images)}")

    return {
        "source": os.path.basename(pdf_path),
        "pages": pages,
        "images": images
    }


def parse_all_pdfs() -> list[dict]:
    """
    Parse all PDFs in data/raw/papers/.
    Returns list of parsed results.
    """
    results = []
    pdf_files = [f for f in os.listdir(RAW_PAPERS_DIR) if f.endswith(".pdf")]

    print(f"Found {len(pdf_files)} PDFs to parse\n")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(RAW_PAPERS_DIR, pdf_file)
        result = parse_pdf(pdf_path)
        results.append(result)

    print(f"\nDone. Parsed {len(results)} PDFs total.")
    return results