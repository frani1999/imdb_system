import requests
import unittest

film_list = ["Blacksmith Scene", "The Clown Barber", "Grandes manoeuvres", "Place Saint-Augustin",
             "Academy for Young Ladies", "Danse fleur de lotus", "Dorotea",
             "Visita de Doña María Cristina y Alfonso XIII a Barcelona", "Beauty and the Beast",
             "The Sign of the Cross"]

API_REST_URL = "http://localhost:8000"


class TestFilms(unittest.TestCase):
    def test_get_films(self):
        for film in film_list:
            response = requests.get(f"{API_REST_URL}/films/{film}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(film.lower(), response.json().get("summary", "").lower())


if __name__ == "__main__":
    unittest.main()
