from google.appengine.ext import db
from handlers.utils import render_str
# model class for entities of kind 'Post'
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.StringProperty()
    comment = db.IntegerProperty(default = 0)
    likes = db.IntegerProperty(default = 0)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    # render newline/multiple spaces in post content in HTML
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)