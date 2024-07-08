# project/pdf_processor.py
import fitz  # PyMuPDF
import io
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader

class PDFProcessor:
    def __init__(self, pdf_bytes):
        self.pdf_bytes = pdf_bytes
        self.document = fitz.open(stream=pdf_bytes, filetype="pdf")

    def extract_text(self):
        text_per_page = []
        for page_num in range(len(self.document)):
            page = self.document.load_page(page_num)
            text_per_page.append(page.get_text())
        return text_per_page

    def determine_type(self, page_text):
        return "TextBasedPDF" if page_text.strip() else "ScannedPDF"

    def classify_pdf(self):
        extracted_text_per_page = self.extract_text()
        result = []
        for page_num, page_text in enumerate(extracted_text_per_page, start=1):
            page_type = self.determine_type(page_text)
            result.append({
                "page_number": page_num,
                "file_type": page_type
            })
        return result

    def split_pdf_to_images(self, pages_per_split=15):
        reader = PdfReader(io.BytesIO(self.pdf_bytes))
        total_pages = len(reader.pages)
        num_files = (total_pages + pages_per_split - 1) // pages_per_split
        all_images_bytes = []
        for i in range(num_files):
            start_page = i * pages_per_split
            end_page = min(start_page + pages_per_split, total_pages)
            images = convert_from_bytes(self.pdf_bytes, first_page=start_page + 1, last_page=end_page)
            for image in images:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                all_images_bytes.append(img_byte_arr.getvalue())
            print(f"Part {i + 1} processed with pages from {start_page + 1} to {end_page}.")
        return all_images_bytes
