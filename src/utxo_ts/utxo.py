from electrum import Electrum
from constants import NETWORK
from request import Request


class UTXO:
    def __init__(self, address):
        self.address = address
        self.u_keys = ("txid", "vout", "value")

    def via_blockbook(self):
        """- https://github.com/trezor/blockbook/blob/master/docs/api.md#get-utxo
        - https://blockbook.tbtc-1.zelcore.io"""
        utxos = Request("BLOCKBOOK").use_rest_get(f"utxo/{self.address}?confirmed=true")
        return [{k: u[k] for k in self.u_keys} for u in utxos if u.get("confirmations")]

    def via_mempool_space(self):
        """- https://mempool.space/testnet/docs/api/rest#get-address-utxo"""
        utxos = Request("MEMPOOLSPACE").use_rest_get(f"address/{self.address}/utxo")
        print(utxos)
        return [
            {k: u[k] for k in self.u_keys}
            for u in utxos
            if u.get("status").get("confirmed")
        ]

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
