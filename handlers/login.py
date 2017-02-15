from handlers import BlogHandler
from models import User
class Login(BlogHandler):
    """Handler for /login page. Handles user info verification and login"""
    def get(self):
        if self.user:
            self.logout()
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', username = username, error = msg)