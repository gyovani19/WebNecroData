import PyPDF2
import csv
import os
import re

def extract_info(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        for i in range(num_pages):
            page = reader.pages[i]
            text += page.extract_text()
        return text

def parse_info(text):
    lines = text.split('\n')
    name = None
    age = None
    for i, line in enumerate(lines):
        if "Nome da Vitima" in line:
            # Extract the name, which is followed by a date in the format dd/mm/yyyy
            next_line = lines[i+1].strip()
            name = re.split(r'\s\d{2}/\d{2}/\d{4}', next_line)[0]  # Split at the date and take the first part
        if "Idade" in line:
            # Extract the age as a digit from the next line
            next_line = lines[i+1].strip()
            age_parts = next_line.split()
            age = next(age_part for age_part in age_parts if age_part.isdigit())
    return name, age

def save_to_csv(data, csv_path):
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Directory where PDF files are stored
pdf_directory_path = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\pdfs"
# Path where you want to save the CSV
output_csv_path = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\output.csv"

# Initialize CSV with headers
with open(output_csv_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Nome da Vitima', 'Idade'])

# Process each PDF in the directory
for filename in os.listdir(pdf_directory_path):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory_path, filename)
        extracted_text = extract_info(pdf_path)
        victim_name, victim_age = parse_info(extracted_text)
        if victim_name and victim_age:
            save_to_csv([victim_name, victim_age], output_csv_path)
