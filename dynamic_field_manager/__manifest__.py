# -*- coding: utf-8 -*-

{
    'name': 'Dynamic Field Manager',
    'version': '17.0.1.0.0',
    'summary': """
        Dynamically Configure Odoo Fields Without Code
    """,
    'description': """
Dynamic Field Manager
=====================

Dynamic Field Manager allows administrators and developers
to dynamically configure Odoo field properties directly
from the Odoo user interface.

Features
========

* Dynamic Readonly Fields
* Dynamic Required Fields
* Dynamic Invisible Fields
* Dynamic Chatter Tracking
* Binary/Image Tracking
* Runtime XML View Modification
* Developer Debug Menu Integration
* Upgrade Safe Architecture

This module helps reduce repetitive XML and Python
customization by allowing runtime field configuration.

Perfect for:
=============

* Odoo Developers
* ERP Administrators
* Odoo Implementation Teams
* Dynamic Customer Requirements
    """,
    'author': 'CodeFusion OdooWorks',
    'website': 'https://github.com/yashsuvta',
    'category': 'Tools',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'USD',
    'depends': ['base','web','mail',],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/dynamic_field_config_views.xml',
        # Menu
        'views/menu.xml',
    ],
    'assets': {

        'web.assets_backend': [
            'dynamic_field_manager/static/src/js/debug_menu.js',
        ],
    },
    'images': [

        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
