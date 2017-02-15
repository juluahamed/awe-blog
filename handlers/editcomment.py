from handlers import BlogHandler
from handlers.utils import get_post_key
from google.appengine.ext import db
class EditComment(BlogHandler):
    """Handler for editing an exsisting comment"""
    def get(self, comb_id):
        post_id = comb_id.split('+')[0]
        comment_id = comb_id.split('+')[1]
        key = get_post_key(int(post_id))
        post = db.get(key)
        c_key = db.Key.from_path('Comment', int(comment_id), parent = key)
        comment = db.get(c_key)
        if post and comment:
            if self.user:
                if self.user.name == comment.user_name:
                    self.render("editcomment.html",post =post, comment = comment)
                else:
                    self.render("editcomment.html", post= post, comment=comment, error ="You can only edit your own comments" )
            else:
                self.redirect('/login')
        else:
            self.error(404)
            return

    def post(self, comb_id):
        post_id = comb_id.split('+')[0]
        comment_id = comb_id.split('+')[1]
        key = get_post_key(int(post_id))
        post = db.get(key)
        c_key = db.Key.from_path('Comment', int(comment_id), parent = key)
        comment = db.get(c_key)
        if self.request.get('comment'):
            new_comment = self.request.get('comment')
            comment.comment = new_comment
            comment.put()
            self.redirect('/blog/%s' % post_id)
        else:
            self.render("editcomment.html", comment=comment, error="Your Comment was empty")