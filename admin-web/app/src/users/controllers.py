# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
import services, time
from app.src.home import services as home_services
from forms import UserForm
from flask import jsonify
from datetime import datetime


UserBP = Blueprint('UserBP', __name__)


# Registered Users Page
@UserBP.route('/users', methods=['GET'])
@login_required
def user_page():
    return render_template('users/index.html')
    # users = services.get_all_users(offset=0, limit=100)
    # if request.method == 'GET':
    #     return render_template('users/index.html', users=users)


@UserBP.route('/users/deactivated', methods=['GET'])
@login_required
def deactivated_user_page():
    return render_template('users/deactivated.html')


@UserBP.route('/users/unverified', methods=['GET'])
@login_required
def unverified_user_page():
    return render_template('users/unverified.html')


@UserBP.route('/datatables/users', methods=['GET'])
@login_required
def ajax_users_datatables():
    users = services.get_search_or_paginate(
        # offset = int(request.args.get('start')),
        # limit = int(request.args.get('length')),
        has_search = bool(request.args.get('search[value]')),
        search_value = str(request.args.get('search[value]')).lower(),
        order = str(request.args.get('order[0][dir]')),
        column = int(request.args.get('order[0][column]')) + 1,
        status = str(request.args.get('status'))
    )
    return jsonify({
        "draw": request.args.get('draw'),
        "recordsTotal": len(users),
        "recordsFiltered": len(users),
        # "recordsTotal": home_services.getAnalytics().json()['user_count'],
        # "recordsFiltered": len(users) if bool(request.args.get('search[value]')) \
        #     else home_services.getAnalytics().json()['user_count'],
        "data": users[int(request.args.get('start')):int(request.args.get('length')) + int(request.args.get('length')) if \
            bool(int(request.args.get('start'))) else int(request.args.get('length'))]
    })


# User Profile Page
@UserBP.route('/user-profile/', methods=['GET'])
@UserBP.route('/user-profile/<int:user_id>', methods=['GET'])
@login_required
def user_profile_page(user_id):
    user_form = UserForm()
    user = services.get_user_profile(user_id)
    if user['date_reminded']:
        label_date_display = 'Reminded Last: '
        date_display = user['date_reminded'].strftime('%d-%m-%Y %H:%M')
    elif user.has_key('email_reminder_send_date'):
        label_date_display = 'Scheduled Reminder On: '
        date_display = user['email_reminder_send_date'].strftime('%d-%m-%Y %H:%M')
    else:
        date_display = None
        label_date_display = None
    return render_template('users/show.html', user=user, user_form=user_form, date_display=date_display, label_date_display=label_date_display)


# Restore Account
@UserBP.route('/user-profile/<int:user_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_account(user_id):
    user_form = UserForm()
    user = services.get_user_profile(user_id)
    if request.method == 'GET':
        return render_template("users/show.html", user=user, user_form=user_form)
    elif request.method == 'POST':
        if user_form.validate():
            restore_user = services.restore_user_account(user_id)
            if restore_user.status_code == 202:
                # flash('Successfully restored.', 'success')
                return redirect(url_for('.user_profile_page', user_id=user_id))
            else:
                # flash(restore_user.text, 'danger')
                return redirect(url_for('.user_profile_page', user_id=user_id))
        else:
            return render_template('users/show.html', user=user, user_form=user_form)


# Ban Account
@UserBP.route('/user-profile/<int:user_id>/ban', methods=['GET', 'POST'])
@login_required
def ban_account(user_id):
    user_form = UserForm()
    user = services.get_user_profile(user_id)
    if request.method == 'GET':
        return render_template("users/show.html", user=user, user_form=user_form)
    elif request.method == 'POST':
        if user_form.validate():
            ban_user = services.ban_user_account(user_id)
            if ban_user.status_code == 202:
                # flash('Successfully banned.', 'success')
                return redirect(url_for('.user_profile_page', user_id=user_id))
            else:
                # flash(ban_user.text, 'danger')
                return redirect(url_for('.user_profile_page', user_id=user_id))
        else:
            return render_template('users/show.html', user=user, user_form=user_form)


# Deactivate Account
@UserBP.route('/user-profile/<int:user_id>/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate_user(user_id):
    if request.method == 'GET':
        deactivate_user = services.deactivate_user_account(user_id)
        if deactivate_user.status_code == 202:
            flash('Successfully deactivated.', 'success')
            return redirect(url_for('.user_profile_page', user_id=user_id))
        else:
            flash(deactivate_user.text, 'danger')
            return redirect(url_for('.user_profile_page', user_id=user_id))


# Resend email
@UserBP.route('/user-profile/<int:user_id>/users/resend/email', methods=['GET','POST'])
@login_required
def resend_email(user_id):
    user_form = UserForm()
    user = services.get_user_profile(user_id)
    # return jsonify(user)
    if request.method == 'GET':
        return render_template('users/show.html', user=user, user_form=user_form)
    elif request.method=='POST':
        if user_form.validate_on_submit():
            # resend_email = services.resend_emails(user_id)
            resend_email = services.resend_emails(user['email'])
            print resend_email.status_code
            if resend_email.status_code == 202:
                flash('Successfully resend the email.', 'success')
                return redirect(url_for('.user_profile_page', user_id=user_id))
            else:
                flash('Error in resending email.', 'danger')
                return redirect(url_for('.user_profile_page', user_id=user_id))
        else:
            return render_template('users/show.html', user=user, user_form=user_form)
