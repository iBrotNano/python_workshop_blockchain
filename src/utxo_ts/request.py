import requests, os
from dotenv import load_dotenv
from requests import Response


class Request:
    def __init__(self, prov):
        load_dotenv()
        self.url = os.getenv(prov)

    def use_rest_get(self, extend):
        res = requests.get(f"{self.url}{extend}")
        return self._handle_request(res)

    def use_rest_post(self, extend, data=None, param=None):
        res = requests.post(f"{self.url}{extend}", data=data, params=param)
        return self._handle_request(res)

    def use_rpc_post(self, method, params=None):
        payload = {"id": 1, "jsonrpc": "2.0", "method": method, "params": params or []}
        res = requests.post(self.url, json=payload)

        if res.status_code != 200:
            raise RuntimeError(f"{res.status_code}: {res.text}")

        data = res.json()

        if data.get("error"):
            raise RuntimeError(data["error"])

    def _handle_request(self, res: Response):
        if res.status_code != 200:
            raise RuntimeError(f"{res.status_code}: {res.text}")

        try:
            print(res.json())
            return res.json()
        except:
            return res.text
