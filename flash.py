from flask import Flask,render_template,abort,jsonify

from model import db

# create flask object
app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('welcome.html')# "welcome to my flask app"

@app.route("/next")
def next_page():
    return "next"
    
counter = 0
@app.route("/counter")
def counter_page():
    global counter
    counter += 1
    return f"counter: {counter}"

#dynamically change url and get data from db
@app.route('/card/<int:index>')
def card_view(index):
    card = db[index]
    return render_template('card.html', card=card, index=index, max_index=len(db)-1)

# show all cards
@app.route('/api/card/')
def api_card_list():
    return jsonify(db)