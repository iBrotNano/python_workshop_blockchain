sender = "tb1qc77mj2yguhdkl6akwjskswzvruha8cpje6m904"
recipient = ""
amt_btc = 0.00001
fee_sats = 1200

from utxo import UTXO
from utils import check_dusty, btc_to_sats

try:
    amt_sats = btc_to_sats(amt_btc)
    check_dusty("amt_sets", amt_btc)
    check_dusty("fee_sats", fee_sats)

    utxo = UTXO(sender)
    utxos = utxo.via_electrum()

    if not utxos:
        raise Exception("no utxos")

    print(f"{utxos=}")

except Exception as e:
    print(f"ERROR: {e}")
