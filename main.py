from flask import Flask, request, redirect, render_template, flash
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
   

    def __init__(self, title, body):
        self.title = title
        self.body = body




@app.route('/', methods=['POST', 'GET'])
def index():
    
    


    return render_template('blog.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        new_blog= Blog(title_name, body_name)
        db.session.add(new_blog)
        db.session.commit()
      
    return render_template('new_post.html')

    

if __name__ == "__main__":
    app.run()