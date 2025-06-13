{
    'name': 'Always Debug Mode',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Automatically enable debug mode for selected users',
    'description': 'Adds an option to always enable debug mode for specific users. If enabled, debug=1 is appended to the URL after login or homepage visit.',
    'author': '',
    'depends': ['base', 'web'],
    'data': [
        'views/res_users_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

