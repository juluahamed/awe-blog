from handlers import BlogHandler
from handlers.utils import check_user_logged_in, check_valid_post, user_owns_post
from google.appengine.ext import db


class DeletePost(BlogHandler):
    """Handler for deleting an exsisting Post"""
    @check_user_logged_in
    @check_valid_post
    @user_owns_post
    def get(self, post_id, post = None):
        post.delete()
        self.render("deletepost.html")