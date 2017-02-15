from google.appengine.ext import db
import jinja2
import os


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

##### blog stuff

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

def get_post_key(post_id):
    return db.Key.from_path('Post', post_id, parent=blog_key())