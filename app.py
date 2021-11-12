import os
import grpc
import imagesend_pb2
import imagesend_pb2_grpc
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
    # get user input and selection from Front ends
    if request.method == "POST":
        session['user_city'] = request.form.get("user_city")
        session['travel_city'] = request.form.get("travel_city")
    if request.method == "GET":
        session['user_city']  = request.args.get("user_city")
        session['travel_city'] = request.args.get("travel_city")

    # send the message to the front ends
    if len(session['user_city']) == 0 or len(session['travel_city']) ==0:
        return {'message':"error!"}
    else:
        return {'message':"success!",'user_city':session['user_city'],'travel_city':session['travel_city']}


@app.route("/options")
def options():
    return render_template("options.html")

# microsevice get the image and download them into local folder
def microsevice_image(image_Name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = imagesend_pb2_grpc.ImageSendStub(channel)
        response = stub.Imagerequest(imagesend_pb2.image_name(image_name1=image_Name))
    # set the photo path
    filename1 = "./static/image_"+image_Name+"/"+image_Name+"1.jpg"
    os.makedirs(os.path.dirname(filename1), exist_ok=True)
    with open(filename1,"wb") as f:
        f.write(response.images1)
    filename2 = "./static/image_"+image_Name+"/"+image_Name+"2.jpg"
    os.makedirs(os.path.dirname(filename2), exist_ok=True)
    with open(filename2,"wb") as f:
        f.write(response.images2)

# get imagelist according to name
def get_imagelist(city_name):
    imagelist = os.listdir('static/image_'+city_name)
    return imagelist

@app.route("/picture")
def picture():
    # use mircoservice get the image from server
    microsevice_image(session['travel_city'])
    if session['travel_city'] == 'New York':
        # creat the imagelist for the html
        imagelist = ['image_New York/'+ image for image in get_imagelist('New York')]
    elif session['travel_city'] == 'Los Angeles':
        imagelist = ['image_Los Angeles/'+ image for image in get_imagelist('Los Angeles')]
    elif session['travel_city'] == 'San Francisco':
        imagelist = ['image_San Francisco/'+ image for image in get_imagelist('San Francisco')]

    return render_template("picture.html", city_name = session['travel_city'], imagelist = imagelist)

@app.route("/main")
def back():
    return render_template("main.html")

@app.route("/options")
def backop():
    return render_template("options.html")
