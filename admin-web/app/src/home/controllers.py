# -*- coding: utf-8 -*-

import base64
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
import services
from flask_login import login_required, logout_user, current_user, login_user
from app.src.companies import services as company_services
from app.src.resources import services as resource_services
from app.src.users import services as user_services
from app.src.tickets import services as ticket_services
from app.src.utils import helpers
from app.src.users.models import User
from app.src.users import dao as user_dao

from forms import LoginForm
import time

HomeBP = Blueprint('HomeBP', __name__)


@HomeBP.route('/', methods=['GET'])
@login_required
def home():
    data = services.getAnalytics().json()
    resources = resource_services.get_resources(limit=4)
    users = user_services.get_all_users(limit=12)
    return render_template("dashboards/index.html", data=data,
                           resources=resources, users=users)


@HomeBP.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('.home'))
    elif request.method == 'POST' and login_form.validate_on_submit():
        sanitized_inputs = helpers.sanitize(request.form)
        username = sanitized_inputs['username']
        password = sanitized_inputs['password']
        b64_userpass = base64.b64encode('{}:{}'.format(username, password))
        basic_auth = 'Basic {}'.format(b64_userpass)
        user_creds = {
            'username': username,
            'password': password
        }
        login = services.login(user_creds, basic_auth)
        print login
        if login.status_code == 200:
            has_admin_role = False
            for role in login.json()['roles']:
                if role == 'ADMIN':
                    has_admin_role = True
            if has_admin_role:
                user = User(login.json())
                session['user_basic'] = basic_auth
                login_user(user)
                if user_dao.get(user.id) is None:
                    user_dao.add(user)
                else:
                    user_dao.update(user)
                return redirect(url_for('.home'))
            else:
                flash("You have no admin rights", 'danger')
        else:
            flash(login.content, 'danger')
    return render_template('login.html', login_form=login_form)


@HomeBP.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # services.logout(current_user.id)
    logout_user()
    return redirect(url_for('.login'))
