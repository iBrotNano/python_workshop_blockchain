from electrum import Electrum
from constants import WALLET_OBJ, NETWORK


class UTXO:
    def __init__(self, address):
        self.address = address

    def via_electrum(self):
        """https://github.com/spesmilo/electrum/blob/master/electrum/commands.py#L492"""
        utxos = Electrum(NETWORK).call("getaddressunspent", self.address)
        return [self.map_keys(u) for u in utxos if self.tx_confirmed(u.get("tx_hash"))]

    def tx_confirmed(self, txid):
        """https://github.com/spesmilo/electrum/blob/master/electrum/commands.py#L1661"""
        status_data = Electrum(NETWORK).call("get_tx_status", txid)
        return status_data.get("confirmations")

    def map_keys(self, utxo):
        return {
            "txid": utxo.get("tx_hash"),
            "vout": utxo.get("tx_pos"),
            "value": utxo.get("value"),
        }
