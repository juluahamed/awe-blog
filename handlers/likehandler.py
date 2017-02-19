from handlers import BlogHandler
from models import Like
from handlers.utils import check_valid_post, check_user_logged_in, user_owns_post_liked
from google.appengine.ext import db

class LikeHandler(BlogHandler):
    @check_user_logged_in
    @check_valid_post
    @user_owns_post_liked
    def post(self, post_id, post):
        like = post.post_likes.filter('user =', self.user).get()
        if not like:
            l = Like(user = self.user, post = post, post_id = int(post_id), user_name = self.user.name, parent = post)
            l.put()
            post.likes += 1
            post.put()
            self.redirect('/blog/%s' % post_id)
        else:
            like.delete()
            post.likes -= 1
            post.put()
            self.redirect('/blog/%s' % post_id)