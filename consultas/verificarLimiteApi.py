import requests
from pathlib import Path


# =========================
# Configurações
# =========================

BASE_URL = "https://api.github.com/graphql"
TOKEN_PATH = Path(__file__).parent.parent / "secrets" / "token_github.txt"


# =========================
# Funções auxiliares
# =========================

def carregar_token():
    with open(TOKEN_PATH, "r") as f:
        return f.read().strip()


def verificar_rate_limit(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    query = """
    query {
      rateLimit {
        limit
        remaining
        resetAt
        used
      }
    }
    """

    response = requests.post(
        BASE_URL,
        headers=headers,
        json={"query": query}
    )

    response.raise_for_status()
    return response.json()


# =========================
# Execução
# =========================

def main():
    try:
        token = carregar_token()
        data = verificar_rate_limit(token)

        rate = data["data"]["rateLimit"]

        print("✅ Rate limit info:")
        print(f"Limite total: {rate['limit']}")
        print(f"Requisições restantes: {rate['remaining']}")
        print(f"Reset em: {rate['resetAt']}")
        print(f"Usadas: {rate['used']}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")


if __name__ == "__main__":
    main()