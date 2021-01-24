import sqlite3
import random
"""Author: Enrique Chung """
"""The code below creates a simple banking system with a database created using sqlite"""

database =sqlite3.connect('card.s3db')
Options = ["1. Create an account","2. Log into account","0. Exit"]  #contains the options in the very front screen

#creates the table for the database
cur = database.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card'
            ' (given_name VARCHAR(20), '
            'family_name VARCHAR(20), '
            'number TEXT,pin TEXT,'
            ' balance INTEGER DEFAULT 0)')

"""This code generates a new card number for users
    @param: None
    @Worst Case: O(1)
    @Best Case: O(1)
    output: a card number"""
def createCardNumber():
    current = "400000"
    for i in range(0,9):
        current += str(random.randrange(0,9))
    current += create_checksum(current)
    return int(current)
"""This function creates a checksum value that is used to validate a card number
    @param: the first 15 digits of the card number
    @Worst Case: O(1)
    @Best Case: O(1)
    Output: checksum value"""
def create_checksum(digits):
    digitlist = list(digits)
    for i in range(0,15,2):
        digitlist[i] = int(digitlist[i])*2
    for i in range(0,15):
        if int(digitlist[i]) > 9:
            digitlist[i] = int(digitlist[i]) - 9
    sum = 0
    for i in digitlist:
        sum += int(i)
    if sum%10 ==0:
        return "0"
    else:
        return str(10- sum%10)


"""This function gets the balance of a card
    @param: the card number
    @Time complexity: O(log(n)) where n is the size of the table
    Output: The balance of the card"""
def get_balance(cardNum):
    cur.execute('SELECT Balance FROM card WHERE number =' + str(cardNum))
    card_balance = cur.fetchall()
    return card_balance[0][0]

"""This function creates a pin number for the user
    @param: None
    @Time complexity: O(1)
    Output: A pin number"""
def generatePin():
    current = ""
    for i in range(0,4):
        current += str(random.randrange(0,9))
    return str(current)

"""This function checks if the card number generated already exists in the table
    @param: Card number
    @Time complexity: O(log(n)) where n is the size of the table
    output: BOOLEAN"""
def is_available(cardNum):
    cur.execute('SELECT * FROM card where number =' + str(cardNum))
    cardnumber = cur.fetchone()
    print(cardnumber)
    if (cardnumber)== None:
        return True
    else:
        return False

"""This function generates the whole account for a person
    @param: None
    @Time complexity: O(log(n)) where n is the size of the table
    output: None"""
def generateAccount():
    possible_card_number = createCardNumber()
    while not is_available(possible_card_number):
        possible_card_number = createCardNumber()
    pin = generatePin()
    print("Enter your given name: ")
    given = input()
    print("Enter your family name: ")
    family = input()
    cur.execute('INSERT INTO card VALUES ("' +
                given +'","'
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
    output: Boolean"""
def check_details(cardNumber,pinNumber):

    cur.execute('SELECT * FROM card WHERE (number =' + cardNumber + ') AND pin ='+ pinNumber)
    validate = cur.fetchall()
    database.commit()
    if len(validate) != 0:
        return True
    else:
        return False

"""This function tells you if the cardNum received is valid (i.e it follows luhn's algorithm
    @param: Card number
    @Time complexity: O(1)
    Outpu: Boolean)"""
def is_valid(cardNum):
    if len(cardNum)!= 16:
        return False
    if cardNum[-1] == create_checksum(cardNum[:15]):
        return True
    else:
        return False
"""This function checks if the card exists in the database
    @param: card Number
    @Time complexity: O(log(n)) where n is the size of the table
    output: Boolean"""
def exists(cardNum):
    cur.execute('SELECT * FROM card WHERE number =' + cardNum)
    x = cur.fetchall()
    database.commit()
    if len(x) >0:
        return True
    else:
        return False

"""This function places a deposit into your account
    @param: Card number
    @Time complexity: O(log(n)) where n is the size of the table
    output: None
"""
def add_income(cardNum):
    print("How much would you like to add?")
    amount = input()
    cur.execute("UPDATE card SET  balance = '"  + amount + "' WHERE number ='"+ cardNum + "'")
    database.commit()
    print("Income was added!")


"""This function transfers money from one account to another
    @param: card to transfer to, card to transfer from
    @time complexity: O(log(n)) where n is the size of the table
    output: None"""
def transfer(num,cardNum):
    print("Enter how much money you want to transfer: ")
    amount = input()
    cur.execute('SELECT balance FROM card WHERE number =' + cardNum)
    balance = cur.fetchall()
    database.commit()
    if int(amount) > balance[0][0]:
        print("Not enough money! ")
    else:
        cur.execute('SELECT balance FROM card WHERE number ='+ num)
        current_balance = cur.fetchall()[0][0]
        database.commit()
        updated_balance = current_balance + int(amount)
        cur.execute("UPDATE card SET balance ='" + str(updated_balance) + "' WHERE number = '"+ num + "'")
        database.commit()
        cur.execute("UPDATE card SET balance = '" + str(balance[0][0]-int(amount))+"' WHERE number = '" + cardNum + "'")
        print("Success!")



"""This function serves as the main and runs the whole system."""
def menu():
    decision = None
    while decision != '0':
        for i in Options:
            print(i)
        decision  = input()
        if decision == '1':
            generateAccount()
        if decision == '2':
            print("Please enter your card number: ")
            cardNum = input()
            print("Please enter your pin: ")
            pin = input()
            if check_details(cardNum,pin):
                print("You have successfully logged in!")
                second_decision = None
                while second_decision != '5':
                    print("1. Balance")
                    print("2. Add income")
                    print("3. Do transfer")
                    print("4. Close account")
                    print("5. Log out")
                    print("0. Exit")
                    second_decision = input()

                    #The first option exits the loop and shuts down the system
                    if second_decision == "0":
                        second_decision = '5'
                        decision = '0'
                    #The second option returns the balance of the card
                    elif second_decision == "1":
                        cur.execute('SELECT balance FROM card WHERE number =' + str(cardNum))
                        balance = cur.fetchone()
                        database.commit()
                        print(balance[0])

                    #The third option adds to the balance
                    elif second_decision == "2":
                        add_income(cardNum)
                    #This option transfers money from one account to another
                    elif second_decision == "3":
                        print("Transfer")
                        print("Enter card number: ")
                        num = input()
                        if num == cardNum:
                            print("You can't transfer money to the same account!")
                        if not is_valid(num):
                            print("Probably you made a mistake in the card number. Please try again!")
                        elif not exists(num):
                            print("Such a card does not exist.")
                        else:
                            transfer(num,cardNum)
                    #This option closes the account
                    elif second_decision == "4":
                        cur.execute('DELETE FROM card WHERE number =' + cardNum)
                        database.commit()
                        print("The account has been closed! ")
                        second_decision = '5'
                    #This option logs out of the account
                    elif second_decision =="5":
                        print("successfully logged out")
                    else:
                        print("invalid command")
            else:
                print("Wrong card number or PIN!")
    if decision == '0':
            print("Bye!")
menu()
