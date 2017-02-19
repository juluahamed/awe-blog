from handlers import BlogHandler
from handlers.utils import check_user_logged_in, check_valid_post, check_valid_comment, user_owns_comment  
from google.appengine.ext import db

class DeleteComment(BlogHandler):
    """Handler for deleting an exsisting comment"""
    @check_user_logged_in
    @check_valid_post
    @check_valid_comment
    @user_owns_comment
    def get(self, post_id, comment_id, post = None, comment = None):
        comment.delete()
        post.comment -= 1
        post.put()
        self.redirect('/blog/%s' % post_id)