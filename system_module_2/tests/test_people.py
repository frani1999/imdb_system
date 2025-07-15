from system_module_2.client.client import API_REST_URL
import requests

people_list = ["Marlon Brando",
               "Richard Gere",
               "Mel Gibson",
               "Farah Samson",
               "Kat Pedroso",
               "Ella Salvador",
               "Walter Frank",
               "Ewan de la Motte",
               "Yvette Allen",
               "Juanita Allen",
               "Alejandro Acuña Sevilla",
               "Bill Johnson",
               "Edmund Kirby",
               "Steve Eat",
               "Oscar Escobar",
               "Mike Burdick",
               "Jose Cardeño",
               "Frank Holliday",
               "Ariane Sherrod",
               "Yang Cao"]


def test_get_person():
    for person in people_list:
        response = requests.get(f"{API_REST_URL}/people/{person}")
        assert response.status_code == 200
        assert person.lower() in response.json().get("summary", "").lower()


