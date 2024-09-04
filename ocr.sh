#!/bin/bash

# Lista de pastas de entrada
FOLDERS=("2017" "2018" "2019" "2020" "2021" "2022")

# Loop sobre cada pasta de entrada
for folder in "${FOLDERS[@]}"; do
  # Caminho para a pasta de entrada
  INPUT_DIR="Laudos/$folder"
  
  # Caminho para a pasta de saída
  OUTPUT_DIR="${folder}OCR"
  
  # Verifique se o diretório de saída existe, caso contrário, crie-o
  if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
  fi

  # Loop sobre todos os arquivos PDF na pasta de entrada
  for pdf_file in "$INPUT_DIR"/*.pdf; do
    # Extraia o nome do arquivo sem extensão
    base_name=$(basename "$pdf_file" .pdf)
    # Defina o caminho do arquivo de saída
    output_file="$OUTPUT_DIR/$base_name.pdf"
    # Aplique o OCR ao PDF
    ocrmypdf "$pdf_file" "$output_file"
  done

  echo "OCR concluído para a pasta $folder!"
done

echo "Processo de OCR concluído para todas as pastas!"
