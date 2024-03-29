import os.path
import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
from binascii import hexlify
import tornado.web
from tornado.options import define, options

define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="ticket", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="", help="blog database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # POST METHOD :
            (r"/signup", signup),
            (r"/closeticket", closeticket),  # Balance Using API Format : /closeticket/API
            (r"/getticketcli", getticketcli),# Balance Using Authentication Format : /getticketcli/Username/Password
            (r"/getticketmod", getticketmod),  # deposit Using API Format : /getticketmod/API/Amount
            (r"/changestatus", changestatus), # deposit Using Authentication Format : /changestatus/Username/Password/Amount
            (r"/restoticketmod", restoticketmod),# Withdeaw Using API Format : /restoticketmod/API/amount
            (r"/login", login),
            (r"/logout", logout),
            (r"/sendticket", sendticket), # Withdraw using  AuthenticationFormat : /restoticketmod/username/password/amount
            (r".*", defaulthandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def check_user(self,user):
        resuser = self.db.get("SELECT * from user where username = %s",user)
        if resuser:
            return True
        else :
            return False

    def check_api(self,api):
        resuser = self.db.get("SELECT * from user where apitoken = %s", api)
        if resuser:
            return True
        else:
            return False
    def check_auth(self,username,password):
        resuser = self.db.get("SELECT * from user where username = %s and password = %s", username,password)
        if resuser:
            return True
        else:
            return False

class defaulthandler(BaseHandler):
    def get(self):
        output = {'status':'Wrong Command','code':"201"}
        self.write(output)

    def post(self, *args, **kwargs):
        output = {'status':'Wrong Command','code':"201"}
        self.write(output)

class signup(BaseHandler):
    def get(self,*args):
        username = self.get_argument('username')
        password = self.get_argument('password')
        firstname = self.get_argument('firstname')
        lastname = self.get_argument('lastname')
        if not self.check_user(username):
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("INSERT INTO user (username, password, firstname ,lastname,apitoken,admin) "
                                     "values (%s,%s,%s,%s,%s,%s) "
                                     , username,password,firstname,lastname,api_token,False)

            output = {
                        "message": "Signed Up Successfully",
                        "code": "200"
                    }

            self.write(output)
        else:
            output = {'status': 'User Exist','code':"201"}
            self.write(output)
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        firstname = self.get_argument('firstname')
        lastname = self.get_argument('lastname')
        if not self.check_user(username):
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("INSERT INTO user (username, password, firstname, lastname, apitoken, admin) "
                                     "values (%s,%s,%s,%s,%s,%s)"
                                     , username,password,firstname,lastname,api_token,False)

            output = {
                        "message": "Signed Up Successfully",
                        "code": "200"
                    }
            self.write(output)
        else:
            output = {'code': '201', 'status':"User Exist"}
            self.write(output)

class login(BaseHandler):
    def get(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username,password):
            api_token = str(hexlify(os.urandom(16)))
            self.db.execute("UPDATE user set apitoken=%s where username=%s and password = %s",api_token,username,password)
            user = self.db.get("SELECT * from user where username = %s and password = %s", username, password)
            output = {
                    "message": "Logged in Successfully",
                    "code": "200",
                     "token" : user.apitoken,
                    }
            self.write(output)
        else:
            output = {'status': 'FALSE','code':"201"}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username,password):
            api_token = str(hexlify(os.urandom(16)))
            self.db.execute("UPDATE user set apitoken=%s where username=%s and password = %s",api_token,username,password)
            user = self.db.get("SELECT * from user where username = %s and password = %s", username, password)
            output = {
                    "message": "Logged in Successfully",
                    "code": "200",
                     "token" : user.apitoken,
                    }
            self.write(output)
        else:
            output = {'status': 'FALSE',
                       'code':"201" }
            self.write(output)

