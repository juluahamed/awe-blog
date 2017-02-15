from handlers import BlogHandler
from handlers.utils import get_post_key
from google.appengine.ext import db
class DeletePost(BlogHandler):
    """Handler for deleting an exsisting Post"""
    def get(self, post_id):
        if self.user:
            key = get_post_key(int(post_id))
            post = db.get(key)

            if not post:
                self.error(404)
                return
            
            if self.user.name == post.author:
                post.delete()
                self.render("deletepost.html")
            else:
                self.render("deletepost.html", error="You can only delete your own posts")
        else:
            self.redirect('/login')