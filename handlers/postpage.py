from handlers import BlogHandler
from models import Comment, Like
from handlers.utils import get_post_key, check_valid_post
from google.appengine.ext import db

class PostPage(BlogHandler):
    """Handler for each Post. Shows/handles content, comments & likes"""
    @check_valid_post
    def get(self, post_id, post):
        comments = post.post_comments.order("-created")
        error = self.request.get('error')
        if self.request.get('error'):
            if error == '1':
                error = "Your comment is empty"
            elif error == '2':
                error = "You cannot like your own post"
            elif error == '3':
                error = "You can only edit/delete the posts that you own"
            elif error == '4':
                error = "You can only edit/delete the comments that you own"
        if self.user:
            like = Like.all().ancestor(post).filter("user_name =", self.user.name).get()
        else:
            like = None
        self.render("permalink.html", post = post, like = like, comment = comments, error= error)