USE_TESTNET = True
LANGUAGE = "english"

# import random
import secrets
from mnemonic import Mnemonic
from rich import console

from bip_utils import (
    Bip39SeedGenerator as seedgen,
    Bip44Changes as derive,
    Bip84 as target,
    Bip44,
    Bip84Coins as coins,
)

MNEMO = Mnemonic(LANGUAGE)
NETWORK = coins.BITCOIN_TESTNET if USE_TESTNET else coins.BITCOIN
terminal = console.Console()


def get_seed():
    # print(MNEMO.wordlist)
    # words = random.sample(MNEMO.wordlist, 11) ... NIEMALS FÜR ZUFALLSZAHLEN BENUTZEN
    words = [secrets.choice(MNEMO.wordlist) for _ in range(11)]

    for candidate in MNEMO.wordlist:
        seed = " ".join(words + [candidate])
        if MNEMO.check(seed):
            return seed


def get_account(seed: str):
    seed_bytes = seedgen(seed).Generate()
    wallet = target.FromSeed(seed_bytes, NETWORK)
    account = wallet.Purpose().Coin().Account(0)
    return account.Change(derive.CHAIN_EXT).AddressIndex(0)


def get_keys(acc: Bip44):
    return {
        "private_key": acc.PrivateKey().ToWif(),
        "public_key": acc.PublicKey().RawCompressed().ToHex(),
        "address": acc.PublicKey().ToAddress(),
    }


seed = get_seed()
terminal.print(f"{seed=}")
account = get_account(seed)
keys = get_keys(account)
terminal.print(keys)
