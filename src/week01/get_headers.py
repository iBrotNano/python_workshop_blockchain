import json
import requests
from rich import console

terminal = console.Console()

block_hash = "00000000000000000001d56f71888db978e05b32474ac2456a9d5fde748e8ec7"

base_url = "https://blockstream.info/api/"
request_slug = "block/"
full_api_url = f"{base_url}{request_slug}{block_hash}"
terminal.print(full_api_url)

response = requests.get(full_api_url)
response.raise_for_status()
data = response.json()
terminal.print(data)

blockheader = {
    "version": data.get("version"),
    "merkle_root": data.get("merkle_root"),
    "previous_block_hash": data.get("previousblockhash"),
    "bits": data.get("bits"),
    "nonce": data.get("nonce"),
}

path = "blockheader.json"

with open(path, "w") as file:
    json.dump(blockheader, file, indent=4)
