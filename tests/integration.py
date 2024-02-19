import unittest
import requests
import psycopg2
from time import sleep
import json

ticket_url = 'http://localhost:8000'
statistics_url = 'http://localhost:8001'
add_ticket_url = f'{ticket_url}/add_ticket'
get_ticket_by_id_url = f'{ticket_url}/get_ticket_by_id'

def check_connect():
    try:
        conn = psycopg2.connect(
            dbname='TicketAirport',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        conn.close()
        return True
    except:
        return False


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_db_connection(self):
        sleep(5)
        self.assertEqual(check_connect(), True)

    def test_ticket_service_connection(self):
        r = requests.get("http://localhost:8000/health", verify=False)
        self.assertEqual(r.status_code, 200)

    def test_statistics_service_connection(self):
        r = requests.get("http://localhost:8001/health", verify=False)
        self.assertEqual(r.status_code, 200)

    def test_ticket_get(self):
        res = requests.get(f"{get_ticket_by_id_url}?ticket_id=1").json()
        self.assertTrue('passenger_name' in res.keys())
        self.assertTrue('passport' in res.keys())
        self.assertTrue('id_airplane' in res.keys())
        self.assertTrue('direction' in res.keys())


if __name__ == '__main__':
    unittest.main()
