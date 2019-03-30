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
            #GET METHOD :
            (r"/signup/([^/]+)/([^/]+)", signup),
            (r"/getTicket/([^/]+)", getTicket), #Balance Using API Format : /getTicket/API
            (r"/GetTicket/([^/]+)/([^/]+)", GetTicket),  # Balance Using Authentication Format : /GetTicket/Username/Password
            (r"/apideposit/([^/]+)/([^/]+)", apideposit),  # deposit Using API Format : /apideposit/API/Amount
            (r"/ChangeStatus/([^/]+)/([^/]+)/([^/]+)", ChangeStatus),  # deposit Using Authentication Format : /ChangeStatus/Username/Password/Amount
            (r"/apiwithdraw/([^/]+)/([^/]+)", apiwithdraw), # Withdraw Using API Format : /apiwithdraw/API/amount
            (r"/SendTicket/([^/]+)/([^/]+)/([^/]+)", SendTicket),   # Withdeaw using  AuthenticationFormat : /apiwithdraw/username/password/amount
            (r"/login/([^/]+)/([^/]+)", login),
            (r"/logout/([^/]+)", logout),
            # POST METHOD :
            (r"/signup", signup),
            (r"/getTicket", getTicket),  # Balance Using API Format : /getTicket/API
            (r"/GetTicket", GetTicket),# Balance Using Authentication Format : /GetTicket/Username/Password
            (r"/apideposit", apideposit),  # deposit Using API Format : /apideposit/API/Amount
            (r"/ChangeStatus", ChangeStatus), # deposit Using Authentication Format : /ChangeStatus/Username/Password/Amount
            (r"/apiwithdraw", apiwithdraw),# Withdeaw Using API Format : /apiwithdraw/API/amount
            (r"/login", login),
            (r"/logout", logout),
            (r"/SendTicket", SendTicket), # Withdeaw using  AuthenticationFormat : /apiwithdraw/username/password/amount
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
        resuser = self.db.get("SELECT * from user where api = %s", api)
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
        output = {'status':'Wrong Command'}
        self.write(output)

    def post(self, *args, **kwargs):
        output = {'status':'Wrong Command'}
        self.write(output)


class signup(BaseHandler):
    def get(self,*args):
        if not self.check_user(args[0]):
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("INSERT INTO user (username, password, firstname ,lastname,apitoken) "
                                     "values (%s,%s,%s,%s) "
                                     , args[0],args[1],args[2],args[3],api_token)

            output = {'api': api_token,
                      'status': 'OK'}
            self.write(output)
        else:
            output = {'status': 'User Exist'}
            self.write(output)
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        firstname = self.get_argument('firstname')
        lastname = self.get_argument('lastname')
        if not self.check_user(username):
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("INSERT INTO user (username, password, firstname, lastname, apitoken) "
                                     "values (%s,%s,%s,%s) "
                                     , username,password,firstname,lastname,api_token)

            output = {'api' : api_token,
                      'status' : 'OK'}
            self.write(output)
        else:
            output = {'status': 'User Exist'}
            self.write(output)

class getTicket(BaseHandler):
    def get(self,*args):
        if self.check_api(args[0]):
            user = self.db.get("SELECT * from user where api = %s",args[0])
            output = {'API' : user.api,
                      'Command': 'Balance',
                'Username' : user.username,
                      'Balance' : user.balance
                      }
            self.write(output)

        else :
            self.write("Wrong API")
    def post(self, *args, **kwargs):
        api_token=self.get_argument('api')
        if self.check_api(api_token):
            user = self.db.get("SELECT * from user where api = %s",api_token)
            output = {'API' : user.api,
                      'Command': 'Balance',
                'Username' : user.username,
                      'Balance' : user.balance
                      }
            self.write(output)
        else :
            self.write("Wrong API")

class GetTicket(BaseHandler):
    def get(self,*args):
        if self.check_auth(args[0],args[1]):
            user = self.db.get("SELECT * from user where username = %s and password = %s", args[0],args[1])
            output = {'API' : user.api,
                      'Command' : 'Balance',
                'Username' : user.username,
                      'Balance' : user.balance}
            self.write(output)
        else :
            output = {'status':'Wrong Authentication'}
            self.write(output)
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username,password):
            user = self.db.get("SELECT * from user where username = %s and password = %s", username,password)
            output = {'API' : user.api,
                      'Command' : 'Balance',
                'Username' : user.username,
                      'Balance' : user.balance}
            self.write(output)
        else :
            output = {'status': 'Wrong Authentication'}
            self.write(output)


class apideposit(BaseHandler):
    def get(self,*args):
        if self.check_api(args[0]):
            user_old = self.db.get("SELECT * from user where api = %s", args[0])
            self.db.execute("UPDATE user set balance = balance + %s where api = %s",int(args[1]),args[0])
            user_new = self.db.get("SELECT * from user where api = %s", args[0])
            output = {'API': user_new.api,
                      'Command' : 'Deposit',
                      'Username': user_new.username,
                      'Old Balance' : user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)
        else:
            output = {'status': 'Wrong API'}
            self.write(output)

    def post(self, *args, **kwargs):
        api_token = self.get_argument('api')
        amount = self.get_argument('amount')
        if self.check_api(api_token):
            user_old = self.db.get("SELECT * from user where api = %s", api_token)
            self.db.execute("UPDATE user set balance = balance + %s where api = %s",int(amount),api_token)
            user_new = self.db.get("SELECT * from user where api = %s", api_token)
            output = {'API': user_new.api,
                      'Command' : 'Deposit',
                      'Username': user_new.username,
                      'Old Balance' : user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)
        else:
            output = {'status': 'Wrong API'}
            self.write(output)


