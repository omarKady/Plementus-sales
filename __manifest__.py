# -*- coding: utf-8 -*-
{
    'name': "plementus",

    'summary': """
        Custom module for sales enhancement ..
        """,

    'description': """
        Custom module that mimic odoo sales ..
    """,

    'author': "Omar Ahmed",

    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'payment'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
