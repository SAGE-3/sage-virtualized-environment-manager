import unittest
import requests
import os
import time

class TestAPI(unittest.TestCase):
    def setUp(self):
        os.system("./tests/init.sh 3")
        time.sleep(2)

    def tearDown(self):
        os.system("./tests/stop.sh")
        time.sleep(1)


    def test_allocation(self):
        print("Testing Allocation")
        url = "http://localhost:4024/api/vm/any/allocate"
        payload = {
            'vm': 'vnc-x11-firefox',
            'env': {
                'FIREFOX_THEME': 0
            }
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, json=payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json())
        self.assertIn('uid', response.json())


    def test_container_reconnect_via_any(self):
        print("Testing Container Reconnect with /api/vm/any")
        url = "http://localhost:4024/api/vm/any/allocate"
        payload = {
            'vm': 'vnc-x11-firefox',
            'env': {
                'FIREFOX_THEME': 0
            }
        }
        headers = {'Content-Type': 'application/json'}

        uid = requests.post(url, json=payload, headers=headers).json()["uid"]

        response = requests.post(f"http://localhost:4024/api/vm/any/{uid}", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json())
        self.assertIn('uid', response.json())


    def test_container_reconnect_via_ws_check(self):
        print("Testing Container Reconnect on WS Check")
        url = "http://localhost:4024/api/vm/any/allocate"
        payload = {
            'vm': 'vnc-x11-firefox',
            'env': {
                'FIREFOX_THEME': 0
            }
        }
        headers = {'Content-Type': 'application/json'}

        uid = requests.post(url, json=payload, headers=headers).json()["uid"]

        response = requests.get(f"http://localhost:4024/api/vm/ws/{uid}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json())


    def test_container_auto_shutdown(self):
        print("Testing Container Shutdown on no Active Connections")
        url = "http://localhost:4024/api/vm/any/allocate"
        payload = {
            'vm': 'vnc-x11-firefox',
            'env': {
                'FIREFOX_THEME': 0
            }
        }
        headers = {'Content-Type': 'application/json'}

        uid = requests.post(url, json=payload, headers=headers).json()["uid"]

        time.sleep(7)

        response = requests.get(f"http://localhost:4024/api/vm/ws/{uid}")
        self.assertIn('details', response.json())
        self.assertEqual( response.json().get("details", ""), "container not running")


    # def test_container_redeploy(self):
    #   Check if the data are is saved, you need to go into the container terminal and ls



if __name__ == '__main__':
    os.system("./tests/build")
    unittest.main()