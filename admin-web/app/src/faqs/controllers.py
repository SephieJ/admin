# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_required
import services
from forms import FaqsForm, QuestionsForm
from app.src.utils import helpers
from HTMLParser import HTMLParser
import ast

FaqBP = Blueprint('FaqBP', __name__)


# FAQs Page
@FaqBP.route('/faqs', methods=['GET'])
@FaqBP.route('/faqs/', methods=['GET'])
@login_required
def faq_page():
    return index()


# Add FAQs
@FaqBP.route('/faqs/add', methods=['GET', 'POST'])
@login_required
def add_faq_page():
    faqs_form = FaqsForm()
    if request.method == 'GET':
        return render_template("faqs/add.html", faqs_form=faqs_form)
    elif request.method == 'POST':
        if faqs_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            faqs = {
                'name': name,
                'description': description
            }
            add_faq = services.add_faqs(faqs)
            if add_faq.status_code == 201:
                flash(add_faq.text, 'success')
                return redirect(url_for('.faq_page'))
            else:
                flash('Error in FAQ Category', 'danger')
                return render_template('faqs/add.html', faqs_form=faqs_form)
        else:
            return render_template('faqs/add.html', faqs_form=faqs_form)


# View FAQ Detail
@FaqBP.route('/faqs/<int:faq_id>', methods=['GET'])
@login_required
def view_faq_page(faq_id):
    if request.method == 'GET':
        if faq_id is None:
            return index()
        else:
            faq = services.view_faq(faq_id)
            questions = services.get_questions(faq_id)
            faq = services.view_faq(faq_id)
            return render_template("faqs/show.html",
                                    questions=questions,
                                    faq=faq)


# Update FAQs
@FaqBP.route('/faqs/<int:faq_id>/edit', methods=['GET', 'POST'])
@login_required
def update_faq_page(faq_id):
    faqs_form = FaqsForm()
    faq = services.view_faq(faq_id)
    if request.method == 'GET':
        faqs_form.description.data = faq['description']
        return render_template('faqs/edit.html', faq=faq, faqs_form=faqs_form)
    elif request.method == 'POST':
        if faqs_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            faqs = {
                'name': name,
                'description': description
            }
            update_faq = services.edit_faq(faq_id, faqs)
            if update_faq.status_code == 202:
                flash(update_faq.text, 'success')
                return redirect(url_for('.faq_page'))
            else:
                flash('Error in FAQ Category', 'danger')
                return render_template('faqs/edit.html', faq=faq, faqs_form=faqs_form)
        else:
            return render_template('faqs/edit.html', faq=faq, faqs_form=faqs_form)


# Delete FAQs
@FaqBP.route('/faqs/<int:faq_id>/delete', methods=['GET'])
@login_required
def delete_faq(faq_id):
    if request.method == 'GET':
        delete_faq = services.delete_faq(faq_id)
        if delete_faq.status_code == 202:
            flash(delete_faq.text, 'success')
            return redirect(url_for('.faq_page'))
        else:
            flash(delete_faq.text, 'danger')
        return redirect(url_for('.faq_page'))


# Archived FAQs Page
@FaqBP.route('/faqs/archived', methods=['GET'])
@login_required
def archived_faq_page():
    faqs = services.get_archived_faqs()
    return render_template("faqs/archived.html", faqs=faqs)


