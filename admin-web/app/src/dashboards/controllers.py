# # -*- coding: utf-8 -*-

# from flask import Blueprint, render_template, url_for
# from flask_login import login_required
# from app.src.companies import services as company_services
# from app.src.resources import services as resource_services
# from app.src.users import services as user_services
# from app.src.tickets import services as ticket_services
# # from app.src.utils import helpers

# DashboardBP = Blueprint('DashboardBP', __name__)


# # Dashboards Page
# # @DashboardBP.route('/dashboard', methods=['GET'])
# # @login_required
# # def dashboard_page():
# #     companies = company_services.get_companies()
# #     resources = resource_services.get_resources()
# #     users = user_services.get_all_users()
# #     tickets = ticket_services.get_tickets()
# #     return render_template("dashboards/index.html", companies=companies,
# #                            resources=resources, users=users, tickets=tickets)
