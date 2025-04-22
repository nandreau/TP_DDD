# tools/login.py
import json
import requests

BASE_URL = "http://127.0.0.1:8000/api"
USERS_FILE = "tools/test_users.json"
TOKENS_FILE = "tools/tokens.json"
def login_all_users():
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    tokens = {}
    for user in users:
        res = requests.post(f"{BASE_URL}/login/", json={
            "username": user["login"],
            "password": user["password"]
        })

        if res.status_code == 200 and "token" in res.json():
            tokens[user["login"]] = {
                "token": res.json()["token"],
                "role": user["role"]
            }
            print(f"✅ {user['login']} connecté en tant que {user['role']}")
        else:
            print(f"❌ Échec pour {user['login']}")
            tokens[user["login"]] = { "token": None, "role": user["role"] }

    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

if __name__ == "__main__":
    login_all_users()
