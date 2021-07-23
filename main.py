from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_login import login_required, logout_user, current_user, login_user, LoginManager, UserMixin
from forms import RegistrationForm, loginForm, FridgeForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from webdata import output
from webdata.recipe import get_recipes
import requests
app = Flask(__name__)
proxied = FlaskBehindProxy(app) 
app.config['SECRET_KEY'] = 'd552b24612de9b25e081844d77829297'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
querystring = {"includeNutrition":"true"}
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,  nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    fridge = db.relationship('Fridge',backref = 'user', lazy = True)
    #myrecipes = db.relationship('Recipes', backref = 'user', lazy = True)
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    
class Fridge (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), nullable = False )
    date = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    def __repr__(self):
        return f"Fridge('{self.item}')"

class Recipe (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    real_id = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return f"Fridge('{self.real_id}')"

    

    
# class Recipes (db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    food_id = db.Column(db.String(10),unique= True ,nullable = False)
#    food = db.Column(db.String(200),unique = True, nullable = False)
#    date = db.Column(db.DateTime, default = datetime.utcnow)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#    def __repr__(self):
#        return f"Recipes('{self.food_id}','{self.food}')"

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@app.route("/")
def home():
    return render_template('home.html', subtitle='Home Page', subtitle2='Welcome to "We Have Food At Home"', text2='Have you ever wanted McDonalds, but your mom tells you "No because we have food at home"? Have you ever been too lazy to go out to eat? Are you trying to save money? Well this is the place for you!!')
@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page', text='Contributers: Adaora Onwumel, Erica Lee, Stanley Duru')
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('registration.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('myFridge'))
    log_form = loginForm()
    password_entered = log_form.password.data
    user_entered = log_form.username.data
    #credentials invalid

    
    if log_form.validate_on_submit():  
        user = User.query.filter_by(username=log_form.username.data).first()
        if user and user.check_password(password=log_form.password.data):
            login_user(user)
            return redirect(url_for('myFridge'))
        flash('Incorrect Username or Password')
        return redirect(url_for('login'))   
    return render_template('login.html', title='Login', form=log_form)

#@app.route('/update/<int:id>', methods = ['GET', 'POST'])
#def update(id):
    

@app.route('/myFridge', methods=['GET', 'POST'])
def myFridge():
#     form = FridgeForm()
#     if form.validate_on_submit():
#         flash('Created', 'success')
#         return redirect(url_for('myFridge'))
#     return render_template('myFridge.html', subtitle= 'My Fridge', text='This is my Fridge')
    item_list = current_user.fridge
    if request.method == "POST":
        item_name = request.form['item']
        new_item = Fridge(item = item_name , user = current_user)
        db.session.add(new_item)
        db.session.commit()
        return render_template('myFridge.html', subtitle= 'My Fridge', text='This is my Fridge', ingredients = item_list)
        #except:
    #    return "There was an Error!"
    else:
        #items = u.fridge
        return render_template('myFridge.html', subtitle= 'My Fridge', text='This is my Fridge', ingredients = item_list)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

@app.route('/Recipes', methods=['GET', 'POST'])
def Recipes():

    ingredients = []
    show_recipes = []
    for food in current_user.fridge:
        ingredients.append(food.item)
    show_recipes = get_recipes(ingredients)
    
    
    return render_template('Recipes.html', subtitle= 'Recipes Found', content = show_recipes)

@app.route('/Recipes/recipeinfo')
def info():
      recipe_id = 1003464
      #recipe_id = request.args['id']
      recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
      ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipe_id)
      equipmentWidget = "recipes/{0}/equipmentWidget".format(recipe_id)

      recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers).json()

      recipe_headers = {
          'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
          'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
          'accept': "text/html"
      }
      querystring = {"defaultCss":"true", "showBacklink":"true"}

      recipe_info['inregdientsWidget'] = requests.request("GET", url + ingedientsWidget, headers=recipe_headers, params=querystring).text
      recipe_info['equipmentWidget'] = requests.request("GET", url + equipmentWidget, headers=recipe_headers, params=querystring).text

      return render_template('info.html', recipe=recipe_info)
    
    
@app.route('/delete/<int:id>')
def delete(id):
    item_delete = Fridge.query.get_or_404(id)
    try:
        db.session.delete(item_delete)
        db.session.commit()
        return redirect(url_for('myFridge'))
    except:
        return "Could not delete"
    
@app.route('/Jokes-Trivia', methods=['GET', 'POST'])
def Jokes_trivia():
    return render_template('Jokes_trivia.html', subtitle="Random Joke/Trivia generator")

@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")