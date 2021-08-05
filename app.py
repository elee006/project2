from flask import Flask, render_template
from flask import url_for, flash, redirect, request, session
from flask_login import login_required, logout_user
from flask_login import current_user, login_user, LoginManager, UserMixin
from forms import RegistrationForm, loginForm, FridgeForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from webdata import output
from webdata.prices_walmart import *
from webdata.search import search_recipes
from webdata.recipe import *
from webdata.meal import *
import requests
import sqlite3


app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'd552b24612de9b25e081844d77829297'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = SQLAlchemy(app)


login_manager = LoginManager(app)
headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}
querystring = {"includeNutrition": "true"}
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    fridge = db.relationship('Fridge', backref='user', lazy=True)
    # myrecipes = db.relationship('Recipes', backref = 'user', lazy = True)

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
    item = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.String(50))

    def __repr__(self):
        return f"Fridge('{self.item}','{self.price}')"


class SavedRecipes (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.String(10), unique=True, nullable=False)
    food = db.Column(db.String(200), unique=True, nullable=False)
    image = db.Column(db.String(200), unique=True, nullable=False)
    link = db.Column(db.String(200), unique=True, nullable=False)
    sum = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"""Recipes('{self.user_id}','{self.food_id}'
        ,'{self.food}','{self.image}','{self.sum}')"""

class PlanRecipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    sum = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"""Recipes('{self.user_id}','{self.food}'
        ,'{self.image}','{self.sum}','{self.link}')"""
    

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

# l = Fridge.query.filter_by(user_id = 1).all()
# t = [i.item for i in l]
# print(t)


@app.route("/")
def home():
    return render_template(
        'home.html',
        subtitle='Home Page',
        subtitle2='Welcome to "We Have Food At Home"',
        text2="""""ave you ever wanted McDonalds, but your mom tells you
        'No because we have food at home'?
        Have you ever been too lazy to go out to eat?
        Are you trying to save money? Well this is the place for you!!""")


@app.route("/about")
def about():
    return render_template(
        'about.html',
        subtitle='About Page',
        text="""Contributers: Adaora Onwumel, Erica Lee,
        Stanley Duru, Oluwademilade Bolatimi""")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data)
