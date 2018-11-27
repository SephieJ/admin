# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required
import services
from forms import TicketForm
from forms import TicketSupportForm
from forms import SupportChatForm
from flask_login import current_user
from app.src.utils import helpers
from flask import jsonify

TicketBP = Blueprint('TicketBP', __name__)


# Support Requests Page
@TicketBP.route('/support-requests', methods=['GET'])
@login_required
def ticket_page():
    tickets = services.get_tickets()
    return render_template("tickets/index.html", tickets=tickets)


# View Support Request Detail
@TicketBP.route('/support-requests/<int:ticket_id>', methods=['GET'])
@login_required
def view_tickets_page(ticket_id):
    ticket_form = TicketForm()
    if request.method == 'GET':
        ticket = services.view_tickets(ticket_id)
        return render_template('tickets/show.html', ticket=ticket, ticket_form=ticket_form)


# Close Ticket
@TicketBP.route('/support-requests/<int:ticket_id>/close', methods=['POST'])
@login_required
def close_tickets(ticket_id):
    ticket_form = TicketForm()
    support_id = current_user.id
    ticket = services.view_tickets(ticket_id)
    if request.method == 'GET':
        return render_template('tickets/show.html', ticket=ticket, ticket_form=ticket_form)
    elif request.method == 'POST':
        if ticket_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            solution = sanitized_inputs['solution']
            support = {
                'support_id': support_id,
                'solution': solution
            }
            close_tickets = services.close_tickets(ticket_id, support)
            if close_tickets.status_code == 202:
                flash('Successfully closed.', 'success')
                return redirect(url_for('.view_tickets_page', ticket_id=ticket_id))
            else:
                flash('Error in closing support request', 'danger')
                return redirect(url_for('.view_tickets_page', ticket_id=ticket_id))
        else:
            return render_template('tickets/show.html', ticket=ticket, ticket_form=ticket_form)


# Accept Ticket
@TicketBP.route('/support-requests/<int:ticket_id>/accept/', methods=['GET', 'POST'])
@login_required
def accept_tickets(ticket_id):
    support_id = current_user.id
    ticket_form = TicketForm()
    ticket = services.view_tickets(ticket_id)
    if request.method == 'GET':
        return render_template('tickets/show.html', ticket=ticket, ticket_form=ticket_form)
    elif request.method == 'POST':
        support = {'support_id': support_id}
        accept_tickets = services.accept_tickets(ticket_id, support)
        if accept_tickets.status_code == 202:
            flash('Ticket successfully accepted.', 'success')
            return redirect(url_for('.view_tickets_page', ticket_id=ticket_id))
        else:
            flash('Error in accepting support request', 'danger')
            return redirect(url_for('.view_tickets_page', ticket_id=ticket_id))
    else:
        return render_template('tickets/show.html', ticket=ticket, ticket_form=ticket_form)

@TicketBP.route('/admin/supportrequests', methods=['GET', 'POST'])
@login_required
def client_supportrequests_page():
    chats = services.support_chat_messages()
    if request.method == 'POST':
        support_form = TicketSupportForm()
        if support_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            tickets = {
                'reference_code': sanitized_inputs['reference_code'],
                'status'   : sanitized_inputs['status'],
                'admin_id' : current_user.id,
                'solution' : sanitized_inputs['solution'],
            }
            resp = services.admin_support_request_update(tickets)
    return jsonify(chats.json())

@TicketBP.route('/admin/supportrequests/<string:reference_code>', methods=['GET', 'POST'])
@login_required
def client_supportrequests_profile_page(reference_code):
    get_profile = services.support_requests_profile(reference_code)
    if request.method == 'POST':
        support_form = SupportChatForm()
        if support_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            conversation = {
                'reference_code': reference_code,
                'message': sanitized_inputs['message'],
                'sender_id' : current_user.id,
                'sender_type' : "Admin"
            }
            services.admin_support_conversations(conversation)
            get_profile = services.support_requests_profile(reference_code)
    return jsonify(get_profile.json())
