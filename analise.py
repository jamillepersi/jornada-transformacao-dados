import pandas as pd

def carregar_dados():
    df = pd.read_csv("dados/mudanca_pessoal_periodos.csv", sep=";", encoding="latin-1")
    return df

def intensidade_por_area(df):
    resultado = df.groupby("area")["intensidade"].mean().sort_values(ascending=False)
    return resultado

def contagem_impacto(df):
    resultado = df["impacto"].value_counts()
    return resultado

def intensidade_por_fase(df):
    resultado = df.groupby("fase")["intensidade"].mean().sort_values(ascending=False)
    return resultado

def intensidade_por_periodo(df):
    resultado = df.groupby("periodo")["intensidade"].mean()
    return resultado

def gerar_analises():
    df = carregar_dados()

    analises = {
        "intensidade_area": intensidade_por_area(df),
        "impactos": contagem_impacto(df),
        "intensidade_fase": intensidade_por_fase(df),
        "intensidade_periodo": intensidade_por_periodo(df)
    }

    return analises
