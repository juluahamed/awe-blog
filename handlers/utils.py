from google.appengine.ext import db
import jinja2
import os
from functools import wraps


#Setup for Jinja2
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

##### blog utily functions
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

def get_post_key(post_id):
    return db.Key.from_path('Post', post_id, parent=blog_key())

#####Decoraters
# *args, **kwargs used for parameter transfer
#args[0] -> self
#args[1] -> post id
#args[2] -> comment id
# so used to accomadate change in parameter count 
#while dealing with posts and comments


#checks post_id and returns post object
#throws 404 if post_id invalid
def check_valid_post(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
    	post_id = args[1]
        key = get_post_key(int(post_id))
        post = db.get(key)
        if post:
        	if len(args) > 2:
				return func(args[0], post_id, args[2], post=post)
        	else:
        		return func(args[0], post_id, post=post)
        else:
            args[0].error(404)
            return
    return wrapper

#checks if user logged in
#else routes to login page
def check_user_logged_in(func):
    @wraps(func)
    #def wrapper(self, post_id):
    def wrapper(*args, **kwargs):
        if not args[0].user:
            args[0].redirect('/login')
            return
        else:
        	if len(args) > 2:
        		return func(args[0], args[1], args[2])
    		elif len(args) == 1:
        		return func(args[0])
    		else:
    			return func(args[0], args[1])
    return wrapper


def user_owns_post_liked(func):
    @wraps(func)
    def wrapper(self, post_id, post):
        if post.user.name == self.user.name:
            self.redirect('/blog/%s?error=%s' % (post_id, str(2)))
            return
        else:
            return func(self, post_id, post)
    return wrapper

#verify if the logged in user is the owner of post
def user_owns_post(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs['post'].user.name == args[0].user.name:
        	if len(args) > 2:
        		return func(args[0], args[1], args[2], post= kwargs['post'])
    		else:
    			return func(args[0], args[1], post= kwargs['post'])
        else:
            args[0].redirect('/blog/%s?error=3' % args[1])
            return
    return wrapper

#checks if comment_id is valid
def check_valid_comment(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        comment_id = args[2]
        c_key = db.Key.from_path('Comment', int(comment_id), parent = get_post_key(int(args[1])))
        comment = db.get(c_key)
        if comment:
            return func(args[0], args[1], args[2], post =kwargs['post'], comment=comment)
        else:
            args[0].error(404)
        return
    return wrapper

#checks if logged in user is the owner of comment
def user_owns_comment(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		if kwargs['comment'].user.name == args[0].user.name:
			return func(args[0],args[1],args[2], post=kwargs['post'], comment=kwargs['comment'])
		else:
			args[0].redirect('/blog/%s?error=4' % args[1])
			return
	return wrapper

