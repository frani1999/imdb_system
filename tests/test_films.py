from system_module_2.client.client import API_REST_URL
import requests
import unittest

film_list = ["Blacksmith Scene", "Cinderella", "Extraordinary Engineering", "Smoke Signal After Show",
             "American Illuminati 2", "Chino & Nacho", "Theory", "Raghav Radio", "The Prince in the Rainforest",
             "Nina Simone: Live in '65 & '68"]


class TestFilms(unittest.TestCase):
    def test_get_films(self):
        for film in film_list:
            response = requests.get(f"{API_REST_URL}/films/{film}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(film.lower(), response.json().get("summary", "").lower())


if __name__ == "__main__":
    unittest.main()
