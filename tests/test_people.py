import requests
import unittest

people_list = ["Marlon Brando", "Mel Gibson", "Frank Sinatra", "Antonio Banderas", "Charles Chaplin",
               "Harrison Ford", "Morgan Freeman", "Michael J. Fox", "Tom Hanks", "Jennifer Lopez"]

API_REST_URL = "http://localhost:8000"


class TestPeople(unittest.TestCase):
    def test_get_people(self):
        for person in people_list:
            response = requests.get(f"{API_REST_URL}/people/{person}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(person.lower(), response.json().get("summary", "").lower())


if __name__ == "__main__":
    unittest.main()
