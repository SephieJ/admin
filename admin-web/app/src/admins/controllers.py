# -*- coding: utf-8 -*-

import base64
from flask import Blueprint, render_template, request, flash, redirect, url_for, session , jsonify
from flask_login import login_required
import services
import time
from datetime import datetime
import dateutil.parser
from forms import AdminForm, UpdateForm, ChangePasswordForm
from app.src.utils import helpers


AdminBP = Blueprint('AdminBP', __name__)


# List of Admin Users Page
@AdminBP.route('/admin-users', methods=['GET'])
@login_required
def admin_page():
    admins = services.get_all_admins()
    if request.method == 'GET':
        return render_template('admins/index.html', admins=admins)


# Add Admin User
@AdminBP.route('/admin-users/add', methods=['GET', 'POST'])
@login_required
def add_admin_page():
    admin_form = AdminForm()
    if request.method == 'GET':
        return render_template("admins/add.html", admin_form=admin_form)
    elif request.method == 'POST':
        if admin_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            first_name = sanitized_inputs['first_name']
            last_name = sanitized_inputs['last_name']
            landline_number = sanitized_inputs['landline_number']
            mobile_number = sanitized_inputs['mobile_number']
            # image = request.files['image']
            #birth_date = sanitized_inputs['birth_date']
            designation = sanitized_inputs['designation']
            email = sanitized_inputs['email']
            roles = sanitized_inputs['roles']
            username = sanitized_inputs['username']
            password = sanitized_inputs['password']
            #date_object = datetime.strptime(birth_date, "%d-%m-%Y")
            # if image.filename is None:
            #     image_url = ''

            # else:
            #     image_url = helpers.upload(image)

            admin = {
                'first_name': first_name,
                'last_name': last_name,
                # 'image_url': image_url,
                'landline_number': landline_number,
                'mobile_number': mobile_number,
                #'image_url': image_url,
                #'birth_date': date_object.strftime("%Y-%m-%d"),
                'designation': designation,
                'email': email,
                'roles': roles,
                'username': username,
                'password': password,
            }
            add_admin = services.add_admin(admin)
            if add_admin.status_code == 201:
                flash('Successfully created a new Admin User', 'success')
                return redirect(url_for('.admin_page'))
            else:
                flash('Error in creating Admin User', 'danger')
                return render_template('admins/add.html', admin_form=admin_form)
        else:
            return render_template('admins/add.html', admin_form=admin_form)


# User Profile Page
@AdminBP.route('/admin-user/<string:username>', methods=['GET'])
@login_required
def admin_profile_page(username):
    admin_form = AdminForm()
    admin = services.get_admin_profile(username)
    # return jsonify(admin)
    return render_template('admins/show.html', admin=admin, admin_form=admin_form)


# Update Admin User
@AdminBP.route('/admin-user/<string:username>/edit', methods=['GET', 'POST'])
@login_required
def edit_admin_page(username):
    admin_form = UpdateForm()
    admin = services.get_admin_profile(username)
    if request.method == 'GET':
        return render_template("admins/edit.html", admin_form=admin_form, admin=admin)
    elif request.method == 'POST':
        if admin_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            first_name = sanitized_inputs['first_name']
            last_name = sanitized_inputs['last_name']
            landline_number = sanitized_inputs['landline_number']
            mobile_number = sanitized_inputs['mobile_number']
            #image = request.files['image']
            #birth_date = sanitized_inputs['birth_date']
            designation = sanitized_inputs['designation']
            email = sanitized_inputs['email']
            roles = sanitized_inputs['roles']
            #date_object = datetime.strptime(birth_date, "%d-%m-%Y")
            # if image.filename is None:
            #     image_url = ''
            # else:
            #     image_url = helpers.upload(image)
            # birth_date = dateutil.parser.parse(birth_date)
            #bday = datetime.strptime(birth_date, "%d-%m-%Y").strftime("%Y-%m-%d")

            admin = {
                'first_name': first_name,
                'last_name': last_name,
                'landline_number': landline_number,
                'mobile_number': mobile_number,
                #'image_url': image_url,
                #'birth_date':  bday,
                'designation': designation,
                'email': email,
                'roles': roles
            }
            print admin
            edit_admin = services.edit_admin_user(username, admin)
            if edit_admin.status_code == 202:
                flash(edit_admin.text, 'success')
                return redirect(url_for('.admin_page'))
            else:
                flash(edit_admin.text, 'danger')
                return render_template('admins/edit.html', admin_form=admin_form, admin=admin)
        else:
            return render_template('admins/edit.html', admin_form=admin_form, admin=admin)


# Delete Admin User
@AdminBP.route('/admin-user/<string:username>/delete', methods=['POST'])
@login_required
def delete_admin(username):
    admin_form = AdminForm()
    admin = services.get_admin_profile(username)
    if request.method == 'GET':
        return render_template("admins/show.html", admin_form=admin_form, admin=admin)
    elif request.method == 'POST':
        delete_admin = services.delete_admin_user(username)
        if delete_admin.status_code == 202:
            # flash('Successfully banned.', 'success')
            return redirect(url_for('.admin_profile_page', username=username))
        else:
            # flash('Error in banning resource', 'danger')
            return redirect(url_for('.admin_profile_page', username=username))
    else:
        return render_template('admins/show.html', admin=admin, admin_form=admin_form)


# Restore Companies
@AdminBP.route('/admin-user/<string:username>/restore', methods=['GET', 'POST'])
@login_required
def restore_admin(username):
    admin_form = AdminForm()
    admin = services.get_admin_profile(username)
    if request.method == 'GET':
        return render_template("admins/show.html", admin_form=admin_form, admin=admin)
    elif request.method == 'POST':
        restore_admin = services.restore_admin_user(username)
        if restore_admin.status_code == 202:
            flash('Successfully banned.', 'success')
            return redirect(url_for('.admin_profile_page', username=username))
        else:
            flash('Error in banning resource', 'danger')
            return redirect(url_for('.admin_profile_page', username=username))
    else:
        return render_template('admins/show.html', admin=admin, admin_form=admin_form)


# Change Password
@AdminBP.route('/admin-user/<string:username>/password', methods=['GET', 'POST'])
@login_required
def change_password(username):
    change_password_form = ChangePasswordForm()
    password = services.get_admin_profile(username)
    if request.method == 'GET':
        return render_template("admins/change_pw.html", change_password_form=change_password_form, password=password)
    elif request.method == 'POST':
        if change_password_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            old_password = sanitized_inputs['old_password']
            new_password = sanitized_inputs['new_password']
            confirm_password = sanitized_inputs['confirm_password']
            change_password = services.change_password(username, old_password, new_password, confirm_password)
            if change_password.status_code == 202:
                flash('Password successfully changed.' 'success')
                return redirect(url_for('.admin_page'))
            else:
                flash('Error in changing password.' 'danger')
                return redirect(url_for('.admin_page'))
                b64_userpass = base64.b64encode('{}:{}'.format(username, new_password))
                basic_auth = 'Basic {}'.format(b64_userpass)
                session['user_basic'] = basic_auth
        else:
            return render_template('admins/change_pw.html', change_password_form=change_password_form, password=password)