# Restore FAQs
@FaqBP.route('/faqs/<int:faq_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_faq(faq_id):
    if request.method == 'GET':
        restore_faq = services.restore_faqs(faq_id)
        if restore_faq.status_code == 202:
            flash('Successfully restored.', 'success')
        else:
            flash(restore_faq.text, 'danger')
        return redirect(url_for('.archived_faq_page'))


# Questions Page
@FaqBP.route('/faqs/<int:faq_id>/questions', methods=['GET'])
def question_page(faq_id):
    if request.method == 'GET':
        questions = services.get_questions(faq_id)
        faq = services.view_faq(faq_id)
        return render_template("faqs/show.html", questions=questions, faq=faq)


# Add Questions
@FaqBP.route('/faqs/<int:faq_id>/add-questions', methods=['GET', 'POST'])
@login_required
def add_question_page(faq_id):
    questions_form = QuestionsForm()
    faq = services.view_faq(faq_id)
    if request.method == 'GET':
        return render_template("faqs/add_questions.html", questions_form=questions_form, faq=faq)
    elif request.method == 'POST':
        if questions_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            question = sanitized_inputs['question']
            response = sanitized_inputs['response']
            questions = {
                'question': question,
                'response': response
            }
            add_question = services.add_questions(faq_id, questions)
            if add_question.status_code == 201:
                flash(add_question.text, 'success')
                return redirect(url_for('.question_page', faq_id=faq_id))
            else:
                flash(add_question.text, 'danger')
                return redirect(url_for('.add_question_page', faq_id=faq_id))
        else:
            return render_template('faqs/add_questions.html', questions_form=questions_form, faq=faq)


# View Questions by FAQ Category
@FaqBP.route('/faqs/<int:faq_id>/view-questions/<int:question_id>', methods=['GET'])
@login_required
def view_question_page(faq_id, question_id):
    if request.method == 'GET':
        question = services.view_questions(faq_id, question_id)
        faq = services.view_faq(faq_id)
        return render_template("faqs/show_questions.html", question=question, faq=faq, faq_id=faq_id)


# Edit Questions by FAQ Category
@FaqBP.route('/faqs/<int:faq_id>/question/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_question_page(faq_id, question_id):
    questions_form = QuestionsForm()
    question = services.view_questions(faq_id, question_id)
    faq = services.view_faq(faq_id)
    if request.method == 'GET':
        questions_form.response.data = question['response']
        return render_template('faqs/edit_questions.html', faq=faq, question=question, questions_form=questions_form)
    elif request.method == 'POST':
        if questions_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            question = sanitized_inputs['question']
            response = sanitized_inputs['response']
            questions = {
                'question': question,
                'response': response
            }
            update_question = services.update_questions(faq_id, question_id, questions)
            if update_question.status_code == 202:
                flash(update_question.text, 'success')
                return redirect(url_for('.question_page', faq_id=faq_id))
            else:
                flash(update_question.text, 'danger')
                return redirect(url_for('.edit_question_page', faq_id=faq_id, question_id=question_id))
        else:
            return render_template('faqs/edit_questions.html', questions_form=questions_form, faq=faq, question=question)


# Delete Questions by FAQ Category
@FaqBP.route('/faqs/<int:faq_id>/question/<int:question_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_questions(faq_id, question_id):
    if request.method == 'GET':
        delete_question = services.delete_questions(faq_id, question_id)
        if delete_question.status_code == 202:
            flash(delete_question.text, 'success')
        else:
            flash(delete_question.text, 'danger')
        return redirect(url_for('.question_page', faq_id=faq_id))


# Archived Questions Page
@FaqBP.route('/faqs/<int:faq_id>/archived-questions', methods=['GET'])
@login_required
def archived_question_page(faq_id):
    if request.method == 'GET':
        questions = services.get_archived_questions(faq_id)
        faq = services.view_faq(faq_id)
        return render_template("faqs/archived_questions.html", questions=questions, faq=faq)


# Restore Questions by FAQ Category
@FaqBP.route('/faqs/<int:faq_id>/question/<int:question_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_questions(faq_id, question_id):
    if request.method == 'GET':
        restore_question = services.restore_questions(faq_id, question_id)
        if restore_question.status_code == 202:
            flash(restore_question.text, 'success')
        else:
            flash(restore_question.text, 'danger')
        return redirect(url_for('.question_page', faq_id=faq_id))


def index():
    faqs = services.get_faqs()
    return render_template('faqs/index.html', faqs=faqs)


@FaqBP.route('/faqs/sort-faqs', methods=['POST'])
@login_required
def sort_faqs():
    sorted_list_data = ast.literal_eval(request.form.get('sorted_list'))
    sorted_list = { 'arrangement': sorted_list_data }
    sort_faqs = services.sort_faqs_or_questions(sorted_list)
    if sort_faqs.status_code == 202:
        return jsonify({'status': 'arrangement success'})
    else:
        return jsonify({'status': 'something went wrong'})


@FaqBP.route('/faqs/<int:faq_id>/sort-questions', methods=['POST'])
@login_required
def sort_faq_questions(faq_id):
    sorted_list_data = ast.literal_eval(request.form.get('sorted_list'))
    sorted_list = { 'arrangement': sorted_list_data }
    sort_faqs = services.sort_faqs_or_questions(sorted_list, faq_id)
    if sort_faqs.status_code == 202:
        return jsonify({'status': 'arrangement success'})
    else:
        return jsonify({'status': 'something went wrong'})