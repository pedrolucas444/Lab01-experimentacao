import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

plt.rcParams['font.size'] = 12

DATA_PATH = Path(__file__).parent.parent / "data" / "repos_1000.csv"
OUTPUT_PATH = Path(__file__).parent.parent / "graficos"


# =========================
# Carregamento e preparo
# =========================

def carregar_dados():

    df = pd.read_csv(DATA_PATH)

    hoje = datetime.now()

    df["createdAt"] = pd.to_datetime(df["createdAt"]).dt.tz_localize(None)
    df["updatedAt"] = pd.to_datetime(df["updatedAt"]).dt.tz_localize(None)

    df["idade_anos"] = (hoje - df["createdAt"]).dt.days / 365.25
    df["dias_desde_update"] = (hoje - df["updatedAt"]).dt.days

    # total de issues
    df["total_issues"] = df["issues"] + df["closedIssues"]

    # percentual de issues fechadas
    df["percentual_issues_fechadas"] = (
        df["closedIssues"] / df["total_issues"] * 100
    ).fillna(0)

    return df


# =========================
# RQ01
# Sistemas populares são maduros?
# =========================

def rq01_idade_repos(df):

    print("\nRQ01 — Idade dos repositórios")

    print(f"Média: {df['idade_anos'].mean():.2f} anos")
    print(f"Mediana: {df['idade_anos'].median():.2f} anos")

    plt.figure(figsize=(10,6))

    plt.hist(df["idade_anos"], bins=30)

    plt.xlabel("Idade (anos)")
    plt.ylabel("Número de repositórios")

    plt.title("RQ01 — Idade dos Repositórios")

    plt.savefig(OUTPUT_PATH / "rq01_idade.png")

    plt.close()


# =========================
# RQ02
# Contribuição externa
# =========================

def rq02_pull_requests(df):

    print("\nRQ02 — Pull Requests Aceitas")

    print(f"Média: {df['mergedPRs'].mean():.0f}")
    print(f"Mediana: {df['mergedPRs'].median():.0f}")

    plt.figure(figsize=(10,6))

    plt.hist(df["mergedPRs"], bins=50)

    plt.yscale("log")

    plt.xlabel("Número de PRs aceitas")
    plt.ylabel("Repositórios")

    plt.title("RQ02 — Contribuição externa (PRs)")

    plt.savefig(OUTPUT_PATH / "rq02_prs.png")

    plt.close()


# =========================
# RQ03
# Releases
# =========================

def rq03_releases(df):

    print("\nRQ03 — Releases")

    print(f"Média: {df['releases'].mean():.1f}")
    print(f"Mediana: {df['releases'].median():.0f}")

    plt.figure(figsize=(10,6))

    plt.hist(df["releases"], bins=50)

    plt.yscale("log")

    plt.xlabel("Número de releases")
    plt.ylabel("Repositórios")

    plt.title("RQ03 — Frequência de Releases")

    plt.savefig(OUTPUT_PATH / "rq03_releases.png")

    plt.close()


# =========================
# RQ04
# Atualização
# =========================

def rq04_atualizacao(df):

    print("\nRQ04 — Frequência de atualização")

    print(f"Média: {df['dias_desde_update'].mean():.0f} dias")
    print(f"Mediana: {df['dias_desde_update'].median():.0f} dias")

    plt.figure(figsize=(10,6))

    plt.hist(df["dias_desde_update"], bins=50)

    plt.xlabel("Dias desde última atualização")
    plt.ylabel("Repositórios")

    plt.title("RQ04 — Tempo desde última atualização")

    plt.savefig(OUTPUT_PATH / "rq04_update.png")

    plt.close()


# =========================
# RQ05
# Linguagens
# =========================

def rq05_linguagens(df):

    print("\nRQ05 — Linguagens mais usadas")

    linguagens = df["primaryLanguage"].fillna("None").value_counts().head(10)

    for lang, count in linguagens.items():
        print(f"{lang}: {count}")

    plt.figure(figsize=(12,6))

    linguagens.plot(kind="bar")

    plt.xlabel("Linguagem")
    plt.ylabel("Repositórios")

    plt.title("RQ05 — Linguagens mais populares")

    plt.xticks(rotation=45)

    plt.savefig(OUTPUT_PATH / "rq05_linguagens.png")

    plt.close()


# =========================
# RQ06
# Issues fechadas
# =========================

def rq06_issues(df):

    print("\nRQ06 — Percentual de issues fechadas")

    df_validos = df[df["total_issues"] > 0]

    print(f"Média: {df_validos['percentual_issues_fechadas'].mean():.1f}%")
    print(f"Mediana: {df_validos['percentual_issues_fechadas'].median():.1f}%")

    plt.figure(figsize=(10,6))

    plt.hist(df_validos["percentual_issues_fechadas"], bins=30)

    plt.xlabel("Percentual de issues fechadas (%)")
    plt.ylabel("Repositórios")

    plt.title("RQ06 — Percentual de Issues Fechadas")

    plt.savefig(OUTPUT_PATH / "rq06_issues.png")

    plt.close()


# =========================
# Execução
# =========================

def main():

    OUTPUT_PATH.mkdir(exist_ok=True)

    df = carregar_dados()

    print("\nTotal de repositórios analisados:", len(df))

    rq01_idade_repos(df)
    rq02_pull_requests(df)
    rq03_releases(df)
    rq04_atualizacao(df)
    rq05_linguagens(df)
    rq06_issues(df)

    print("\nAnálise finalizada.")
    print("Gráficos salvos na pasta /graficos")


if __name__ == "__main__":
    main()