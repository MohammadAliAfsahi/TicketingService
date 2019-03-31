import requests
import os
import platform
import time
import sys
import platform

PARAMS = CMD = USERNAME = PASSWORD = API = ""
HOST = "192.168.0.105"
PORT = "1104"


def __authgetcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"/"+USERNAME+"/"+PASSWORD


def __api__():
    return "http://" + HOST + ":" + PORT + "/" + CMD + "/" + API


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
                r=requests.get(__api__()).json()
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
                    data = requests.get(__api__()).json()
                    print_bal(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '2':
                    clear()
                    CMD = "apideposit"
                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    data = requests.get(__api__()+"/"+amount).json()
                    print_depwith(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '3':
                    clear()
                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    CMD = "apibalance"
                    data = requests.get(__api__()).json()
                    if int(amount) > int(data['Balance']):
                        print("Insufficient Balance")
                        input("Press Any Key To Continue ...")
                    else:
                        CMD = "apiwithdraw"
                        data = requests.get(__api__() + "/" + amount).json()
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
                r = requests.get(__authgetcr__()).json()
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
                    data = requests.get(__authgetcr__()).json()
                    print_bal(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '2':
                    clear()
                    CMD = "authdeposit"
                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    data = requests.get(__authgetcr__()+"/"+amount).json()
                    print_depwith(data)
                    input("Press Any Key To Continue ...")
                if func_type[:-1] == '3':
                    clear()

                    print("Enter Your Amount : ")
                    amount = sys.stdin.readline()[:-1]
                    CMD = "authbalance"
                    data = requests.get(__authgetcr__()).json()
                    if(int(amount) > data['Balance']):
                        print("Insufficient Balance")
                        input("Press Any Key To Continue ...")
                    else:
                        CMD = "authwithdraw"
                        data = requests.get(__authgetcr__()+"/"+amount).json()
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
            r = requests.get(__authgetcr__()).json()
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

