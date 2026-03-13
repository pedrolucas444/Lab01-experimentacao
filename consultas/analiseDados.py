import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from pathlib import Path

# Configuração dos gráficos
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (10, 6)

# Caminhos
DATA_PATH = Path(__file__).parent.parent / "data" / "repos_1000.csv"
OUTPUT_PATH = Path(__file__).parent.parent / "graficos"


# =========================
# Carregamento e preparo
# =========================

def carregar_dados():
    print("📂 Carregando dados...")
    
    # Verificar se o arquivo existe
    if not DATA_PATH.exists():
        print(f"❌ Arquivo não encontrado: {DATA_PATH}")
        print("Execute primeiro o coletarRepositorios.py")
        return None
    
    df = pd.read_csv(DATA_PATH)
    
    print(f"✅ Dados carregados: {len(df)} repositórios")
    print(f"📋 Colunas disponíveis: {df.columns.tolist()}")
    
    # CORREÇÃO: Usar datetime com timezone UTC
    hoje = datetime.now(timezone.utc)
    
    # Converter datas - REMOVENDO o timezone pra ficar compatível
    df["createdAt"] = pd.to_datetime(df["createdAt"]).dt.tz_localize(None)
    df["updatedAt"] = pd.to_datetime(df["updatedAt"]).dt.tz_localize(None)
    
    # Calcular métricas
    df["idade_anos"] = (hoje.replace(tzinfo=None) - df["createdAt"]).dt.days / 365.25
    df["dias_desde_update"] = (hoje.replace(tzinfo=None) - df["updatedAt"]).dt.days
    
    # Total de issues (abertas + fechadas)
    df["total_issues"] = df["openIssues"] + df["closedIssues"]
    
    # CORREÇÃO: Criar coluna como float64 desde o início
    df["percentual_issues_fechadas"] = 0.0  # Agora é float
    
    # Percentual de issues fechadas (evitar divisão por zero)
    mask = df["total_issues"] > 0
    df.loc[mask, "percentual_issues_fechadas"] = (
        df.loc[mask, "closedIssues"] / df.loc[mask, "total_issues"] * 100
    ).astype(float)  # Garantir que é float
    
    return df


# =========================
# RQ01 - Sistemas populares são maduros?
# =========================

