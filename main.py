from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector as SQL
from database import conn, cursor
from banking import BankAccount
# FastAPI app
app = FastAPI()

class BankAccount(BaseModel):
    account_number: str
    balance: float

class Transaction(BaseModel):
    account_number: str
    amount: float

# Routes
@app.post("/create_account/", response_model=BankAccount)
def create_account(account: BankAccount):
    try:
        query = "INSERT INTO accounts (account_number, balance) VALUES (%s, %s)"
        cursor.execute(query, (account.account_number, account.balance))
        conn.commit()
        return account
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

@app.get("/get_balance/{account_number}", response_model=BankAccount)
def get_balance(account_number: str):
    try:
        query = "SELECT account_number, balance FROM accounts WHERE account_number = %s"
        cursor.execute(query, (account_number,))
        account = cursor.fetchone()
        if account:
            return {"account_number": account[0], "balance": float(account[1])}
        else:
            raise HTTPException(status_code=404, detail="Account not found")
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

@app.post("/deposit/", response_model=BankAccount)
def deposit(transaction: Transaction):
    try:
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        cursor.execute(query, (transaction.amount, transaction.account_number))
        conn.commit()
        return get_balance(transaction.account_number)  # Return updated balance
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

@app.post("/withdraw/", response_model=BankAccount)
def withdraw(transaction: Transaction):
    try:
        query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
        cursor.execute(query, (transaction.amount, transaction.account_number))
        conn.commit()
        return get_balance(transaction.account_number)  # Return updated balance
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

