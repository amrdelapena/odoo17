# -*- coding: utf-8 -*-
{
    'name': "Hotel Management System",

    'summary': "Hotel Management System for Guest Registration and Billing",

    'description': """
        Hotel Management System
        =======================
        Handles guest registration, room bookings, and billing.
    """,

    'author': "ROYTEK",
    'website': "https://www.yourcompany.com",

    'category': 'Hospitality',
    'version': '1.0',

    # Dependencies
    'depends': ['base'],

    # Data files to load
    'data': [
        'security/ir.model.access.csv',
        'views/mainmenu.xml',
        'views/charges.xml',
        'views/roomtypes.xml',
        'views/rooms.xml',
        'views/guests.xml',
        'views/guestregistration.xml',
    ],

    # Assets (optional, for web interface)
    # 'assets': {
    #     'web.assets_backend': [
    #         'hotel/static/src/js/custom_script.js',
    #         'hotel/static/src/scss/styles.scss',
    #     ],
    # },

    'installable': True,
    'application': True,
    'auto_install': False,
}
