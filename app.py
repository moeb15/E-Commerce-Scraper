from flask import Flask, render_template, request, Response, flash,redirect 
from utils.newegg_scraper import extract_data
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/',methods=['GET','POST'])
def homepage():
    if request.method == 'POST' and request.form['search_query'] != '':
        query = request.form['search_query']
        print(query)
        df, fname = extract_data(query)
        resp = Response(
               df.to_csv(),
               mimetype="text/csv",
               headers={"Content-disposition":
               f"attachment; filename={fname}"})
        #flash("File Downloaded!")
        return resp
    else:
        return render_template('homepage.html')


app.run(port=8080,host='0.0.0.0')