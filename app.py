from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_BINDS']={
        'two':'sqlite:///questions.db',
        'three':'sqlite:///users.db'}
db=SQLAlchemy(app)

class Posts(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    title=db.Column(db.String(200), nullable=False)
    content=db.Column(db.String(200), nullable=False)
    likes=db.Column(db.Integer, default=0)

class Questions(db.Model):
    __bind_key__='two'
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    ques=db.Column(db.String(200), nullable=False)
    ans=db.Column(db.String(200), default="No Answers")

class Users(db.Model):
    __bind_key__='three'
    Name=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(200), primary_key=True)
    password=db.Column(db.String(200), nullable=False)
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        n=request.form['Name']
        e=request.form['email']
        p=request.form['password']
        ele=Users(Name=n,email=e,password=p)
        db.session.add(ele)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')
@app.route('/add-question',methods=['GET','POST'])
def add_question():
    if request.method=='POST':
        t=request.form['title']
        q=request.form['ques']
        ele=Questions(title=t,ques=q)
        db.session.add(ele)
        db.session.commit()
        return redirect('/')
    return render_template('add-question.html')
@app.route('/questions/answer',methods=['GET','POST'])
def answered():
    if request.method=='POST':
        a=request.form['ans']
        ele=Questions(ans=ans)
        db.session.add(ele)
        db.session.commit()
        return redirect('/questions')
    allquestions=Questions.query.all()
    return render_template('questions.html')
@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        e=request.form['email']
        p=request.form['password']
        m= Users.query.filter_by(email=e).first()
        pp=m.password
        if(p==pp):
            return redirect('/')
    return render_template('login.html')
@app.route('/')
def myaccount():
    allposts=Posts.query.all()
    return render_template('myaccount.html',allposts=allposts)
@app.route('/posts')
def posts():
    allposts=Posts.query.all()
    return render_template('posts.html',allposts=allposts)
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')
@app.route('/add-post',methods=['GET','POST'])
def post_add():
    if request.method=='POST':
        t=request.form['title']
        c=request.form['content']
        n=request.form['name']
        ele= Posts(title=t, content=c,name=n)
        db.session.add(ele)
        db.session.commit()
        return redirect('/')
    return render_template('post-add.html')
if __name__=="__main__":
    app.run(debug=True, port=5000)