import requests
import unittest

messenger_url = 'http://localhost:8001'
login_url = f'{messenger_url}/login'
send_message_url = f'{messenger_url}/send_message'
sent_messages_url = f'{messenger_url}/get_messages_to_user'

admin_url = 'http://localhost:8000'
get_messages_url = f'{admin_url}/get_messages'
delete_message_url = f'{admin_url}/delete_message'

class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_1_login(self):
        res = requests.post(f"{login_url}?name=Artem")
        self.assertEqual(res, "You logged in as Artem")

    def test_2_send_message(self):
        res = requests.post(f"{send_message_url}?receiver_name=test&text=hello")
        self.assertEqual(res, "Success")

    def test_3_find_sent_message(self):
        res = requests.get(f"{sent_messages_url}?username=test").json()
        found = False
        for message in res:
            if message['receiver_name'] == 'test' and message['text'] == 'hello':
                found = True
                break
        self.assertTrue(found, "Sent message was not found in the received messages")

    def test_4_find_message_in_admin(self):
        res = requests.get(f"{get_messages_url}")
        found = False
        for message in res:
            if message['receiver_name'] == 'test' and message['text'] == 'hello':
                found = True
                break
        self.assertTrue(found, "Sent message was not found in the received messages")

    def test_5_delete_message(self):
        id = 0
        res = requests.get(f"{get_messages_url}")
        for message in res:
            if message['receiver_name'] == 'test' and message['text'] == 'hello':
                id = message.id
                break
        res = requests.post(f"{delete_message_url}?id={id}")
        self.assertEqual(res, "Success")

if __name__ == '__main__':
    unittest.main()
