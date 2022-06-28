from ensurepip import bootstrap
from flask import Flask,jsonify, request
import pandas as pd
from flask import Flask, url_for, redirect,render_template 
from flask_bootstrap import Bootstrap
import random
app = Flask(__name__)
Bootstrap(app)


data = pd.read_csv('static/RisingWasabiOutput.csv')
df = pd.DataFrame(data,columns=["JP_title","JP_Body","Url_JP","Url_eng","English_Title","English_Body"])
print('----------------------',df[df['English_Title'].str.contains('Japan')].index)


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
        print(inpt)
        articles = []
        kw = ", ".join(inpt)
        for x in inpt:
            list_art = df[df['English_Title'].str.contains(x)].index
            print(list(list_art))
            articles += list(list_art) 
        articles_to_send = [[x, df.iloc[x]] for x in articles]
        return render_template("search.html",articles = articles_to_send, kw=kw)


        print(articles)




if __name__ == ("__main__"):
    app.run(debug=True)