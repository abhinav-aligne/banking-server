# Create virtual environment
# python -m venv .venv          (.venv is basically the environment folder)
# activation of virtual environment: .\.venv\Scripts\activate

'''
Creating a virtual bank system which holds the information of a customer account details
if a customer wants to deposit, withdrawal, transfer the funds then the customer can do it easily while inputing the infromation
'''
import random                                                       # importing random module for account numbers
class BankAccount():
    number_of_customers = 0                                         #it tracks the number of customers who opened the account
    account_number = random.randint(10000,100000)                   #it provides the random account number to that particular customer who opened the account
    balance = 0
    def __init__(self,name,phone_number,age,gender,pin,initial_deposit):       #constructor with the main parameters
        
        self.name = name                                            #name of the customer
        self.phone_number = phone_number                            #phone number of the cusomter
        self.age = age
        self.gender = gender
        self.account_balance = initial_deposit                      #account balance is initialized using the initial deposit parameter
        self.pin = pin                                              #customer account pin number
        self.customer_account_number = BankAccount.account_number   #customer account number is initialized using the BankAccount class attribute
        
        BankAccount.account_number += 1                             #BankAccount class attribute is incremented by 1 cuz if any customer adds another account then it will automatically added into BankAccount details
        BankAccount.number_of_customers += 1                        #keep track of number of customers via incrementation
        BankAccount.balance = self.account_balance

    def show_details(self):                                         #class method -1 which provides the information of the customer
        print(f'''\n\t\t Personal Details \n
                Name : {self.name}
                Age: {self.age}
                Gender: {self.gender}
                Account Number: {self.customer_account_number}
                Balance: {self.account_balance}''')
        
    def deposit(self):                                              #class method-2 which deposit the amount to the customer account
        amount = int(input("Enter the deposit amount: "))
        if amount > 0:
            self.account_balance = self.account_balance + amount
            print(f"The transaction is successful")
            print(f"Current Balance: {self.account_balance}")
            BankAccount.balance = self.account_balance
        else:
            print(f"Invalid amount")
            print(f"The trasaction is failed. Please try agian!")
            
    def withdraw(self):                                             #class method-2 which withdrawal the amount from the customer's account
        amount = int(input("Enter the withdrawal amount: "))
        if amount <= self.account_balance and amount > 0:
            self.account_balance = self.account_balance - amount
            print(f"Transaction Successfully Completed!")
            print(f"The account balance has been upadted | Current Balance : {self.account_balance}")
            BankAccount.balance = self.account_balance
        else:
            print(f"Transaction Failed!")
            print(f"Insuffient Funds | Current Balance: {self.account_balance}")
            
    def transfer(self,other):                                       #class method-3 which transfer the amount to the another account
        amount = int(input("Enter the transfer amount: "))
        if amount <= self.account_balance and amount > 0:
            self.account_balance = self.account_balance - amount
            other.account_balance = other.account_balance + amount
            print(f"Transaction Successfully Completed!")
            print(f"The account balance has been upadted")
            print(f"Current Balance of {self.name}: {self.account_balance}")
            BankAccount.balance = self.account_balance
        else:
            print(f"Transaction Failed!")
            print(f"Insuffient Funds | Current Balance: {self.account_balance}")