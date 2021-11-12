from flask import Flask, render_template, request, jsonify, redirect, url_for , send_file
from flask import session
import os
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def root():
    return render_template("main.html")

@app.route("/search",methods=["GET", "POST"])
def search():
    if request.method == "POST":
        session['user_city'] = request.form.get("user_city")
        session['travel_city'] = request.form.get("travel_city")
    if request.method == "GET":
        session['user_city']  = request.args.get("user_city")
        session['travel_city'] = request.args.get("travel_city")

    if len(session['user_city']) == 0 or len(session['travel_city']) ==0:
        return {'message':"error!"}
    else:
        return {'message':"success!",'user_city':session['user_city'],'travel_city':session['travel_city']}


@app.route("/options")
def options():
    return render_template("options.html")

# IMAGE_FOLDER = os.path.join('static', 'imageny')
# app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
@app.route("/picture")
def picture():
    if session['travel_city'] == 'New York':
        # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'NY.jpg')
        imagelist = os.listdir('static/imageny')
        imagelist = ['imageny/' + image for image in imagelist]
    else:
        imagelist = os.listdir('static/imagela')
        imagelist = ['imagela/' + image for image in imagelist]
    return render_template("picture.html", city_name = session['travel_city'], imagelist = imagelist)

@app.route("/main")
def back():
    return render_template("main.html")

@app.route("/options")
def backop():
    return render_template("options.html")
