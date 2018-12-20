from jinja2 import Environment, FileSystemLoader
from tornado.web import RequestHandler
from bokeh.util import session_id

import tornado

USERNAME = "sunderland"

def isAuthenticated(username) :
    if USERNAME == username:
        return True
    return False

class AuthLoginHandler(RequestHandler):

    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""

        env = Environment(loader = FileSystemLoader('templates'))
        template = env.get_template('login.html')
        self.write(template.render(errormessage = errormessage,
          asset_path='/assets/'
        ))

    def check_permission(self, password, username):
        if username == USERNAME and password == "N0ttob3shared":
            return True
        return False

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(password, username)
        if auth:
            sid = tornado.escape.json_encode(session_id.generate_session_id('7vchp9EInHrD11xgrdXT02gASwvoIQBIfoEUxVMaRRYx', True))
            self.set_secure_cookie("bkapp_sid", "{}".format(sid))
            self.set_current_user(username)
            self.redirect(self.get_argument("next", "/parking-permits"))
        else:
            error_msg = "?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect("/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
            self.clear_cookie("bkapp_sid")

class AuthLogoutHandler(RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("bkapp_sid")
        self.redirect(self.get_argument("next", "/parking-permits"))
