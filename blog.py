from handlers import BlogFront,BlogHandler,DeleteComment,DeletePost,EditComment,EditPost,DeleteComment
from handlers import Login,Logout,NewPost,PostPage,Register

import webapp2


# URLs and handlers
app = webapp2.WSGIApplication([('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/editcomment/(.*)', EditComment),
                               ('/blog/deletecomment/(.*)', DeleteComment),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
