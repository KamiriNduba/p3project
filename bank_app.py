from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class BankTransaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Integer)

class Bank:
    def __init__(self):
        self.engine = create_engine('sqlite:///bank.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def deposit(self, user_id, amount):
        transaction = BankTransaction(user_id=user_id, amount=amount)
        self.session.add(transaction)
        self.session.commit()

    def withdraw(self, user_id, amount):
        balance = self.get_balance(user_id)
        if amount <= 0:
            print("Invalid amount. Please enter a positive value.")
        elif balance < amount:
            print("Insufficient funds. You cannot withdraw more than your balance.")
        else:
            transaction = BankTransaction(user_id=user_id, amount=-amount)
            self.session.add(transaction)
            self.session.commit()
            print("You have withdrawn: $", amount)

    def get_balance(self, user_id):
        deposits = self.session.query(BankTransaction).filter_by(user_id=user_id).filter(BankTransaction.amount > 0).all()
        withdrawals = self.session.query(BankTransaction).filter_by(user_id=user_id).filter(BankTransaction.amount < 0).all()
        balance = sum(transaction.amount for transaction in deposits) - sum(transaction.amount for transaction in withdrawals)
        return balance

    def delete_account(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        self.session.delete(user)
        self.session.commit()

def main():
    bank = Bank()

    while True:
        choice = main_menu()
        if choice == '1':
            login(bank)
        elif choice == '2':
            create_account(bank)
        elif choice == '3':
            print("Thank you for using our bank and Future Computer Programmer ATM Machine!")
            print("For your continued support, we are offering 3% cash back on all debit purchases.")
        elif choice == '4':
            print("Thanks for stopping by FinTech Bank!")
            break
        else:
            print("Invalid choice!")

def main_menu():
    print("**** MAIN MENU ****\n")
    print("1 -> Login to Banking Menu")
    print("2 -> Create New Account")
    print("3 -> View Promotions")
    print("4 -> Quit the Program")
    return input("Enter your choice: ")

def create_account(bank):
    username = input("Please create a username: ")
    password = input("Please create a password: ")
    user = User(username=username, password=password)
    bank.session.add(user)
    bank.session.commit()
    print("Account created!")

def login(bank):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user = bank.session.query(User).filter_by(username=username, password=password).first()
    if user:
        print("Login Successful!")
        account_menu(bank, user.id)
    else:
        print("Incorrect username or password!")

def account_menu(bank, user_id):
    while True:
        choice = banking_menu()
        if choice == 'a':
            amount = int(input("Enter how much you would like to deposit: "))
            bank.deposit(user_id, amount)
        elif choice == 'b':
            amount = int(input("Enter how much you would like to withdraw: "))
            bank.withdraw(user_id, amount)
        elif choice == 'c':
            balance = bank.get_balance(user_id)
            print("Your current balance is: $", balance)
        elif choice == 'd':
            delete_account(bank, user_id)
            print("Account deleted successfully!")
            return
        elif choice == 'e':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice!")

def banking_menu():
    print("*** BANKING MENU ***\n")
    print("a. Deposit Money")
    print("b. Withdraw Money")
    print("c. Check Balance")
    print("d. Delete Account")
    print("e. Return to Main Menu")
    return input("Enter your choice: ")

def delete_account(bank, user_id):
    confirm = input("Are you sure you want to delete your account? (yes/no): ")
    if confirm.lower() == 'yes':
        bank.delete_account(user_id)
    else:
        print("Account deletion cancelled.")

if __name__ == "__main__":
    main()
