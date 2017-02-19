from handlers import BlogHandler
from handlers.utils import get_post_key, check_user_logged_in, check_valid_post
from handlers.utils import check_valid_comment, user_owns_comment 
from google.appengine.ext import db

class EditComment(BlogHandler):
    """Handler for editing an exsisting comment"""
    @check_user_logged_in
    @check_valid_post
    @check_valid_comment
    @user_owns_comment
    def get(self, post_id, comment_id, post = None, comment = None):
        self.render("editcomment.html",post =post, comment = comment)
        
    @check_user_logged_in
    @check_valid_post
    @check_valid_comment
    @user_owns_comment
    def post(self, post_id, comment_id, post = None, comment = None):
        new_comment = self.request.get('comment')
        if new_comment:
            comment.comment = new_comment
            comment.put()
            self.redirect('/blog/%s' % post_id)
        else:
            self.render("editcomment.html", comment=comment, post=post, error="Your Comment was empty")