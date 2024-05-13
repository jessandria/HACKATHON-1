import random
import psycopg2 # to connect to sql 

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
        print("Account created successfully!")