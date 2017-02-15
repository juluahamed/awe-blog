from handlers import BlogHandler
from models import Post
from handlers.utils import blog_key

class NewPost(BlogHandler):
    """Handler for creating new post. Accepts subject&content from user"""
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.render("newpost.html", error="You should be logged in to post a new blog")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, author = self.user.name)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)