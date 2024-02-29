import unittest
import psycopg2
from pathlib import Path
import asyncio
import sys

BASE_DIR = Path(__file__).resolve().parent

sys.path.append(str(BASE_DIR / 'messenger_service/app'))
sys.path.append(str(BASE_DIR / 'admin_service/app'))

from messenger_service.app.main import service_alive as messenger_status
from admin_service.app.main import service_alive as admin_status

class TestIntegration(unittest.TestCase):

    def test_db_connection(self):
        def test_database(self):
            try:
                conn = psycopg2.connect(
                    dbname='Shalaev',
                    user='postgres',
                    password='password',
                    host='localhost',
                    port='5432'
                )
                conn.close()
                check = True
            except Exception as e:
                check = False
            self.assertEqual(check, True)

    def test_messenger_service_connection(self):
        r = asyncio.run(messenger_status())
        self.assertEqual(r.status_code, 200)

    def test_admin_service_connection(self):
        r = asyncio.run(admin_status())
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
