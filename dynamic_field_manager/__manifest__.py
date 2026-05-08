{
    'name': 'Dynamic Field Manager',
    'version': '1.0',
    'summary': 'Dynamic readonly, required, invisible and tracking fields',
    'category': 'Tools',
    'author': 'Custom',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/dynamic_field_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dynamic_field_manager/static/src/js/debug_menu.js',
        ],
    },
    'installable': True,
    'application': True,
    "price": 10.00,
    "currency": "USD",
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
}