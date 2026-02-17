from fpdf import FPDF
from relatorio import gerar_relatorio


def limpar_texto(texto):
    """
    Remove caracteres que o FPDF não suporta
    """

    substituicoes = {
        "•": "-",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-"
    }

    for original, novo in substituicoes.items():
        texto = texto.replace(original, novo)

    return texto


def exportar_pdf():

    texto = gerar_relatorio()
    texto = limpar_texto(texto)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for linha in texto.split("\n"):
        pdf.multi_cell(0, 8, linha.encode("latin-1", "ignore").decode("latin-1"))

    pdf.output("Relatorio_Jornada_Transformacao.pdf")

    print("PDF gerado com sucesso!")
