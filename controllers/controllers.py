# -*- coding: utf-8 -*-
# from odoo import http


# class Plementus(http.Controller):
#     @http.route('/plementus/plementus/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/plementus/plementus/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('plementus.listing', {
#             'root': '/plementus/plementus',
#             'objects': http.request.env['plementus.plementus'].search([]),
#         })

#     @http.route('/plementus/plementus/objects/<model("plementus.plementus"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('plementus.object', {
#             'object': obj
#         })
