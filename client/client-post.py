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
    1. Balance
    2. Deposit
    3. Withdraw
    4. Logout
    5. Exit
    """)

while True:
    clear()
    print("""WELCOME TO BANK CLIENT
    Please Choose What You Want To Do :
    1. signin
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
                CMD = "apicheck"
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
                CMD = "authcheck"
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
                    CMD = "authbalance"
                    PARAMS = {'username':USERNAME,'password':PASSWORD}
                    data = requests.post(__postcr__(),PARAMS).json()
                    print_bal(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '2':
                    clear()
                    CMD = "authdeposit"
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
                    CMD = "authbalance"
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
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            CMD = "signup"
            clear()
            PARAMS={'username':USERNAME,'password':PASSWORD}
            r = requests.post(__postcr__(),PARAMS).json()
            if str(r['status']) == "OK":
                print("Your Acount Is Created\n"+"Your Username :"+USERNAME+"\nYour API : "+r['api'])
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

