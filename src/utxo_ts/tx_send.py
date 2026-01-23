# tx_send.py

# USER INPUT #####################################

sender = "tb1qc77mj2yguhdkl6akwjskswzvruha8cpje6m904"
recipient = "tb1qq62c2cvkv0cm9sek69wqvtmznxdj7q6lvzfpdw"

amt_btc = 0.0003
fee_sats = 600

###################################################

from utxo import UTXO
from utils import check_dusty, btc_to_sats
from tx_build import TX
from tx_build_change import TXC
from request import Request

try:

    amt_sats = btc_to_sats(amt_btc)
    check_dusty("amt_sats", amt_sats)
    check_dusty("fee_sats", fee_sats)

    utxo = UTXO(sender)
    try:
        utxos = utxo.via_electrum()
        if not utxos:
            raise ValueError("no utxos via electrum: trying fallback ...")
    except Exception as e:
        print(e)
        utxos = utxo.via_mempool_space() or utxo.via_blockbook()

    if not utxos:
        raise Exception("no utxos")
    print("utxos", utxos)

    raw_tx, unblocked = TXC(sender).build(recipient, amt_sats, fee_sats, utxos)
    if not raw_tx:
        raise ValueError("no tx wab built")
    print("raw_tx", raw_tx)
    print("unblocked", unblocked)

    try:
        sx = Request("MEMPOOLSPACE").use_rest_post("tx", raw_tx)
    except Exception as e:
        print(f"ERROR: {e} -> mempool.space failed -> now trying quicknode ...")
        sx = Request("QUICKNODE").use_rpc_post("sendrawtransaction", [raw_tx])
    print("sx", sx)

except Exception as e:
    print(f"ERROR:", e)
