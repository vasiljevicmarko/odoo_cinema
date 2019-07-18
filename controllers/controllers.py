# -*- coding: utf-8 -*-
from odoo import http

# class CinemaManagement(http.Controller):
#     @http.route('/cinema_management/cinema_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cinema_management/cinema_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cinema_management.listing', {
#             'root': '/cinema_management/cinema_management',
#             'objects': http.request.env['cinema_management.cinema_management'].search([]),
#         })

#     @http.route('/cinema_management/cinema_management/objects/<model("cinema_management.cinema_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cinema_management.object', {
#             'object': obj
#         })