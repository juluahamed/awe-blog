from google.appengine.ext import db
from user import User
from post import Post
# model class for entities of kind 'Like'
class Like(db.Model):
	user = db.ReferenceProperty(User, collection_name = 'user_likes')
	post = db.ReferenceProperty(Post, collection_name = 'post_likes')
	user_name = db.StringProperty(required = True)
	post_id = db.IntegerProperty(required =True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)