import json
import requests
from pathlib import Path
import argparse

BASE_URL = "http://127.0.0.1:8000/api"
TESTS_DIR = Path("tools/tests")
TOKENS_FILE = "tools/tokens.json"

def run_tests(debug=False):
    with open(TOKENS_FILE, "r") as f:
        tokens = json.load(f)

    for user, data in tokens.items():
        role = data["role"]
        token = data["token"]
        print(f"\n=== TESTS POUR {role.upper()} ===")
        file_path = TESTS_DIR / f"{role}.json"
        if not file_path.exists():
            print(f"⚠️  Aucun fichier de test pour {role}")
            continue
        if not token:
            print(f"⚠️  Pas de token pour {role}")
            continue

        with open(file_path, "r") as f:
            tests = json.load(f)

        headers = { "Authorization": f"Token {token}" }
        ok, ko = [], []

        for test in tests:
            try:
                url = f"{BASE_URL}{test['path']}"
                method = test['method']
                data = test.get('body')

                response = requests.request(method, url, headers=headers, json=data)

                if response.status_code == test["expected_status"]:
                    ok.append(test)
                    if debug:
                        print(f"✅ [{method}] {test['path']} → {response.status_code}")
                        print("↪ Response:", safe_text(response))
                else:
                    ko.append((test, response.status_code, response.text))
            except Exception as e:
                ko.append((test, "EXCEPTION", str(e)))

        print(f"✅ {len(ok)} réussites | ❌ {len(ko)} erreurs")
        for fail in ko:
            test, code, detail = fail
            print(f"  ❌ {test['method']} {test['path']} → {code} (attendu : {test['expected_status']})")
            if debug:
                print("↪ Response:", detail)

def safe_text(response):
    try:
        return response.json()
    except Exception:
        return response.text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testeur d'API REST pour les rôles")
    parser.add_argument("-d", "--debug", action="store_true", help="Afficher les réponses détaillées")
    args = parser.parse_args()

    run_tests(debug=args.debug)
