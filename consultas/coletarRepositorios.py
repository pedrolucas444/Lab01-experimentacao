import requests
import json
import time
from pathlib import Path


# =========================
# Configurações
# =========================

BASE_URL = "https://api.github.com/graphql"
TOKEN_PATH = Path(__file__).parent.parent / "secrets" / "token_github.txt"
QUERY_PATH = Path(__file__).parent / "query.graphql"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "repos_100.json"


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
    response = requests.post(
        BASE_URL,
        headers=headers,
        json={"query": query, "variables": variables or {}},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


# =========================
# Coleta principal
# =========================

def fetch_100_repos():
    token = carregar_token()
    query = carregar_query()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_repos = []
    cursor = None

    while len(all_repos) < 100:
        try:
            variables = {"cursor": cursor} if cursor else None
            data = fazer_requisicao(query, headers, variables)

            if "errors" in data:
                print("Erro GraphQL:", data["errors"])
                break

            search_data = data["data"]["search"]
            batch = search_data["nodes"]

            all_repos.extend(batch)

            if not search_data["pageInfo"]["hasNextPage"]:
                break

            cursor = search_data["pageInfo"]["endCursor"]
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            break

    return all_repos[:100]


# =========================
# Execução
# =========================

def main():
    repos = fetch_100_repos()

    OUTPUT_PATH.parent.mkdir(exist_ok=True, parents=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump({"nodes": repos}, f, indent=2)

    print(f"Total coletado: {len(repos)} repositórios")
    print(f"Salvo em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()