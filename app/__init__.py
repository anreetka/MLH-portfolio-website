import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

name="Anreet Kaur"

@app.route('/')
def index():
    active_page = 'home'
    return render_template('index.html', name="Anreet Kaur", active_page=active_page, url=os.getenv("URL"))



