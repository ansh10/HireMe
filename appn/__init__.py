
#<----------------------------Initialization------------------------------------>
from flask import Flask, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import desc

app = Flask(__name__)
mail = Mail(app)
csrf = CSRFProtect(app)
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.fastmail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USERNAME'] = 'mehire@fastmail.com'
app.config['MAIL_PASSWORD'] = 'Hireme060124'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///appn.db'
app.config['SECRET_KEY']='a9e8114cc489fd31534dfa47'
db=SQLAlchemy(app)
#<------------------------------------------------------------------------------>
#<-----------------------------db-models---------------------------------------->
class Employer_post(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=50),nullable=False)
    company_name=db.Column(db.String(length=50),nullable=False)
    email_address=db.Column(db.String(length=60),nullable=False)
    role=db.Column(db.String(length=40),nullable=False)
    skills_req=db.Column(db.String(length=100),nullable=False)

class User(db.Model): 
    id = db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=50),nullable=False)
    age=db.Column(db.Integer(),nullable=False)
    interested_role=db.Column(db.String(length=30),nullable=False)
    skills=db.Column(db.String(length=100),nullable=False)
#<------------------------------------------------------------------------------>
#<---------------------------------forms---------------------------------------->
from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email

class EmployerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    company_name = StringField('Company', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = StringField('job position', validators=[DataRequired()])
    skills1 = StringField('Skill set required', validators=[DataRequired()])
    post = SubmitField('POST')

class JobSeekerForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    role = StringField('job position', validators=[DataRequired()])
    skills2 = StringField('Skill set required', validators=[DataRequired()])
    Next = SubmitField('NEXT')

class ApplyForm(FlaskForm):
    post_id = HiddenField('Post ID')
    submit=SubmitField(label='Apply')
#<----------------------------------------------------------------------------->


#<---------------------------------routes-------------------------------------->
@app.route('/')
@app.route('/home')
def index():
    return render_template('homepage.html', title ='Home')

@app.route('/about')
def abt():
    return render_template('about.html')


@app.route('/Post-Employer') 
def post_employer():
    return render_template('postemployer.html')


@app.route('/Employer', methods = ['GET','POST'])
def Employer():
    form = EmployerForm()
    if form.is_submitted():
        post=Employer_post(name=form.name.data,company_name=form.company_name.data,email_address=form.email.data,role=form.role.data,skills_req=form.skills1.data)
        db.session.add(post)
        db.session.commit()
        print('yeaaaa')
        return redirect(url_for('post_employer'))
    return render_template('employer_page.html',form=form)


@app.route('/Main-Dashboard')
def Dashboard():
    posts=Employer_post.query.all()
    form = ApplyForm()
    return render_template('dashboard.html',posts=posts, form = form)


@app.route('/Job-Seeker', methods = ['GET','POST'])
def Job_Seeker():
    form = JobSeekerForm()
    if form.is_submitted():
        user=User(username=form.username.data,age=form.age.data,interested_role=form.role.data,skills=form.skills2.data)
        db.session.add(user)
        db.session.commit()
        print('yeaaaa')
        return redirect(url_for('Dashboard'))
    return render_template('job_seeker.html',form=form)
    
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        form = ApplyForm(request.form)
        if form.validate():
            post_id = form.post_id.data
            print(f"Post ID: {post_id}")
            latest_user = User.query.order_by(User.id.desc()).first_or_404()
            applicant_name = latest_user.username
            #print( applicant_name)
        else:
            print("Form validation failed.")
    return render_template('homepage.html')
    


#<----------------------------------------------------------------------------->