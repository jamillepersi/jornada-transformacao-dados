import pandas as pd
import os


def gerar_relatorio():

    # ===============================
    # LOCALIZAR ARQUIVO COM SEGURANÇA
    # ===============================
    caminho = os.path.join(
        os.path.dirname(__file__),
        "dados",
        "mudanca_pessoal_periodos.csv"
    )

    if not os.path.exists(caminho):
        return "\n⚠ Arquivo de dados não encontrado na pasta /dados"

    # ===============================
    # LER CSV (compatível com Excel)
    # ===============================
    try:
      df = pd.read_csv(caminho, sep=",", encoding="utf-8")
    except:
      try:
        df = pd.read_csv(caminho, sep=";", encoding="latin1")
      except:
        df = pd.read_csv(caminho, sep=";", encoding="latin1", on_bad_lines="skip")


    # ===============================
    # MAPEAR IMPACTO PARA NÚMEROS
    # ===============================
    mapa_impacto = {
        "muito negativo": -2,
        "negativo": -1,
        "neutro": 0,
        "positivo": 1,
        "muito positivo": 2
    }

    if "impacto" in df.columns:
        df["impacto_num"] = (
            df["impacto"]
            .astype(str)
            .str.lower()
            .map(mapa_impacto)
        )
        df["impacto_num"] = pd.to_numeric(df["impacto_num"], errors="coerce")

    # ===============================
    # IMPACTO POR ÁREA
    # ===============================
    impacto_area = None
    if "area" in df.columns and "impacto_num" in df.columns:
        impacto_area = (
            df.groupby("area")["impacto_num"]
            .mean()
            .sort_values(ascending=False)
        )

    # ===============================
    # FASES MAIS FREQUENTES
    # ===============================
    fases_freq = None
    if "fase" in df.columns:
        fases_freq = df["fase"].value_counts()

    # ===============================
    # CONSTRUIR RELATÓRIO
    # ===============================
    relatorio = "\nRELATÓRIO AUTOMÁTICO DA JORNADA\n"
    relatorio += "-" * 40 + "\n"

    # ---- IMPACTO ----
    if impacto_area is not None:
        relatorio += "\nÁreas com maior impacto positivo:\n"
        for area, valor in impacto_area.items():
            relatorio += f"- {area}: {valor:.2f}\n"

    # ---- FASES ----
    if fases_freq is not None:
        relatorio += "\nFases mais registradas:\n"
        for fase, qtd in fases_freq.items():
            relatorio += f"- {fase}: {qtd} registros\n"

    # ===============================
    # PARTE REFLEXIVA (AUTOCONHECIMENTO)
    # ===============================
    relatorio += "\nLeitura Reflexiva:\n"

    if impacto_area is not None and len(impacto_area) > 0:
        melhor_area = impacto_area.idxmax()
        pior_area = impacto_area.idxmin()

        relatorio += (
            f"\n• A área com maior crescimento percebido foi '{melhor_area}'. "
            "Esse campo pode estar funcionando como fonte de fortalecimento pessoal.\n"
        )

        relatorio += (
            f"• A área '{pior_area}' apresentou menor impacto médio. "
            "Pode indicar espaço de cuidado, reavaliação ou desenvolvimento interno.\n"
        )

    if fases_freq is not None and len(fases_freq) > 0:
        fase_principal = fases_freq.idxmax()

        relatorio += (
            f"• A fase mais vivenciada foi '{fase_principal}'. "
            "Isso sugere o momento predominante do seu ciclo de transformação atual.\n"
        )

    relatorio += (
        "\nEste relatório representa um retrato quantitativo e simbólico da jornada registrada. "
        "Os dados mostram tendências, mas o significado real emerge da reflexão consciente sobre "
        "suas experiências e escolhas.\n"
    )

    return relatorio
