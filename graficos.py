import pandas as pd
import matplotlib.pyplot as plt


def gerar_graficos(df):

    # =========================
    # Distribuição por área
    # =========================
    contagem_area = df["area"].value_counts()

    contagem_area.plot(kind="bar")
    plt.title("Distribuição das Transformações por Área da Vida")
    plt.xlabel("Área")
    plt.ylabel("Quantidade")
    plt.show()


    # =========================
    # Impacto emocional
    # =========================
    contagem_impacto = df["impacto"].value_counts()

    contagem_impacto.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Distribuição do Impacto Emocional")
    plt.ylabel("")
    plt.show()


    # =========================
    # Intensidade média por área
    # =========================
    intensidade_media = df.groupby("area")["intensidade"].mean()

    intensidade_media.plot(kind="bar")
    plt.title("Intensidade Média das Transformações por Área")
    plt.xlabel("Área")
    plt.ylabel("Intensidade média")
    plt.show()
