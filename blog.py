from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os
import json

app = Flask(__name__)
api_base = "https://expressblog.nomon.repl.co/api"

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
  try:
    filename = os.path.join(app.root_path, 'blog.json')
    with open(filename) as f:
      brand_update = json.loads(f.read())
    brand.update(brand_update)
  except:
    print("missing or invalid blog.json")


@app.route('/meta/about')
def about_view():
  return render_template('clean-blog/about.html', brand=brand)


@app.route('/meta/contact')
def contact_view():
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
    post_request = requests.get(api_base + "/post/" + slug)
    posts = post_request.json()
    if len(posts) < 1:
        return render_template('clean-blog/404.html', brand=brand)
      
    # check if image_url is set, if not, use brand image_url
    if posts[0].get('image_url', '') == '':
      posts[0]['image_url'] = brand['image_url']
    return render_template('clean-blog/post.html', post=posts[0], brand=brand)


if __name__ == '__main__':
    app.run(debug=True)