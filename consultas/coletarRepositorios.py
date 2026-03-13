import requests
import json
import time
import csv
from pathlib import Path


# =========================
# Configurações
# =========================

BASE_URL = "https://api.github.com/graphql"
TOKEN_PATH = Path(__file__).parent.parent / "secrets" / "token_github.txt"
QUERY_PATH = Path(__file__).parent / "query.graphql"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "repos_1000.json"


# =========================
# Funções auxiliares
# =========================

def carregar_token():
    with open(TOKEN_PATH, "r") as f:
        return f.read().strip()


def carregar_query():
    with open(QUERY_PATH, "r") as f:
        return f.read()


def fazer_requisicao(query, headers, variables=None):
    for tentativa in range(3):  # tenta até 3 vezes
        try:
            response = requests.post(
                BASE_URL,
                headers=headers,
                json={"query": query, "variables": variables or {}},
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Tentativa {tentativa + 1} falhou: {e}")
            time.sleep(5)

    raise Exception("Falha após 3 tentativas")


# =========================
# Coleta principal
# =========================

def fetch_1000_repos():
    token = carregar_token()
    query = carregar_query()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_repos = []
    cursor = None

    while len(all_repos) < 1000:
        try:
            variables = {"cursor": cursor} if cursor else None
            data = fazer_requisicao(query, headers, variables)

            if "errors" in data:
                print("Erro GraphQL, tentando novamente...")
                time.sleep(10)
                continue

            search_data = data["data"]["search"]
            batch = [repo for repo in search_data["nodes"] if repo]

            all_repos.extend(batch)

            print(f"Lote recebido: {len(batch)} | Total: {len(all_repos)}/1000")

            if not search_data["pageInfo"]["hasNextPage"]:
                break

            cursor = search_data["pageInfo"]["endCursor"]

            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            break

    return all_repos[:1000]


# =========================
# Salvar CSV
# =========================

def salvar_csv(repos):

    csv_path = Path(__file__).parent.parent / "data" / "repos_1000.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "name",
            "owner",
            "createdAt",
            "updatedAt",
            "primaryLanguage",
            "mergedPRs",
            "releases",
            "issues",
            "closedIssues",
            "stars"
        ])

        for repo in repos:

            # linguagem
            language_data = repo.get("primaryLanguage")
            if language_data:
                language = language_data.get("name", "None")
            else:
                language = "None"

            prs = repo.get("pullRequests", {}).get("totalCount", 0)
            releases = repo.get("releases", {}).get("totalCount", 0)
            issues = repo.get("issues", {}).get("totalCount", 0)
            closed = repo.get("issuesClosed", {}).get("totalCount", 0)

            writer.writerow([
                repo.get("name"),
                repo.get("owner", {}).get("login"),
                repo.get("createdAt"),
                repo.get("updatedAt"),
                language,
                prs,
                releases,
                issues,
                closed,
                repo.get("stargazerCount")
            ])

    print(f"CSV salvo em: {csv_path}")


# =========================
# Execução
# =========================

def main():

    repos = fetch_1000_repos()

    OUTPUT_PATH.parent.mkdir(exist_ok=True, parents=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump({"nodes": repos}, f, indent=2)

    salvar_csv(repos)

    print(f"Total coletado: {len(repos)} repositórios")
    print(f"JSON salvo em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()