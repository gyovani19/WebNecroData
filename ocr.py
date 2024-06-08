import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from pdf2image.exceptions import PDFPageCountError

# Configuração do caminho do Tesseract (necessário para Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang='por')  # Define o idioma para português se necessário

def convert_pdf_to_ocr(pdf_path, output_path):
    try:
        # Ler o PDF e converter em imagens
        images = convert_from_path(pdf_path)
        
        # Criar um novo PDF para o texto extraído
        c = canvas.Canvas(output_path, pagesize=letter)
        
        for img in images:
            # Extrair texto da imagem
            text = extract_text_from_image(img)
            
            # Adicionar uma nova página com o texto extraído
            c.drawString(10, 750, text)
            c.showPage()
        
        # Salvar o PDF final
        c.save()
        print(f"Processado com sucesso: {pdf_path}")
    except PDFPageCountError as e:
        print(f"Erro ao processar {pdf_path}: {str(e)}")

def process_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, filename)
            convert_pdf_to_ocr(input_pdf_path, output_pdf_path)

# Exemplo de uso
input_folder = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\pdfs"
output_folder = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\pdfs-ocr"

process_pdfs_in_folder(input_folder, output_folder)
