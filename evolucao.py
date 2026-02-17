import pandas as pd
import os
import matplotlib.pyplot as plt


def carregar_base():

    caminho = os.path.join(os.path.dirname(__file__), "dados", "mudanca_pessoal_periodos.csv")

    # tenta abrir com padrões diferentes
    try:
        df = pd.read_csv(caminho, sep=";", encoding="utf-8")
    except:
        df = pd.read_csv(caminho, sep=";", encoding="latin1")

    return df


def converter_periodo(df):

    mapa_meses = {
        "jan": "01", "fev": "02", "mar": "03", "abr": "04",
        "mai": "05", "jun": "06", "jul": "07", "ago": "08",
        "set": "09", "out": "10", "nov": "11", "dez": "12"
    }

    def traduzir_periodo(texto):

        if pd.isna(texto):
            return None

        try:
            mes, ano = texto.lower().split("/")
            mes_num = mapa_meses.get(mes[:3])

            if mes_num:
                return f"20{ano}-{mes_num}-01"

        except:
            return None

    df["periodo_convertido"] = df["periodo"].apply(traduzir_periodo)
    df["periodo_convertido"] = pd.to_datetime(df["periodo_convertido"], errors="coerce")

    return df


def gerar_evolucao():

    df = carregar_base()
    df = converter_periodo(df)

    mapa_impacto = {
        "muito negativo": -2,
        "negativo": -1,
        "neutro": 0,
        "positivo": 1,
        "muito positivo": 2
    }

    df["impacto_num"] = df["impacto"].str.lower().map(mapa_impacto)
    df["impacto_num"] = pd.to_numeric(df["impacto_num"], errors="coerce")

    evolucao = (
        df.groupby("periodo_convertido")["impacto_num"]
        .mean()
        .sort_index()
    )

    plt.figure()
    evolucao.plot(marker="o")
    plt.title("Evolução da Jornada Pessoal")
    plt.xlabel("Período")
    plt.ylabel("Impacto Médio")
    plt.grid(True)
    plt.show()
