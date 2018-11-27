# -*- coding: utf-8 -*-
import base64
from flask import Blueprint, render_template, request, url_for, flash, redirect, session , jsonify
from flask_login import login_required
import services
from app.src.users import services as user_services
from forms import NewsletterForm
from app.src.utils import helpers

NewsletterBP = Blueprint('NewsletterBP', __name__)


# Newsletter Page
@NewsletterBP.route('/newsletter', methods=['GET', 'POST'])
@login_required
def newsletter_page():
    newsletter_form = NewsletterForm()
    if request.method == 'GET':
        users = user_services.get_all_users()
        user_key_pair = []
        for user_val in users:
            dic = {
                'email': user_val['email'],
                'name': user_val['first_name'] + ' ' +user_val['last_name']
            }
            user_key_pair.append(dic)
        return render_template('newsletter/index.html', newsletter_form=newsletter_form,
                                                        user_list=user_key_pair)
    elif request.method == 'POST':
        if newsletter_form.is_submitted():
            sanitized_inputs = helpers.sanitize(request.form)
            email_category = sanitized_inputs['email_category']
            emails = sanitized_inputs['emails']
            #emails = request.form.getlist('emails')

            b64_userpass = base64.b64encode('{}:{}'.format("mainadmin", "t!r@dm1nPH"))
            basic_auth = 'Basic {}'.format(b64_userpass)
            session['user_basic'] = basic_auth
            emails_arr = emails.split(',')
            #print type(emails_arr)
            #return jsonify(emails_arr)
            send_newsletter = services.send_newsletter(email_category, emails_arr)
            if send_newsletter.status_code == 200:
                flash('Newsletter succesfully sent.', 'success')
                return redirect(url_for('.newsletter_page'))
            else:
                flash('Error in sending newsletter.', 'danger')
                return redirect(url_for('.newsletter_page'))
        else:
            return render_template('newsletter/index.html', newsletter_form=newsletter_form)

# Newsletter Page
@NewsletterBP.route('/get-users-dt', methods=['GET', 'POST'])
@login_required
def get_user_dt_page():
    newsletter_form = NewsletterForm()
    if request.method == 'GET':
        users = user_services.get_all_users()
        user_key_pair = []
        for user_val in users:
            dic =  [ user_val['email'] , user_val['email'] + ' (' + user_val['first_name'] + ' ' +user_val['last_name'] +')' ]
            user_key_pair.append(dic)
        return jsonify({'data' : user_key_pair})
