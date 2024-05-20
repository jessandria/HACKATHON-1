import random
import psycopg2 # to connect to sql 


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
        elif action.lower()== 'exit':
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


# initiate the class - User
class User:
    def __init__(self, name, surname, card_number, password):
        self.name = name
        self.surname = surname
        self.card_number = card_number
        self.password = password

# class Banking system 
class BankingSystem:

    #connection to PostgreSQL database

    def __init__(self):
        self.connection = psycopg2.connect(
            database="usersdatabase",
            user="postgres",
            password="pmlo14jessie",
            host="localhost",
            port="5433"
        )
        self.cursor = self.connection.cursor()

    #create account
    def create_account(self):
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        password = input("Create a password: ")
        card_number = ''.join(str(random.randint(0, 9)) for _ in range(6))
        self.cursor.execute('''INSERT INTO users (name, surname, card_number, password)
                            VALUES (%s, %s, %s, %s)''', (name, surname, card_number, password))
        self.connection.commit()
        print(f"Account created successfully! \nYour card number is : {card_number}")
    
    #login
    def login(self):
        card_number = input("Enter your card number: ")
        password = input("Enter your password: ")
        self.cursor.execute('''SELECT * FROM users WHERE card_number=%s''', (card_number,))
        user = self.cursor.fetchone()
        
        if user:
            if user[4] == password: #user[4] corresponds to the password column in the database
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
    
    # add money        
    def add_money(self, user_id, amount):
        self.cursor.execute('''UPDATE savings SET amount = amount + %s WHERE user_id = %s''', (amount, user_id))
        self.connection.commit()
        print("Money added successfully!")

    #withdraw_money
    def withdraw_money(self, user_id, amount):
        self.cursor.execute('''SELECT amount FROM savings WHERE user_id = %s''', (user_id,))
        current_balance = self.cursor.fetchone()[0]
        self.connection.commit
        
        if current_balance >= amount:
            self.cursor.execute('''UPDATE savings SET amount = amount - %s WHERE user_id = %s''', (amount, user_id))
            self.connection.commit()
            print("Money withdrawn successfully!")
        else:
            print("Insufficient funds.")

    #transfer money
    def transfer_money(self, sender_id, receiver_card_number, amount):
        self.cursor.execute('''SELECT amount FROM savings WHERE user_id = %s''', (sender_id,))
        sender_balance = self.cursor.fetchone()[0] #retrieve the amount 
        
        if sender_balance >= amount:
            self.cursor.execute('''SELECT id FROM users WHERE card_number = %s''', (receiver_card_number,))
            receiver = self.cursor.fetchone()
            if receiver:
                receiver_id = receiver[0]
                self.cursor.execute('''UPDATE savings SET amount = amount + %s WHERE user_id = %s''', (amount, receiver_id))
                self.cursor.execute('''UPDATE savings SET amount = amount - %s WHERE user_id = %s''', (amount, sender_id))
                self.connection.commit()
                print("Money transferred successfully!")
            else:
                print("Receiver not found.")
        else:
            print("Insufficient funds.")

    def close_connection(self):
        self.connection.close()
        print("Connection closed.")

#   if the actual script is being run, the function main() is called    
if __name__ == "__main__":
    main()
    