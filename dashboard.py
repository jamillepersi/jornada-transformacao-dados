import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt


st.title("🌿 Dashboard da Jornada de Transformação")


# -----------------------------
# carregar base
# -----------------------------

caminho = os.path.join("dados", "mudanca_pessoal_periodos.csv")

try:
    df = pd.read_csv(caminho, sep=";", encoding="utf-8")
except:
    df = pd.read_csv(caminho, sep=";", encoding="latin1")


# -----------------------------
# converter impacto
# -----------------------------

mapa_impacto = {
    "muito negativo": -2,
    "negativo": -1,
    "neutro": 0,
    "positivo": 1,
    "muito positivo": 2
}

df["impacto_num"] = df["impacto"].str.lower().map(mapa_impacto)


# -----------------------------
# filtros interativos
# -----------------------------

st.sidebar.header("Filtros")

area = st.sidebar.multiselect(
    "Área",
    options=df["area"].unique(),
    default=df["area"].unique()
)

fase = st.sidebar.multiselect(
    "Fase",
    options=df["fase"].unique(),
    default=df["fase"].unique()
)

df_filtrado = df[
    (df["area"].isin(area)) &
    (df["fase"].isin(fase))
]


# -----------------------------
# métricas rápidas
# -----------------------------

st.subheader("Resumo Geral")

st.metric(
    "Impacto Médio",
    round(df_filtrado["impacto_num"].mean(), 2)
)

st.metric(
    "Total de Registros",
    len(df_filtrado)
)


# -----------------------------
# gráfico impacto por área
# -----------------------------

st.subheader("Impacto por Área")

impacto_area = df_filtrado.groupby("area")["impacto_num"].mean()

fig, ax = plt.subplots()
impacto_area.plot(kind="bar", ax=ax)
st.pyplot(fig)


# -----------------------------
# gráfico fases
# -----------------------------

st.subheader("Distribuição das Fases")

fase_count = df_filtrado["fase"].value_counts()

fig2, ax2 = plt.subplots()
fase_count.plot(kind="bar", ax=ax2)
st.pyplot(fig2)

st.subheader("Linha do Tempo do Impacto")

# converter período
df_filtrado["periodo_data"] = pd.to_datetime(
    df_filtrado["periodo"],
    format="%b/%y",
    errors="coerce"
)

impacto_periodo = (
    df_filtrado.groupby("periodo_data")["impacto_num"]
    .mean()
    .sort_index()
)

fig3, ax3 = plt.subplots()
impacto_periodo.plot(marker="o", ax=ax3)
st.pyplot(fig3)

import numpy as np

st.subheader("Equilíbrio das Áreas da Vida")

impacto_area = (
    df_filtrado.groupby("area")["impacto_num"]
    .mean()
    .sort_values()
)

categorias = impacto_area.index.tolist()
valores = impacto_area.values.tolist()

# fechar o círculo
categorias += [categorias[0]]
valores += [valores[0]]

angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=True)

fig4, ax4 = plt.subplots(subplot_kw=dict(polar=True))
ax4.plot(angulos, valores)
ax4.fill(angulos, valores, alpha=0.2)

ax4.set_xticks(angulos[:-1])
ax4.set_xticklabels(impacto_area.index)

st.pyplot(fig4)

st.subheader("Leitura Reflexiva da Jornada")

# Área mais fortalecida
area_top = impacto_area.idxmax()
area_fragil = impacto_area.idxmin()

fase_top = df_filtrado["fase"].value_counts().idxmax()

st.markdown(f"""
### 🌿 Interpretação dos Dados

• A área com maior fortalecimento atual é **{area_top}**.  
Isso pode indicar uma base de sustentação emocional ou prática neste momento da sua jornada.

• A área com menor impacto médio é **{area_fragil}**.  
Pode representar um espaço de cuidado, revisão de prioridades ou amadurecimento interno.

• A fase mais vivenciada é **{fase_top}**.  
Essa predominância sugere o ciclo principal que você está atravessando atualmente.

---

✨ Os gráficos mostram padrões.  
✨ O significado nasce quando você relaciona esses padrões com sua história e suas escolhas.
""")
