from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.listings.find_one()
    return render_template("index.html", listings=mars_data)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = mission_to_mars.scrape()
    listings.update(
        {},
        listings_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)