from handlers import BlogHandler
from handlers.utils import check_valid_post, check_user_logged_in, user_owns_post
from google.appengine.ext import db
class EditPost(BlogHandler):
    """Handler for editing an exsisting post"""
    @check_user_logged_in
    @check_valid_post
    @user_owns_post
    def get(self, post_id, post):
        self.render("editpost.html", post = post)

    @check_user_logged_in
    @check_valid_post
    @user_owns_post
    def post(self, post_id, post):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject and content:
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/blog/%s' % str(post_id))
        else:
            error = "Subject and content, please!"
            self.render("editpost.html", post = post, error=error)