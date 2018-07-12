import os
import logging
import requests
import json


from flask import Flask, session, render_template, request,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == None or password == None:
        return render_template("index.html")

    search = db.execute("SELECT username, password, id FROM users WHERE username = :username AND password = :password", {
                        "username": username, "password": password}).fetchall()
    if search[0][0] == username and search[0][1] == password:
        session["username"] = username
        session["user_id"] = search[0][2]
        return render_template("login.html")
    else:
        return render_template("error.html", message="Please Register User")


@app.route("/login", methods=["POST"])
def login():
    checks=True
    zipcode = request.form.get("zipcode")
    city = request.form.get("city")
    if(zipcode == None or city==None):
        zipcodes = []
        cities = []
    else:
        if len(zipcode)>0:
            query = "SELECT * FROM city WHERE zipcode LIKE '" + zipcode + "%'"
            zipcodes = db.execute(query).fetchall()
            return render_template("login.html", check=True, zipcode=zipcodes)

        if len(city)>0:
            query_1 = "SELECT * FROM city WHERE city LIKE '" + city + "%'"
            cities = db.execute(query_1).fetchall()
            return render_template("login.html", check=False,  citie=cities)



@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return render_template("message.html",message="You have Logged Out")

@app.route("/newuser", methods=["GET", "POST"])
def newuser():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == None or password == None:
        return render_template("newuser.html")

    search = db.execute("SELECT username, password FROM users WHERE username = :username AND password = :password", {
                        "username": username, "password": password}).fetchall()
    if len(search) > 0:
        if search[0][0] == username and search[0][1] == password:
            return render_template("error.html", message="Please Login Username already exists")
    else:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                   {"username": username, "password": password})
        db.commit()
        return render_template("success.html", message="Congratulations! You have successfully Registered. Please login for more details")


@app.route("/location/<int:id>", methods=["GET", "POST"])
def location(id):
    user_id = session["user_id"]
    comment = request.form.get("comment")
    checkinValue = request.form.get("checkin")

    if comment != None:
        checkin = 0
        if checkinValue == "checked":
            checkin = 1
        db.execute("INSERT INTO comments (comment, city_id, user_id, checkin) VALUES (:comment, :city_id, :user_id, :checkin)", {
                   "comment": comment, "city_id": id, "user_id": user_id, "checkin": checkin})
        db.commit()

    city_results = db.execute(
        "SELECT city, zipcode, latitude, longitude, population FROM city WHERE id = :id", {"id": id}).fetchall()
    checkin_results = db.execute(
        "SELECT comment FROM comments WHERE city_id = :id AND user_id = :user_id", {"id": id, "user_id": str(user_id)}).fetchall()

    if len(city_results) > 0:
        weather = requests.get("https://api.darksky.net/forecast/54184c3c3683185042f952fa3414f747/" +
                               str(city_results[0].latitude) + "," + str(city_results[0].longitude)).json()
        currentWeather = weather["currently"]
        if len(checkin_results) == 0 and comment is None:
            check = False
            return render_template("location.html", checks=check, url="location/" + str(id), id=id, time=currentWeather["time"], dewpoint=currentWeather["dewPoint"], temp=currentWeather["temperature"], humidity=currentWeather["humidity"], windSpeed=currentWeather["windSpeed"], ozone=currentWeather["ozone"])
        if len(checkin_results) > 0:
            check = True
            return render_template("location.html", checks=check, url="location/" + str(id), id=id, time=currentWeather["time"], dewpoint=currentWeather["dewPoint"], temp=currentWeather["temperature"], humidity=currentWeather["humidity"],windSpeed=currentWeather["windSpeed"], ozone=currentWeather["ozone"], cresult=city_results, checkin_result=checkin_results[0][0])

    return render_template("success.html")


@app.route("/api/<string:zipcode>", methods=["GET", "POST"])
def api(zipcode):
    city_results = db.execute(
        "SELECT id, city, state, zipcode, latitude, longitude, population FROM city WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchall()
    if len(city_results) == 0:
        return jsonify({"error": "Invalid Zipcode"}), 422
    city_id = city_results[0][0]
    checkin_data = db.execute("SELECT SUM(checkin) FROM comments WHERE city_id = :city_id", {"city_id": city_id}).fetchall()
    checkin_data=checkin_data[0][0]

    return jsonify({
        "Name of the place": city_results[0][1],
        "State": city_results[0][2],
        "Zipcode": city_results[0][3],
        "Latitude": float(city_results[0][4]),
        "No of Checkins": checkin_data
    })



