# -*- coding: utf-8 -*-
import base64
import csv
import io
from flask import Blueprint, render_template, request, url_for, flash, redirect, session , jsonify
from flask_login import login_required
import services
from forms import InvitationForm, CSVEmailForm
from app.src.utils import helpers
from app.src.utils import constants

InvitationBP = Blueprint('InvitationBP', __name__)


# Invitation Page
@InvitationBP.route('/admin-users/invite', methods=['GET', 'POST'])
@login_required
def invitation_page():
    invitation_form = InvitationForm()
    csv_form = CSVEmailForm()
    if request.method == 'GET':
        return render_template('invitation/index.html', invitation_form=invitation_form,chat_url=constants.CHAT_SUPPORT_URL,csv_form=csv_form)
    elif request.method == 'POST':
        if invitation_form.is_submitted():
            sanitized_inputs = helpers.sanitize(request.form)
            emails = sanitized_inputs['emails']
            email_category = sanitized_inputs['email_category']
            b64_userpass = base64.b64encode('{}:{}'.format("mainadmin", "t!r@dm1nPH"))
            basic_auth = 'Basic {}'.format(b64_userpass)
            session['user_basic'] = basic_auth
            emails_arr = emails.split(',')
            send_invitation = services.send_invitation(email_category, emails_arr)
            services.remove_emails(email_category)
            print send_invitation.text
            if send_invitation.status_code == 200:
                flash('Email succesfully sent.', 'success')
                return redirect(url_for('.invitation_page'))
            else:
                flash('Error in sending email.', 'danger')
                return redirect(url_for('.invitation_page'))
        else:
            return render_template('invitation/index.html', invitation_form=invitation_form )

@InvitationBP.route('/admin-users/invite/upload', methods=['POST'])
@login_required
def upload_csv_page():
    csv_form = CSVEmailForm()
    if request.method == 'POST':
        if csv_form.is_submitted():
            sanitized_inputs = helpers.sanitize(request.form)
            email_category = sanitized_inputs['email_cat']
            f = request.files['csvfile']
            if not f:
                flash("No files has been uploaded", 'error')
                return redirect(url_for('.invitation_page'))
            services.remove_emails(email_category)
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            total = 0
            inserted = 0
            for row in csv_input:
                data_email = {
                    'name'  : row[0],
                    'email' : row[1],
                    'template_type' : sanitized_inputs['email_cat']
                }
                resp = services.send_emails(data_email)
                json = resp.json()
                if json['code'] == 200:
                    total += 1
                else:
                    inserted += 1
            flash("Successfull! {} records uploaded out of {} records.".format(
                total, inserted), 'success')
            if sanitized_inputs['email_cat'] == 'd':
                return redirect(url_for('.events_page'))
            else:
                return redirect(url_for('.invitation_page'))
# Invitation Page
@InvitationBP.route('/admin-users/events', methods=['GET', 'POST'])
@login_required
def events_page():
    invitation_form = InvitationForm()
    csv_form = CSVEmailForm()
    if request.method == 'GET':
        return render_template('events/index.html', events_form=invitation_form,chat_url=constants.CHAT_SUPPORT_URL,csv_form=csv_form)
    elif request.method == 'POST':
        if invitation_form.is_submitted():
            sanitized_inputs = helpers.sanitize(request.form)
            emails = sanitized_inputs['emails']
            email_category = sanitized_inputs['email_category']
            b64_userpass = base64.b64encode('{}:{}'.format("mainadmin", "t!r@dm1nPH"))
            basic_auth = 'Basic {}'.format(b64_userpass)
            session['user_basic'] = basic_auth
            emails_arr = emails.split(',')
            send_invitation = services.send_invitation(email_category, emails_arr)
            services.remove_emails(email_category)
            print send_invitation.text
            if send_invitation.status_code == 200:
                flash('Email succesfully sent.', 'success')
                return redirect(url_for('.events_page'))
            else:
                flash('Error in sending email.', 'danger')
                return redirect(url_for('.events_page'))
        else:
            return render_template('events/index.html', events_form=events_form )
