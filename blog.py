from handlers import BlogFront,BlogHandler,DeleteComment,DeletePost,EditComment,EditPost,DeleteComment
from handlers import Login,Logout,NewPost,PostPage,Register,NewComment, LikeHandler

import webapp2


# URLs and handlers
app = webapp2.WSGIApplication([('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/([0-9]+)/newcomment', NewComment),
                               ('/blog/([0-9]+)/likehandler', LikeHandler),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/editcomment/([0-9]+)/([0-9]+)', EditComment),
                               ('/blog/deletecomment/([0-9]+)/([0-9]+)', DeleteComment),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
