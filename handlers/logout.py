from handlers import BlogHandler
class Logout(BlogHandler):
    """Logs user out. Calls functions reset the cookie"""
    def get(self):
        self.logout()
        self.redirect('/blog')