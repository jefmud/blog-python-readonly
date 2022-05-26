"""
A simple, clean blog.  Can be run in development mode, FCGI, or WSGI
by Jeff, et. al. 2022

blog.py - this file
blog.json - the branding file
templates/clean-blog - directory with Jinja2 templates
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os
import json

app = Flask(__name__)

# this is the remote API
api_base = "https://expressblog.nomon.repl.co/api"

# defaults, overide this with blog.json file
brand = {
  'title':'My Blog',
  'description':'Yet Another Blog',
  'tags':[''],
  'image_url':'/static/images/mountain.png',
  'facebook_url':'#',
  'github_url':'#',
  'twitter_url':'#',
}


@app.before_request
def before_request():
  # get brand configuration from JSON file
  global brand
  # try to update the brand for the blog.json file
  try:
    filename = os.path.join(app.root_path, 'blog.json')
    with open(filename) as f:
      brand_update = json.loads(f.read())
    # update the key/values to the existing brand
    brand.update(brand_update)
  except:
    # just print the error to the console
    print("missing or invalid blog.json")


@app.route('/meta/about')
def about_view():
  """render a static about page"""
  return render_template('clean-blog/about.html', brand=brand)


@app.route('/meta/contact')
def contact_view():
  """render a static contact page"""
  return render_template('clean-blog/contact.html', brand=brand)


def get_posts():
  """get posts from API"""
  posts_request = requests.get(api_base + "/posts")
  candidates = posts_request.json()
  posts = []
  for post in candidates:
    if post.get('is_published', False):
      for tag in brand.get('tags', []):
        if tag in post.get('tags',''):
          posts.append(post)
          break
  return posts


@app.route('/')
def index():
  posts = get_posts()
  return render_template('clean-blog/index.html', posts=posts, brand=brand)


@app.route('/featured')
def featured():
  posts = get_posts()
  if len(posts) < 1:
    return render_template('clean-blog/404.html', brand=brand)
  return render_template('clean-blog/post.html', post=posts[-1], brand=brand)
  

@app.route('/<slug>')
def post(slug):
    """get the post represented by the slug"""
    # returns a "list" of matching posts, get the last one.
    post_request = requests.get(api_base + "/post/" + slug)
    posts = post_request.json()
    if len(posts) < 1:
        return render_template('clean-blog/404.html', brand=brand)
      
    # check if image_url is set, if not, use brand image_url
    if posts[-1].get('image_url', '') == '':
      posts[-1]['image_url'] = brand['image_url']
    return render_template('clean-blog/post.html', post=posts[-1], brand=brand)


if __name__ == '__main__':
    # run the development server, for production run with gunicorn or fcgi
    app.run(debug=True)
