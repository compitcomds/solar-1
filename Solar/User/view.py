from flask import Blueprint, redirect , url_for
from flask_login import login_required,current_user
from Solar.database import db


User=Blueprint('User',__name__,template_folder='templates/User',static_folder='')

@User.before_request
@login_required
def check_is_User():
    id=current_user.user_id
    if not(current_user.is_authenticated  and current_user.role=='User'):
        return "<h1>this is invalid</h1>","403"


@User.route('/')
def user_index():
    return redirect(url_for('index'))
