import random
import psycopg2

class User:
    def __init__(self, name, surname, card_number, password):
        self.name = name
        self.surname = surname
        self.card_number = card_number
        self.password = password

class BankingSystem:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="usersdatabase",
            user="postgres",
            password="pmlo14jessie",
            host="postgres",
            port="5433"
        )
        self.cur = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            name TEXT,
                            surname TEXT,
                            card_number TEXT UNIQUE,
                            password TEXT
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS savings (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER,
                            amount REAL DEFAULT 0,
                            FOREIGN KEY (user_id) REFERENCES users(id)
                            )''')
        self.conn.commit()
    
    def create_account(self):
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        password = input("Create a password: ")
        card_number = ''.join(str(random.randint(0, 9)) for _ in range(16))
        self.cur.execute('''INSERT INTO users (name, surname, card_number, password)
                            VALUES (%s, %s, %s, %s)''', (name, surname, card_number, password))
        self.conn.commit()
        print("Account created successfully!")
    
    def login(self):
        card_number = input("Enter your card number: ")
        password = input("Enter your password: ")
        self.cur.execute('''SELECT * FROM users WHERE card_number=%s''', (card_number,))
        user = self.cur.fetchone()
        if user:
            if user[4] == password:
                print("Login successful!")
                return user[0]  # Return user id
            else:
                print("Incorrect password.")
                return None
        else:
            print("User not found.")
            create_account = input("Do you want to create an account? (yes/no): ")
            if create_account.lower() == 'yes':
                self.create_account()
                return self.login()
            else:
                return None
    
    def add_money(self, user_id, amount):
        self.cur.execute('''UPDATE savings SET amount = amount + %s WHERE user_id = %s''', (amount, user_id))
        self.conn.commit()
        print("Money added successfully!")
    
    def withdraw_money(self, user_id, amount):
        self.cur.execute('''SELECT amount FROM savings WHERE user_id = %s''', (user_id,))
        current_balance = self.cur.fetchone()[0]
        if current_balance >= amount:
            self.cur.execute('''UPDATE savings SET amount = amount - %s WHERE user_id = %s''', (amount, user_id))
            self.conn.commit()
            print("Money withdrawn successfully!")
        else:
            print("Insufficient funds.")
    
    def transfer_money(self, sender_id, receiver_card_number, amount):
        self.cur.execute('''SELECT amount FROM savings WHERE user_id = %s''', (sender_id,))
        sender_balance = self.cur.fetchone()[0]
        if sender_balance >= amount:
            self.cur.execute('''SELECT id FROM users WHERE card_number = %s''', (receiver_card_number,))
            receiver = self.cur.fetchone()
            if receiver:
                receiver_id = receiver[0]
                self.cur.execute('''UPDATE savings SET amount = amount + %s WHERE user_id = %s''', (amount, receiver_id))
                self.cur.execute('''UPDATE savings SET amount = amount - %s WHERE user_id = %s''', (amount, sender_id))
                self.conn.commit()
                print("Money transferred successfully!")
            else:
                print("Receiver not found.")
        else:
            print("Insufficient funds.")
    
    def close_connection(self):
        self.conn.close()
        print("Connection closed.")

def main():
    print("Welcome to the Banking System!")
    bank = BankingSystem()
    while True:
        action = input("Do you want to Login or Create an account? (login/create): ")
        if action.lower() == 'create':
            bank.create_account()
        elif action.lower() == 'login':
            user_id = bank.login()
            if user_id is not None:
                break
        else:
            print("Invalid option.")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Add money to your account")
        print("2. Withdraw money from your account")
        print("3. Transfer money to another user")
        print("Type 'exit' to cancel.")
        choice = input("Enter your choice: ")
        if choice == '1':
            amount = float(input("Enter the amount to add: "))
            bank.add_money(user_id, amount)
        elif choice == '2':
            amount = float(input("Enter the amount to withdraw: "))
            bank.withdraw_money(user_id, amount)
        elif choice == '3':
            receiver_card_number = input("Enter the receiver's card number: ")
            amount = float(input("Enter the amount to transfer: "))
            bank.transfer_money(user_id, receiver_card_number, amount)
        elif choice.lower() == 'exit':
            break
        else:
            print("Invalid choice.")

    bank.close_connection()

if __name__ == "__main__":
    main()
