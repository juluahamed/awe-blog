from handlers import BlogHandler
from models import Comment
from handlers.utils import get_post_key, check_valid_post, check_user_logged_in
from google.appengine.ext import db
from functools import wraps

class NewComment(BlogHandler):
	@check_user_logged_in
	@check_valid_post
	def post(self, post_id, post = None):
		comment = self.request.get('comment')
		if comment:
			c = Comment(user = self.user, post = post, comment= comment, user_name = self.user.name,
						 post_id= int(post_id), parent = post)
			c.put()
			post.comment += 1
			post.put()
			self.redirect("/blog/%s" % post_id )
		else:
			error="1"
			self.redirect("/blog/%s?error=%s" % (post_id,error))