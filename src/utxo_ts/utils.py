from constants import SATS_PER_BTC, WALLET_PATH, DUST_LIMIT
import json


def btc_to_sats(btc):
    return int(btc * SATS_PER_BTC)


def sats_to_btc(sats):
    return float(sats) / SATS_PER_BTC


def get_balance(utxos):
    values = [utxo["value"] for utxo in utxos]
    return sum(values)


def readJSON(path):
    with open(path, "r") as file:
        return json.load(file)


def get_pk_electrum(sender):
    return readJSON(WALLET_PATH)[sender].split("p2wpkh:")[1]


def check_dusty(name, amt):
    if amt <= DUST_LIMIT:
        raise ValueError(f"{name} dusty: {amt} sats")
