import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import os 

# Função para criar o texto descritivo de cada linha
def criar_texto(vitima):
    return f"""
    Nome da Vítima: {vitima['Nome da Vitima']}
    Idade: {vitima['Idade']}
    Cor: {vitima['Cor']}
    Profissão: {vitima['Profissão']}
    Estado: {vitima['Estado']}
    Histórico: {vitima['Historico']}
    """

# Função para criar um PDF para cada vítima
def criar_pdfs(csv_file, output_dir, imagem_path):
    # Ler o arquivo CSV
    df = pd.read_csv(csv_file)

    # Estilos para o documento
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_title = styles['Title']

    # Tamanho máximo permitido para a imagem
    max_width = 100
    max_height = 100

    # Criar um PDF para cada linha no CSV
    for index, row in df.iterrows():
        # Definir o nome do arquivo PDF baseado no nome da vítima
        nome_arquivo = f"{output_dir}/{row['Nome da Vitima'].replace(' ', '_')}.pdf"

        # Cria o documento PDF
        doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
        story = []

        # Adicionar a imagem centralizada
        try:
            img = Image(imagem_path)
            img.hAlign = 'CENTER'

            # Redimensionar a imagem se for maior que o tamanho máximo permitido
            if img.imageWidth > max_width or img.imageHeight > max_height:
                img.drawWidth = max_width
                img.drawHeight = max_height * (img.imageHeight / img.imageWidth)
            story.append(img)
        except Exception as e:
            print(f"Erro ao adicionar imagem: {e}")

        story.append(Spacer(1, 12))

        # Adicionar o título
        story.append(Paragraph("Relatório da Vítima", style_title))
        story.append(Spacer(1, 12))

        # Adicionar o texto descritivo da vítima
        texto = f"""
        Este documento contém informações detalhadas sobre a vítima. Abaixo estão os detalhes fornecidos:

        <b>Nome da Vítima:</b> {row['Nome da Vitima']}
        <b>Idade:</b> {row['Idade']}
        <b>Cor:</b> {row['Cor']}
        <b>Profissão:</b> {row['Profissão']}
        <b>Estado:</b> {row['Estado']}
        <b>Histórico:</b> {row['Historico']}
        """
        story.append(Paragraph(texto, style_normal))

        # Construir o documento PDF
        doc.build(story)

# Definir os caminhos do arquivo CSV, do diretório de saída e da imagem
csv_file = '/content/drive/MyDrive/Dataset/output.csv'
output_dir = '/content/drive/MyDrive/Dataset'
imagem_path = '/content/drive/MyDrive/Dataset/hipotech.jpeg'

# Criar PDFs separados para cada vítima
criar_pdfs(csv_file, output_dir, imagem_path)