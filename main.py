from flask import Flask,jsonify, request
import pandas as pd
from flask import Flask, url_for, redirect,render_template 
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
Bootstrap(app)


data = pd.read_csv('static/RisingWasabiOutput.csv')
df = pd.DataFrame(data,columns=["JP_title","JP_Body","Url_JP","Url_eng","English_Title","English_Body"]).dropna()


# Website routes
@app.route('/')
def home(): 
    nums = random.sample(range(0,90),5)
    articles_to_send = [[x, df.iloc[x]] for x in nums]
    print(articles_to_send)
    return render_template('home.html',articles = articles_to_send)
    

@app.route('/pages/<num>')
def ind_page(num):
    article_to_send = df.iloc[int(num)]
    print(article_to_send)
    return render_template('blog_page.html',article = article_to_send)

@app.route('/search', methods={"POST","GET"})
def kw_search():
    if request.method == "POST" and request.form:
        inpt = request.form['inpt'].split(' ')
        print(request,inpt)
        articles = []
        kw = ", ".join(inpt)
        print(kw)

        for x in inpt:
            list_art = df[df['English_Title'].str.contains(x.capitalize())].index
            print(list(list_art))
            articles += list(list_art) 
        articles_to_send = [[x, df.iloc[x]] for x in articles if x !=95]
        # print(articles_to_send)
        return render_template("search.html",articles = articles_to_send, kw=kw)


# API routes:

# all articles in JSON
@app.route('/all')
def all():
    all_articles =[{
            "JP_title": x["JP_title"],
            "JP_Body": x["JP_Body"],
            "Url_JP": x["Url_JP"],
            "Url_eng": x["Url_eng"],
            "English_Title": x["English_Title"],
            "English_Body": x["English_Body"],
        } for i, x in df.iterrows()
    ]
    return jsonify(all_articles)


# Individual article in JSON
@app.route('/all/<int:article>')
def article_api(article):
    ind_art = df.iloc[int(article)]
    print(ind_art)
    art = {
            "JP_title": ind_art["JP_title"],
            "JP_Body": ind_art["JP_Body"],
            "Url_JP": ind_art["Url_JP"],
            "Url_eng": ind_art["Url_eng"],
            "English_Title": ind_art["English_Title"],
            "English_Body": ind_art["English_Body"],        
        }
    return jsonify({"article":art})


# Find all with the entered Keywords
@app.route('/all/search-json',methods=['GET', "POST"])
def search():
    if request.method == "POST":
        kw = request.form['inpt'].split()
        print(kw)
        articles = []
        for x in kw:
            list_art = df[df['English_Title'].str.contains(x.capitalize())].index
            print(list(list_art))
            articles += list(list_art) 
        print('=============================',articles)

        articles_to_send = [df.iloc[x] for x in articles if x !=95]
        print('============================',articles_to_send)
        art = [{
                "JP_title": x["JP_title"],
                "JP_Body": x["JP_Body"],
                "Url_JP": x["Url_JP"],
                "Url_eng": x["Url_eng"],
                "English_Title": x["English_Title"],
                "English_Body": x["English_Body"],        
            } for x in articles_to_send
        ]
       
        return jsonify(art)

app.config['JSON_AS_ASCII'] = False

if __name__ == ("__main__"):
    app.run(debug=False)
