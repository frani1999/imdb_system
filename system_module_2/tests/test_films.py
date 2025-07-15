from system_module_2.client.client import API_REST_URL
import requests

film_list = ["Blacksmith Scene",
             "Le fakir, mystère indien",
             "Cinderella",
             "Place Saint-Augustin",
             "Extraordinary Engineering",
             "An Ordained Fate",
             "Smoke Signal After Show",
             "The elevator",
             "American Illuminati 2",
             "A Cute Guest",
             "Chino & Nacho",
             "Homo Sexians",
             "Theory",
             "The Finish Line",
             "Raghav Radio",
             "Mesebolygo",
             "The Prince in the Rainforest",
             "The Expected",
             "Puissance 4",
             "Nina Simone: Live in '65 & '68"]


def test_get_film():
    for film in film_list:
        response = requests.get(f"{API_REST_URL}/films/{film}")
        assert response.status_code == 200
        assert film.lower() in response.json().get("summary", "").lower()
