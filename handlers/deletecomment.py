from handlers import BlogHandler
from handlers.utils import get_post_key
from google.appengine.ext import db
class DeleteComment(BlogHandler):
    """Handler for deleting an exsisting comment"""
    def get(self, comb_id):
        post_id = comb_id.split('+')[0]
        comment_id = comb_id.split('+')[1]
        key = get_post_key(int(post_id))
        post = db.get(key)
        c_key = db.Key.from_path('Comment', int(comment_id), parent = key)
        comment = db.get(c_key)
        if self.user:
            if self.user.name == comment.user_name:
                comment.delete()
                post.comment -= 1
                post.put()
                self.redirect('/blog/%s' % post_id)
            else:
                self.render("deletecomment.html", error="You can only delete your own comments")
        else:
            self.redirect('/login')