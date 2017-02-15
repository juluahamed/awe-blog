from handlers.bloghandler import BlogHandler
from models import Post
class BlogFront(BlogHandler):
    """Handler for '/blog' page.Displays recent posts"""
    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts = posts)