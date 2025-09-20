# ===== INÍCIO DO CÓDIGO 100% CORRIGIDO =====
import subprocess
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

print("--- INICIANDO SCRIPT DE GERAÇÃO DE DADOS ---")

NOME_DO_ARQUIVO = "notas.csv"

try:
    # --- CORREÇÃO FINAL: Adicionamos decimal=',' para entender números como 7,9 ---
    # Também garantimos que o separador de colunas é ';'
    df = pd.read_csv(NOME_DO_ARQUIVO, encoding='utf-8-sig', sep=';', decimal=',')
    
    print(f"Arquivo '{NOME_DO_ARQUIVO}' carregado com sucesso.")
    print("Colunas encontradas:", df.columns.tolist())

except FileNotFoundError:
    print(f"ERRO FATAL: O arquivo '{NOME_DO_ARQUIVO}' não foi encontrado na pasta.")
    sys.exit()
except Exception as e:
    print(f"Ocorreu um erro crítico ao ler o arquivo: {e}")
    sys.exit()

# Validação das colunas para evitar o KeyError
colunas_necessarias = ['Turma', 'Nota_Matematica', 'Acesso_Internet', 'Genero']
for col in colunas_necessarias:
    if col not in df.columns:
        print(f"ERRO FATAL: A coluna obrigatória '{col}' não foi encontrada no arquivo.")
        sys.exit()

# 1. Gerar e salvar TODOS os gráficos
print("Gerando gráficos...")
plt.figure()
sns.histplot(df['Nota_Matematica'], kde=True, bins=10).set_title('Distribuição Geral das Notas')
plt.savefig('histograma_notas.png')
plt.close()

plt.figure()
sns.boxplot(x='Turma', y='Nota_Matematica', data=df).set_title('Notas por Turma')
plt.savefig('boxplot_turmas.png')
plt.close()

plt.figure()
sns.countplot(x='Acesso_Internet', data=df).set_title('Acesso à Internet dos Alunos')
plt.savefig('acesso_internet.png')
plt.close()

plt.figure()
df['Genero'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('husl'))
plt.title('Distribuição por Gênero')
plt.ylabel('')
plt.savefig('distribuicao_genero.png')
plt.close()

# ESTES ERAM OS GRÁFICOS QUE ESTAVAM FALTANDO
plt.figure()
sns.kdeplot(data=df, x='Nota_Matematica', hue='Acesso_Internet', fill=True).set_title('Desempenho vs. Acesso à Internet')
plt.savefig('densidade_internet.png')
plt.close()

plt.figure()
sns.violinplot(x='Genero', y='Nota_Matematica', data=df).set_title('Desempenho por Gênero')
plt.savefig('violino_genero.png')
plt.close()
print("Gráficos gerados com sucesso.")

# 2. Preparar os dados de texto para o JSON
print("Analisando dados para o JSON...")
estatisticas = df['Nota_Matematica'].describe().to_dict()
std_dev = df['Nota_Matematica'].std()

if std_dev < 2.0:
    categoria = 'Homogêneo'
    recomendacoes = 'O desempenho dos alunos é bastante consistente. Para elevar o nível geral, foque em aprofundar os conceitos fundamentais e em atividades práticas.'
elif std_dev > 3.5:
    categoria = 'Polarizado'
    recomendacoes = 'Grande disparidade de desempenho. Implemente a diferenciação pedagógica, com atividades distintas para cada grupo e crie grupos de tutoria.'
else:
    categoria = 'Heterogêneo'
    recomendacoes = 'Desempenho variado. Monitore continuamente para identificar padrões e flexibilize as estratégias de ensino para atender a diferentes ritmos.'

# 3. Montar e salvar o arquivo JSON final
dados_para_app = {
    "titulo": "Análise de Desempenho dos Alunos",
    "estatisticas_gerais": estatisticas,
    "perfil_da_turma": {
        "categoria": categoria,
        "recomendacoes": recomendacoes
    },
    "graficos": [
        {"titulo": "Distribuição Geral das Notas", "arquivo": "histograma_notas.png"},
        {"titulo": "Notas por Turma", "arquivo": "boxplot_turmas.png"},
        {"titulo": "Acesso à Internet dos Alunos", "arquivo": "acesso_internet.png"},
        {"titulo": "Distribuição por Gênero", "arquivo": "distribuicao_genero.png"},
        {"titulo": "Desempenho vs. Acesso à Internet", "arquivo": "densidade_internet.png"},
        {"titulo": "Desempenho por Gênero", "arquivo": "violino_genero.png"}
    ]
}

# ESTE ERA O ARQUIVO QUE ESTAVA FALTANDO
with open('analise_resultados.json', 'w', encoding='utf-8') as f:
    json.dump(dados_para_app, f, ensure_ascii=False, indent=4)

print("Arquivo 'analise_resultados.json' gerado com sucesso.")
print("\n--- SUCESSO! Todos os 7 arquivos para o aplicativo foram criados na pasta 'ProjetoFinal'. ---")
# ===== FIM DO CÓDIGO 100% CORRIGIDO =====