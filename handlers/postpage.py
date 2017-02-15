from handlers import BlogHandler
from models import Comment, Like
from handlers.utils import get_post_key
from google.appengine.ext import db
class PostPage(BlogHandler):
    """Handler for each Post. Shows/handles content, comments & likes"""
    def get(self, post_id):
        key = get_post_key(int(post_id))
        post = db.get(key)
        comments = Comment.all()
        comment = comments.ancestor(post).order("-created")
        if self.user:
            like = Like.all().ancestor(post).filter("user_name =", self.user.name).get()
        else:
            like = None
        if not post:
            self.error(404)
            return
        self.render("permalink.html", post = post, like = like, comment = comment)

    def post(self, post_id):
        key = get_post_key(int(post_id))
        post = db.get(key)
        comments = Comment.all()
        comments = comments.ancestor(post).order("-created")
        
        if self.user:
            like = Like.all().ancestor(post).filter("user_name =", self.user.name).get()
            if not self.request.get('like'):
                if not self.request.get('comment'):
                    self.render("permalink.html", post = post, comment = comments, like = like, error="Your comment is empty")
                else:
                    comment = self.request.get('comment')
                    c = Comment(comment = comment, user_name = self.user.name, post_id= int(post_id), parent = post )
                    c.put()
                    post.comment += 1
                    post.put()
                    self.render("permalink.html", post = post, comment = comments, like = like)
            else:
                if not self.user.name == post.author:
                    if not like:
                        l = Like(post_id = int(post_id), user_name = self.user.name, parent = post)
                        l.put()
                        post.likes += 1
                        post.put()
                        self.render("permalink.html", post = post, comment = comments,  like = l)
                    else:
                        like.delete()
                        post.likes -= 1
                        post.put()
                        self.render("permalink.html", post = post, comment = comments,  like = None)
                else:
                    error = "You cannot like your own post"
                    self.render("permalink.html", post = post, comment = comments,  like = like, error= error)
        else:
            self.render("permalink.html", post = post, comment = comments,  like = None, error ="You should be logged in to comment and like" )
