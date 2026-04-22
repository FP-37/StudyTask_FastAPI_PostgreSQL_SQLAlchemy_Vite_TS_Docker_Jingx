import requests

AUTH_URL = "http://localhost:8001"
BUS_URL = "http://localhost:8002"

USER = {"username": "demo", "password": "demo1234"}

LINES = [
    {"line_number": 1,  "depot_number": 1, "start_time": "06:00", "end_time": "23:00", "length_km": 12.5},
    {"line_number": 5,  "depot_number": 1, "start_time": "05:30", "end_time": "22:30", "length_km": 8.3},
    {"line_number": 10, "depot_number": 2, "start_time": "07:00", "end_time": "21:00", "length_km": 15.7},
    {"line_number": 15, "depot_number": 2, "start_time": "06:30", "end_time": "22:00", "length_km": 20.1},
    {"line_number": 22, "depot_number": 3, "start_time": "05:00", "end_time": "23:30", "length_km": 9.8},
    {"line_number": 34, "depot_number": 3, "start_time": "06:00", "end_time": "20:00", "length_km": 11.2},
    {"line_number": 47, "depot_number": 4, "start_time": "07:30", "end_time": "21:30", "length_km": 18.4},
    {"line_number": 56, "depot_number": 4, "start_time": "06:00", "end_time": "22:00", "length_km": 7.6},
    {"line_number": 63, "depot_number": 5, "start_time": "05:45", "end_time": "23:15", "length_km": 25.0},
    {"line_number": 78, "depot_number": 5, "start_time": "08:00", "end_time": "20:30", "length_km": 14.3},
]


def main():
    r = requests.post(f"{AUTH_URL}/auth/register", json=USER)
    if r.status_code == 400:
        print(f"[seed] user '{USER['username']}' already exists, logging in...")
    elif r.status_code == 200:
        print(f"[seed] registered user '{USER['username']}'")
    else:
        print(f"[seed] register error: {r.status_code} {r.text}")
        return

    r = requests.post(f"{AUTH_URL}/auth/login", json=USER)
    r.raise_for_status()
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[seed] logged in, token obtained")

    for line in LINES:
        r = requests.post(f"{BUS_URL}/bus-lines", json=line, headers=headers)
        if r.status_code == 201:
            print(f"[seed] created line #{line['line_number']} depot={line['depot_number']}")
        else:
            print(f"[seed] skip line #{line['line_number']}: {r.status_code} {r.text}")

    print("[seed] done")


if __name__ == "__main__":
    main()
