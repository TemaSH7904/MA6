import unittest
import requests
import psycopg2
from time import sleep

messenger_url = 'http://localhost:8001'
admin_url = 'http://localhost:8000'


def check_connect():
    try:
        conn = psycopg2.connect(
            dbname='Shalaev',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        conn.close()
        return True
    except Exception as e:
        return False


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_db_connection(self):
        sleep(5)
        self.assertEqual(check_connect(), True)

    def test_messenger_service_connection(self):
        r = requests.get("http://localhost:8001/health", verify=False)
        self.assertEqual(r.status_code, 200)

    def test_admin_service_connection(self):
        r = requests.get("http://localhost:8000/health", verify=False)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
