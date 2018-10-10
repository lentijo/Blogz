from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:chloe@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    body = db.Column(db.String(3000))
   

    def __init__(self, title):
        self.title = title
        self.body = body

tasks = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)

    return render_template('blog.html',title="Build A Blog", tasks=tasks)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    return render_template('blog.html',title="Build A Blog", tasks=tasks)

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)
    return render_template('new_post.html',title="Add a new Blog", tasks=tasks)

    

if __name__ == "__main__":
    app.run()