def rq01_idade_repos(df):
    print("\n" + "="*50)
    print("RQ01 — Idade dos repositórios")
    print("="*50)
    
    print(f"Média: {df['idade_anos'].mean():.2f} anos")
    print(f"Mediana: {df['idade_anos'].median():.2f} anos")
    print(f"Mínimo: {df['idade_anos'].min():.2f} anos")
    print(f"Máximo: {df['idade_anos'].max():.2f} anos")

    plt.figure()
    plt.hist(df["idade_anos"], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel("Idade (anos)")
    plt.ylabel("Número de repositórios")
    plt.title("RQ01 — Distribuição da Idade dos Repositórios")
    plt.grid(True, alpha=0.3)
    
    output_file = OUTPUT_PATH / "rq01_idade.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"📊 Gráfico salvo: {output_file}")


# =========================
# RQ02 - Sistemas populares recebem contribuições externas?
# =========================

def rq02_pull_requests(df):
    print("\n" + "="*50)
    print("RQ02 — Pull Requests Aceitas (Merged)")
    print("="*50)
    
    print(f"Média: {df['mergedPRs'].mean():.0f}")
    print(f"Mediana: {df['mergedPRs'].median():.0f}")
    print(f"Mínimo: {df['mergedPRs'].min()}")
    print(f"Máximo: {df['mergedPRs'].max()}")

    plt.figure()
    
    # Filtrar apenas repositórios com PRs > 0 para melhor visualização
    df_com_prs = df[df['mergedPRs'] > 0]
    
    plt.hist(df_com_prs["mergedPRs"], bins=50, edgecolor='black', alpha=0.7)
    plt.yscale("log")
    plt.xlabel("Número de PRs aceitas")
    plt.ylabel("Repositórios (escala log)")
    plt.title("RQ02 — Distribuição de Pull Requests Aceitas")
    plt.grid(True, alpha=0.3)
    
    output_file = OUTPUT_PATH / "rq02_prs.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"📊 Gráfico salvo: {output_file}")
    
    # Percentual de repositórios sem PRs
    sem_prs = (df['mergedPRs'] == 0).sum()
    print(f"Repositórios sem PRs: {sem_prs} ({sem_prs/len(df)*100:.1f}%)")


# =========================
# RQ03 - Sistemas populares são atualizados com frequência?
# =========================

def rq03_releases(df):
    print("\n" + "="*50)
    print("RQ03 — Número de Releases")
    print("="*50)
    
    print(f"Média: {df['releases'].mean():.1f}")
    print(f"Mediana: {df['releases'].median():.0f}")
    print(f"Mínimo: {df['releases'].min()}")
    print(f"Máximo: {df['releases'].max()}")

    plt.figure()
    
    # Filtrar apenas repositórios com releases > 0
    df_com_releases = df[df['releases'] > 0]
    
    plt.hist(df_com_releases["releases"], bins=50, edgecolor='black', alpha=0.7)
    plt.yscale("log")
    plt.xlabel("Número de releases")
    plt.ylabel("Repositórios (escala log)")
    plt.title("RQ03 — Distribuição de Releases")
    plt.grid(True, alpha=0.3)
    
    output_file = OUTPUT_PATH / "rq03_releases.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"📊 Gráfico salvo: {output_file}")
    
    # Repositórios sem releases
    sem_releases = (df['releases'] == 0).sum()
    print(f"Repositórios sem releases: {sem_releases} ({sem_releases/len(df)*100:.1f}%)")


# =========================
# RQ04 - Sistemas populares são atualizados com frequência?
# =========================

def rq04_atualizacao(df):
    print("\n" + "="*50)
    print("RQ04 — Tempo desde última atualização")
    print("="*50)
    
    print(f"Média: {df['dias_desde_update'].mean():.0f} dias")
    print(f"Mediana: {df['dias_desde_update'].median():.0f} dias")
    print(f"Mínimo: {df['dias_desde_update'].min():.0f} dias")
    print(f"Máximo: {df['dias_desde_update'].max():.0f} dias")

    plt.figure()
    plt.hist(df["dias_desde_update"], bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel("Dias desde última atualização")
    plt.ylabel("Número de repositórios")
    plt.title("RQ04 — Tempo desde a Última Atualização")
    plt.grid(True, alpha=0.3)
    
    output_file = OUTPUT_PATH / "rq04_update.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"📊 Gráfico salvo: {output_file}")
    
    # Repositórios atualizados recentemente (últimos 30 dias)
    recentes = (df['dias_desde_update'] <= 30).sum()
    print(f"Atualizados nos últimos 30 dias: {recentes} ({recentes/len(df)*100:.1f}%)")


# =========================
# RQ05 - Quais as linguagens mais populares?
# =========================

def rq05_linguagens(df):
    print("\n" + "="*50)
    print("RQ05 — Linguagens mais usadas")
    print("="*50)
    
    # Contar linguagens
    linguagens = df["primaryLanguage"].fillna("None").value_counts()
    
    print("\nTop 10 linguagens:")
    for lang, count in linguagens.head(10).items():
        print(f"  {lang}: {count} ({count/len(df)*100:.1f}%)")

    plt.figure(figsize=(12, 6))
    
    # Pegar top 10 para o gráfico
    top10 = linguagens.head(10)
    
    bars = plt.bar(range(len(top10)), top10.values, edgecolor='black', alpha=0.7)
    plt.xticks(range(len(top10)), top10.index, rotation=45, ha='right')
    
    # Adicionar valores nas barras
    for i, (bar, val) in enumerate(zip(bars, top10.values)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(val), ha='center', va='bottom', fontsize=10)
    
    plt.xlabel("Linguagem")
    plt.ylabel("Número de repositórios")
    plt.title("RQ05 — Top 10 Linguagens mais Populares")
    plt.grid(True, alpha=0.3, axis='y')
    
    output_file = OUTPUT_PATH / "rq05_linguagens.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"📊 Gráfico salvo: {output_file}")


# =========================
# RQ06 - Sistemas populares apresentam alta taxa de issues fechadas?
# =========================

def rq06_issues(df):
    print("\n" + "="*50)
    print("RQ06 — Percentual de issues fechadas")
    print("="*50)
    
    # Filtrar apenas repositórios com pelo menos 1 issue
    df_com_issues = df[df["total_issues"] > 0]
    
    if len(df_com_issues) == 0:
        print("Nenhum repositório com issues encontrado!")
        return
    
    print(f"Repositórios com issues: {len(df_com_issues)} ({len(df_com_issues)/len(df)*100:.1f}%)")
    print(f"Média: {df_com_issues['percentual_issues_fechadas'].mean():.1f}%")
    print(f"Mediana: {df_com_issues['percentual_issues_fechadas'].median():.1f}%")

    plt.figure()
    plt.hist(df_com_issues["percentual_issues_fechadas"], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel("Percentual de issues fechadas (%)")
    plt.ylabel("Número de repositórios")
    plt.title("RQ06 — Distribuição do Percentual de Issues Fechadas")
    plt.grid(True, alpha=0.3)
    
    output_file = OUTPUT_PATH / "rq06_issues.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"📊 Gráfico salvo: {output_file}")
    
    # Repositórios com alta taxa (>80%)
    alta_taxa = (df_com_issues['percentual_issues_fechadas'] > 80).sum()
    print(f"Alta taxa (>80%): {alta_taxa} ({alta_taxa/len(df_com_issues)*100:.1f}% dos c/ issues)")


# =========================
# Estatísticas gerais
# =========================

def estatisticas_gerais(df):
    print("\n" + "="*50)
    print("📊 ESTATÍSTICAS GERAIS")
    print("="*50)
    
    print(f"Total de repositórios: {len(df)}")
    print(f"\nMédias gerais:")
    print(f"  ⭐ Stars: {df['stars'].mean():.0f}")
    print(f"  📅 Idade: {df['idade_anos'].mean():.1f} anos")
    print(f"  🔀 PRs aceitas: {df['mergedPRs'].mean():.1f}")
    print(f"  📦 Releases: {df['releases'].mean():.1f}")
    print(f"  🐛 Issues abertas: {df['openIssues'].mean():.1f}")
    print(f"  ✅ Issues fechadas: {df['closedIssues'].mean():.1f}")


# =========================
# Execução principal
# =========================

def main():
    print("🚀 Iniciando análise de dados...")
    
    # Criar diretório de saída
    OUTPUT_PATH.mkdir(exist_ok=True)
    print(f"📁 Diretório de saída: {OUTPUT_PATH}")

    # Carregar dados
    df = carregar_dados()
    if df is None:
        return

    # Estatísticas gerais
    estatisticas_gerais(df)
    
    # Executar todas as análises
    rq01_idade_repos(df)
    rq02_pull_requests(df)
    rq03_releases(df)
    rq04_atualizacao(df)
    rq05_linguagens(df)
    rq06_issues(df)

    print("\n" + "="*50)
    print("✅ Análise finalizada com sucesso!")
    print(f"📊 Todos os gráficos foram salvos em: {OUTPUT_PATH}")
    print("="*50)


if __name__ == "__main__":
    main()