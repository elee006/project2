from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_login import login_required, logout_user, current_user, login_user
from forms import RegistrationForm, loginForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from datetime import datetime
app = Flask(__name__)
proxied = FlaskBehindProxy(app) 
app.config['SECRET_KEY'] = 'd552b24612de9b25e081844d77829297'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    fridge = db.relationship('Fridge',backref = 'user', lazy = True)
    #myrecipes = db.relationship('Recipes', backref = 'user', lazy = True)
  
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    
class Fridge (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50),unique = True, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    def __repr__(self):
        return f"Fridge('{self.item}')"

#class Recipes (db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    food_id = db.Column(db.String(10),unique= True ,nullable = False)
#    food = db.Column(db.String(200),unique = True, nullable = False)
#    date = db.Column(db.DateTime, default = datetime.utcnow)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#    def __repr__(self):
#        return f"Recipes('{self.food_id}','{self.food}')"

@app.route("/")
def home():
    return render_template('home.html', subtitle='Home Page', text='Welcome to "We Have Food At Home"', text2='Have you ever wanted McDonalds, but your mom tells you "No because we have food at home"? Have you ever been too lazy to go out to eat? Are you trying to save money? Well this is the place for you!!')
@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page', text='Contributers: Adaora Onwumel, Erica Lee, Stanley Duru')
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('registration.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    log_form = loginForm()
    password_entered = log_form.password.data
    user_entered = log_form.username.data
    #credentials invalid
    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        if password_entered != user.password:
             flash(f'Incorrect Username/Password')
             return redirect(url_for('login'))
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=log_form)

#@app.route('/update/<int:id>', methods = ['GET', 'POST'])
#def update(id):
    

@app.route('/myFridge', methods=['GET', 'POST'])
def myFridge():
    if request.method == "POST":
        item_name = request.form['item']
        new_item = Fridge(item = item_name)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/myFridge')
        #except:
    #    return "There was an Error!"
    else:
        items = Fridge.query.order_by(Fridge.date)
        return render_template('myFridge.html', subtitle= 'My Fridge', text='This is my Fridge', myFridge = items)

@app.route('/Recipes', methods=['GET', 'POST'])
def Recipes():
    return render_template('Recipes.html', subtitle= 'Recipes Found')

@app.route('/MyRecipes', methods=['GET', 'POST'])
def MyRecipes():
    return render_template('MyRecipes.html', subtitle= "Here are the Recipes you've saved")

@app.route('/Nutrition', methods=['GET', 'POST'])
def Nutrition():
    return render_template('Nutrition.html', subtitle= "Nutritional Facts")

@app.route('/Jokes-Trivia', methods=['GET', 'POST'])
def Jokes_trivia():
    return render_template('Jokes_trivia.html', subtitle="Random Joke/Trivia generator")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")