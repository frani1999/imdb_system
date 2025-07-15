import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from system_module_2.client.client import API_REST_URL
import requests


class ConcurrentSessionTest(unittest.TestCase):

    def setUp(self):
        self.num_requests = 10  # Number of requests
        self.target_url = "/people/Bruce Lee"

    def make_request(self, i):
        try:
            response = requests.get(f"{API_REST_URL}{self.target_url}")
            return i, response.status_code, response.json()
        except Exception as e:
            return i, None, str(e)

    def test_concurrent_people_requests(self):
        results = []
        with ThreadPoolExecutor(max_workers=self.num_requests) as executor:
            futures = [executor.submit(self.make_request, i) for i in range(self.num_requests)]
            for future in as_completed(futures):
                results.append(future.result())

        for i, status_code, content in results:
            with self.subTest(request=i):
                self.assertEqual(status_code, 200)
                self.assertIn("Bruce Lee", content.get("summary", ""))


if __name__ == "__main__":
    unittest.main()
