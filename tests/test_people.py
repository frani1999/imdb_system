from system_module_2.client.client import API_REST_URL
import requests
import unittest

people_list = ["Marlon Brando", "Mel Gibson", "Farah Samson", "Ella Salvador", "Walter Frank",
               "Ewan de la Motte", "Yvette Allen", "Juanita Allen", "Steve Eat", "Yang Cao"]


class TestPeople(unittest.TestCase):
    def test_get_people(self):
        for person in people_list:
            response = requests.get(f"{API_REST_URL}/people/{person}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(person.lower(), response.json().get("summary", "").lower())


if __name__ == "__main__":
    unittest.main()
