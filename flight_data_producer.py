from faker import Faker
from faker_airtravel import AirTravelProvider
import random
import requests
import json

fake = Faker()
fake.add_provider(AirTravelProvider)

USER_URL = "http://localhost:8082/api/users"
FLIGHTS_URL = "http://localhost:8081/api/flights"
BOOKINGS_URL = "http://localhost:8083/api/bookings"
AUTH_URL = "http://localhost:8084/api/auth"


def add_airplane_types(token):
    for i in range(237):
        airplane_type = {"maxCapacity": random.randint(50, 853)}
        x = requests.post(
            f"{FLIGHTS_URL}/airplanetype/add",
            json=airplane_type,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": token,
            },
        )


def add_airplanes(token):
    airplane_types = requests.get(
        f"{FLIGHTS_URL}/airplanetype/all",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        },
    )
    airplane_types = json.loads(airplane_types.text)
    type_list = []
    for x in airplane_types:
        type_list.append(x["id"])
    random.shuffle(type_list)
    for i in type_list:
        airplane = {"airplaneType": i}
        x = requests.post(
            f"{FLIGHTS_URL}/airplane/add",
            json=airplane,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": token,
            },
        )


def add_airports(token):
    for i in range(38):
        airport = fake.airport_object()
        a1 = {"city": airport["city"], "iataId": airport["iata"]}
        x = requests.post(
            f"{FLIGHTS_URL}/airport/add",
            json=a1,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": token,
            },
        )
        if x.status_code != 201:
            print(x.text)
            break


def add_routes(token):
    airports = requests.get(
        f"{FLIGHTS_URL}/airport/all",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        },
    )
    airports = json.loads(airports.text)
    for i in range(41):
        a1 = random.choice(airports)
        a2 = random.choice(airports)
        if a1["iataId"] != a2["iataId"]:
            route = {"origin": a1["iataId"], "destination": a2["iataId"]}
            x = requests.post(
                f"{FLIGHTS_URL}/route/add",
                json=route,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": token,
                },
            )
            if x.status_code != 201:
                print(x.text)
                break


def add_flights(token):
    routes = requests.get(
        f"{FLIGHTS_URL}/route/all",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        },
    )
    routes = json.loads(routes.text)
    airplanes = requests.get(
        f"{FLIGHTS_URL}/airplane/all",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        },
    )
    airplanes = json.loads(airplanes.text)
    for i in range(90):
        route = random.choice(routes)
        airplane = random.choice(airplanes)
        f1 = fake.flight()
        flight = {
            "route": route["id"],
            "departureTime": fake.future_datetime(end_date="+6M").isoformat(),
            "airplane": airplane["id"],
            "seatPrice": f1["price"],
            "reservedSeats": airplane["airplaneType"]["maxCapacity"]
            - random.randint(1, 10),
        }
        x = requests.post(
            f"{FLIGHTS_URL}/add",
            json=flight,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": token,
            },
        )
        if x.status_code != 201:
            print(x.text)
            break


def main():
    up = {"username": "admin", "password": "1234"}
    res = requests.post(f"{AUTH_URL}/login", data=up)
    token = "Bearer " + res.json()["access_token"]
    add_airplane_types(token)
    add_airplanes(token)
    add_airports(token)
    add_routes(token)
    add_flights(token)


if __name__ == "__main__":
    main()
