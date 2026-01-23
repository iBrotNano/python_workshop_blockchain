from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import HDKey
from utils import get_balance, get_pk_electrum
from constants import NETWORK, DUST_LIMIT


class TX:
    def __init__(self, sender):
        self.signer = get_pk_electrum(sender)
        self.key = HDKey(import_key=self.signer, network=NETWORK)

    def build(self, recipient, amt, fee, utxos):
        tx = Transaction(network=NETWORK)

        for utxo in utxos:
            tx.add_input(
                prev_txid=utxo["txid"],
                output_n=utxo["vout"],
                value=utxo["value"],
                address=self.key.address(),
            )

            tx.add_output(amt, recipient)
            change = get_balance(utxos) - (amt + fee)

            if change < 0:
                raise ValueError("insufficient balance")
            elif change > DUST_LIMIT:
                tx.add_output(change, self.key.address())

            tx.sign([self.key])
            return tx.as_hex(), 0
