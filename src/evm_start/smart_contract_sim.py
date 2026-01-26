from get_keys import get_keys
from inspect import signature as sig

null_address = "0x0000"


def require(condition, message: str):
    if not condition:
        raise Exception(message)


def OnlyOwner(func):
    def modifier(*args, **kwargs):
        param_sigs = sig(func)
        bound_args = param_sigs.bind(*args, **kwargs)
        bound_args.apply_defaults()
        _self = bound_args.arguments("self")

        if not _self:
            raise ValueError("not called as self")

        _sender = bound_args.arguments("sender")

        if not _sender:
            raise ValueError("function has no parameter 'sender'")

        require(_self.owner == _sender.address, "only owner allowed")
        return func(*args, **kwargs)

    return modifier


class Wallet:

    def __init__(self, keys):

        self.address = get_keys()["address"]
        self.balance = 0

    def send(self, amount, to):
        self.balance -= amount
        to.balance += amount


class SmartContract:

    owner: str
    address: str
    balance: int
    holders: dict[str, int]
    null_address: str

    def __init__(self, sender: Wallet | "SmartContract"):
        self.owner = sender.address
        self.address = get_keys()["address"]
        self.balance = 0
        self.decimals = 0
        self.totalsupply = 1_000_000 * 10**self.decimals

    @OnlyOwner
    def airdrop(self, sender, _to, _amount):
        require(_amount <= 1_000_000, "not more than one coin")

        if _to in self.holders.keys():
            self.holders[_to] += _amount
        else:
            self.holders[_to] = _amount

    def transfer(self, sender, _amount, _to):
        require(self.holders[sender.address] >= _amount, "insufficient token balance")
        require(_to != null_address, "cant send token to null address")
        sender.balance -= _amount
        _to.balance += _amount
