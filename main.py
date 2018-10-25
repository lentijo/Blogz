from flask import Flask, request, redirect, render_template, session, flash
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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')



@app.route('/signup' , methods=['POST' , 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

    #TODO - validate user's data
       
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
            #TODO - "remember" the user
        else:
            #TODO - user better response messaging
            return '<h1>Duplicate user</h1>'


    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)
    

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all() 
    owner = User.query.filter_by(email=session['email']).first()
    return render_template('blog.html', blogs=blogs, owner=owner)

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    blogs = Blog.query.all()
 
    
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        owner = User.query.filter_by(email=session['email']).first()
        new_blog= Blog(title_name, body_name, owner)
 
        
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