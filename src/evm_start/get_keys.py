from eth_account import Account
import mnemonic

Account.enable_unaudited_hdwallet_features()


def get_keys():
    mnemo = mnemonic.Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)
    account = Account.from_mnemonic(seed_phrase)

    return {
        "address": account.address,
        "private_key": account.key.hex(),
        "seed": seed_phrase,
    }


if __name__ == "__main__":
    print(get_keys())
