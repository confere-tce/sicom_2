import random
import os
import string
import shutil
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape, A4, A3, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

meses_extenso = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]    

def criar_pasta_temporaria():

    comprimento = 15
    pasta_temporaria = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(comprimento))
    pasta_temporaria = os.path.join('uploads', pasta_temporaria)
    os.mkdir(pasta_temporaria)

    return pasta_temporaria

def criar_pasta_tipo_arquivo(pasta_temp, tipo_arquivo):

    pasta_temporaria = os.path.join(pasta_temp, tipo_arquivo)
    os.mkdir(pasta_temporaria)

    return pasta_temporaria

def deletando_pasta(pasta):
    try:
        shutil.rmtree(pasta)
    except OSError as e:
        print(f"Error:{ e.strerror}")

def exportar_pdf(df, filename, formato, orientacao, percentual_tabela, tamanho_letra):
    # Validar o tamanho da página e a orientação (landscape ou portrait)
    tamanhos_validos = {
        "letter": (215.9, 279.4),
        "A4": (595.276, 841.890),  # Tamanho em pontos (A4)
        # Adicione mais tamanhos se necessário
    }

    if formato not in tamanhos_validos:
        raise ValueError("Tamanho de página inválido. Escolha entre 'letter', 'A4', ou adicione um tamanho válido.")

    if orientacao not in ["portrait", "landscape"]:
        raise ValueError("Orientação inválida. Escolha entre 'portrait' ou 'landscape'.")

    if not 0 < percentual_tabela <= 100:
        raise ValueError("O percentual da tabela deve estar entre 0 e 100.")

    if tamanho_letra <= 0:
        raise ValueError("O tamanho da fonte deve ser maior que 0.")
    
    # Calcular a altura mínima das linhas com base no tamanho da fonte
    altura_minima_linha = tamanho_letra * 1.2  # Ajuste o fator conforme necessário

    # Calcular a largura da tabela com base no percentual
    largura_tabela = (percentual_tabela / 100) * tamanhos_validos[formato][0]

    # Criar um buffer de bytes para armazenar o PDF
    buffer = BytesIO()

    # Criar um documento PDF
    if orientacao == "portrait":
        doc = SimpleDocTemplate(buffer, pagesize=(tamanhos_validos[formato][0], tamanhos_validos[formato][1]))
    else:
        doc = SimpleDocTemplate(buffer, pagesize=(tamanhos_validos[formato][1], tamanhos_validos[formato][0]))

    elements = []

    # Adicionar a tabela ao PDF
    table_data = [list(df.columns)] + df.values.tolist()
    for i in range(1, len(table_data)):
        for j in range(len(table_data[i])):
            # Formatar os valores para exibir "0,00" quando o resultado for 0
            if table_data[i][j] == 0:
                table_data[i][j] = "0,00"

            # Formatar o valor para "000.000,00"
            if isinstance(table_data[i][j], str) and '.' in table_data[i][j]:
                table_data[i][j] = '{:,.2f}'.format(float(table_data[i][j])).replace('.', ',')


    # Calcular a largura da célula da tabela
    table = Table(table_data, colWidths=[largura_tabela] * len(df.columns))

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.blue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), tamanho_letra),  # Ajuste o tamanho da fonte
        ('LEADING', (0, 0), (-1, -1), altura_minima_linha),  # Ajuste a altura mínima da linha
        ('SIZE', (0, 0), (-1, -1), tamanho_letra),  # Ajuste o tamanho da fonte
    ])
    table.setStyle(table_style)

    elements.append(table)

    doc.build(elements)

    # Mover o cursor para o início do buffer
    buffer.seek(0)

    # Salvar o PDF no arquivo
    with open(filename, "wb") as f:
        f.write(buffer.read())

def exportar_excel(df, filename):
    try:
        # Substituir pontos por vírgulas nos valores numéricos
        df.replace(r'\.', ',', regex=True, inplace=True)

        # Salvar o DataFrame em um arquivo Excel
        df.to_excel(filename, index=False)
        print(f'Relatório exportado com sucesso para {filename}')

    except Exception as e:
        print(f'Ocorreu um erro ao exportar para Excel: {str(e)}')


