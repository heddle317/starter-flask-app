starter-flask-app
=================

A starter flask application for serving small, static sites.


## Getting Started

### Prerequisites
* Github Account -> https://github.com/join
* Setup SSH keys with Github -> https://help.github.com/articles/generating-ssh-keys
* Heroku Account -> https://id.heroku.com/signup
* Install Heroku toolbelt -> https://toolbelt.heroku.com/
* Setup SSH keys with Heroku -> https://devcenter.heroku.com/articles/keys

### Clone this project
* click the Fork button in the upper right hand corner of this page
* go to your projects directory on your computer (for me, cd ~/projects)
* `git clone git@github.com:[your github username]/starter-flask-app.git`
* `cd starter-flask-app`
* `heroku login`
* `virtualenv venv` (or whatever your virtualenv preferences are)
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `python web.py`
* got to localhost:8000 in your browser to see your website (this will show a blank page)

### Pushing to Heroku
* `heroku create` (only need to do this the first time you push)
* `git add .`
* `git commit -m "[Message about the changes you made.]"`
* `git push heroku master`
* go to the URL heroku gives you

## Editing the html, css, and js files.

The main html file is `home.html`, which is located in the `templates/` folder. Editing this file will show changes in your browser. 

`style.css` and `script.js` are located in the `static/` directory. These are linked in the `home.html` <head></head> section, so changes to these files will show up in the browser on refresh.

## What does this app do?

This application is a very small, simple flask app. Flask is a python framework that does URL routing. If you open the app.py file and take a look at what's inside you'll see the following:

```
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')
```

When you ran the command `pip install -r requirements.txt` you installed Flask. In python that means that you can now import things from the 'flask' library. So at the top of the file you import Flask and render_template from flask. These are functions that you will need to serve your `home.html` file. 

```
app = Flask(__name__)
```

This simply creates a very basic flask application. For more information about what you can do with Flask, here are some resources:

* Flask Docs - http://flask.pocoo.org/docs/
* Flask megatutorial - http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

```
@app.route('/')
```

This is the part of the code that does URL routing. In this case, the `/` route will go to the function hello. If you have a domain name `website.com`, the `/` route => `http://website.com/`. It's basically the base url for the domain name.

```
def hello():
    return render_template('home.html')
```
The function hello is also very simple. This function simply returns the template `home.html`. Flask knows to look in the templates folder for template files, so you only have to tell it the name or path of the file inside templates. If you put an html file outside of the templates folder, Flask will not be able to find it.


## Adding New Routes

This code has a route for `/`, but what if you want to add new routes? Lets say you're making a website and you want to have an about page. You can add a new route like this:

```
@app.route('/about')
def about():
    return render_template('about.html')
```

This will render a template `about.html` (which should live in your templates folder) when someone goes to the URL http://website.com/about. (website.com being the base domain name for your site).

I have also added a `base.html` file that `home.html` extends. You can also extend your new `about.html` file off of `base.html` like this:

```
{% extends "base.html" %}
{% block content %}
    Your html goes here....
{% endblock %}
```

The advantage of this is that when you extend an html file, you get everything in that file plus what's in your current file. You can add a nav bar to the `base.html` file that will show up in both your `home.html` file and your `about.html`. This way you don't have to rewrite shared HTML multiple times.
