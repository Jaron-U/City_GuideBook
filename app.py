# Reference from: https://www.thepythoncode.com/article/extract-weather-data-python
import re
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import urllib.parse
import json
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




####Weater page
# Reference from: https://www.thepythoncode.com/article/extract-weather-data-python
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
LANGUAGE = "en-US,en;q=0.5"
# create a soup
def create_soup(soup):
    result = {}
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    result['temp_now'] = soup.find("span", attrs={"id": "wob_ttm"}).text
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
    return result

#get next days weather
def get_next_days(soup):
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"})[1:]:
        # extract the name of the day
        day_name = day.findAll("div")[0].attrs['aria-label']
        # get weather status for that day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        max_temp = temp[1].text
        min_temp = temp[3].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    return next_days

# get weather data
def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # creat a soup
    soup = bs(html.text, "html.parser")
    # store all results on this dictionary
    result = create_soup(soup)
    # get next few days' weather
    next_days = get_next_days(soup)
    result['next_days'] = next_days
    return result

@app.route("/weather")
def weather():
    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    city = session['travel_city']
    URL += city
    data = get_weather_data(URL)
    return render_template("weather.html", city_name = session['travel_city'], data = data, url = URL)




####distance###
def distance_read(url):
    url = ''.join(url.split())
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15')
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    return html

@app.route("/distance")
def distance():
    url = "https://www.trippy.com/distance/{0}-to-{1}".format(session['user_city'], session['travel_city'])
    html = distance_read(url)
    a = html.find('Nonstop drive: ') + 23
    b = html.find('<', a)
    distance_mile = html[a:b]
    c = b+21
    d = html.find('<', c)
    distance_km = html[c:d]
    e = html.find('Driving time: ') + 22
    f = html.find('<', e)
    driving_time = html[e:f]
    return render_template("distance.html", user_city = session['user_city'], city_name = session['travel_city'], 
    url = url, distance_m = distance_mile, distance_km = distance_km, driving_t = driving_time)





#####scenicspots####
def get_name_rating(item, result, soup, i):
    result['name'] = item.find('h4').get_text()
    result['reviewCount'] = soup.select('[class*=reviewCount]')[i].get_text()
    result['rating'] = soup.select('[aria-label*=rating]')[i]['aria-label']

def get_type_position(item, result):
    name = item.find("p")
    name = str(name)
    a = name.find("css-1p8aobs")+13
    b = name.find('<', a)
    result['type'] = name[a:b]
    c = name.find("css-1e4fdj9")+13
    d = name.find('<', c)
    result['position'] = name[c:d]

def get_link(item, result):
    u_link = "https://www.yelp.com/"
    link = item.find("a")
    link = str(link)
    a = link.find("css-1lwccx4") + 20
    b = link.find("\"", a)
    result['link'] = u_link+link[a:b]

@app.route("/scenicspots")
def scenicspots():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'}
    url = 'https://www.yelp.com/search?find_desc=scenic+spots&find_loc='+session['travel_city']
    response=requests.get(url,headers=headers)
    soup=bs(response.content,'lxml')
    restaustants = soup.select('[class*=container]')[10:18]
    i=0; t_result={}
    for item in restaustants:
        if item.find('h4'):
            result = {}
            get_name_rating(item, result, soup, i)
            get_type_position(item, result)
            get_link(item, result)
            t_result[i] = result
            i += 1
    return render_template("scenicspots.html", city_name = session['travel_city'], 
    url = url, result = t_result)



########restaurant##########
# Reference from: https://levelup.gitconnected.com/scraping-yelp-data-with-python-and-beautiful-soup-39f9088bf633
def get_name_rating_rest(item, result, soup, i):
    result['name'] = item.find('h4').get_text()
    result['reviewCount'] = soup.select('[class*=reviewCount]')[i+2].get_text()
    result['rating'] = soup.select('[aria-label*=rating]')[i+2]['aria-label']
    result['priceRange'] = soup.select('[class*=priceRange]')[i].get_text()

def get_type_rest(all_p, result):
    temp = all_p
    type_r = 'css-1p8aobs'
    types = ''
    while type_r in temp:
        a = temp.find('css-1p8aobs')+13
        b = temp.find('<', a)
        types += "["
        types += temp[a:b] + "]  "
        temp = temp[b:]
    result['type'] = types

def get_position_rest(all_p, result):
    a = all_p.find("css-1e4fdj9") + 13
    b = all_p.find("<", a)
    result['position'] = all_p[a:b]

def get_link_rest(item, result):
    link = item.find('h4')
    link = str(link)
    u_link = "https://www.yelp.com/"
    a = link.find('href=\"')+6
    b = link.find('\"', a)
    result['link'] = u_link+link[a:b]

@app.route("/restaurant")
def restaurant():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'}
    url='https://www.yelp.com/search?cflt=restaurants&find_loc='+session['travel_city']
    response=requests.get(url,headers=headers)
    soup=bs(response.content,'lxml')
    restaustants = soup.select('[class*=container]')[16:24]
    i=0; t_result={}
    for item in restaustants:
        if item.find('h4'):
            result = {}
            get_name_rating_rest(item, result, soup, i)
            all_p = item.find("p")
            all_p = str(all_p)
            get_type_rest(all_p,result)
            get_position_rest(all_p, result)
            get_link(item, result)
            t_result[i] = result
            i+=1
    return render_template("restaurant.html", city_name = session['travel_city'], 
    url = url, result = t_result)
