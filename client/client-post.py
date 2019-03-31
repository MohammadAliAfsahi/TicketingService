import requests
import os
import time
import platform
import sys

PARAMS = CMD = USERNAME = PASSWORD = API = ""
HOST = "localhost"
PORT = "1104"


def __postcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"?"


def print_bal(r):
    print("YOUR BALANCE IS : " + str(r['Balance']))


def print_depwith(r):
    print("YOUR OLD BALANCE IS : " + str(r['Old Balance'])
          +"\n"+"YOUR NEW BALANCE IS : "+str(r['New Balance']))

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def show_func():
    print("USERNAME : "+USERNAME+"\n"+"API : " + API)
    print("""What Do You Prefer To Do :
    1. Send Ticket
    2. Get Ticket
    3. Close Ticket
    4. Get ticket(Needs Admin privileges)
    5. Response to Ticket(Needs Admin privileges)
    6. Change Status of tickets(Needs Admin privileges)
    7. logout
    8. Exit
    """)

while True:
    clear()
    print("""WELCOME
    Please Choose What You Want To Do :
    1. login
    2. signup
    3. exit
    """)
    status = sys.stdin.readline()
    if status[:-1] == '1':
        clear()
        print("""What Kind Of Login Do You Prefer :
            1. API
            2. USERNAME | PASSWORD
            """)
        login_type = sys.stdin.readline()
        if login_type[:-1] == '1':
            clear()
            while True:
                print("API : ")
                API = sys.stdin.readline()[:-1]
                CMD = "login"
                PARAMS = {'api':API}
                r=requests.post(__postcr__(),params=PARAMS).json()
                if r['status'] == 'TRUE':
                    clear()
                    print("API IS CORRECT\nLogging You in ...")
                    USERNAME = r['username']
                    time.sleep(2)
                    break
                else:
                    clear()
                    print("API IS INCORRECT\nTRY AGAIN ...")
                    time.sleep(2)
            while True:
                clear()
                show_func()
                func_type = sys.stdin.readline()
                if func_type[:-1] == '1':
                    clear()
                    CMD = "apibalance"
                    PARAMS = {'api': API}
                    data = requests.post(__postcr__(),PARAMS).json()
                    print_bal(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '2':
                    clear()
                    CMD = "apideposit"
                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    PARAMS = {'api': API,'amount':amount}
                    data = requests.post(__postcr__(),PARAMS).json()
                    print_depwith(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '3':
                    clear()
                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    CMD = "apibalance"
                    PARAMS = {'api': API}
                    data = requests.post(__postcr__(),PARAMS).json()
                    if int(amount) > int(data['Balance']):
                        print("Insufficient Balance")
                        input("Press Any Key To Continue ...")
                    else:
                        CMD = "apiwithdraw"
                        PARAMS = {'api': API, 'amount': amount}
                        data = requests.post(__postcr__(),PARAMS).json()
                        print_depwith(data)
                        input("Press Any Key To Continue ...")
                if func_type[:-1] == '4':
                    break
                if func_type[:-1] == '5':
                    sys.exit()

        elif login_type[:-1] == '2':
            clear()
            while True:
                print("USERNAME : ")
                USERNAME = sys.stdin.readline()[:-1]
                print("PASSWORD : ")
                PASSWORD = sys.stdin.readline()[:-1]
                CMD = "login"
                PARAMS = {'username':USERNAME,'password':PASSWORD}
                r = requests.post(__postcr__(),PARAMS).json()
                if r['status'] == 'TRUE':
                    clear()
                    print("USERNAME AND PASSWORD IS CORRECT\nLogging You in ...")
                    API = r['api']
                    time.sleep(2)
                    break
                else:
                    clear()
                    print("USERNAME AND PASSWORD IS INCORRECT\nTRY AGAIN ...")
                    time.sleep(2)
            while True:
                clear()
                show_func()
                func_type = sys.stdin.readline()
                if func_type[:-1] == '1':
                    clear()
                    CMD = "sendticket"
                    PARAMS = {'username':USERNAME,'password':PASSWORD}
                    data = requests.post(__postcr__(),PARAMS).json()
                    print_bal(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '2':
                    clear()
                    CMD = "getticketcli"
                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    PARAMS = {'username': USERNAME, 'password': PASSWORD,'amount':amount}
                    data = requests.post(__postcr__(),PARAMS).json()
                    print_depwith(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '3':
                    clear()
                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    CMD = "closeticket"
                    PARAMS = {'username': USERNAME, 'password': PASSWORD}
                    data = requests.post(__postcr__(),PARAMS).json()
                    if(int(amount) > data['Balance']):
                        print("Insufficient Balance")
                        input("Press Any Key To Continue ...")
                    else:
                        CMD = "authwithdraw"
                        PARAMS = {'username': USERNAME, 'password': PASSWORD, 'amount': amount}
                        data = requests.post(__postcr__(),PARAMS).json()
                        print_depwith(data)
                        input("Press Any Key To Continue ...")
                if func_type[:-1] == '4':
                    break
                if func_type[:-1] == '5':
                    sys.exit()

    elif status[:-1] == '2':
        clear()
        while True:
            print("To Create New Account Enter The Authentication")
            print("USERNAME : ")
            while True:
                USERNAME = sys.stdin.readline()[:-1]
                if not USERNAME == "":
                    break
            print("PASSWORD : ")
            while True:
                PASSWORD = sys.stdin.readline()[:-1]
                if not PASSWORD == "":
                    break
            print("FIRST NAME:")
            FIRSTNAME = sys.stdin.readline()[:-1]
            print("LAST NAME:")
            LASTNAME = sys.stdin.readline()[:-1]
            CMD = "signup"
            clear()
            PARAMS={'username':USERNAME,'password':PASSWORD,'firstname':FIRSTNAME,'lastname':LASTNAME}
            r = requests.post(__postcr__(),PARAMS).json()
            if str(r['code']) == "200":
                print("Your Acount Is Created\n"+"Your Username :"+USERNAME+"\n")
                input("Press Any Key To Continue ...")
                break
            else :
                print(r['status']+"\n"+"Try Again")
                input("Press Any Key To Continue ...")
                clear()

    elif status[:-1] == '3':
        sys.exit()
    else:
        print("Wrong Choose Try Again")

