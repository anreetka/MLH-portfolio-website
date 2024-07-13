import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict 

dotenv_path = os.path.join(os.path.dirname(__file__), '../example.env')
load_dotenv(dotenv_path=dotenv_path)
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
              user=os.getenv("MYSQL_USER"),
              password=os.getenv("MYSQL_PASSWORD"),
              host=os.getenv("MYSQL_HOST"),
              port=3306)

class TimelinePost(Model):
    name=CharField()
    email=CharField()
    content=TextField()
    created_at=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database =  mydb

mydb.connect()
mydb.create_tables([TimelinePost])
print(mydb)

name="Anreet Kaur"

@app.route('/')
def index():
    active_page = 'home'
    return render_template('index.html', name="Anreet Kaur", active_page=active_page, url=os.getenv("URL"))

@app.route('/work_experiences')
def work_experiences():
    work_experiences=[
        {'company': 'MLH Fellowship', 'position': 'Production Engineering Fellow', 'duration': 'Jun 2024 - Present', 'description': 'Received acceptance into highly selective (acceptance rate < 2.5%) Production Engineering program sponsored by Meta through MLH Fellowship'},
        {'company':'SIRT Centre - Research', 'position': 'Junior Programmer Intern', "duration": 'Jan 2024 - Apr 2024', 'description':'Got nominated for Generator Student Awards 2024 in "Team Collaboration in Research" category for outstanding teamwork in the Virtual Reality project during my internship'},
        {'company':'SkillHat', 'position': 'Diversity in Tech Talent: Web Development Fellow', "duration": 'Jan 2024 - Mar 2024', 'description':'Selected from over 1,000+ applicants for a $10,000 scholarship for this 3-month tech fellowship on  web development with best practices. Additionally, developed push notification features for a community project with JavaScript and Web Push Library, allowing smoother integration with Express js backend'},
        {'company':'Sheridan College', 'position': 'Peer Mentor - Team Lead', "duration": 'Sep 2023 - Dec 2023', 'description':'Earned nomination for Student Choice – Dare to Care Leadership Award for 2023-2024, recognizing exceptional commitment of a student leader to a supportive and inclusive campus environment'}
    ]
    return render_template('work_experiences.html', name=name, title="Work Experiences", work_experiences=work_experiences)

@app.route('/education')
def education():

    education=[
        {'institution': 'Sheridan College', 'degree': 'Computer Science Co-op (3-year)', 'duration': 'Dec 2025'}
    ]

    return render_template('education.html', name=name, title="Education", education=education)

@app.route('/hobbies')
def hobbies():

    hobbies=[
        {
            "activity":"Hiking",
            "image": "https://images.pexels.com/photos/1365425/pexels-photo-1365425.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        },
        {
            "activity":"Chess",
            "image": "https://en.chessbase.com/Portals/all/thumbs/112/112140%20(2).png"
        },
        {
            "activity": "Badminton",
            "image": "https://i0.wp.com/www.healthfitnessrevolution.com/wp-content/uploads/2014/03/badminton-1428047_1920-2.jpg?resize=1024%2C683&ssl=1"
        },
        {
            "activity": "Gardening",
            "image": "https://st2.depositphotos.com/1194063/5332/i/450/depositphotos_53326813-stock-photo-farmer-planting-young-seedlings.jpg"
        }
    ]

    return render_template('hobbies.html',  name=name, title="Hobbies", hobbies=hobbies)

@app.route('/map')
def map():
    return render_template('map.html', name=name, title="Map")

#add a timeline post
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email= request.form['email']
    content=request.form['content']
    timeline_post= TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)
    
#get all the timeline posts
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return{
        'timeline_posts':[
            model_to_dict(p)
            for p in
                TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

#delete the latest timeline post from a specific user
@app.route('/api/delete_timeline_post', methods=['POST'])
def delete_time_line_post():
    name=request.form['name']
    email=request.form['email']
    try:
        selected_post=TimelinePost.select().where((TimelinePost.name==name) & (TimelinePost.email==email)).order_by(TimelinePost.created_at.desc()).get()

        if selected_post:
            deleted_time = selected_post.created_at
            selected_post.delete_instance()
            return f"\nRecent post by {name} and {email} at {deleted_time} has been deleted."
    
    except DoesNotExist:
        return f"\nA post from {name} at {email} was not found in the database. please check again!"

