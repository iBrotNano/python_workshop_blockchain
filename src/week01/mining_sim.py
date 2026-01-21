from hashlib import sha256
import time
import json
import struct
from rich import console

terminal = console.Console()
path = "blockheader.json"

with open(path, "r") as file:
    blockheader = json.load(file)

terminal.print(blockheader)
terminal.rule()

max_target = 0xFFFF << 208
difficulty = 121_658_450_774_825
simplifier = 10**18
sim_difficulty = difficulty / simplifier
target = max_target / sim_difficulty
terminal.print(f"0x{int(max_target):064x}")
terminal.print(f"0x{int(target):064x}")


def build_header(hd, ts, nc) -> bytearray:
    return (
        struct.pack("<L", hd["version"])
        + bytes.fromhex(hd["previous_block_hash"])
        + bytes.fromhex(hd["merkle_root"])
        + struct.pack("<L", int(ts))
        + struct.pack("<L", hd["bits"])
        + struct.pack("<L", nc)
    )


nonce = 0
start_time = int(time.time())
timestamp = start_time

terminal.rule()
terminal.print("Start mining")

while True:
    header = build_header(blockheader, timestamp, nonce)
    hash = sha256(sha256(header).digest()).digest()

    # terminal.print(f"n: {nonce} | {hash[::-1].hex()}")

    if int.from_bytes(hash, "little") < target:
        hex_hash = hash[::-1].hex()
        break

    timestamp = int(time.time())
    nonce += 1

terminal.rule()
terminal.print(f"{hex_hash=}")
terminal.print(f"duration: {int(time.time()) - start_time}")
terminal.print(f"attempts: {nonce + 1}")
