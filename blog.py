import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = 'fart'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)


##### user stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


##### blog stuff

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.StringProperty()
    comment = db.IntegerProperty(default = 0)
    likes = db.IntegerProperty(default = 0)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

def get_post_key(post_id):
    return db.Key.from_path('Post', post_id, parent=blog_key())
    

class Comment(db.Model):
    comment = db.TextProperty(required = True)
    user_name = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        return self.comment.replace('\n', '<br>')

class Like(db.Model):
    user_name = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required =True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts = posts)

class PostPage(BlogHandler):
    def get(self, post_id):
        key = get_post_key(int(post_id))
        post = db.get(key)
        comments = Comment.all()
        comment = comments.ancestor(post).order("-created")
        #like = Like.all().ancestor(post).filter("user_name =", self.user.name).get()
        if not post:
            self.error(404)
            return
        self.render("permalink.html", post = post, like = None, comment = comment)
    def post(self, post_id):
        key = get_post_key(int(post_id))
        post = db.get(key)
        comments = Comment.all()
        comments = comments.ancestor(post).order("-created")
        
        if self.user:
            like = Like.all().ancestor(post).filter("user_name =", self.user.name).get()
            if not self.request.get('like'):
                if not self.request.get('comment'):
                    self.render("permalink.html", post = post, comment = comments, like = like, error="Your comment is empty")
                else:
                    comment = self.request.get('comment')
                    c = Comment(comment = comment, user_name = self.user.name, post_id= int(post_id), parent = post )
                    c.put()
                    post.comment += 1
                    post.put()
                    self.render("permalink.html", post = post, comment = comments, like = like)
            else:
                if not self.user.name == post.author:
                    #l_key = db.Key.from_path('Post', int(post_id), parent = post)
                    #like = Like.all().ancestor(post).filter("user_name =", self.user.name).get()
                    if not like:
                        l = Like(post_id = int(post_id), user_name = self.user.name, parent = post)
                        l.put()
                        post.likes += 1
                        post.put()
                        self.render("permalink.html", post = post, comment = comments,  like = l)
                    else:
                        like.delete()
                        post.likes -= 1
                        post.put()
                        self.render("permalink.html", post = post, comment = comments,  like = None)
                else:
                    error = "You cannot like your own post"
                    self.render("permalink.html", post = post, comment = comments,  like = like, error= error)
        else:
            self.render("permalink.html", post = post, comment = comments,  like = None, error ="You should be logged in to comment and like" )

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.render("newpost.html", error="You should be logged in to post a new blog")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, author = self.user.name)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

class EditPost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = get_post_key(int(post_id))
            post = db.get(key)
            if not post:
                self.error(404)
                return
            if self.user.name == post.author:
                self.render("editpost.html", post = post)
            else:
                self.render("editpost.html", error = "You can only edit your own post")
        else:
            self.redirect('/blog')
        

        

    def post(self, post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        key = get_post_key(int(post_id))
        p = db.get(key)
        if subject and content:
            p.subject = subject
            p.content = content
            p.author = self.user.name
            p.put()
            self.redirect('/blog/%s' % str(post_id))
        else:
            error = "subject and content, please!"
            self.render("editpost.html", post = p, error=error)

class DeletePost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = get_post_key(int(post_id))
            post = db.get(key)

            if not post:
                self.error(404)
                return
            
            if self.user.name == post.author:
                post.delete()
                self.render("deletepost.html")
            else:
                self.render("deletepost.html", error="You can only delete your own posts")
        else:
            self.redirect('/blog')

class EditComment(BlogHandler):
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
                    self.render("editcomment.html", comment = comment)
                else:
                    self.render("editcomment.html", post= post, comment=comment, error ="You can only edit your own comments" )
            else:
                self.redirect('/blog')
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


class DeleteComment(BlogHandler):
    def get(self, comb_id):
        post_id = comb_id.split('+')[0]
        comment_id = comb_id.split('+')[1]
        key = get_post_key(int(post_id))
        post = db.get(key)
        c_key = db.Key.from_path('Comment', int(comment_id), parent = key)
        comment = db.get(c_key)
        if self.user:
            if self.user.name == comment.user_name:
                comment.delete()
                post.comment -= 1
                post.put()
                self.redirect('/blog/%s' % post_id)
            else:
                self.render("deletecomment.html", error="You can only delete your own comments")
        else:
            self.redirect('/blog')





USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

def exsisting_user(username):
    return User.by_name(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Register(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        if exsisting_user(self.username):
            params['error_username'] = "This username is already taken"
            have_error =True
        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            u = User.by_name(self.username)
            if u:
                msg = 'That user already exists.'
                self.render('signup-form.html', error_username = msg)
            else:
                u = User.register(self.username, self.password, self.email)
                u.put()
                self.login(u)
                self.redirect('/blog')

class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')


app = webapp2.WSGIApplication([('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               #('/liked/([0-9]+)',LikedPost),
                               #('/blog/([0-9]+)/newcomment', NewComment),
                               ('/blog/editcomment/(.*)', EditComment),
                               ('/blog/deletecomment/(.*)', DeleteComment),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