class ChangeStatus(BaseHandler):
    def get(self, *args):
        if self.check_auth(args[0],args[1]):
            user_old = self.db.get("SELECT * from user where username = %s and password = %s", args[0], args[1])
            self.db.execute("UPDATE user set balance = balance + %s where username=%s and password = %s", int(args[2]), args[0],args[1])
            user_new = self.db.get("SELECT * from user where username = %s and password = %s", args[0], args[1])
            output = {'API': user_new.api,
                      'Command': 'Deposit',
                      'Username': user_new.username,
                      'Old Balance': user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)
        else:
            output = {'status': 'Wrong Authentication'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        amount = self.get_argument('amount')
        if self.check_auth(username,password):
            user_old = self.db.get("SELECT * from user where username = %s and password = %s", username,password)
            self.db.execute("UPDATE user set balance = balance + %s where username=%s and password = %s", int(amount), username,password)
            user_new = self.db.get("SELECT * from user where username = %s and password = %s", username,password)
            output = {'API': user_new.api,
                      'Command': 'Deposit',
                      'Username': user_new.username,
                      'Old Balance': user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)
        else:
            output = {'status': 'Wrong Authentication'}
            self.write(output)


class apiwithdraw(BaseHandler):
    def get(self,*args):
        if self.check_api(args[0]):
            user_old = self.db.get("SELECT * from user where api = %s", args[0])
            if int(args[1]) > user_old.balance :
                print(args[1],user_old.balance)
                output = {'status': 'Insufficient Balance'}
                self.write(output)
                return

            self.db.execute("UPDATE user set balance = balance - %s where api = %s",int(args[1]),args[0])
            user_new = self.db.get("SELECT * from user where api = %s", args[0])
            output = {'API': user_new.api,
                      'Command' : 'Withdraw',
                      'Username': user_new.username,
                      'Old Balance' : user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)
        else:
            output = {'status': 'Wrong API'}
            self.write(output)


    def post(self, *args, **kwargs):
        api_token = self.get_argument('api')
        amount = self.get_argument('amount')
        if self.check_api(api_token):
            user_old = self.db.get("SELECT * from user where api = %s", api_token)
            self.db.execute("UPDATE user set balance = balance - %s where api = %s",int(amount),api_token)
            user_new = self.db.get("SELECT * from user where api = %s", api_token)
            output = {'API': user_new.api,
                      'Command' : 'Withdraw',
                      'Username': user_new.username,
                      'Old Balance' : user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)
        else:
            output = {'status': 'Wrong API'}
            self.write(output)

class SendTicket(BaseHandler):
    def get(self, *args,**kwargs):
        if self.check_auth(args[0],args[1]):
            user_old = self.db.get("SELECT * from user where username = %s and password = %s", args[0], args[1])

            if user_old.balance < int(args[2]) :
                output = {'status' : 'Insufficient Balance'}
                self.write(output)
                return

            self.db.execute("UPDATE user set balance = balance - %s where username=%s and password = %s", int(args[2]), args[0],args[1])
            user_new = self.db.get("SELECT * from user where username = %s and password = %s", args[0], args[1])
            output = {'API': user_new.api,
                      'Command': 'Withdraw',
                      'Username': user_new.username,
                      'Old Balance': user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)

        else:
            output = {'status': 'Wrong Authentication'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        amount = self.get_argument('amount')
        if self.check_auth(username, password):
            user_old = self.db.get("SELECT * from user where username = %s and password = %s", username, password)
            if user_old.balance < int(amount) :
                output = {'status': 'Insufficient Balance'}
                self.write(output)
                return
            self.db.execute("UPDATE user set balance = balance - %s where username=%s and password = %s", int(amount),
                            username, password)
            user_new = self.db.get("SELECT * from user where username = %s and password = %s", username, password)
            output = {'API': user_new.api,
                      'Command': 'Deposit',
                      'Username': user_new.username,
                      'Old Balance': user_old.balance,
                      'New Balance': user_new.balance}
            self.write(output)

        else:
            output = {'status': 'Wrong Authentication'}
            self.write(output)


class help(BaseHandler):
    def get(self, *args, **kwargs):
       self.write("Tornado is Runnig")


class login(BaseHandler):
    def get(self, *args, **kwargs):
        if self.check_auth(args[0],args[1]):
            user = self.db.get("SELECT * from user where username = %s and password = %s", args[0], args[1])
            output = {'status' : 'TRUE',
                      'api' : user.api,
                      'username' : user.username}
            self.write(output)
        else:
            output = {'status': 'FALSE'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username,password):
            user = self.db.get("SELECT * from user where username = %s and password = %s", username, password)
            output = {'status': 'TRUE',
                      'api': user.api,
                      'username': user.username}
            self.write(output)
        else:
            output = {'status': 'FALSE'}
            self.write(output)


class logout(BaseHandler):
    def get(self, *args, **kwargs):
        if self.check_api(args[0]):
            user = self.db.get("SELECT * from user where api = %s", args[0])
            output = {'status': 'TRUE',
                      'api': user.api,
                      'username': user.username}
            self.write(output)
        else:
            output = {'status': 'FALSE'}
            self.write(output)

    def post(self, *args, **kwargs):
        api = self.get_argument('api')
        if self.check_api(api):
            user = self.db.get("SELECT * from user where api = %s", api)
            output = {'status': 'TRUE',
                      'api': user.api,
                      'username': user.username}
            self.write(output)
        else:
            output = {'status': 'FALSE'}
            self.write(output)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
