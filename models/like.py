from google.appengine.ext import db
# model class for entities of kind 'Like'
class Like(db.Model):
    user_name = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required =True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)