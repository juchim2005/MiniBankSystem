from transactions import Transactions
class User:

    def __init__(self, login, password, balance=0):
        self.login = login
        self.password = password
        self.transactions = Transactions.initialize_csv(self)
        self.balance = balance

    @classmethod
    def from_dict(self, data):
        return User(data["login"], data["password"],data["balance"])
    
    def to_dict(self):
        dict = {"login": self.login, "password": self.password, "balance": self.balance}
        return dict
    
    
    