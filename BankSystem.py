import sqlite3
import random

"""Author: Enrique Chung """
"""The code below creates a simple banking system with a database created using sqlite"""
"""This code generates a new card number for users
    @param: None
    @Time complexity: O(1)
    @Output: a card number"""


def create_card_number():
    current = "400000"
    for i in range(9):
        current += str(random.randrange(0, 9))
    current += create_checksum(current)
    return int(current)


"""This function creates a checksum value that is used to validate a card number.
    This is done using Luhn's Algorithm.
    @param: the first 15 digits of the card number
    @Time Complexity: O(1)
    @Output: checksum value"""


def create_checksum(digits):
    digit_list = list(digits)
    for i in range(0, 15, 2):
        digit_list[i] = int(digit_list[i]) * 2

    for i in range(15):
        if int(digit_list[i]) > 9:
            digit_list[i] = int(digit_list[i]) - 9
    total = 0
    for i in digit_list:
        total += int(i)
    if total % 10 == 0:
        return "0"
    else:
        return str(10 - total % 10)


"""This function gets the balance of a card
    @param: the card number
    @Time complexity: O(log(n)) where n is the size of the table
    @Output: The balance of the card"""


def get_balance(card_num):
    cur.execute("SELECT Balance FROM card WHERE number =" + card_num)
    card_balance = cur.fetchall()
    return card_balance[0][0]


"""This function creates a pin number for the user
    @param: None
    @Time complexity: O(1)
    @Output: A pin number"""


def generate_pin():
    current = ""
    for i in range(4):
        current += str(random.randrange(0, 9))
    return str(current)


"""This function checks if the card number generated already exists in the table
    @param: Card number
    @Time complexity: O(log(n)) where n is the size of the table
    @Output: BOOLEAN"""


def is_available(card_num):
    cur.execute("SELECT * FROM card where number = " + str(card_num))
    card_number = cur.fetchone()
    database.commit()
    if card_number is None:
        return True
    else:
        return False


"""This function generates the whole account for a person
    @param: None
    @Time complexity: O(log(n)) where n is the size of the table
    @Output: None"""


def generate_account():
    possible_card_number = create_card_number()
    while not is_available(possible_card_number):
        possible_card_number = create_card_number()
    pin = generate_pin()
    print("Enter your given name: ")
    given = input()
    print("Enter your family name: ")
    family = input()
    cur.execute('INSERT INTO card VALUES ("' +
                given + '","'
                + family + '","'
                + str(possible_card_number) + '","'
                + pin + '",0)')
    database.commit()
    print("Your card has been created")
    print("Your card number: ")
    print(possible_card_number)
    print("Your pin number: ")
    print(pin)


"""This function checks if the details of the log in is correct. 
    @param: Card Number and Pin 
    @Time Complexity: O(log(n)) where n is the size of the table
    @Output: Boolean"""


def check_details(card_number, pin_number):
    cur.execute("SELECT * FROM card WHERE (number = " + card_number + ") AND pin =" + pin_number)
    validate = cur.fetchall()
    database.commit()
    if len(validate) != 0:
        return True
    else:
        return False


"""This function tells you if the cardNum received is valid (i.e it follows luhn's algorithm
    @param: Card number
    @Time complexity: O(1)
    @Output: Boolean)"""


def is_valid(card_number):
    if len(card_number) != 16:
        return False
    if card_number[-1] == create_checksum(card_number[:15]):
        return True
    else:
        return False


"""This function checks if the card exists in the database
    @param: card Number
    @Time complexity: O(log(n)) where n is the size of the table
    @Output: Boolean"""


def exists(card_number):
    cur.execute('SELECT * FROM card WHERE number =' + card_number)
    x = cur.fetchall()
    database.commit()
    if len(x) > 0:
        return True
    else:
        return False


"""This function places a deposit into your account
    @param: Card number
    @Time complexity: O(log(n)) where n is the size of the table
    @Output: None
"""


def add_income(card_number,amount):

    cur.execute("SELECT balance FROM card WHERE number = '" + card_number + "'")
    current_balance = cur.fetchall()[0][0]
    database.commit()
    new_balance = current_balance + int(amount)
    cur.execute("UPDATE card SET  balance = '" + str(new_balance) + "' WHERE number ='" + card_number + "'")
    database.commit()


"""This function transfers money from one account to another
    @param: card to transfer to, card to transfer from
    @time complexity: O(log(n)) where n is the size of the table
    @Output: None"""


def transfer(num, card_number):
    print("Enter how much money you want to transfer: ")
    amount = input()
    cur.execute('SELECT balance FROM card WHERE number =' + card_number)
    balance = cur.fetchall()
    database.commit()
    if int(amount) > balance[0][0]:
        print("Not enough money! ")
    else:
        cur.execute('SELECT balance FROM card WHERE number =' + num)
        database.commit()
        add_income(num,amount)
        add_income(card_number,'-' + amount)
        print("Success!")


"""This function prints all the options after you have logged in
    @param: None
    @Time complexity: O(1)
    @Output: None"""


def print_options():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


"""This function serves as the main and runs the whole system."""

def menu():
    decision = None
    while decision != '0':
        for i in Options:
            print(i)
        decision = input()
        if decision == '1':
            generate_account()
        if decision == '2':
            print("Please enter your card number: ")
            your_card_number = input()
            print("Please enter your pin: ")
            pin = input()
            if check_details(your_card_number, pin):
                print("You have successfully logged in!")
                second_decision = None
                while second_decision != '5':
                    print_options()
                    second_decision = input()

                    # The first option exits the loop and shuts down the system
                    if second_decision == "0":
                        second_decision = '5'
                        decision = '0'
                    # The second option returns the balance of the card
                    elif second_decision == "1":
                        cur.execute('SELECT balance FROM card WHERE number =' + str(your_card_number))
                        balance = cur.fetchone()
                        database.commit()
                        print(balance[0])

                    # The third option adds to the balance
                    elif second_decision == "2":
                        print("How much would you like to add?")
                        amount = input()
                        while not amount.isdigit():
                            print("invalid input, please enter a number: ")
                            amount = input()
                        add_income(your_card_number,amount)
                        print("Income was added!")
                    # This option transfers money from one account to another
                    elif second_decision == "3":
                        print("Transfer")
                        print("Enter card number: ")
                        num = input()
                        if num == your_card_number:
                            print("You can't transfer money to the same account!")
                        if not is_valid(num):
                            print("Probably you made a mistake in the card number. Please try again!")
                        elif not exists(num):
                            print("Such a card does not exist.")
                        else:
                            transfer(num, your_card_number)
                    # This option closes the account
                    elif second_decision == "4":
                        cur.execute('DELETE FROM card WHERE number =' + your_card_number)
                        database.commit()
                        print("The account has been closed! ")
                        second_decision = '5'
                    # This option logs out of the account
                    elif second_decision == "5":
                        print("successfully logged out")
                    else:
                        print("invalid command")
            else:
                print("Wrong card number or PIN!")
        else:
            print("invalid command")
    if decision == '0':
        print("Bye!")


if __name__ == "__main__":
    database = sqlite3.connect('card.s3db')
    Options = ["1. Create an account", "2. Log into account",
               "0. Exit"]  # contains the options in the very front screen

    # creates the table for the database
    cur = database.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card'
                ' (given_name VARCHAR(20), '
                'family_name VARCHAR(20), '
                'number TEXT,pin TEXT,'
                ' balance INTEGER DEFAULT 0)')
    menu()
