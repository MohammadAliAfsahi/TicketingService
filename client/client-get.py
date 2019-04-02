import requests
import os
import platform
import time
import sys
import platform


PARAMS = CMD = USERNAME = PASSWORD = API = TOKEN = ""
HOST = "localhost"
PORT = "1104"


def __authgetcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD


def __api__():
    return "http://" + HOST + ":" + PORT + "/" + CMD + "/" + API


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
       os.system('clear')


def show_func():
    print("USERNAME : "+USERNAME+"\n"+"TOKEN : " + TOKEN)
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
        while True:
            clear()
            print("""Enter :
            USERNAME | PASSWORD
                """)
            USERNAME = PASSWORD = ""
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
            CMD = "login"
            PARAMS = {'username':USERNAME,'password':PASSWORD}
            r = requests.get(__authgetcr__(),params=PARAMS).json()
            if r['code'] == '200':
                clear()
                TOKEN = r['token']
                print("USERNAME AND PASSWORD IS CORRECT\nLogging You in ...")
                print("Your token is : ",TOKEN)
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
                MESSAGE = ""
                SUBJECT = ""
                clear()
                CMD = "sendticket"
                print("Enter Your message subject:")
                while True:
                    SUBJECT = sys.stdin.readline()[:-1]
                    if not SUBJECT == "":
                        break
                print("Enter your message:")
                while True:
                    MESSAGE = sys.stdin.readline()[:-1]
                    if not MESSAGE == "":
                        break
                PARAMS = {'token':TOKEN,'subject':SUBJECT,'body':MESSAGE}
                data = requests.get(__authgetcr__(),params=PARAMS).json()
                if data['code'] == "200":
                    print(data['message']+"\n")
                    print("Ticket ID: "+str(data['id']))
                else :
                    print("Something went wrong!")
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '2':
                clear()
                CMD = "getticketcli"
                PARAMS = {'token':TOKEN}
                data = requests.get(__authgetcr__(),params=PARAMS).json()
                if data['code'] == "200":
                    for i in range(len(data)-2):
                        print("Subject : "+data['block '+str(i)]['subject']+"")
                        print("Message : "+data['block '+str(i)]['body']+"")
                        print("Status  : "+data['block '+str(i)]['status']+"")
                        print("date    : "+data['block '+str(i)]['date']+"")
                        print("ID      : "+str(data['block '+str(i)]['id']))
                        print("+---------------------------------------------+")  
                else:
                    print(data['status'])
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '3':
                clear()
                CMD = "closeticket"
                print("Enter Ticket's ID:")
                ID = ""
                while True:
                    ID = sys.stdin.readline()[:-1]
                    if not ID == "":
                        break
                PARAMS = {'token':TOKEN,'id':ID}
                data = requests.get(__authgetcr__(),params=PARAMS).json()
                if data['code'] == "200":
                    print(data['message'])
                else:
                    print(data)
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '4':
                CMD = "getticketmod"
                PARAMS = {'token':TOKEN}
                data = requests.get(__authgetcr__(),params=PARAMS).json()
                if data['code'] == "200":
                    for i in range(len(data)-2):
                        print("Subject : "+data['block '+str(i)]['subject']+"")
                        print("Message : "+data['block '+str(i)]['body']+"")
                        print("Status  : "+data['block '+str(i)]['status']+"")
                        print("date    : "+data['block '+str(i)]['date']+"")
                        print("ID      : "+str(data['block '+str(i)]['id']))
                        #print("Response: "+str(data['block '+str(i)]['response']))
                        print("+---------------------------------------------+")
                else:
                    print(data['status'])
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '5':
                CMD = "restoticketmod"
                ID = ""
                print("Enter Ticket's ID:")
                while True:
                    ID = sys.stdin.readline()[:-1]
                    if not ID == "":
                        break
                print("Enter your message:")
                MESSAGE = ""
                while True:
                    MESSAGE = sys.stdin.readline()[:-1]
                    if not MESSAGE == "":
                        break
                PARAMS = {'token':TOKEN,'id':ID,'body':MESSAGE}
                data = requests.get(__authgetcr__(),params=PARAMS).json()
                if data['code'] == "200":
                    print(data['message'])
                else:
                    print(data['status'])
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '6':
                CMD = "changestatus"
                ID = ""
                print("Enter Ticket's ID:")
                while True:
                    ID = sys.stdin.readline()[:-1]
                    if not ID == "":
                        break
                print("""Choose One of the Status:\n\t1. Open\n\t2. Close\n\t3. In Progress""")
                STATUS = 0
                while True:
                    STATUS = sys.stdin.readline()[:-1]
                    if not STATUS == "":
                        if STATUS == "1":
                            STATUS = "Open"
                        if STATUS == "2":
                            STATUS = "Close"
                        if STATUS == "3":
                            STATUS = "in progress" 
                        break
                PARAMS = {'token':TOKEN,'id':ID,'status':STATUS}
                data = requests.get(__authgetcr__(),params=PARAMS).json()
                if data['code'] == "200":
                    print(data['message'])
                else:
                    print(data['status'])
                input("Press Any Key To Continue ...")
                pass
            if func_type[:-1] == '7':
                CMD = "logout"
                PARAMS = {'username':USERNAME,'password':PASSWORD}
                data = requests.get(__authgetcr__(),params=PARAMS).json()
                if r['code'] == '200':
                    clear()
                    print("USERNAME AND PASSWORD IS CORRECT\nLogging You out ...")
                    print(r['message'])
                    time.sleep(2)
                    break
                else:
                    clear()
                    print("USERNAME AND PASSWORD IS INCORRECT\nTRY AGAIN ...")
                    time.sleep(2)
            if func_type[:-1] == '8':
                sys.exit()


    elif status[:-1] == '2':
        clear()
        while True:
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
            r = requests.get(__authgetcr__(),params=PARAMS).json()
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

