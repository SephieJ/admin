# -*- coding: utf-8 -*-

from flask import Flask, g
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_menu import Menu
from flask import render_template
from flask import request
from app.src.users import services as user_services
# from app.src.categories import services as category_services
from app.src.users.controllers import UserBP
from app.src.categories.controllers import CategoryBP
from app.src.home.controllers import HomeBP
from app.src.companies.controllers import CompanyBP
from app.src.faqs.controllers import FaqBP
from app.src.resources.controllers import ResourceBP
from app.src.admins.controllers import AdminBP
from app.src.tickets.controllers import TicketBP
from app.src.banners.controllers import BannerBP
from app.src.invitation.controllers import InvitationBP
from app.src.newsletter.controllers import NewsletterBP

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Secret key for CSRF token
app.config['SECRET_KEY'] = "\xe3X|L\xa5\x92\xfb~%*\x8e\xa3\xf5\xab\t\x18\x12vY\xd7\x9at\xf8\x08"

# Path to the upload dir ectory
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Allowed file extensions for image upload
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['TEMPLATES_AUTO_RELOAD'] = True

csrf = CSRFProtect(app)
csrf.init_app(app)
Menu(app=app)


@app.route('/tickets')
def tickets():
    return render_template('layouts/master_layout.html')

#Ticketing Page
# @TicketBP.route('/tickets', methods=['GET'])
# @login_required
# def tickets_list_page():
#     return render_template("tickets/list.html")
@app.route('/ticket-list')
def ticket_list_page():
        return render_template('tickets/list.html')

@app.route('/ticket-sample')
def ticket_sample_page():
        return render_template('tickets/list-sample.html')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "HomeBP.login"


@login_manager.user_loader
def load_user(user_id):
    return user_services.get(int(user_id))


@app.before_request
def sidebar_filter():
    g.activepage = request.endpoint


# @app.context_processor
# def fetch_categories():
#     categories = category_services.get_category_list()
#     return dict(categories=categories)

app.register_blueprint(UserBP)
app.register_blueprint(CategoryBP)
app.register_blueprint(HomeBP)
app.register_blueprint(CompanyBP)
app.register_blueprint(FaqBP)
app.register_blueprint(ResourceBP)
app.register_blueprint(AdminBP)
app.register_blueprint(TicketBP)
app.register_blueprint(BannerBP)
app.register_blueprint(InvitationBP)
app.register_blueprint(NewsletterBP)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5002, threaded=True)
