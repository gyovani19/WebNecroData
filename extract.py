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

def normalize_text(text):
    # Normaliza o texto, substituindo cedilhas e acentos por versões simples
    normalized_text = text.replace('ç', 'c').replace('Ç', 'C').replace('é', 'e').replace('É', 'E').replace('í', 'i').replace('Í', 'I').replace('ó', 'o').replace('Ó', 'O').replace('ú', 'u').replace('Ú', 'U').replace('ã', 'a').replace('Ã', 'A').replace('õ', 'o').replace('Õ', 'O').replace('â', 'a').replace('Â', 'A').replace('ê', 'e').replace('Ê', 'E').replace('ô', 'o').replace('Ô', 'O')
    return normalized_text

def extract_instrucao(lines, index):
    instrucao = None
    possible_instructions = ["FUND.INCOMPLETO", "FUND.COMPLETO","1° Grau Completo","2° Grau Completo" "MED.COMPLETO", "NÉD.COMPLETO", "MÉD.COMPLETO", "NÉD.COMPLETO ","SUP.INCOMPLETO ","SUP. INCOMPLETO ""SUP.COMPLETO","NÃO ALFABETIZADO","IGNORADO", "2º  Grau  InCompleto  "]  # Adicione aqui outros tipos de instrução conforme necessário
    
    for i in range(index + 1, len(lines)):  # Começa da linha seguinte ao índice
        line = lines[i].strip()
        for instruction in possible_instructions:
            if instruction in line:
                if instruction in ["NÉD.COMPLETO", "MÉD.COMPLETO", "NÉD.COMPLETO "]:
                    instrucao = "MED.COMPLETO"
                else:
                    instrucao = instruction
                break
        if instrucao:
            break
    else:
        instrucao = "INDEFINIDO/ANALFABETO"
    return instrucao

def parse_info(text):
    lines = text.split('\n')
    name = None
    age = None
    color = None
    profession = None
    state = None
    historico = None
    instrucao = None
    tipo_laudo = None  # Variável para armazenar o tipo de laudo
    state_abbreviations = r'\b(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)\b'
    
    for i, line in enumerate(lines):
        # Extrai o nome da vítima
        if "Nome da Vitima" in line:
            next_line = lines[i + 1].strip()
            name_match = re.match(r'^(.+?)\s+\d{2}/\d{2}/\d{4}', next_line)
            if name_match:
                name = name_match.group(1).strip()

        # Extrai a idade da vítima
        if "Idade" in line:
            next_line = lines[i + 1].strip()
            age_parts = next_line.split()
            age = next((age_part for age_part in age_parts if age_part.isdigit()), None)

        if "Cor" in line and color is None:
            next_line = lines[i + 1].strip()
            color_match = re.search(r'\b(BRANCA|PARDA|PRETA|AMARELA|INDÍGENA|IGNORADO|IGNORADA)\b', next_line, re.IGNORECASE)
            if color_match:
                color = color_match.group(0).upper()
                profession_start = color_match.end()
                profession_with_spaces = next_line[profession_start:].strip()
        
        # Verifica se a profissão está definida como "MASCULINO IGNORADO IGNORADO"
                if re.match(r'MASCULINO IGNORADO IGNORADO|', profession_with_spaces, re.IGNORECASE):
                    profession = "IGNORADO"
                else:
                    profession_end = re.search(state_abbreviations, profession_with_spaces)
                    if profession_end:
                        profession = profession_with_spaces[:profession_end.start()].strip()
                        state = profession_end.group(0).upper()


        # Extrai o histórico da vítima, detalhando o que aconteceu
        if "Historico" in line:
            historico_lines = []
            for j in range(i + 1, len(lines)):
                if re.search(r'(Exame Externo|Descrição)', lines[j]):
                    break
                historico_lines.append(lines[j])
            historico = " ".join(historico_lines).strip()

        # Extrai a instrução da vítima
        if re.search(r'Instr[uú][çc][aã]o|Instrug[aá]o|Instru[cç][aã]o', line, re.IGNORECASE):
            instrucao = extract_instrucao(lines, i)

    # Verifica o tipo de laudo no final do processamento
    for line in lines:
        if "CADAVERICO" in line.upper():
            tipo_laudo = "CADAVERICO"
            break
    else:
        tipo_laudo = "NÃO CADAVERICO"

    return name, age, color, profession, state, historico, instrucao, tipo_laudo

def save_to_csv(data, csv_path):
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Diretório onde os PDFs são armazenados
pdf_directory_path = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\pdfs-ocr\2021"
# Caminho onde o CSV é armazenado
output_csv_path = r"C:\Users\gyova\OneDrive\Programas\GitHub\WebNecroData\output2021.csv"

# Inicializa CSV com cabeçalhos se o arquivo não existir
if not os.path.exists(output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Ano', 'Nome do Arquivo', 'Tipo de Laudo', 'Nome da Vitima', 'Idade', 'Cor', 'Profissão', 'Estado', 'Historico', 'Instrução'])

# Processa cada PDF dentro do diretório
for filename in os.listdir(pdf_directory_path):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory_path, filename)
        extracted_text = extract_info(pdf_path)
        normalized_text = normalize_text(extracted_text)
        victim_name, victim_age, victim_color, victim_profession, victim_state, victim_historico, victim_instrucao, tipo_laudo = parse_info(normalized_text)
        print(f"Saving: 2021, {filename}, {victim_name}, {victim_age}, {victim_color}, {victim_profession}, {victim_state}, {victim_historico}, {victim_instrucao}, {tipo_laudo}")
        save_to_csv(['2021', filename, tipo_laudo, victim_name, victim_age, victim_color, victim_profession, victim_state, victim_historico, victim_instrucao], output_csv_path)
        if not all([victim_name, victim_age, victim_color, victim_profession, victim_state, victim_historico, victim_instrucao, tipo_laudo]):
            print(f"Failed to extract complete data from: {filename}")
            print(f"Missing data - Name: {victim_name}, Age: {victim_age}, Color: {victim_color}, Profession: {victim_profession}, State: {victim_state}, Historico: {victim_historico}, Instrução: {victim_instrucao}, Tipo de Laudo: {tipo_laudo}")
