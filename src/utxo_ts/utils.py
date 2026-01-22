from constants import SATS_PER_BTC, DUST_LIMIT


def btc_to_sats(btc):
    return int(btc * SATS_PER_BTC)


def sats_to_btc(sats):
    return float(sats / SATS_PER_BTC)


def get_balance(utxos):
    value = [u.get("value", 0) for u in utxos]
    return sum(value)


def check_dusty(name, sats):
    if sats <= DUST_LIMIT:
        raise ValueError(f"{name} dusty: {sats} sats")