class logout(BaseHandler):
    def get(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username,password):
            self.db.execute("UPDATE user set apitoken=%s where username=%s and password = %s"," ",username,password)
            output = {
                        "message": "Logged Out Successfully",
                        "code": "200"
                    }
            self.write(output)
        else:
            output = {'status': 'FALSE','code':"201"}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username,password):
            self.db.execute("UPDATE user set apitoken=%s where username=%s and password = %s"," ",username,password)
            output = {
                        "message": "Logged Out Successfully",
                        "code": "200"
                        }
            self.write(output)
        else:
            output = {'status': 'FALSE','code':"201"}
            self.write(output)

class sendticket(BaseHandler):
    def get(self, *args,**kwargs):
        token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken=%s", token)
            status = "Open"
            ticket_id = self.db.execute("INSERT INTO tickets (subject, body, status, userid) "
                                     "values (%s,%s,%s,%s) "
                                     , subject,body,status,user.id)
            output ={
                        "message": "Ticket Sent Successfully",
                        "id": ticket_id,
                        "code": "200"
                    } 
            self.write(output)
        else:
            output = {'code': '400'}
            self.write(output)

    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken=%s", token)
            status = "Open"
            ticket_id = self.db.execute("INSERT INTO tickets (subject, body, status, userid) "
                                     "values (%s,%s,%s,%s)"
                                     , subject,body,status,user.id)
            output ={
                        "message": "Ticket Sent Successfully",
                        "id": ticket_id,
                        "code": "200"
                    }
            self.write(output)

        else:
            output = {'code': '400'}
            self.write(output)

class closeticket(BaseHandler):
    def get(self,*args):
        api_token = self.get_argument('token')
        id_ticket = self.get_argument('id')
        if self.check_api(api_token):
            self.db.get("SELECT * from user where apitoken = %s",api_token)
            self.db.execute("UPDATE tickets set status=%s where id = %s","Close",id_ticket)
            message = "Ticket With id -"+str(id_ticket)+"- Closed Successfully"
            output = {
                        "message": message,
                        "code": "200"
                    }
            self.write(output)

        else :
            self.write("Wrong API")
    def post(self, *args, **kwargs):
        api_token = self.get_argument('token')
        id_ticket = self.get_argument('id')
        if self.check_api(api_token):
            self.db.get("SELECT * from user where apitoken = %s",api_token)
            self.db.execute("UPDATE tickets set status=%s where id = %s","Close",id_ticket)
            message = "Ticket With id -"+str(id_ticket)+"- Closed Successfully"
            output = {
                        "message": message,
                        "code": "200"
                    }

            self.write(output)
        else :
            self.write("Wrong API")

class getticketcli(BaseHandler):
    def get(self,*args):
        token = self.get_argument('token')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            tickets = self.db.query("SELECT * from tickets where userid = %s",user.id)
            No = "There Are -"+str(len(tickets))+"- Ticket"
            output = {
                        "tickets": No,
                        "code": "200"
                    }
            for i in range(len(tickets)):
                block = {
                            "subject" : tickets[i]['subject'],
                            "body" : tickets[i]['body'],
                            "status" : tickets[i]['status'],
                            "id" : tickets[i]['id'],
                            "date" : str(tickets[i]["date"])
                        }
                string = "block "+str(i)
                output.update({string:block})

            self.write(output)
        else :
            output = {'status':'Wrong Authentication','code':"400"}
            self.write(output)
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            tickets = self.db.query("SELECT * from tickets where userid = %s",user.id)
            No = "There Are -"+str(len(tickets))+"- Ticket"
            output = {
                        "tickets": No,
                        "code": "200"
                    }
            for i in range(len(tickets)):
                block = {
                            "subject" : tickets[i]['subject'],
                            "body" : tickets[i]['body'],
                            "status" : tickets[i]['status'],
                            "id" : tickets[i]['id'],
                            "date" : str(tickets[i]["date"])
                        }
                string = "block "+str(i)
                output.update({string:block})

            self.write(output)
        else :
            output = {'status': 'Wrong Authentication','code':"400"}
            self.write(output)