#         l = Fridge.query.order_by(Fridge.user_id = user.id).all()
#         print(l)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # if so - send to home page
    return render_template('registration.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('myFridge'))
    log_form = loginForm()
    password_entered = log_form.password.data
    user_entered = log_form.username.data
    # credentials invalid

    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        if user and user.check_password(password=log_form.password.data):
            login_user(user)
            return redirect(url_for('myFridge'))
        flash('Incorrect Username or Password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=log_form)

# @app.route('/update/<int:id>', methods = ['GET', 'POST'])
# def update(id):


@app.route('/myFridge', methods=['GET', 'POST'])
def myFridge():
    #     form = FridgeForm()
    #     if form.validate_on_submit():
    #         flash('Created', 'success')
    #         return redirect(url_for('myFridge'))
    # return render_template('myFridge.html', subtitle= 'My Fridge',
    # text='This is my Fridge')
    item_list = current_user.fridge
    items = [i.item for i in item_list]
    if request.method == "POST":
        item_name = request.form['item']
        new_item = Fridge(
            item=item_name,
            user=current_user,
            price=new_price(item_name))
        try:
            db.session.add(new_item)
            db.session.commit()

            return render_template(
                'myFridge.html',
                subtitle='My Fridge',
                text='This is my Fridge',
                ingredients=item_list)
        except BaseException:
            db.session.rollback()
            item_delete = Fridge.query.filter_by(item=item_name).first()
            db.session.delete(item_delete)
            db.session.commit()
            db.session.add(new_item)
            db.session.commit()
            return render_template(
                'myFridge.html',
                subtitle='My Fridge',
                text='This is my Fridge',
                ingredients=item_list)
        # return render_template('myFridge.html', subtitle= 'My Fridge',
        #  text='This is my Fridge', ingredients = item_list)
        # except:
    #    return "There was an Error!"
    else:
        Fridge_total = meal_Price(items)
        print(Fridge_total)
        # items = u.fridge
        return render_template(
            'myFridge.html',
            subtitle='My Fridge',
            text='This is my Fridge',
            ingredients=item_list)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


@app.route('/Recipes', methods=['GET', 'POST'])
def Recipes():

    ingredients = []
    show_recipes = []
    message = "No recipes found"
    for food in current_user.fridge:
        ingredients.append(food.item)
    show_recipes = get_recipes(ingredients)
    vegan_value = request.form.getlist('vegan')
    vege_value= request.form.getlist('vegetarian')
    gluten_value = request.form.getlist('gluten_free')
    dairy_value = request.form.getlist('dairy')
    if show_recipes == []:
        return render_template(
            'Recipes.html',
            subtitle='Recipes Found',
            error=message)
    else:
        df = get_data(show_recipes)
        Calories(df)
        Proteins(df)
        Carbs(df)
        return render_template(
            'Recipes.html',
            subtitle='Recipes Found',
            content=show_recipes,
            vg = vegan_value,
            ve = vege_value,
            g = gluten_value,
            d = dairy_value)


@app.route('/Recipes/recipeinfo')
def info():
    # recipe_id = 1003464
    recipe_id = str(request.args['id'])
    print(recipe_id)
    recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
    ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipe_id)
    equipmentWidget = "recipes/{0}/equipmentWidget".format(recipe_id)
    recipe_info = requests.request(
        "GET",
        url + recipe_info_endpoint,
        headers=headers).json()

    recipe_headers = {
        'x-rapidapi-host': """spoonacular-recipe-
        food-nutrition-v1.p.rapidapi.com""",
        'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
        'accept': "text/html"}
    querystring = {"defaultCss": "true", "showBacklink": "true"}

    recipe_info['inregdientsWidget'] = requests.request(
        "GET", url + ingedientsWidget,
        headers=recipe_headers, params=querystring).text
    recipe_info['equipmentWidget'] = requests.request(
        "GET", url + equipmentWidget,
        headers=recipe_headers, params=querystring).text

    return render_template('info.html', recipe=recipe_info)


@app.route('/delete/<int:id>')
def delete(id):
    item_delete = Fridge.query.get_or_404(id)
    try:
        db.session.delete(item_delete)
        db.session.commit()
        return redirect(url_for('myFridge'))
    except BaseException:
        return "Could not delete"


@app.route('/Jokes-Trivia', methods=['GET', 'POST'])
def Jokes_trivia():
    return render_template(
        'Jokes_trivia.html',
        subtitle="Random Joke/Trivia generator")


@app.route('/myMealPlan', methods=['GET', 'POST'])
def MealPlan():
    data={}
    cal =''
    pro =''
    fat =''
    carb =''
    if request.method == 'POST':
        calories = request.form['cal']
        items = request.form['ex']
        option = request.form['option']
        if option == "No Preference":
            option =""
        query = {'Calories':calories, 'Exclude':items, 'Option':option}
        info = get_meals(query)
        plan =[]
        for r in info[0]:
            r_add = PlanRecipes(
                    food = r[0],
                    image = r[1],
                    sum = r[2],
                    link = r[3],
                    user_id = current_user.id)
            plan.append(r_add)
        cal = "Calories: {}".format(info[1]["calories"])
        pro = "Proteins: {}g".format(info[1]["protein"])
        fat = "Fat: {}g".format(info[1]["fat"])
        carb = "Carbohydrates: {}g".format(info[1]["carbohydrates"])
        
        for recipe in plan:
            data[recipe.food] = [recipe.sum, recipe.image, recipe.link]

                
                
    return render_template('mealPlan.html', subtitle="My Meal Plan", text = data, cal = cal, pro = pro, fat = fat, carb = carb)


@app.route('/myRecipes', methods=['GET', 'POST'])
def myRecipes():
    data = {}
    user_recipes = SavedRecipes.query.filter_by(user_id=current_user.id).all()
    for recipe in user_recipes:
        data[recipe.food] = [recipe.sum, recipe.image, recipe.food_id, recipe.link]
    return render_template(
        'MyRecipes.html',
        subtitle="Saved Recipes",
        text=data)


@app.route('/addrecipe/<id>')
def add(id):
    r = getrecipe(id)
    r_add = SavedRecipes(
        food_id=id,
        food=r[0],
        image=r[1],
        sum=r[2],
        link=r[3],
        user_id=current_user.id)
    try:
        db.session.add(r_add)
        db.session.commit()
        flash(f'Recipe Added!', 'success')
        return redirect(url_for('myRecipes'))
    except BaseException:
        f = "Recipe already added. Choose a different recipe"
        return f


@app.route('/deleterecipe/<id>')
def delete_recipe(id):
    item_delete = SavedRecipes.query.filter_by(food_id=id).first()
    try:
        db.session.delete(item_delete)
        db.session.commit()
        return redirect(url_for('myRecipes'))
    except BaseException:
        return "Could not delete"


@app.route('/searchresults', methods=['GET', 'POST'])
def search():
    query = request.form['query']
    message = "No recipes found"
    show_recipes = get_recipes_search(query)
    # prices = get_recipe_prices(show_recipes)
    if show_recipes == []:
        return render_template(
            'searchedrecipes.html',
            subtitle='Recipes Found',
            error=message)
    else:
        return render_template(
            'searchedrecipes.html',
            subtitle='Recipes Found',
            content=show_recipes)


@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login'))

@app.route("/Calories")
def CaloriesPage():
    return render_template('templates/Calories.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
