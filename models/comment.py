from google.appengine.ext import db
# model class for entities of kind 'Comment'
class Comment(db.Model):
    comment = db.TextProperty(required = True)
    user_name = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    # render newline/multiple spaces in comment in HTML
    def render(self):
        return self.comment.replace('\n', '<br>')