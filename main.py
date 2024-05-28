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
    color = None
    profession = None
    state = None
    historico = None
    state_abbreviations = r'\b(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)\b'
    
    for i, line in enumerate(lines):
        #extrai o nome da vitima
        if "Nome da Vitima" in line:
            next_line = lines[i + 1].strip()
            name_match = re.match(r'^(.+?)\s+\d{2}/\d{2}/\d{4}', next_line)
            if name_match:
                name = name_match.group(1).strip()
                print(f"Found Name: {name}")

        #extrai a idade da vitima
        if "Idade" in line:
            next_line = lines[i + 1].strip()
            age_parts = next_line.split()
            age = next((age_part for age_part in age_parts if age_part.isdigit()), None)
            print(f"Found Age: {age}")

        #extrai a cor da vitima
        if "Cor" in line and color is None:
            next_line = lines[i + 1].strip()
            color_match = re.search(r'\b(BRANCA|PARDA|PRETA|AMARELA|INDÍGENA)\b', next_line, re.IGNORECASE)
            #após extrair a cor, extrai a profissão e o estado, caso existam
            if color_match:
                color = color_match.group(0).upper()
                print(f"Found Color: {color}")
                profession_start = color_match.end()
                profession_with_spaces = next_line[profession_start:].strip()
                profession_end = re.search(state_abbreviations, profession_with_spaces)
                if profession_end:
                    profession = profession_with_spaces[:profession_end.start()].strip()
                    state = profession_end.group(0).upper()
                    print(f"Found Profession: {profession}")
                    print(f"Found State: {state}")
                else:
                    profession = profession_with_spaces
                    print(f"Found Profession: {profession}")

        #extrai o historico da vitima, detalhando o que aconteceu
        if "Historico" in line:
            historico_lines = []
            for j in range(i + 1, len(lines)):
                if re.search(r'(Exame Externo|Descrição)', lines[j]):
                    break
                historico_lines.append(lines[j])
            historico = " ".join(historico_lines).strip()
            print(f"Found Historico: {historico}")
    
    return name, age, color, profession, state, historico

def save_to_csv(data, csv_path):
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Diretório onde os pdfs são armazenados
pdf_directory_path = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\pdfs"
# Caminho onde o CSV é armazenado
output_csv_path = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\output.csv"

# Inicializa CSV com cabeçalhos
with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nome da Vitima', 'Idade', 'Cor', 'Profissão', 'Estado', 'Historico'])

# Processa cada PDF dentro do diretório
for filename in os.listdir(pdf_directory_path):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory_path, filename)
        extracted_text = extract_info(pdf_path)
        victim_name, victim_age, victim_color, victim_profession, victim_state, victim_historico = parse_info(extracted_text)
        if all([victim_name, victim_age, victim_color, victim_profession, victim_state, victim_historico]):
            print(f"Saving: {victim_name}, {victim_age}, {victim_color}, {victim_profession}, {victim_state}, {victim_historico}")
            save_to_csv([victim_name, victim_age, victim_color, victim_profession, victim_state, victim_historico], output_csv_path)
        else:
            print(f"Failed to extract complete data from: {filename}")
            print(f"Missing data - Name: {victim_name}, Age: {victim_age}, Color: {victim_color}, Profession: {victim_profession}, State: {victim_state}, Historico: {victim_historico}")
