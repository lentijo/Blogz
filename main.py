from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:chloe@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    body = db.Column(db.String(3000))
   

    def __init__(self, title, body):
        self.title = title
        self.body = body




@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)
    

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all() 
    return render_template('blog.html', blogs=blogs)

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    blogs = Blog.query.all()
 
    
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        new_blog= Blog(title_name, body_name)
 
        
        if not title_name or not body_name:
            flash('All fields must be filled! Please try again.','error')
            return render_template('new_post.html', title_name=title_name, body_name=body_name)
        
        else:
            db.session.add(new_blog)
            db.session.commit()
            blog_id=new_blog.id
            return redirect('/single_post?id={0}' .format(blog_id))
      
    
    return render_template('new_post.html', blogs=blogs)

@app.route('/single_post')
def view_post():
    id = request.args.get('id')
    blog_query = Blog.query.filter_by(id=id).all()
    return render_template('single_post.html', title="", blog_query=blog_query)

if __name__ == "__main__":
    app.run()