from handlers import BlogHandler
from models import Post
from handlers.utils import blog_key, check_user_logged_in

class NewPost(BlogHandler):
    """Handler for creating new post. Accepts subject & content from user"""
    @check_user_logged_in
    def get(self):
        self.render("newpost.html")

    @check_user_logged_in
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject and content:
            p = Post(user = self.user, subject = subject, content = content, author = self.user.name, parent = blog_key())
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)