class getticketmod(BaseHandler):
    def get(self,*args):
        token = self.get_argument('token')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            if user.admin == True:
                tickets = self.db.query("SELECT * from tickets")
                No = "There Are -"+str(len(tickets))+"- Ticket"
                output = {
                            "tickets": No,
                            "code": "200"
                        }
                for i in range(len(tickets)):
                    block = {
                                "subject" : tickets[i]['subject'],
                                "body" : tickets[i]['body'],
                                "status" : tickets[i]['status'],
                                "id" : tickets[i]['id'],
                                "date" : str(tickets[i]["date"])
                            }
                    string = "block "+str(i)
                    output.update({string:block})

                self.write(output)
            else:
                self.write({'status':"You don't have permission for this section",'code':"201"})
        else :
            output = {'status':'Wrong Authentication','code':"201"}
            self.write(output)
    
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            if user.admin == True:
                tickets = self.db.query("SELECT * from tickets")
                No = "There Are -"+str(len(tickets))+"- Ticket"
                output = {
                            "tickets": No,
                            "code": "200"
                        }
                for i in range(len(tickets)):
                    block = {
                                "subject" : tickets[i]['subject'],
                                "body" : tickets[i]['body'],
                                "status" : tickets[i]['status'],
                                "id" : tickets[i]['id'],
                                "date" : str(tickets[i]["date"])
                            }
                    string = "block "+str(i)
                    output.update({string:block})

                self.write(output)
            else:
                self.write({'status':"You don't have permission for this section",'code':"400"})
        else :
            output = {'status': 'Wrong Authentication','code':"400"}
            self.write(output)

class changestatus(BaseHandler):
    def get(self,*args):
        token = self.get_argument('token')
        id_ticket = self.get_argument('id')
        status = self.get_argument('status')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            if user.admin == True:
                self.db.execute("UPDATE tickets set status=%s where id = %s", status,id_ticket)
                output = {
                            "message": "Status Ticket With id -"+str(id_ticket)+"- Changed Successfully",
                            "code": "200"
                        }
                self.write(output)
            else:
                self.write({'status':"You don't have permission for this section",'code':"201"})
        else :
            output = {'status':'Wrong Authentication','code':"201"}
            self.write(output)
        
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        id_ticket = self.get_argument('id')
        status = self.get_argument('status')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            if user.admin == True:
                self.db.execute("UPDATE tickets set status=%s where id = %s", status, id_ticket)
                output = {
                            "message": "Status Ticket With id -"+str(id_ticket)+"- Changed Successfully",
                            "code": "200"
                        }
                self.write(output)
            else:
                self.write({'status':"You don't have permission for this section",'code':"201"})
        else :
            output = {'status':'Wrong Authentication','code':"201"}
            self.write(output)


class restoticketmod(BaseHandler):
    def get(self,*args):
        token = self.get_argument('token')
        id_ticket = self.get_argument('id')
        body = self.get_argument('body')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            if user.admin == True:
                self.db.execute("UPDATE tickets set response=%s where id = %s", body, id_ticket)
                output = {
                            "message": "Response to Ticket With id -"+str(id_ticket)+"- Sent Successfully",
                            "code": "200"
                        }
                self.write(output)
            else:
                self.write({'status':"You don't have permission for this section",'code':"201"})
        else :
            output = {'status':'Wrong Authentication','code':"201"}
            self.write(output)
        
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        id_ticket = self.get_argument('id')
        body = self.get_argument('body')
        if self.check_api(token):
            user = self.db.get("SELECT * from user where apitoken = %s", token)
            if user.admin == True:
                self.db.execute("UPDATE tickets set response=%s where id = %s", body, id_ticket)
                output = {
                            "message": "Response to Ticket With id -"+str(id_ticket)+"- Sent Successfully",
                            "code": "200"
                        }
                self.write(output)
            else:
                self.write({'status':"You don't have permission for this section",'code':"201"})
        else :
            output = {'status':'Wrong Authentication','code':"201"}
            self.write(output)


class help(BaseHandler):
    def get(self, *args, **kwargs):
       self.write("Tornado is Runnig")

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
