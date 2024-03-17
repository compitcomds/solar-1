from flask import Blueprint,redirect,flash,render_template,url_for,request,session
from Solar import app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin,login_user,login_required,current_user,logout_user
from Solar.Auth.form import LoginForm, RegistrationForm, ForgotPasswordForm, OtpForm, ResetPasswordForm
from secrets import token_hex
from Solar.database import db
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from Solar.Auth.otp import check_otp,generate_otp

## can use flask cache memory to store the memeory into flask carche ##

Auth=Blueprint('Auth',__name__,template_folder='templates/Auth',static_folder='')


bcrypt = Bcrypt(app)
login_manager=LoginManager(app)


class User(UserMixin):
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role=role

    def get_id(self):
        return str(self.user_id)

    @staticmethod
    def get(user_id, name, role):
        return User(user_id=user_id, name=name,role=role)

      

@login_manager.user_loader
def load_user(user_id):
    # Assuming you have a way to retrieve the user from the user ID
    user_data = db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data['_id'], user_data['name'],user_data['role'])
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@Auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_data = db.users.find_one({'email': form.email.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user = User(user_data['_id'],user_data['name'],user_data['role'])
            token = token_hex(16)  # Generate a 32-character random token
            db.users.update_one({'_id': user.user_id}, {'$set': {'token': token}})
            login_user(user)
            if user_data['role'] in ['Admin']:
                response = redirect(url_for('Admin.Admin_index'))###--- this also change
                response.set_cookie('token', token)
                return response
            elif user_data['role'] in ['User']:
                response = redirect(url_for("User.user_index"))###--- this also change
                response.set_cookie('token', token)
                return response
        else:
            flash('Invalid username or password!', 'error')
    return render_template('login.html', form=form)

@Auth.route('/register', methods=['GET', 'POST'])
def register():
    collection = db['users']
    form = RegistrationForm()
    if form.validate_on_submit():
        if db.users.find_one({'email': form.email.data}):
            flash('Email already exists!','error')    
        else:
            date=str(datetime.now()+timedelta(days=30))[0:10]
            
            password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            data = {'email': form.email.data,
                    'password': password_hash,
                    'name': form.name.data ,
                    'role': 'User',
                    'token':None,
                    'date_of_register':date,
                    'active':0,
                    }
            collection.insert_one(data)
            flash('Registration successful! You can now login.', 'success')
            return redirect('/login')
    return render_template('register.html', form=form)


@Auth.route('/forgot_password' , methods=['GET', 'POST'])
def forgot_password():
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        userX=db.users.find_one({'email':email})
        if userX:
            session['email']=email
            session['otp_bycrypt']=generate_otp(email,6)
            return redirect (url_for('Auth.otp'))
        flash('Not user', 'error')
        return render_template('forgot_password.html',form=form)
        
        # return session.get('email')
    return render_template('forgot_password.html',form=form)

@Auth.route('/otp', methods=['GET', 'POST'])
def otp():
    if session.get('email') and session.get('otp_bycrypt') :
        form=OtpForm()
        if form.validate_on_submit():
            otp=form.otp.data
            if check_otp(otp,session.get('otp_bycrypt')):
                return redirect (url_for('Auth.reset_password'))
            else:
                flash('Invalid Otp!', 'error')
                return render_template('otp.html',form=form)
        return render_template('otp.html',form=form)
    else:
        return redirect (url_for('Auth.forgot_password'))


@Auth.route('/resetPassword', methods=['GET', 'POST'])
def reset_password():
    if not session.get('email'):
        return redirect (url_for('Auth.login'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.users.update_one({'email': session.get('email')}, {'$set': {'password': password_hash}})
        session.pop('email',None)
        session.pop('otp_bycrypt',None)
        return redirect(url_for('Auth.login'))
    return render_template('resetPassword.html',form=form)


@Auth.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
    

@Auth.route('/logout')
@login_required
def logout():
    db.users.update_one({'_id': current_user.user_id}, {'$set': {'token': None}})
    logout_user()
    response = redirect(url_for('Auth.login'))
    response.delete_cookie('token')  # Remove the token cookie
    session.clear()
    return redirect (url_for('index'))


