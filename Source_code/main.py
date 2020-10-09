#database and flask
from flask import (Flask , render_template, request, url_for, redirect, flash,
session, abort)
from flask_sqlalchemy import (sqlalchemy, SQLAlchemy)
from werkzeug.security import (generate_password_hash, check_password_hash)
from tmdbv3api import (TMDb ,Movie)
tmdb = TMDb()
tmdb.api_key = '038ccad8e2308a919051973010c8ee94'
tmdb.language = 'en'
tmdb.debug = True
movie=Movie()

#Machine learning part
from MovieLens import MovieLens
from surprise import SVD, SVDpp
from Evaluator import Evaluator
import random
import numpy as np
import pandas as pd
from movie_by_genre import MovieGenres

def LoadMovieLensData():
    ml = MovieLens()
    print("Loading movie ratings...")
    data = ml.loadMovieLensLatestSmall()
    print("\nComputing movie popularity ranks ...")
    rankings = ml.getPopularityRanks()
    return (ml, data, rankings)

np.random.seed(0)
random.seed(0)

#Load up common data set for the recommender algorithms
(ml, evaluationData, rankings) = LoadMovieLensData()

#Construct an Evaluator to, you know, evaluate them
evaluator = Evaluator(evaluationData, rankings)

SVD
SVD = SVD()
evaluator.AddAlgorithm(SVD, "SVD")
movieInfo = MovieGenres()



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SECRET_KEY'] = 'LPU12345'
db=SQLAlchemy(app)
username=""
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '' % self.username
db.create_all()

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(username=username, pass_hash=hashed_pwd)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])



def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return render_template('show.html',movies=getRecommend(username),username=username)
        else:
            flash("Invalid username or password.")

    return render_template("login.html")

def getRecommend(username):
    user_id = int(username)
    movieInfo = MovieGenres()
    if user_id in movieInfo.users:
        results = evaluator.SampleTopNRecs(ml,testSubject=user_id,k=20)
        recommend=getmovie(results)
    else:
        results=movieInfo.movie_by_genre()
        recommend=getmovie(results)
    
    return recommend

def getmovie(results):
    details=[]
    for result in results:
        m=result.index('(')
        film_name=result[:m]
        print(film_name)
        try:
            search=movie.search(film_name)
            for res in search:
                my_data={'title':'random','overview':'random','poster':'random'}
                my_data['title']=res.title
                my_data['overview']=res.overview
                my_data['poster']=res.poster_path
                print("movie fetched "+my_data['title']+"...")
                details.append(my_data)
                break
        except:
            print("Movie not found not database trying for other....")
    return details

@app.route("/logout/<string:username>")
def logout(username):
    session.pop(username, None)
    flash("successfully logged out.")
    return redirect(url_for('login'))

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method=="POST":
        search_movie =request.form['search_movie']
        searched_movie=[]
        try:
            searched=movie.search(search_movie)
            for res in searched:
                my_data={'title':'random','overview':'random','poster':'random'}
                my_data['title']=res.title
                my_data['overview']=res.overview
                my_data['poster']=res.poster_path
                print("movie fetched "+my_data['title']+"...")
                searched_movie.append(my_data)
        except:
            print("Movie not found not database trying for other....")
        return render_template("searched.html",movies=searched_movie,movie=search_movie,username=username)
    else:
        return render_template("searched.html",movies=searched_movie,movie=search_movie,username=username)
# @app.rout('/movie',methods=['GET'])
# def recommend():
#     if request.method=='GET':



if __name__ == '__main__':
    app.run(debug=False)
