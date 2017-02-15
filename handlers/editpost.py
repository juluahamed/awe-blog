from handlers import BlogHandler
from handlers.utils import get_post_key
from google.appengine.ext import db
class EditPost(BlogHandler):
    """Handler for editing an exsisting post"""
    def get(self, post_id):
        if self.user:
            key = get_post_key(int(post_id))
            post = db.get(key)
            if not post:
                self.error(404)
                return
            if self.user.name == post.author:
                self.render("editpost.html", post = post)
            else:
                self.render("editpost.html", error = "You can only edit your own post")
        else:
            self.redirect('/login')

    def post(self, post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        key = get_post_key(int(post_id))
        p = db.get(key)
        if subject and content:
            p.subject = subject
            p.content = content
            p.author = self.user.name
            p.put()
            self.redirect('/blog/%s' % str(post_id))
        else:
            error = "subject and content, please!"
            self.render("editpost.html", post = p, error=error)