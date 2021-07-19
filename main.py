from flask import Flask, render_template, url_for, flash, redirect
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html', subtitle='Home Page', text='Welcome to "We Got Food At Home"')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")