from analise import gerar_analises, carregar_dados
from graficos import gerar_graficos
from relatorio import gerar_relatorio
from evolucao import gerar_evolucao
from exportar_pdf import exportar_pdf


gerar_analises()

df = carregar_dados()
gerar_graficos(df)

print("\nRELATÓRIO AUTOMÁTICO DA JORNADA:\n")
print(gerar_relatorio())

gerar_evolucao()
exportar_pdf()
