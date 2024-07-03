from banking import BankAccount
import mysql.connector as SQL

def connectivity():
    global conn,cur
    try:
        conn = SQL.connect(
            user ='root',
            password = "Aligne",
            host = "localhost",
            port = 3306
        )
    except Exception as e:
        print("cannot connect")
    cur = conn.cursor()
    # # 1-> cur.execute("CREATE DATABASE banking")
    sql1 = "USE banking"
    cur.execute(sql1)
    sql2 = '''
                    CREATE TABLE IF NOT EXISTS records
                    (
                        account_no INT PRIMARY KEY,
                        name VARCHAR(100),
                        age INT NOT NULL,
                        gender VARCHAR(10), 
                        phone_number VARCHAR(20) UNIQUE NOT NULL,
                        pin INT,
                        balance FLOAT NOT NULL
                    )
                    '''
    cur.execute(sql2)    

connectivity()

customer_details = {}                 # use account no. as key and class object (customer account) as value (KEY:VALUE)
mobile_link = {}                      # use mobile no. as key and store account no. as value, for linking purpose
def new_customer():
    global name, phone_number, age, gender,pin
    name = input('Enter the name of customer: ')
    phone_number = int(input("Mobile Number must be of 6 digits. Enter mobile number: "))
    if len(str(phone_number)) != 6:
        print('Invalid Number')
        return
    age = int(input("Enter the age: "))
    gender = input("Enter your gender: ")
    initial_deposit = float(input('Enter the initial deposit amount: '))
    if initial_deposit <= 0:
        print('Invalid Amount')
        return
    pin = int(input('Pin must be of 3 digits. Create PIN: '))
    if len(str(pin)) != 3 :
        print('Invalid Pin')
        return
    
    customer = BankAccount(name=name, phone_number=phone_number, age=age, gender=gender, pin = pin, initial_deposit = initial_deposit)
    customer_details[customer.customer_account_number] = customer                   # account. no. stored as key and oject as value
    mobile_link[customer.phone_number] = customer.customer_account_number           # mobile number linked
    print("\n\t\t\t New User Created! ")
    print(f'\tWelcome {customer.name} to Bank. {customer.customer_account_number} is your account number\n')

def login():
    account_number = int(input('Enter your Account Number: '))
    account_pin = int(input('Enter your Account PIN: '))
    if account_number in customer_details.keys() and account_pin == customer_details[account_number].pin :
        print(f'\n{customer_details[account_number].name} Logged in')
        customer_details[account_number].show_details()
    else:
        print('Account either not exist or the pin is wrong')
        return
    while True:
        user_input = input('''
                            Press 1 for deposit:
                            Press 2 for withdrawl:
                            Press 3 for money transfer:
                            Press 4 to log out
                            ''')
        if user_input == '1':
            customer_details[account_number].deposit()
            # update_balance(BankAccount.balance, BankAccount.account_number)
            query_deposit = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
            cur.execute(query_deposit, (BankAccount.amount, BankAccount.account_number))
            conn.commit()
        
        elif user_input == '2':
            customer_details[account_number].withdraw()
            # update_balance(BankAccount.balance, BankAccount.account_number)
            query_withdraw = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
            cur.execute(query_withdraw, (BankAccount.amount, BankAccount.account_number))
            conn.commit()
            
        elif user_input == '3':
            mobile = int(input('Enter the mobile number of recepient: '))
            if mobile in mobile_link.keys():
                secondary = mobile_link[mobile]             # use mobile no. to get account details.
                customer_details[account_number].transfer(customer_details[secondary])
            else:
                print('The mobile number you have enter does not have an account associated with it')
        elif user_input == '4':
            print('Logged Out')
            return
        else:
            print('Invalid input try again')
        print('\n#############################################################\n')
        customer_details[account_number].show_details()


while True:
    user_input = input('''
                        Press 1 for creating a new customer:
                        Press 2 for logging in as an existing customer:
                        Press 3 for displaying number of customers:
                        Press 4 for exit
                        ''')

    if user_input == '1':
        print("Create user")
        new_customer() 
        connectivity( )
        sql_query = '''INSERT INTO records
                        (account_no,name,age,gender,phone_number,pin,balance)
                        VALUES(%s,%s,%s,%s,%s,%s,%s)
                    '''
        try:
            cur.execute(sql_query,((BankAccount.account_number-1),name,age, gender,phone_number,pin,BankAccount.balance))
            conn.commit()
            print("-"*50)

        except Exception as error:
            conn.rollback()
            print("Something went wrong.",error)   
        cur.close()
        conn.close() 
                 
    elif user_input == '2':
        login()
    elif user_input == '3':
        print(f"There currently {BankAccount.number_of_customers} customers in bank.")
    elif user_input == '4':
        print('\t\t Thank You for using the code.')
        print("\t\t © Abhinav Gera \n\n")
        break
    else:
        print('Invalid input try again')