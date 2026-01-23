from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import HDKey
from utils import get_balance, get_pk_electrum
from constants import NETWORK, DUST_LIMIT


class TXC:
    def __init__(self, sender):
        self.signer = get_pk_electrum(sender)
        self.key = HDKey(import_key=self.signer, network=NETWORK)

    def build(self, recipient, amt, fee, utxos, maxc=10):
        total_balance = get_balance(utxos)
        tx = Transaction(network=NETWORK)
        inp_val = 0

        for utxo in utxos:
            tx.add_input(
                prev_txid=utxo["txid"],
                output_n=utxo["vout"],
                value=utxo["value"],
                address=self.key.address(),
            )

            inp_val += utxo["value"]

            if inp_val >= amt + fee:
                break

        unblocked = total_balance - inp_val
        tx.add_output(amt, recipient)
        tx, fee = self.add_changes(tx, amt, fee, inp_val, maxc)
        tx.sign([self.key])
        return tx.as_hex(), unblocked

    def add_changes(self, tx: Transaction, amt, fee, inp_val, maxc):
        change = inp_val - (amt + fee)

        if change < 0:
            raise ValueError(f"negative change: {change}")
        elif change < DUST_LIMIT:
            return tx, fee + change
        else:
            c_outs = min(maxc, change // DUST_LIMIT)
            c_val = change // c_outs
            rest = int(change % c_outs)
            tx.add_output(c_val + rest, self.key.address())

            for _ in range(c_outs - 1):
                tx.add_output(c_val, self.key.address())

            return tx, fee
