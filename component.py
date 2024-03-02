import requests
import unittest
import json

messenger_url = 'http://localhost:8001'
login_url = f'{messenger_url}/login'
send_message_url = f'{messenger_url}/send_message'
sent_messages_url = f'{messenger_url}/get_messages_to_user'

admin_url = 'http://localhost:8000'
get_messages_url = f'{admin_url}/get_messages'
delete_message_url = f'{admin_url}/delete_message'

class TestComponent(unittest.TestCase):

    def test_1_login(self):
        res = requests.post(f"{login_url}?name=Artem")
        self.assertEqual(res.text, '"You logged in as Artem"')

    def test_2_send_message(self):
        res = requests.post(f"{send_message_url}?receiver_name=test&text=hello", )
        self.assertEqual(res.text, '"Success"')

    def test_3_find_sent_message(self):
        res = requests.get(f"{sent_messages_url}?username=test").json()
        found = False
        for message in res:
            if message['receiver_name'] == 'test' and message['text'] == 'hello':
                found = True
                break
        self.assertTrue(found, True)

    def test_4_find_message_in_admin(self):
        res = requests.get(f"{get_messages_url}").json()
        found = False
        for message in res:
            if message['receiver_name'] == 'test' and message['text'] == 'hello':
                found = True
                break
        self.assertTrue(found, True)

    def test_5_delete_message(self):
        id = 0
        res = requests.get(f"{get_messages_url}").json()
        for message in res:
            if message['receiver_name'] == 'test' and message['text'] == 'hello':
                id = message["id"]
                break
        res = requests.delete(f"{delete_message_url}?message_id={id}")
        self.assertEqual(res.text, '"Success"')

if __name__ == '__main__':
    unittest.main()
