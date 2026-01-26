class Bankaccount:

    def __init__(self, iban, owner):

        self.iban = iban

        self.owner = owner

        self.balance = 0

    def deposit(self, amount):

        self.balance += amount

    def transfer(self, amount, to):

        self.balance -= amount

        to.balance += amount

        print(self.owner, "transfers", amount, "to", to.owner)

    def withdraw(self, amount):

        self.balance -= amount


#########################################################


account1 = Bankaccount("123-456", "Alice Adriana")

account2 = Bankaccount("654-321", "Bob Builder")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


account1.deposit(500)

account1.transfer(200, account2)

account2.withdraw(50)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


print(account1.owner, account1.balance)

print(account2.owner, account2.balance)
